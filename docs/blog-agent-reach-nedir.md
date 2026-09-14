# Yapay zekâ ajanına internet gözü tak: Agent Reach nedir?

Claude Code, Cursor ya da Codex gibi bir yapay zekâ ajanı kullanıyorsan şunu fark etmişsindir: kod yazmada çok iyi, ama internette bir şey bulmasını istediğinde tökezliyor.

"Şu YouTube videosu ne anlatıyor?" diyorsun, izleyemiyor. "Reddit'te bu hatayı yaşayan var mı?" diyorsun, 403 hatası alıyor. "Twitter'da insanlar bu ürün hakkında ne diyor?" diyorsun, Twitter'ın API'si para istiyor. Giriş isteyen bir siteyi hiç sorma.

## Sorun: çok zeki ama gözleri bağlı

Ajanını çok zeki bir asistan gibi düşün. Ama bu asistan bir odaya kapatılmış. Kapıların çoğu kilitli. Bazı kapılarda "üyelere özel" yazıyor. Bazılarında bir güvenlik görevlisi "robot musun?" diye soruyor. Bazı kapılar açılıyor ama içerisi karanlık, sayfa boş geliyor.

Asistan zeki. Ama göremiyorsa işe yaramıyor.

## Bu repo ne yapar?

**Agent Reach** o kapıların anahtarlarını toplayıp ajanına veren bir araç.

İki şey yapar:

**1. Hazır kanalları kurar.** Her platform için en iyi çalışan aracı seçer ve kurar. YouTube altyazıları, GitHub repoları, RSS akışları, web sayfaları, web araması, Bilibili gibi kanallar ekstra ayar olmadan çalışır. Twitter, Reddit, Facebook, Instagram gibi platformlar için de yolu hazırlar. Sonra `agent-reach doctor` komutuyla hangi kanalın çalıştığını tek listede gösterir.

**2. Erişemediği sitelerde senin Chrome'unu kullanır.** Bir site giriş istiyorsa, Cloudflare ile engelliyorsa ya da boş sayfa veriyorsa ajan **OpenCLI** adlı araca geçer. OpenCLI, Chrome'una eklediğin küçük bir eklenti üzerinden çalışır. Chrome'da zaten giriş yaptığın siteleri, senin açık oturumunla okur. Site karşısında normal bir kullanıcı görür: seni.

## Kurulum: sadece linki ajanına ver

Kurulum için komut ezberlemen gerekmiyor. Ajanına şu cümleyi yapıştır:

```
Şu talimatları oku ve Agent Reach'i benim için kur: https://raw.githubusercontent.com/ecinaro/brainlab-agent-reach/main/docs/install.md
```

Bu kadar.

Ajan linkteki talimatları okur ve gerisini kendisi yapar: bilgisayarının Windows mu, Mac mi, sunucu mu olduğuna bakar, paketi kurar, eksik araçları listeler, senden izin aldıktan sonra kurar, skill dosyasını yerleştirir ve sonunda sana Türkçe bir rapor verir.

Bu yöntem terminal erişimi olan her ajanla çalışır: Claude Code, Cursor, Codex, OpenClaw, Windsurf ve benzerleri.

## Senin yapman gereken tek şey

Ajan çoğu işi halleder. Ama iki şeyi güvenlik nedeniyle **senin** yapman gerekir:

1. **Chrome'a OpenCLI eklentisini ekle.** [Chrome Web Mağazası'ndaki OpenCLI sayfasını](https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk) aç ve "Chrome'a ekle"ye tıkla. Chrome, hiçbir programın senin yerine eklenti kurmasına izin vermez. Bu iyi bir şey.
2. **Okumak istediğin sitelere Chrome'da giriş yap.** Reddit, Facebook, Instagram, X, hangisi lazımsa. Normal şekilde, kendin.

Ajan sonra `opencli doctor` çalıştırıp eklentinin bağlandığını kontrol eder. Takılırsan detaylı rehber burada: [OpenCLI'ı Chrome'a kurma rehberi](opencli-chrome-kurulum.md).

## Kurulunca neler sorabilirsin?

Artık ajanına şöyle şeyler diyebilirsin:

- "Bu YouTube videosunun altyazısını çek ve bana 5 maddede özetle."
- "Reddit'te bu kütüphane hakkında son bir ayda neler konuşulmuş, olumlu ve olumsuz yorumları ayır."
- "Twitter'da bu ürün hakkında insanlar ne diyor, genel havayı çıkar."
- "Şu sayfa giriş istiyor, Chrome'umdan açıp içeriğini oku ve önemli kısımları listele."

Hangi aracı kullanacağını ajan kendisi seçer. Sen sadece ne istediğini söylersin.

## Güvenlik notu

İnsanın aklına ilk gelen soru şu: "Ajan benim Chrome'umu kullanıyorsa, hesabıma ne yapar?"

Kurallar net:

- **Şifreni kimseye vermiyorsun.** Giriş yapan sensin. OpenCLI sadece zaten açık olan oturumu kullanır.
- **Ajan giriş yapmaz, captcha çözmez.** Böyle bir şey çıkarsa durur ve sana söyler.
- **Ajan sadece okur.** Beğenmez, paylaşmaz, mesaj atmaz.
- **Her şey bilgisayarında kalır.** Cookie'ler ve ayarlar kendi bilgisayarındaki bir dosyada durur.

Yine de Cookie ile çalışan platformlarda ana hesabın yerine ikinci bir hesap kullanmak iyi bir alışkanlık. Bazı platformlar otomatik okumayı fark edip hesabı kısıtlayabilir.

## Repo

Kod açık kaynak, MIT lisanslı: https://github.com/ecinaro/brainlab-agent-reach

Bu repo, [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) projesinin Türkçe çatalıdır. OpenCLI tarafı [jackwener/opencli](https://github.com/jackwener/opencli) projesine dayanır. Emek onların, biz Türkçeleştirip OpenCLI yedeğini ekledik.
