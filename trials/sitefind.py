"""Site bulma yönteminin ortak parçaları.

Yöntem (docs/FINDINGS.md, bölüm 7-13):
1. Unvandaki hukuki ekler atılır, kısa adla aranır.
2. Rehber siteleri aramadan dışlanır.
3. İlk 5 sonuç içinden alan adında şirket adı geçen site seçilir.
4. Seçilen sitede teknokent ya da şehir adı aranır. Varsa kabul edilir.
"""
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "trials" / "out"
USER_AGENT = "sonar-trial/0.1 (+https://github.com/erenbezek/sonar)"

# Arama sonuçlarını dolduran rehber siteleri ve listenin kendisi.
EXCLUDE_DOMAINS = [
    "linkedin.com", "rocketreach.co", "pitchbook.com", "finance.yahoo.com", "instagram.com",
    "zoominfo.com", "x.com", "twitter.com", "facebook.com", "mapquest.com", "crunchbase.com",
    "tracxn.com", "cbinsights.com", "youtube.com", "cyberpark.com.tr",
]

LEGAL_RX = re.compile(
    r"(?<!\w)(ANON[İI]M|Ş[İI]RKET[İI]|A\.\s?Ş\.?|AŞ|LTD\.?|ŞT[İI]\.?|L[İI]M[İI]TED|SANAY[İI]|SAN\.|"
    r"T[İI]CARET|T[İI]C\.|VE|[İI]THALAT|[İI]HRACAT|PAZARLAMA)(?!\w)"
)
_FOLD = str.maketrans("çğıöşüâîû", "cgiosuaiu")
PLACE_RX = re.compile(r"cyberpark|bilkent|ankara")
CONTACT_RX = re.compile(r"iletisim|contact|bize-ulas|ulasim")
BOT_CHECK_RX = re.compile(r"security verification|not a robot|robot değilim", re.I)
SHORT_WORD = 4  # bundan kısa ilk kelime "kısa" sayılır


def read_key(name: str) -> str:
    for line in (ROOT / ".env" / "keys").read_text().splitlines():
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip()
    raise SystemExit(f"{name} .env/keys dosyasında yok")


def ca_bundle() -> str:
    """Sistem sertifikaları + certs/ klasöründeki ara sertifikalar."""
    OUT.mkdir(parents=True, exist_ok=True)
    bundle = OUT / "bundle.pem"
    system = next(p for p in ("/etc/ssl/certs/ca-certificates.crt", "/etc/pki/tls/certs/ca-bundle.crt", "/etc/ssl/cert.pem") if Path(p).exists())
    bundle.write_text(Path(system).read_text() + "".join(p.read_text() for p in sorted((ROOT / "certs").glob("*.pem"))))
    return str(bundle)


def lower_tr(s: str) -> str:
    return s.replace("İ", "i").replace("I", "ı").lower().translate(_FOLD)


def fold(s: str) -> str:
    """Küçük harf, Türkçe harfler sadeleşmiş, sadece harf ve rakam."""
    return re.sub(r"[^a-z0-9]", "", lower_tr(s))


def host(url: str) -> str:
    h = (urlparse(url if "//" in url else "http://" + url).hostname or "").lower()
    return h.removeprefix("www.")


def same_site(a: str, b: str) -> bool:
    return a == b or a.endswith("." + b) or b.endswith("." + a)


def short_name(name: str) -> str:
    """Unvandan hukuki ekleri atar: 'X YAZILIM A.Ş.' -> 'X YAZILIM'."""
    return " ".join(LEGAL_RX.sub(" ", name.replace("LTD.ŞTİ", "LTD. ŞTİ").replace(",", " ")).split())


def first_word(name: str) -> str:
    tokens = short_name(name).split()
    return fold(tokens[0]) if tokens else ""


def has_short_first_word(name: str) -> bool:
    w = first_word(name)
    return bool(w) and len(w) < SHORT_WORD


def search(query: str, api_key: str, max_results: int = 5) -> list[dict]:
    r = requests.post(
        "https://api.tavily.com/search",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"query": query, "max_results": max_results, "search_depth": "basic", "exclude_domains": EXCLUDE_DOMAINS},
        timeout=60,
    )
    return r.json().get("results", []) if r.status_code == 200 else []


def choose(name: str, results: list[dict]) -> tuple[int | None, str | None]:
    """Alan adında şirket adının ilk kelimesi geçen ilk sonuç.

    İlk kelime kısaysa alan adının başında olmalı ('t2' -> t2.com.tr evet, fal.ai hayır).
    """
    word = first_word(name)
    if not word:
        return None, None
    for i, result in enumerate(results):
        h = host(result["url"])
        folded = fold(h)
        hit = folded.startswith(word) if len(word) < SHORT_WORD else word in folded
        if hit:
            return i + 1, h
    return None, None


def _get(url: str, bundle: str) -> tuple[str | None, str]:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=25, verify=bundle)
        if not r.encoding or r.encoding.lower() == "iso-8859-1":
            r.encoding = r.apparent_encoding
        return r.url, r.text
    except Exception:  # noqa: BLE001
        return None, ""


def _contact_links(base: str, html: str) -> list[str]:
    links: list[str] = []
    for href in re.findall(r'href=["\']([^"\']+)["\']', html):
        if CONTACT_RX.search(lower_tr(href)) and not href.startswith(("mailto:", "tel:", "#")):
            url = urljoin(base, href)
            if url not in links:
                links.append(url)
    return links[:2]


def verify(site_host: str, bundle: str, browser=None) -> tuple[str, str]:
    """Sitede teknokent ya da şehir adı geçiyor mu.

    Önce düz okuma (ana sayfa, sonra iletişim sayfası). Bulunamazsa ve browser verildiyse
    aynı adımlar Playwright ile tekrarlanır. Bot doğrulama sayfası aşılmaya çalışılmaz.
    Döner: (verified | unverified | unreadable, açıklama)
    """
    # Bazı siteler sadece www ile açılıyor (mapyazilim.com), bu yüzden iki adres de denenir.
    final, html, base = None, "", "https://" + site_host
    for candidate in ("https://" + site_host, "https://www." + site_host):
        final, html = _get(candidate, bundle)
        time.sleep(1)
        if html:
            base = candidate
            break
    if html:
        m = PLACE_RX.search(lower_tr(html))
        if m:
            return "verified", f"plain/home:{m.group(0)}"
        for url in _contact_links(final, html):
            _, contact_html = _get(url, bundle)
            time.sleep(1)
            m = PLACE_RX.search(lower_tr(contact_html))
            if m:
                return "verified", f"plain/contact:{m.group(0)}"
    if browser is None:
        return ("unverified", "plain read only") if html else ("unreadable", "no response")
    page = browser.new_page(user_agent=None)
    try:
        try:
            page.goto(base, wait_until="networkidle", timeout=40000)
        except Exception:  # noqa: BLE001
            pass
        html = page.content()
        if BOT_CHECK_RX.search(html):
            return "unreadable", "bot check page"
        m = PLACE_RX.search(lower_tr(html))
        if m:
            return "verified", f"browser/home:{m.group(0)}"
        for url in _contact_links(page.url, html):
            try:
                page.goto(url, wait_until="networkidle", timeout=40000)
            except Exception:  # noqa: BLE001
                pass
            m = PLACE_RX.search(lower_tr(page.content()))
            if m:
                return "verified", f"browser/contact:{m.group(0)}"
        return "unverified", f"no place name ({len(page.inner_text('body').split())} words in browser)"
    except Exception as e:  # noqa: BLE001
        return "unreadable", type(e).__name__
    finally:
        page.close()


def load_companies() -> list[tuple[str, str, str]]:
    path = OUT / "companies.tsv"
    if not path.exists():
        raise SystemExit("Önce trials/cyberpark_list.py çalıştırılmalı.")
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t") + ["", ""]
        rows.append((parts[0], parts[1], parts[2]))
    return rows
