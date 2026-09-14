# OpenCLI'ı Chrome'a kurma rehberi

Bu rehber, ajanının giriş isteyen ya da robotları engelleyen siteleri okuyabilmesi için OpenCLI'ı nasıl kuracağını adım adım anlatır.

Kısa hali [README](../README.md) içinde. Burası detaylı hali.

---

## OpenCLI nedir?

[OpenCLI](https://github.com/jackwener/opencli) (`@jackwener/opencli`, Apache-2.0) web sitelerini komut satırı komutlarına çeviren bir araçtır.

Farkı şu: siteye kendi başına bağlanmaz. **Senin gerçek Chrome'unu** kullanır. Chrome'da hangi sitelere giriş yaptıysan, OpenCLI o açık oturumla sayfayı okur. Site karşısında normal bir kullanıcı görür.

Nasıl bağlanır, tek satırda:

```
opencli  ⇄  localhost:19825 (arka plan servisi, kendiliğinden açılır)  ⇄  Chrome eklentisi ("Browser Bridge")  ⇄  senin Chrome'un
```

- `opencli` komutunu ajan çalıştırır.
- Arka plan servisi (daemon) bilgisayarında, `localhost:19825` adresinde çalışır. Dışarıya açık değildir.
- Chrome eklentisi komutu Chrome'a iletir.
- Chrome sayfayı açar, OpenCLI içeriği okur.

Hazır 160'tan fazla site adaptörü var (`opencli list`). Adaptörü olmayan siteler için genel komutlar da var:

- `opencli web read --url <adres> --stdout` → herhangi bir sayfayı Markdown metne çevirir.
- `opencli browser <oturum-adı> open <adres>`, `state`, `extract`, `close` → tarayıcıyı adım adım kullanır.

Çıktı biçimi `-f json|yaml|md|csv|table` ile seçilir.

---

## Gereksinimler

| Ne | Neden |
|---|---|
| **Masaüstü bilgisayar** (Windows, macOS ya da Linux) | OpenCLI gerçek bir Chrome penceresine ihtiyaç duyar. Ekranı olmayan sunucuda çalışmaz. |
| **Google Chrome** | Eklenti Chrome'a kurulur. |
| **Node.js 20 veya üstü** (20.18+ önerilir) | OpenCLI bir npm paketidir. Kontrol: `node -v` |

Node yoksa [nodejs.org](https://nodejs.org) adresinden LTS sürümünü kur. macOS'ta `brew install node` da olur.

---

## 1. OpenCLI'ı kur

### macOS / Linux

```bash
npm install -g @jackwener/opencli
opencli --version
```

`EACCES` (izin yok) hatası alırsan `sudo` kullanmak yerine Node'u [nvm](https://github.com/nvm-sh/nvm) ile kurman daha güvenlidir.

### Windows

PowerShell ya da Komut İstemi'nde:

```powershell
npm install -g @jackwener/opencli
opencli --version
```

PowerShell "bu sistemde betik çalıştırma devre dışı" (script policy) hatası verirse `npm` yerine `npm.cmd` yaz:

```powershell
npm.cmd install -g @jackwener/opencli
opencli.cmd --version
```

### Agent Reach ile kurmak

Agent Reach zaten kuruluysa şu komut da OpenCLI'ı kurar:

```bash
agent-reach install --env=auto --system --channels=opencli
```

---

## 2. Chrome eklentisini ekle

Bu adımı **sen** yaparsın. Chrome'un güvenlik kuralları gereği hiçbir program eklentiyi senin yerine kuramaz.

### Yol A: Chrome Web Mağazası (kolay)

1. Şu linki Chrome'da aç: https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk
2. **Chrome'a ekle**ye tıkla.
3. Çıkan pencerede **Uzantı ekle**yi onayla.

### Yol B: Elle yükleme (mağaza açılmazsa)

1. https://github.com/jackwener/opencli/releases sayfasına git.
2. En yeni sürümdeki `opencli-extension-v*.zip` dosyasını indir.
3. Zip'i bir klasöre çıkar. Bu klasörü silme, Chrome oradan okur.
4. Chrome adres çubuğuna `chrome://extensions` yaz.
5. Sağ üstteki **Geliştirici modu** anahtarını aç.
6. **Paketlenmemiş öğe yükle**ye tıkla, çıkardığın klasörü seç.

Eklentinin açık (etkin) olduğundan emin ol.

---

## 3. Sitelere giriş yap

Chrome'da okumak istediğin sitelere normal şekilde giriş yap. Örneğin reddit.com, facebook.com, instagram.com, x.com.

- Girişi **sen** yaparsın. Şifreni ajana verme, ajan da senden istememeli.
- Captcha ya da "robot değilim" kutusu çıkarsa onu da sen geçersin.
- Mümkünse ana hesabın yerine ikinci bir hesap kullan. Platformlar otomatik okumayı fark edip hesabı kısıtlayabilir.

Chrome açık kaldığı sürece oturum geçerlidir.

---

## 4. Kontrol et

```bash
opencli doctor
```

Eklentinin bağlı (connected) göründüğünü kontrol et. Sonra küçük bir deneme yap:

```bash
opencli web read --url https://example.com --stdout
```

Ekranda "Example Domain" metnini görüyorsan her şey çalışıyor.

Agent Reach tarafında da kontrol et:

```bash
agent-reach doctor
```

---

## 5. Güncelleme

```bash
npm update -g @jackwener/opencli
```

(Windows'ta gerekirse `npm.cmd update -g @jackwener/opencli`.)

Eklenti:

- Mağazadan kurduysan Chrome kendisi günceller.
- Elle yüklediysen yeni zip'i indir, klasörü değiştir, `chrome://extensions` sayfasında **Güncelle**ye bas.

Güncellemeden sonra `opencli doctor` ile tekrar kontrol et.

---

## Sorun giderme

| Belirti | Anlamı | Çözüm |
|---|---|---|
| Çıkış kodu **69** | Browser Bridge bağlı değil | Chrome'u aç. `chrome://extensions` sayfasında OpenCLI eklentisini etkinleştir. Sonra `opencli doctor`. |
| Çıkış kodu **77** | O siteye giriş yapılmamış | Chrome'da siteye giriş yap, komutu tekrar çalıştır. |
| Çıkış kodu **75** | Zaman aşımı | Sayfa geç yüklendi. Biraz bekleyip tekrar dene. Chrome'un açık ve takılmamış olduğunu kontrol et. |
| `opencli doctor` servise ulaşamıyor | Arka plan servisi takıldı | `opencli daemon status`, sonra `opencli daemon restart`. |
| `attach failed: chrome-extension://...` | Başka bir eklenti Chrome'un hata ayıklayıcısını kullanıyor | 1Password gibi eklentileri geçici olarak kapat, tekrar dene. |
| `opencli` komutu bulunamadı | npm global klasörü PATH'te değil | Terminali kapatıp aç. Olmazsa `npm root -g` ile klasörü bul ve PATH'e ekle. |
| Windows'ta `npm` betik hatası | PowerShell betik politikası | `npm.cmd` kullan. |
| `node` sürümü eski | Node 20 altı | Node 20+ kur (`node -v` ile kontrol et). |

Daha fazlası: [troubleshooting.md](troubleshooting.md)

---

## Ajanlar OpenCLI'ı nasıl kullanır?

Ajan önce normal yolu dener (ör. Jina Reader, platforma özel araç). Şu durumlarda OpenCLI'a geçer:

- Site giriş istiyor.
- Cloudflare ya da captcha sayfası geliyor.
- Sayfa JavaScript ile yüklendiği için boş geliyor.
- 401, 403 ya da 429 hatası geliyor.

Ajanın izlediği karar sırası şu dosyada yazılı: [agent_reach/skill/references/opencli-fallback.md](../agent_reach/skill/references/opencli-fallback.md)

Hazır adaptörü olan platformlarda (Reddit, Facebook, Instagram, XiaoHongShu, Twitter, Bilibili) ajan doğrudan `opencli <site> ...` komutlarını kullanır. `agent-reach doctor --json` hangi platformda hangi yolun aktif olduğunu gösterir.

---

## Güvenlik kuralları

- **Ajan giriş yapmaz.** Kullanıcı adı, şifre ya da doğrulama kodu girmez. Girişi her zaman sen yaparsın.
- **Ajan captcha çözmez.** Robot doğrulaması çıkarsa durur ve sana söyler.
- **Ajan sadece okur.** Beğenme, paylaşma, yorum, mesaj, satın alma gibi işlemler yapmaz.
- **Şifre paylaşılmaz.** OpenCLI zaten açık olan oturumu kullanır. Şifren ajana hiç gelmez.
- **Veri bilgisayarında kalır.** Servis sadece `localhost` üzerinde çalışır.
- **Cookie aktarılmaz.** `agent-reach configure xhs-cookies` gibi komutlar Cookie'yi OpenCLI'a veya Chrome'a aktarmaz. OpenCLI yalnızca Chrome'da zaten var olan ve kullanıcının açıkça kontrol ettiği oturumu kullanır.

İstemediğin bir siteyi okumasını istemiyorsan o siteden Chrome'da çıkış yapman yeterli.
