#!/usr/bin/env bash
# Access check: hedef dosyasındaki her adrese bir istek atar ve sonucu tablo olarak yazar.
# Aynı betik hem yerelde hem GitHub Actions'ta çalışır, böylece iki sonuç karşılaştırılabilir.
#
# Kullanım: bash scripts/access_check.sh [hedef dosyası]
#
# Çıktı sütunları:
#   http    Son HTTP kodu (000: bağlantı kurulamadı)
#   bytes   İndirilen sayfa boyutu
#   tls     ok: sertifika doğrulandı. unverified: sunucu sertifika zincirini eksik
#           gönderdiği için doğrulama kapatılarak tekrar denendi.
#   marker  Sayfada beklenen metin bulundu mu (bot doğrulama sayfalarını ayırmak için)
#   result  ok: HTTP 200 ve marker bulundu. fail: diğer her durum.
set -u

targets="${1:-$(dirname "$0")/access_check_targets.tsv}"
user_agent="sonar-access-check/0.1 (+https://github.com/erenbezek/sonar)"
body="$(mktemp)"
trap 'rm -f "$body"' EXIT

fetch() {
  # $1: adres, geri kalanlar: ek curl seçenekleri
  local url="$1"
  shift
  : > "$body"
  curl -sS -L --max-time 30 -A "$user_agent" -o "$body" \
    -w '%{http_code}\t%{size_download}' "$@" "$url" 2>/dev/null
}

printf 'kind\tname\thttp\tbytes\ttls\tmarker\tresult\n'

while IFS=$'\t' read -r kind name url marker; do
  case "$kind" in '' | \#*) continue ;; esac

  tls="ok"
  stats="$(fetch "$url")"
  exit_code=$?

  # curl 60: sertifika doğrulanamadı. Engel mi, sertifika sorunu mu ayırt etmek için
  # doğrulamayı kapatıp bir kez daha dener ve bunu tls sütununda belirtir.
  if [ "$exit_code" -eq 60 ]; then
    tls="unverified"
    stats="$(fetch "$url" -k)"
  fi

  http="${stats%%$'\t'*}"
  bytes="${stats##*$'\t'}"

  if grep -qaiF -- "$marker" "$body"; then found="yes"; else found="no"; fi
  if [ "$http" = "200" ] && [ "$found" = "yes" ]; then result="ok"; else result="fail"; fi

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$kind" "$name" "$http" "$bytes" "$tls" "$found" "$result"
  sleep 1
done < "$targets"
