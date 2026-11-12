#!/usr/bin/env bash
# Access check: hedef dosyasındaki her adrese bir istek atar ve sonucu tablo olarak yazar.
# Aynı betik hem yerelde hem GitHub Actions'ta çalışır, böylece iki sonuç karşılaştırılabilir.
#
# Kullanım: bash scripts/access_check.sh [hedef dosyası]
#
# Sertifika doğrulaması her zaman açıktır. Bazı siteler ara sertifikayı göndermediği için
# sistem sertifikalarına certs/ klasöründekiler eklenir.
#
# Çıktı sütunları:
#   http    Son HTTP kodu (000: bağlantı kurulamadı)
#   bytes   İndirilen sayfa boyutu
#   tls     ok: sertifika doğrulandı. error: sertifika doğrulanamadı.
#   marker  Sayfada beklenen metin bulundu mu (bot doğrulama sayfalarını ayırmak için)
#   result  ok: HTTP 200 ve marker bulundu. fail: diğer her durum.
set -u

script_dir="$(cd "$(dirname "$0")" && pwd)"
targets="${1:-$script_dir/access_check_targets.tsv}"
extra_certs_dir="$script_dir/../certs"
user_agent="sonar-access-check/0.1 (+https://github.com/erenbezek/sonar)"

# Sistem sertifika dosyasını bul (dağıtıma göre yeri değişir).
system_bundle=""
for candidate in /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt /etc/ssl/cert.pem; do
  if [ -f "$candidate" ]; then
    system_bundle="$candidate"
    break
  fi
done
if [ -z "$system_bundle" ]; then
  echo "Sistem sertifika dosyası bulunamadı." >&2
  exit 1
fi

body="$(mktemp)"
bundle="$(mktemp)"
trap 'rm -f "$body" "$bundle"' EXIT

# Güven listesi: sistem sertifikaları + certs/ klasöründeki ara sertifikalar.
cat "$system_bundle" "$extra_certs_dir"/*.pem > "$bundle"

printf 'kind\tname\thttp\tbytes\ttls\tmarker\tresult\n'

while IFS=$'\t' read -r kind name url marker; do
  case "$kind" in '' | \#*) continue ;; esac

  : > "$body"
  stats="$(curl -sS -L --max-time 30 -A "$user_agent" --cacert "$bundle" -o "$body" \
    -w '%{http_code}\t%{size_download}' "$url" 2>/dev/null)"
  exit_code=$?

  # curl 60: sertifika doğrulanamadı.
  if [ "$exit_code" -eq 60 ]; then tls="error"; else tls="ok"; fi

  http="${stats%%$'\t'*}"
  bytes="${stats##*$'\t'}"

  if grep -qaiF -- "$marker" "$body"; then found="yes"; else found="no"; fi
  if [ "$http" = "200" ] && [ "$found" = "yes" ]; then result="ok"; else result="fail"; fi

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$kind" "$name" "$http" "$bytes" "$tls" "$found" "$result"
  sleep 1
done < "$targets"
