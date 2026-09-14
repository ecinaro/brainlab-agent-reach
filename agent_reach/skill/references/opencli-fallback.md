# Erişilemeyen siteler için OpenCLI yedeği

OpenCLI (`@jackwener/opencli`), Browser Bridge eklentisi üzerinden kullanıcının **gerçek,
giriş yapılmış Chrome'unu** sürer. Normal yolların okuyamadığı sayfaları (giriş duvarı,
Cloudflare, captcha, JS ile çizilen içerik) kullanıcının kendi oturumuyla okur.

Bu yol yavaştır ve kullanıcının gerçek oturumunu kullanır. **Normal yol çalışıyorsa kullanma.**

## Ne zaman?

Aşağıdakilerden biri olursa bu merdivene geç:

- HTTP **401 / 403 / 429** yanıtı.
- Cloudflare **"Just a moment..."**, captcha, **"verify you are human"** sayfası.
- Giriş duvarı: "Giriş yap", "Sign in to continue", "Log in to see more" vb.
- Boş veya çok kısa içerik; yalnızca JS iskeleti (`<div id="root"></div>`, "Enable JavaScript").
- Kullanıcının tarayıcısında erişimi olduğu paywall benzeri içerik.
- Platformun kendi agent-reach kanalı kapalı veya hata veriyor (`agent-reach doctor --json`).

## Merdiven (sırayla dene, içerik gelince dur)

Komutlar hem PowerShell hem bash'te çalışır: URL'leri ve CSS seçicileri her zaman **çift
tırnakla** ver. Aşağıdaki `ara` oturum adını her görev için benzersiz bir adla değiştir
(ör. `ara-makale1`) ve görev boyunca aynı adı kullan.

### 0. Normal yol

Önce kanalın kendi aracını kullan (bkz. ilgili referans). Genel web sayfaları için:

```bash
# Windows PowerShell
curl.exe -s "https://r.jina.ai/<url>"

# bash / Git Bash / macOS / Linux
curl -s "https://r.jina.ai/<url>"
```

Çıktı yukarıdaki "Ne zaman?" belirtilerinden birini gösteriyorsa 1. adıma geç.

### 1. OpenCLI hazır mı?

```bash
opencli doctor
```

- Komut bulunamadıysa: kullanıcıya OpenCLI'ın kurulu olmadığını söyle ve
  `agent-reach install --channels opencli` komutunu veya kurulum rehberini öner:
  https://github.com/ecinaro/brainlab-agent-reach/blob/main/docs/opencli-chrome-kurulum.md
- **exit 69** veya "extension not connected": **DUR** ve kullanıcıya aynen şunu söyle:
  "Chrome'da OpenCLI eklentisini aç (chrome://extensions) ve tekrar dene."
  Eklenti bağlanmadan sonraki adımlara geçme.

### 2. Bu site için adapter var mı?

```bash
# Tüm adapter'lar; site adı veya alan adıyla filtrele
opencli list -f json | grep -i "<site>"                  # bash
opencli list -f json | Select-String -Pattern "<site>"   # PowerShell

# Varsa komutlarına bak, sonra salt-okunur komutu çalıştır
opencli <site> --help -f yaml
opencli <site> <komut> ... -f json
```

Adapter varsa genel okuyucudan daha iyi, yapılandırılmış veri verir. Arama gerekiyorsa
arama adapter'ları da var:

```bash
opencli google search "<sorgu>" -f json
opencli duckduckgo search "<sorgu>" -f json
opencli brave search "<sorgu>" -f json
opencli archive wayback "<url>" -f json   # sayfanın arşivlenmiş kopyası
```

### 3. Genel okuyucu: herhangi bir sayfa → Markdown

```bash
opencli web read --url "<url>" --stdout
```

- **`--stdout` şart**: olmadan çıktıyı `./web-articles` altına dosya olarak kaydeder
  (çalışma alanında dosya oluşturma kuralını ihlal eder).
- Yavaş SPA'lar: `--wait 6` (varsayılan 3 sn) veya `--wait-until networkidle`
  (ya da `domstable`).
- Belirli bir öğe yüklenene kadar bekle: `--wait-for "<css>"` (ör. `--wait-for "article"`).
- iframe içindeki içerik: `--frames all-same-origin`.
- Neden boş geldiğini anlamak için: `--diagnose`.

### 4. Tarayıcı oturumu (adım adım okuma)

Genel okuyucu yetmezse (sonsuz kaydırma, parça parça yüklenen içerik, API'den gelen veri):

```bash
# Sekmeyi arka planda aç
opencli browser ara open "<url>" --window background

# URL, başlık ve [N] indeksli etkileşimli öğeleri gör (giriş duvarı / captcha var mı kontrol et)
opencli browser ara state

# İçeriği Markdown olarak, paragraf bütünlüğünü koruyarak parça parça çek
opencli browser ara extract --chunk-size 8000
# Çıktıda next_start_char varsa, bitene kadar devam et:
opencli browser ara extract --chunk-size 8000 --start <next_start_char>
```

İhtiyaca göre:

```bash
opencli browser ara scroll down          # tembel yüklenen içerik için
opencli browser ara wait time 2          # veya: wait selector ".comments"
opencli browser ara find --css "<seçici>"
opencli browser ara get html --selector main --as json
opencli browser ara network              # yakalanan API yanıtlarının önizlemeleri
opencli browser ara network --detail <key>   # tek bir yanıtın tam gövdesi
opencli browser ara screenshot "<geçici-dizin>/sayfa.png"   # /tmp veya $env:TEMP altına
```

Bitince **HER ZAMAN** kapat:

```bash
opencli browser ara close
```

### 5. Kullanıcının zaten açık sekmesi

Yalnızca kullanıcı "sayfa Chrome'umda açık" derse, yeni sekme açmak yerine o sekmeye bağlan:

```bash
opencli browser ara bind
opencli browser ara state
opencli browser ara extract --chunk-size 8000
opencli browser ara unbind
```

Bağlandığın sekmeyi `close` ile kapatma; işin bitince `unbind` kullan.

### 6. Çıkış kodlarına göre davran

| Kod | Anlamı | Ne yap |
|-----|--------|--------|
| 0 | Başarılı | İçeriğin gerçekten dolu olduğunu kontrol et |
| 2 | Kullanım hatası | `--help -f yaml` ile sözdizimini kontrol et, komut uydurma |
| 66 | Boş sonuç | İçerik gerçekten boş; kullanıcıya böyle söyle |
| 69 | Browser Bridge bağlı değil | DUR: "Chrome'da OpenCLI eklentisini aç (chrome://extensions) ve tekrar dene." |
| 75 | Zaman aşımı | Bir kez daha, daha uzun beklemeyle dene (`--wait 8` / `wait time 5`) |
| 77 | Hedef sitede giriş yok | Kullanıcıdan Chrome'da siteye kendisinin giriş yapmasını iste, sonra tekrar dene |
| 78 | Yapılandırma / kimlik bilgisi eksik | Kullanıcıya neyin eksik olduğunu söyle; kimlik bilgisi isteme veya girme |
| 1 | Genel hata | Bir sonraki merdiven basamağına geç |

### 7. Hâlâ olmuyorsa

Neyin denendiğini ve hangi hatanın alındığını dürüstçe raporla. Engeli açıklamak için:

```bash
opencli browser ara analyze "<url>"   # anti-bot sağlayıcısı, API adayları, en yakın adapter
opencli browser ara close
```

**Asla içerik uydurma**; okunamayan sayfanın içeriğini tahmin edip özet gibi sunma.

## Kurallar (kesin)

- **Giriş, şifre, 2FA ve captcha'yı asla otomatikleştirme.** Gerekirse kullanıcıdan
  Chrome'da kendisinin yapmasını iste.
- **Salt-okunur çalış.** Gönder / paylaş / yorum / beğen / satın al / sil gibi öğelere tıklama.
  Formlara yazı yazma veya doldurma; tek istisna, kullanıcı arama istediğinde sitenin
  arama kutusu.
- `eval` yalnızca **salt-okunur** JavaScript için (ör. `document.title`, metin okumak);
  sayfayı, depolamayı veya cookie'leri değiştiren kod çalıştırma.
- Kişisel verileri asla URL'ye veya sorgu parametresine koyma.
- Kullanıcının niyetine ve sitenin kullanım koşullarına saygı göster; toplu kazıma yapma,
  istekler arasında makul bekle.
- Normal yol çalışıyorsa OpenCLI kullanma (yavaştır ve kullanıcının gerçek oturumunu kullanır).
- Açtığın her oturumu `close` ile kapat (bağlandığın sekmeyi `unbind` ile bırak).
- Başlarken söyle: "agent-reach ile, OpenCLI yedeği üzerinden (kullanıcının Chrome oturumu)".

## Örnek: Cloudflare korumalı bir makale

```text
$ curl.exe -s "https://r.jina.ai/https://ornek-haber.com/yazi/123"
... "Just a moment..." ... "Verify you are human" ...       → engellendi, merdivene geç

$ opencli doctor
✓ daemon running  ✓ extension connected                       → hazır

$ opencli web read --url "https://ornek-haber.com/yazi/123" --stdout --wait-until networkidle
# Makale başlığı
Makalenin tam metni Markdown olarak...                       → içerik geldi, dur
```
