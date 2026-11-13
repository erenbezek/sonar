"""Site scan'in ortak parçaları: sayfayı okuma, metni çıkarma, okunacak sayfaları seçme."""
import re
import time
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

from sitefind import USER_AGENT, fold, host, lower_tr, same_site

BROWSER_THRESHOLD = 50  # ana sayfa düz okumada bundan az kelime verirse Playwright denenir

# Bağlantı metninde ya da adresinde aranan kelimeler (fold edilmiş: küçük harf, Türkçe harf ve boşluk yok).
CATEGORY_WORDS = {
    "product": ["urun", "cozum", "hizmet", "product", "solution", "service", "faaliyet", "yetenek", "capabilit",
                "neyapiyoruz", "whatwedo", "sektor", "sector", "proje", "project", "portfolio"],
    "about": ["hakkimizda", "hakkinda", "kurumsal", "about", "bizkimiz", "whoweare", "company", "corporate"],
    "career": ["kariyer", "career", "insankaynak", "jobs", "joinus", "acikpozisyon"],
}
PICKS = {"product": 2, "about": 1, "career": 1}
SKIP_PATH_RX = re.compile(r"haber|news|blog|duyuru|basin|press|etkinlik|event|kvkk|gizlilik|privacy|cookie|cerez|login|giris|sepet|cart")
SKIP_FILE_RX = re.compile(r"\.(pdf|jpe?g|png|gif|zip|docx?|xlsx?|mp4)$", re.I)


class _Page(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "template"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.text: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._link: list | None = None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag == "a":
            self._link = [dict(attrs).get("href") or "", []]

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        if tag == "a" and self._link:
            self.links.append((self._link[0], " ".join("".join(self._link[1]).split())))
            self._link = None

    def handle_data(self, data):
        if self.skip:
            return
        self.text.append(data)
        if self._link:
            self._link[1].append(data)


def parse(html: str) -> tuple[str, list[tuple[str, str]]]:
    """HTML'den görünen metni ve bağlantıları (adres, metin) çıkarır."""
    page = _Page()
    try:
        page.feed(html)
    except Exception:  # noqa: BLE001
        pass
    return " ".join(" ".join(page.text).split()), page.links


def get(url: str, bundle: str) -> tuple[str | None, str]:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30, verify=bundle)
        if not r.encoding or r.encoding.lower() == "iso-8859-1":
            r.encoding = r.apparent_encoding
        return r.url, r.text
    except Exception:  # noqa: BLE001
        return None, ""


def home_candidates(url: str) -> list[str]:
    """Listedeki adres açılmazsa denenecek adresler: https/http, www'li/www'suz, ana alan adı."""
    h = host(url)
    hosts = [h]
    labels = h.split(".")
    if len(labels) > 2 and labels[-2] not in ("com", "org", "net", "gov", "edu"):
        hosts.append(".".join(labels[1:]))  # en.simovate.com -> simovate.com
    elif len(labels) > 3:
        hosts.append(".".join(labels[1:]))
    out = [url if "//" in url else "http://" + url]
    for candidate_host in hosts:
        for scheme in ("https://", "http://"):
            for prefix in ("", "www."):
                candidate = f"{scheme}{prefix}{candidate_host}/"
                if candidate not in out:
                    out.append(candidate)
    return out


def read_home(url: str, bundle: str) -> tuple[str | None, str, str]:
    """Ana sayfayı düz okur. Yönlendirme sayfasını (meta refresh) izler. Döner: (son adres, html, not)."""
    for candidate in home_candidates(url):
        final, html = get(candidate, bundle)
        time.sleep(1)
        if not html:
            continue
        note = "" if candidate == (url if "//" in url else "http://" + url) else f"fallback:{candidate}"
        m = re.search(r'<meta[^>]+http-equiv=["\']?refresh["\']?[^>]+content=["\'][^"\']*url=([^"\'>\s]+)', html, re.I)
        if m:
            final2, html2 = get(urljoin(final, m.group(1)), bundle)
            time.sleep(1)
            if html2:
                return final2, html2, (note + " meta-refresh").strip()
        return final, html, note
    return None, "", "no response"


def select_pages(base: str, links: list[tuple[str, str]]) -> dict[str, list[tuple[str, str, float]]]:
    """Ana sayfadaki bağlantılardan okunacak sayfaları seçer. Döner: kategori -> [(adres, bağlantı metni, puan)]."""
    scored: dict[str, dict[str, tuple[str, float]]] = {c: {} for c in CATEGORY_WORDS}
    for href, text in links:
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        url = urljoin(base, href).split("#")[0]
        if not same_site(host(url), host(base)) or SKIP_FILE_RX.search(url):
            continue
        path = urlparse(url).path
        if url.rstrip("/") == base.rstrip("/") or path in ("", "/"):
            continue
        if SKIP_PATH_RX.search(lower_tr(path)):
            continue
        text_f, path_f = fold(text), fold(path)
        depth = len([p for p in path.split("/") if p])
        for category, words in CATEGORY_WORDS.items():
            in_text = any(w in text_f for w in words)
            in_path = any(w in path_f for w in words)
            if not (in_text or in_path):
                continue
            score = 2.0 * in_text + 1.0 * in_path + (1.0 if 0 < len(text.split()) <= 4 else 0.0) - 0.2 * depth
            if url not in scored[category] or score > scored[category][url][1]:
                scored[category][url] = (text, score)
    picked: dict[str, list[tuple[str, str, float]]] = {}
    taken: set[str] = set()
    for category in ("career", "about", "product"):  # dar kategoriler önce, aynı sayfa iki kez seçilmesin
        ranked = sorted(scored[category].items(), key=lambda kv: -kv[1][1])
        picked[category] = []
        for url, (text, score) in ranked:
            if url in taken:
                continue
            picked[category].append((url, text, score))
            taken.add(url)
            if len(picked[category]) == PICKS[category]:
                break
    return picked


def render(browser, url: str) -> tuple[str, str]:
    """Sayfayı Playwright ile açar. Döner: (son adres, html)."""
    page = browser.new_page()
    try:
        try:
            page.goto(url, wait_until="networkidle", timeout=40000)
        except Exception:  # noqa: BLE001
            pass
        return page.url, page.content()
    except Exception:  # noqa: BLE001
        return url, ""
    finally:
        page.close()


_BLOCK_TAGS = {"p", "div", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "br", "tr", "td", "th", "section", "article",
               "header", "footer", "nav", "main", "aside", "form", "table", "blockquote", "figcaption", "option", "button"}


class _Blocks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in _Page.SKIP:
            self.skip += 1
        if tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in _Page.SKIP and self.skip:
            self.skip -= 1
        if tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def lines(html: str) -> list[str]:
    """HTML'den görünen metni satır satır çıkarır (blok etiketleri satır böler)."""
    parser = _Blocks()
    try:
        parser.feed(html)
    except Exception:  # noqa: BLE001
        pass
    out = []
    for line in "".join(parser.parts).split("\n"):
        line = " ".join(line.split())
        if line:
            out.append(line)
    return out


def drop_repeats(pages: list[list[str]]) -> list[list[str]]:
    """Bir satır sitenin sayfalarında ilk geçtiği yerde kalır, sonraki tekrarları atılır (menü, altbilgi)."""
    seen: set[str] = set()
    out = []
    for page_lines in pages:
        kept = []
        for line in page_lines:
            key = line.casefold()
            if key not in seen:
                seen.add(key)
                kept.append(line)
        out.append(kept)
    return out
