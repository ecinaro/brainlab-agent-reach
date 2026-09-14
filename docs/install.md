# Agent Reach — Kurulum Rehberi

## İnsanlar için

Bu cümleyi yapay zekâ ajanına yapıştır:

```
Şu talimatları oku ve Agent Reach'i benim için kur: https://raw.githubusercontent.com/ecinaro/brainlab-agent-reach/main/docs/install.md
```

> 🛡️ **Varsayılan olarak güvenli:** `agent-reach install` sadece bilgisayarı kontrol eder ve eksikleri listeler. Hiçbir şeyi değiştirmez.
> Sistem düzeyinde kurulum (`--system`) ancak sen açıkça izin verdikten sonra yapılır.

Ajanın sadece iki şey için sana ihtiyaç duyar: Chrome'a OpenCLI eklentisini eklemek ve sitelere giriş yapmak. Detay: [opencli-chrome-kurulum.md](opencli-chrome-kurulum.md)

---

## Yapay zekâ ajanları için

Bu bölüm sana (ajana) yazıldı. Adımları sırayla uygula. **Kullanıcıyla her zaman Türkçe konuş.** Kısa ve basit cümleler kur. Teknik terim kullanırsan bir cümleyle açıkla.

### Amaç

Agent Reach'i ve üst akış (upstream) araçlarını kur. Böylece kullanıcının ajanı interneti okuyabilsin.

Kurulumdan sonra üst akış araçlarını doğrudan kullanacaksın (OpenCLI, twitter-cli, bili-cli, rdt-cli, yt-dlp, mcporter, gh CLI vb.). Agent Reach bir sarmalayıcı (wrapper) değildir. Görevi: araç seçmek, kurmak, sağlık kontrolü yapmak ve yönlendirmek.

### ⚠️ Sınırlar

Sorun çözerken bu sınırların dışına çıkma:

- Kullanıcı açıkça onaylamadıkça **`sudo` ile komut çalıştırma.**
- `~/.agent-reach/` dışındaki **sistem dosyalarını değiştirme.**
- Bu rehberde geçmeyen **paketleri kurma.**
- Güvenlik duvarını, güvenlik ayarlarını ya da sistem korumalarını **kapatma.**
- Ajanın çalışma alanında (workspace / proje klasörü) **repo klonlama, dosya oluşturma, komut çalıştırma.**
- **Kullanıcının yerine giriş yapma, şifre isteme, captcha çözme, Chrome eklentisi kurma.** Bunları kullanıcı kendisi yapar.
- Bir şey yüksek yetki gerektiriyorsa **kullanıcıya ne gerektiğini söyle**, kararı ona bırak.

### 📁 Klasör kuralları

Agent Reach dosyaları kendi klasörlerine gider. **Asla ajanın çalışma alanına değil:**

| Amaç | Klasör | Örnek |
|---|---|---|
| Ayarlar ve anahtarlar | `~/.agent-reach/` | `~/.agent-reach/config.yaml` |
| Üst akış araç repoları | `~/.agent-reach/tools/` | `~/.agent-reach/tools/xiaoyuzhou/` |
| Geçici dosyalar | `/tmp/` | `/tmp/yt-dlp-output/` |
| Skill dosyaları | `~/.claude/skills/agent-reach/`, `~/.agents/skills/agent-reach/`, `~/.config/opencode/skills/agent-reach/`, `~/.openclaw/skills/agent-reach/` | SKILL.md |

**Neden?** Çalışma alanına repo klonlar ya da dosya oluşturursan kullanıcının proje klasörünü kirletirsin. Zamanla ajanını bozabilir. Çalışma alanını temiz tut.

### Adım 0: Ortamı tanı

Kurulumdan önce şunları öğren:

```bash
# İşletim sistemi
uname -s            # Linux / Darwin (macOS). Windows'ta: $env:OS veya `ver`

# Python (3.10+ gerekli)
python3 --version   # Windows'ta: py -3 --version

# Node.js (OpenCLI için 20+ gerekli)
node -v

# Chrome kurulu mu? Ekran var mı?
```

Karar ver:

- **Yerel bilgisayar (masaüstü, Chrome var):** Tam kurulum + OpenCLI önerilir.
- **Sunucu / VPS (ekran yok, Chrome yok):** OpenCLI atlanır. Cookie tabanlı yollar ve MCP kullanılır.

`agent-reach install --env=auto` bunu kendisi de tespit eder ve çıktının başında `Environment: Local computer` ya da `Environment: Server/VPS` yazar.

> ⚠️ **OpenClaw kullanıyorsan önce `exec` iznini aç.** Agent Reach, ajanın kabuk komutu çalıştırmasına dayanır. OpenClaw varsayılan `messaging` araç profilindeyse komut çalıştıramazsın. Kullanıcıya şunu çalıştırmasını söyle:
>
> ```bash
> openclaw config set tools.profile "coding"
> ```
> Ya da `~/.openclaw/openclaw.json` içinde `"tools": { "profile": "coding" }` ayarla. Sonra Gateway'i yeniden başlat (`openclaw gateway restart`) ve yeni bir sohbet aç. Claude Code, Cursor, Windsurf gibi diğer ajanlar bundan etkilenmez.

### Adım 1: Paketi kur

> PyPI'daki `agent-reach` paketi bu proje **değildir.** Her zaman aşağıdaki GitHub linkini kullan.

```bash
# Önerilen: pipx (en az dert)
pipx install https://github.com/ecinaro/brainlab-agent-reach/archive/main.zip
agent-reach install --env=auto               # Sadece kontrol (varsayılan)

# Python Homebrew'dan geliyorsa / PEP 668 (externally-managed-environment) hatası alırsan
# sanal ortam (venv) kullan:
python3 -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate
pip install https://github.com/ecinaro/brainlab-agent-reach/archive/main.zip
agent-reach install --env=auto               # Sadece kontrol (varsayılan)
```

> 💡 **Windows / Microsoft Store Python takma adı?**
> `python3 --version` Microsoft Store'u açıyorsa ya da `where python3`
> `...\AppData\Local\Microsoft\WindowsApps\python3.exe` gösteriyorsa, bu gerçek bir Python değil,
> Windows'un Store kısayoludur. Python Launcher `py -3` ya da gerçek kurulum klasöründeki `python.exe` kullan.
>
> PowerShell örneği:
> ```powershell
> py -3 -m venv $env:USERPROFILE\.agent-reach-venv
> $env:USERPROFILE\.agent-reach-venv\Scripts\Activate.ps1
> python -m pip install https://github.com/ecinaro/brainlab-agent-reach/archive/main.zip
> agent-reach install --env=auto
> ```
> PowerShell betik politikası `Activate.ps1` ya da `npm` çalıştırmayı engellerse `npm.cmd` kullan veya venv içindeki `python.exe`'yi doğrudan çağır.

> 💡 **macOS / Homebrew Python `externally-managed-environment` diyor mu?**
> Bu PEP 668 korumasıdır, Agent Reach'in hatası değil. Önce `pipx install ...` dene ya da önce `venv` oluştur.

### Adım 2: Kontrol et, izin al, kur

Varsayılan komut çekirdek altyapıyı (gh CLI, Node.js, mcporter, Exa araması, yt-dlp ayarı) sistemi değiştirmeden kontrol eder:

```bash
agent-reach install --env=auto
```

Çıktıyı kullanıcıya Türkçe özetle ve **izin iste**. Örnek:

> "Kontrol bitti. Eksik olanlar: X, Y. Bunları kurmam için bilgisayarında global araç kurmam ve `~/.agent-reach/` altına ayar yazmam gerekiyor. Kurayım mı?"

Kullanıcı açıkça "evet" derse:

```bash
agent-reach install --env=auto --system
```

`--system` eksikleri kurar/ayarlar ve şu kurulumsuz çalışan kanalları açar:

- Web (Jina Reader), YouTube, GitHub, RSS, Exa araması, V2EX, Bilibili (temel)

**Kurulum modları:**

```bash
agent-reach install --env=auto             # Sadece kontrol; güvenli varsayılan
agent-reach install --env=auto --safe      # Aynı: sadece kontrol (uyumluluk için)
agent-reach install --env=auto --system    # Harici/sistem kurulumuna açık izin
agent-reach install --env=auto --dry-run   # --system'in ne yapacağını önizle
```

### Adım 3: Skill'i kur

Skill dosyası (SKILL.md), ajanlara hangi platformda hangi komutu çağıracaklarını anlatır. Varsayılan dil Türkçedir.

```bash
agent-reach skill --install
```

Bu komut skill dosyalarını bulunan ajan klasörlerine yazar (`~/.claude/skills`, `~/.agents/skills`, `~/.config/opencode/skills`, `~/.openclaw/skills`). `--system` kurulumu skill'i zaten kurar; bu komut en güncel hali yeniden yazar.

### Adım 4: OpenCLI (erişilemeyen siteler için yedek)

**Sadece yerel bilgisayarda.** Sunucuda bu adımı atla ve kullanıcıya "OpenCLI masaüstü ve Chrome ister, sunucuda kullanılamaz" de.

OpenCLI, kullanıcının gerçek Chrome'unu bir eklenti üzerinden kullanır:

```
opencli  ⇄  localhost:19825 (daemon)  ⇄  Chrome eklentisi  ⇄  kullanıcının Chrome'u
```

İki işe yarar:

1. Reddit, Facebook, Instagram, XiaoHongShu için ana yol; Twitter ve Bilibili altyazı için yedek yol.
2. **Genel yedek:** Başka hiçbir yolla okunamayan siteler için (giriş duvarı, Cloudflare/captcha, JavaScript yüzünden boş gelen sayfa, 401/403/429).

Kullanıcıya kısaca açıkla ve izin iste:

> "Bazı siteler giriş ister ya da robotları engeller. OpenCLI adlı bir araçla bu siteleri senin Chrome'undan, senin açık oturumunla okuyabilirim. Şifren bana gelmez, her şey bilgisayarında kalır, sadece okurum. Kurayım mı?"

Evet derse (Node.js 20+ gerekir):

```bash
agent-reach install --env=auto --system --channels=opencli
# ya da doğrudan:
npm install -g @jackwener/opencli
# Windows PowerShell betik hatası verirse:
npm.cmd install -g @jackwener/opencli
```

Sonra **kullanıcıya şu adımları yapmasını söyle.** Bunları sen yapamazsın ve yapmaya çalışmamalısın (Chrome güvenlik kuralı + hesap güvenliği):

> **Senin yapman gereken 3 şey:**
> 1. Şu linki Chrome'da aç ve **Chrome'a ekle**ye tıkla: https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk
>    (Mağaza açılmazsa: https://github.com/jackwener/opencli/releases sayfasından `opencli-extension-v*.zip` indir → klasöre çıkar → `chrome://extensions` → Geliştirici modu → Paketlenmemiş öğe yükle.)
> 2. Chrome'da okumamı istediğin sitelere normal şekilde giriş yap (ör. reddit.com, facebook.com, instagram.com, x.com).
> 3. Bitince bana "tamam" yaz.

Kullanıcı "tamam" deyince doğrula:

```bash
opencli doctor
opencli web read --url https://example.com --stdout
```

`opencli doctor` eklentiyi bağlı (connected) göstermeli. Göstermiyorsa:

- Çıkış kodu **69**: eklenti bağlı değil → kullanıcıdan `chrome://extensions` sayfasında OpenCLI'ı etkinleştirmesini iste.
- Çıkış kodu **77**: siteye giriş yapılmamış → kullanıcıdan Chrome'da giriş yapmasını iste.
- Çıkış kodu **75**: zaman aşımı → tekrar dene.
- `attach failed: chrome-extension://...` → kullanıcıdan 1Password gibi hata ayıklayıcı kullanan eklentileri geçici kapatmasını iste.
- Daemon takıldıysa: `opencli daemon status`, `opencli daemon restart`.

**Kullanım kuralları (her zaman):**

- Önce normal yolu dene. OpenCLI'a sadece normal yol başarısız olursa geç. Karar sırası: `agent_reach/skill/references/opencli-fallback.md`.
- Genel komutlar: `opencli web read --url <adres> --stdout` (sayfa → Markdown), `opencli browser <oturum> open <adres>` / `state` / `extract` / `close`.
- Hazır adaptörler: `opencli list`. Çıktı biçimi: `-f json|yaml|md|csv|table`.
- **Asla** giriş formu doldurma, şifre girme, captcha çözme. Giriş gerekiyorsa dur ve kullanıcıya söyle.
- **Sadece oku.** Beğenme, paylaşma, yorum, mesaj, satın alma yapma.

Detaylı kullanıcı rehberi: [opencli-chrome-kurulum.md](opencli-chrome-kurulum.md)

### Adım 5: Kullanıcıya isteğe bağlı kanalları sor

Temel kurulumdan sonra **kullanıcıya** başka hangi kanalları istediğini sor. Bu listeyi göster:

> Temel kanallar hazır! Artık web'de arama yapabilir, YouTube izleyebilir, GitHub okuyabilirim.
>
> İstersen bunları da açabilirim. Hangileri lazım?
>
> - 🌟 **OpenCLI** (masaüstü için önerilir) — Tek kurulumla Reddit, Facebook, Instagram, Bilibili altyazı, Twitter yedeği ve erişilemeyen siteler için genel yedek. XiaoHongShu'da sadece Chrome'da zaten var olan ve kullanıcının açıkça kontrol ettiği oturumu kullanır.
> - 🐦 **Twitter/X** — tweet arama, akış (giriş Cookie'si gerekir)
> - 📈 **Xueqiu** — hisse fiyatları, popüler gönderiler (giriş Cookie'si gerekir)
> - 🎙️ **Xiaoyuzhou podcast** — sesi yazıya dökme (ücretsiz Groq anahtarı gerekir)
> - 📕 **XiaoHongShu** — arama, okuma, yorumlar (OpenCLI mevcut oturumla; MCP/eski araçlar Cookie-Editor ile)
> - 📖 **Reddit** — arama ve gönderi okuma (giriş şart: masaüstünde OpenCLI ya da rdt-cli + Cookie)
> - 📘 **Facebook** — arama, sayfa, akış, grup listesi (masaüstünde OpenCLI, Chrome oturumunu kullanır)
> - 📷 **Instagram** — kullanıcı arama, profil, son gönderiler, Explore (masaüstünde OpenCLI)
> - 📺 **Bilibili tam sürüm** — popüler, sıralama, arama, video detayı (bili-cli, giriş gerekmez)
> - 💼 **LinkedIn** — profil, iş arama
>
> Hangilerini istediğini yaz. Örneğin "Twitter ve Reddit'i kur", "Facebook ve Instagram'ı kur" ya da "hepsini kur".

Kullanıcının seçimine göre çalıştır:

```bash
agent-reach install --env=auto --system --channels=opencli,xiaohongshu   # Masaüstü, XiaoHongShu seçti
agent-reach install --env=auto --system --channels=facebook,instagram    # Masaüstü Meta kanalları
agent-reach install --env=auto --system --channels=all                   # Kullanıcı hepsini onayladı
```

Desteklenen kanal adları: `opencli`, `twitter`, `xiaoyuzhou`, `xueqiu`, `xiaohongshu`, `reddit`, `facebook`, `instagram`, `bilibili`, `linkedin`, `all`

### Adım 6: Bozuk olanları düzelt

`agent-reach doctor` çalıştır ve çıktıya bak.

Olabildiğince çok kanalı ✅ yapmaya çalış. Kurulumda bir şey başarısız olduysa ya da doctor ❌/⚠️ gösteriyorsa sorunu bul ve düzeltmeye çalış. Ama yukarıdaki sınırların içinde kal. Düzeltme yüksek yetki ya da sistem değişikliği gerektiriyorsa önce kullanıcıya sor.

Kullanıcıya sadece gerçekten onun girdisi gerektiğinde sor (Cookie, izin vb.).

### Adım 7: Kullanıcı girdisi gereken ayarlar

Bazı kanallar sadece kullanıcının verebileceği bilgilere ihtiyaç duyar. Doctor çıktısına göre eksik olanı iste:

> 🔒 **Güvenlik önerisi:** Cookie ya da tarayıcı oturumu gerektiren platformlarda (Twitter, XiaoHongShu, Reddit, Facebook, Instagram) ana hesap yerine **ikinci/yedek bir hesap** kullanılmasını öner. Cookie/oturum ile erişimin iki riski var:
> 1. **Hesap kısıtlama** — platformlar tarayıcı dışı erişimi fark edip hesabı kısıtlayabilir ya da kapatabilir.
> 2. **Bilgi sızması** — Cookie hesaba tam erişim verir; yedek hesap, bir sızıntıda zararı sınırlar.

> 🍪 **Cookie / oturum:**
>
> Cookie isteyen klasik CLI'lar için (Twitter, Xueqiu vb.) **önce Cookie-Editor ile içe aktarmayı** öner. En basit ve en güvenilir yol budur:
> 1. Kullanıcı kendi tarayıcısında ilgili platforma giriş yapar.
> 2. [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) Chrome eklentisini kurar.
> 3. Eklentiye tıklar → Export → Header String.
> 4. Dışa aktarılan metni ajana verir.
>
> Twitter için sadece kullanıcının Cookie-Editor ile açıkça dışa aktardığı içerik kabul edilir. Agent Reach XiaoHongShu'ya kullanıcı adına giriş yapmaz ve tarayıcıdan XiaoHongShu Cookie'si okumaz. XiaoHongShu için OpenCLI yalnızca Chrome'da zaten var olan ve kullanıcının açıkça kontrol ettiği oturumu kullanır. Hazır oturum yoksa Cookie-Editor ile dışa aktarıp xiaohongshu-mcp / eski araçları yapılandır. Xueqiu ve Bilibili platform bazında açıkça içe aktarılabilir, örneğin `agent-reach configure --from-browser chrome --platform xueqiu`; bu komut başka platformları taramaz ve kaydetmez.

**Twitter arama ve gönderi:**
> "Twitter aramasını açmak için Twitter Cookie'lerine ihtiyacım var. Chrome'a Cookie-Editor eklentisini kur, x.com'a git, eklentiye tıkla → Export → Header String, çıkan metni bana yapıştır."

```bash
agent-reach configure twitter-cookies
```

Bu komut `twitter_auth_token` ve `twitter_ct0` değerlerini Agent Reach'in kendi `doctor` kontrolü için kaydeder. `doctor` üst akıştaki `twitter status` komutunu çalıştırmaz ve mevcut Shell'i değiştirmez. `twitter search/read/...` komutlarını doğrudan çalıştırmadan önce o işlemin ortamında şunları açıkça ayarlaman gerekir:

```bash
export TWITTER_AUTH_TOKEN="..."
export TWITTER_CT0="..."
twitter search "query" -n 10
```

> **Proxy notu (erişimin kısıtlı olduğu ağlar):**
>
> twitter-cli ve rdt-cli Python ile yazılmıştır; proxy gereken ağlarda ortam değişkeniyle proxy verilebilir.
>
> **Senin (ajanın) yapman gerekenler:**
> 1. Kullanıcının proxy ayarladığını doğrula: `agent-reach configure proxy` (gizli giriş)
> 2. Ortam değişkenlerini ayarla: `export HTTP_PROXY="..." HTTPS_PROXY="..."`
> 3. Gerisini Agent Reach halleder, kullanıcının ek bir şey yapmasına gerek yok.
>
> Kullanıcı "fetch failed" hatası bildirirse [troubleshooting.md](troubleshooting.md) dosyasına bak.

**Reddit (giriş şart, kurulumsuz yol yok):**
> Reddit'in anonim erişimi kapalı, resmi API elle onay istiyor. Masaüstü kullanıcıları için ilk tercih OpenCLI (Chrome'da reddit.com'a giriş yapılmış olması yeterli). Sunucu / eski kurulum kullanıcıları için rdt-cli:

```bash
# PyPI geride; GitHub'dan kur (koddaki _RDT_GIT_SOURCE ile aynı sabit sürüm)
pipx install 'git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66'
rdt login   # Tarayıcı Cookie'sini otomatik çeker; tarayıcısız sunucuda doctor'ın gösterdiği gibi Cookie'yi elle yaz
```

> Reddit'e erişimin engellendiği ağlarda proxy gerekir. Sunucu IP'si engellenirse konut (residential) proxy kullanılabilir (ör. https://webshare.io, ayda yaklaşık 1 $):
> ```bash
> agent-reach configure proxy
> ```

**XiaoHongShu (birden fazla yol, ortama göre seç):**

> **Kimlik doğrulama sınırı:** Agent Reach XiaoHongShu'ya kullanıcı adına giriş yapmaz ve
> tarayıcı Cookie'si okumaz. OpenCLI yalnızca Chrome'da zaten var olan ve kullanıcının açıkça kontrol ettiği oturumu kullanır;
> `agent-reach configure xhs-cookies` Cookie'yi OpenCLI'a veya Chrome'a aktarmaz.
> Hazır oturum yoksa otomatik giriş yapma; Cookie-Editor ile elle dışa aktarıp
> xiaohongshu-mcp ya da eski araçları yapılandır:
>
> ```bash
> agent-reach configure xhs-cookies
> ```
>
> Bu açık komut, kullanıcının verdiği xiaohongshu.com alan adına ait Cookie setini kaydeder/içe aktarır. Önce
> Cookie adlarını ve kapsamını doğrula. xiaohongshu.com dışındaki alan adlarına ait Cookie'ler yok sayılır.
>
> **Masaüstü bilgisayar (OpenCLI önerilir):**

```bash
agent-reach install --system --channels opencli
```

> Kurulumdan sonra kullanıcıya tek elle yapılacak adımı anlat (Chrome güvenlik kuralı, senin yerine yapılamaz):
> 1. https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk adresini aç
> 2. **Chrome'a ekle**ye tıkla
> 3. `opencli doctor` ile doğrula (eklenti bağlı görünmeli)
>
> AUTH_REQUIRED hatası gelir ve kullanıcının hazır oturumu yoksa kullanıcı adına otomatik giriş yapma;
> aşağıdaki xiaohongshu-mcp / eski araç Cookie-Editor yoluna geç.
>
> **Sunucu / masaüstü olmayan ortam (xiaohongshu-mcp):**
> 1. https://github.com/xpzouying/xiaohongshu-mcp/releases adresinden platforma uygun binary'yi `~/.agent-reach/tools/` klasörüne indir
> 2. Servisi başlat (ilk çalıştırmada yaklaşık 150 MB'lık başsız tarayıcı iner, bitmesini bekle)
> 3. Yukarıdaki Cookie-Editor akışıyla Cookie'yi elle içe aktar
> 4. Bağla: `mcporter config add xiaohongshu http://localhost:18060/mcp --scope home`
> 5. Çağırırken mutlaka `--timeout 120000` ekle
>
> **Eski kurulum kullanıcıları (xhs-cli):** Zaten kurulu xhs-cli yedek yol olarak çalışmaya devam eder
> (üst akış 2026-03'ten beri güncellenmiyor, yeni kurulum önerilmez); kimlik doğrulama yine yukarıdaki
> Cookie-Editor elle dışa aktarma akışıyla yapılır.

**Facebook / Instagram (masaüstünde OpenCLI):**
> Bu iki platform OpenCLI ile çalışır: kullanıcının kendi Chrome oturumunu kullanır, hesap şifresi kaydetmez, Meta Graph API onay sürecine girmez. Sunucu / masaüstü olmayan ortamlar desteklenmez.

```bash
agent-reach install --system --channels facebook,instagram
```

> Kurulumdan sonra:
> 1. Chrome'da OpenCLI eklentisinin kurulu olduğunu ve `opencli doctor` kontrolünden geçtiğini doğrula
> 2. Kullanıcı Chrome'da facebook.com / instagram.com'a kendisi giriş yapar
> 3. Ajan doğrudan çağırır:
>    ```bash
>    opencli facebook search "query" -f yaml
>    opencli facebook profile zuck -f yaml
>    opencli facebook groups -f yaml
>    opencli instagram search "query" -f yaml     # kullanıcı arama
>    opencli instagram profile nasa -f yaml
>    opencli instagram user nasa -f yaml          # belirli kullanıcının son gönderileri
>    ```
>
> Facebook Groups şu an sadece giriş yapan kullanıcının görebildiği grup listesini / son hareketleri okumayı vaat eder; herhangi bir grubun gönderi ve yorumları garanti değildir. Instagram `search` kullanıcı aramasıdır, site genelinde gönderi araması değildir. 429 ya da giriş hatası gelirse kullanıcıdan Chrome'da tekrar giriş yapmasını iste ve istek sıklığını düşür.

**Xueqiu (hisse fiyatları + popüler gönderiler):**
> "Xueqiu giriş Cookie'si istiyor. Önce Chrome'da xueqiu.com'a giriş yap, sonra şunu çalıştıracağım:"

```bash
agent-reach configure --from-browser chrome --platform xueqiu
```

> Sadece Xueqiu'nun ihtiyaç duyduğu en az Cookie okunur ve kaydedilir; başka platformlar okunmaz.

**Xiaoyuzhou podcast (Groq Whisper):**
> "Xiaoyuzhou podcast'lerini yazıya dökme aracı zaten kurulu. Sadece ücretsiz bir Groq API anahtarı lazım."

Betik Agent Reach ile otomatik kurulur, kullanıcının sadece anahtar vermesi yeterli:

```bash
agent-reach configure groq-key
```

> **Groq API anahtarı alma (ücretsiz, kredi kartı gerekmez, 30 saniye):**
> 1. https://console.groq.com adresini aç
> 2. Google/GitHub hesabıyla giriş yap (ya da kayıt ol)
> 3. Soldaki menü → API Keys → Create API Key
> 4. `gsk_` ile başlayan anahtarı kopyala, ajana ver (gizli giriş istemine yapıştır)
>
> **Kullanım:**
> Kullanıcı bir Xiaoyuzhou linki verir, ajan şunu çalıştırır:
> ```bash
> bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh https://www.xiaoyuzhoufm.com/episode/xxxxx
> ```
>
> Sesi indirir → dönüştürüp parçalar → Groq Whisper ile yazıya döker → tam metni çıkarır.
>
> **Ücretsiz kota ve sınırlar:**
> - Saatte yaklaşık 2 saatlik ses (7200 saniye); aşılırsa 15 dakika sonra kendiliğinden açılır
> - Günlük birkaç bölüm için fazlasıyla yeterli
> - Kalite yüksek (Whisper large-v3) ama konuşmacıları ayırmaz
> - 2 saatten uzun bölümleri parça parça işle

**LinkedIn (isteğe bağlı — mcp-server-linkedin):**
> "LinkedIn'in temel içeriği Jina Reader ile okunabilir. Tam özellikler (profil detayı, kişi ve iş arama) için mcp-server-linkedin gerekir."

> **Kurulum (stdio önerilir):**
> Önce resmi talimatlarla `uv` kur (`uvx` de onunla gelir):
> https://docs.astral.sh/uv/getting-started/installation/
>
> ```bash
> mcporter config add linkedin --command uvx --arg mcp-server-linkedin@latest --env UV_HTTP_TIMEOUT=300 --scope home
> ```
>
> `uvx` en güncel servisi gerektiğinde indirip başlatır; ayrıca Python paketi ya da sürekli çalışan HTTP servisi gerekmez.
>
> **İlk giriş (tarayıcı ekranı gerekir):**
> ```bash
> uvx mcp-server-linkedin@latest --login
> ```
> Açılan tarayıcıda LinkedIn'e **kullanıcı kendisi** giriş yapar; oturum `~/.linkedin-mcp/profile/` klasörüne kaydedilir. Ekranı olmayan sunucularda aynı komut VNC gibi görünür bir masaüstünde çalıştırılmalıdır.
>
> Detaylar: https://github.com/stickerdaniel/linkedin-mcp-server

### Adım 8: Son kontrol ve rapor

Son kez çalıştır:

```bash
agent-reach doctor
```

Sonra kullanıcıya **Türkçe**, kısa ve basit bir rapor ver:

1. Kaç kanal çalışıyor (✅), hangileri çalışmıyor (❌/⚠️).
2. Birden fazla yolu olan platformlarda şu an hangi yol kullanılıyor (`agent-reach doctor --json` içindeki `active_backend`).
3. OpenCLI durumu: kurulu mu, eklenti bağlı mı, yedek olarak hazır mı.
4. Kullanıcının hâlâ yapması gerekenler (ör. Chrome eklentisini eklemek, bir siteye giriş yapmak, Cookie vermek).
5. Deneyebileceği 2-3 örnek istek (ör. "Bu YouTube videosunu özetle", "Reddit'te X hakkında ne konuşuluyor?").

### Adım 9: Günlük izleme (sadece OpenClaw)

**OpenClaw** içinde çalışıyorsan kullanıcıya sor:

> "Agent Reach kuruldu. Her gün otomatik kontrol eden bir görev ayarlayayım mı? Kanalların çalışıp çalışmadığını ve yeni sürüm olup olmadığını takip eder. Sadece sorun olursa haber verir, yoksa rahatsız etmez."

Kullanıcı kabul ederse şu görevle bir **cron job** oluştur (günlük, `sessionTarget: "isolated"`, `delivery: "announce"`):

```
agent-reach watch komutunu çalıştır.
Çıktıda sorun (❌ ⚠️) ya da yeni sürüm (🆕) yoksa kullanıcıya haber verme, sessizce bitir.
Sorun ya da yeni sürüm varsa tam raporu kullanıcıya Türkçe gönder ve çözüm öner.
Yeni sürüm varsa kullanıcıya güncellemek isteyip istemediğini sor (şu cümle ajana verilirse tam güncelleme yapılır: Şu talimatları oku ve Agent Reach'i benim için güncelle: https://raw.githubusercontent.com/ecinaro/brainlab-agent-reach/main/docs/update.md).
```

Kullanıcı bu işi başka bir ajana vermek isterse seçimi ona bırak.

---

## Hızlı başvuru

| Komut | Ne yapar |
|---|---|
| `agent-reach install --env=auto` | Sadece bağımlılık ve kanal kontrolü (varsayılan) |
| `agent-reach install --env=auto --system` | Çekirdek harici araçları açık izinle kurar/ayarlar |
| `agent-reach install --env=auto --system --channels=twitter,xiaohongshu` | Onaylanan isteğe bağlı kanalları kurar |
| `agent-reach install --env=auto --system --channels=all` | Açık onaydan sonra her şeyi kurar |
| `agent-reach install --env=auto --safe` | Güvenli varsayılanın uyumluluk takma adı |
| `agent-reach install --env=auto --dry-run` | Ne yapılacağını önizler |
| `agent-reach skill --install` | Skill dosyalarını ajan klasörlerine kurar |
| `agent-reach doctor` | Kanal durumunu gösterir |
| `agent-reach watch` | Hızlı sağlık + güncelleme kontrolü (zamanlanmış görevler için) |
| `agent-reach check-update` | Yeni sürüm var mı bakar |
| `agent-reach configure twitter-cookies` | Twitter Cookie'sini gizli girişle kaydeder; doğrudan çağrı için yine ortam değişkenleri gerekir |
| `agent-reach configure proxy` | Proxy adresini gizli girişle kaydeder; otomatik açma anahtarı değildir |
| `agent-reach configure groq-key` | Xiaoyuzhou yazıya dökme anahtarını gizli girişle kaydeder |
| `opencli doctor` | OpenCLI ve Chrome eklentisi bağlantısını kontrol eder |

Kurulumdan sonra üst akış araçlarını doğrudan kullan. Tam komut listesi SKILL.md içinde:

| Platform | Üst akış aracı | Örnek |
|---|---|---|
| Twitter/X | `twitter` (yedek `opencli`) | `TWITTER_AUTH_TOKEN` / `TWITTER_CT0` ayarladıktan sonra `twitter search "query" -n 10` |
| YouTube | `yt-dlp` | `yt-dlp --dump-json URL` |
| Bilibili | `bili` (altyazı `opencli` ile) | `bili search "query" --type video` / `opencli bilibili subtitle BVxxx` |
| Reddit | `opencli` (yedek `rdt`) | `opencli reddit search "query" -f yaml` / `rdt read POST_ID` |
| Facebook | `opencli` | `opencli facebook search "query" -f yaml` |
| Instagram | `opencli` | `opencli instagram user nasa -f yaml` |
| GitHub | `gh` | `gh search repos "query"` |
| Web | `curl` + Jina | `curl -s "https://r.jina.ai/URL"` |
| Erişilemeyen site (yedek) | `opencli` | `opencli web read --url URL --stdout` |
| Exa araması | `mcporter` | `mcporter call exa.web_search_exa query="..." numResults=5` |
| XiaoHongShu | `opencli` (sunucuda `mcporter`) | `opencli xiaohongshu search "query" -f yaml` |
| Xiaoyuzhou podcast | `transcribe.sh` | `bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh <URL>` |
| LinkedIn | `mcporter` | `mcporter call linkedin.get_person_profile linkedin_username="..."` |
| RSS | `feedparser` | `python3 -c "import feedparser; ..."` |

> Birden fazla yolu olan platformlarda `agent-reach doctor --json` içindeki `active_backend` esas alınır.

---

Teşekkürler: Bu rehber [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) projesinin kurulum rehberinden Türkçeleştirildi. OpenCLI: [jackwener/opencli](https://github.com/jackwener/opencli).
