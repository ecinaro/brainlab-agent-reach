# Twitter gelişmiş özellikler kurulum rehberi (twitter-cli)

Twitter'da temel okuma Jina Reader ile ücretsiz çalışır, ayar gerekmez.

Gelişmiş özellikler için twitter-cli (@public-clis/twitter-cli) gerekir:

- Tweet arama (`twitter search`)
- Tweet'in ve konuşma zincirinin tamamını okuma (`twitter tweet`, `twitter thread`)
- Kullanıcı akışı (`twitter timeline`)
- Uzun yazı okuma (`twitter article`)

twitter-cli ücretsiz ve açık kaynak bir araçtır (pipx ile kurulur), ama Twitter hesabının Cookie'sine ihtiyaç duyar.

> Masaüstünde Chrome'da x.com'a giriş yaptıysan OpenCLI de yedek yol olarak kullanılabilir. Detay: [docs/opencli-chrome-kurulum.md](../../docs/opencli-chrome-kurulum.md)

## Hızlı kurulum

1. twitter-cli kurulu mu kontrol et:

```bash
which twitter && echo "installed" || echo "not installed"
```

2. twitter-cli'yi kur:

```bash
pipx install twitter-cli
```

3. Komutun kurulduğunu doğrula (bu adımda kimlik doğrulama isteği yapılmaz):

```bash
twitter --help
```

## Cookie alma (Cookie-Editor yolu, önerilir)

1. [Cookie-Editor](https://cookie-editor.com/) tarayıcı eklentisini kur
2. x.com'a giriş yap
3. Cookie-Editor simgesine tıkla → Export → Header String
4. Ayar komutunu çalıştır:

```bash
agent-reach configure twitter-cookies
```

Bu komut `auth_token` ve `ct0` değerlerini çıkarır ve güvenli şekilde
`~/.agent-reach/config.yaml` dosyasına kaydeder. Amaç, `agent-reach doctor`'ın açık kimlik bilgilerinin tam olup olmadığını kontrol edebilmesidir.
`doctor`, `twitter status` komutunu çalıştırmaz, hesabın gerçekten çalışıp çalışmadığını canlı doğrulamaz ve mevcut Shell'i değiştirmez.

Varsayılan olarak sadece `~/.agent-reach/config.yaml` dosyasına yazar. Kullanıcı kimlik bilgilerinin kopyalanmasını açıkça kabul eder ve
`--sync-legacy-twitter` bayrağını açıkça eklersen şu dosyalara da yazılır:

- `~/.config/xfetch/session.json`
- `~/.config/bird/credentials.env`

```bash
agent-reach configure twitter-cookies --sync-legacy-twitter
```

`agent-reach uninstall` bu eski (legacy) kopyalar için sadece uyarı verir, onları otomatik silmez. Temizlemek gerekirse
önce kullanıcıdan onay al, sonra bu iki dosyayı elle sil.

`twitter` bağımsız bir üst akış komutudur, Agent Reach'in ayar dosyasını okumaz. `twitter status/search/read/...`
komutlarını doğrudan çalıştırırken bir sonraki bölümde anlatıldığı gibi mevcut Shell'de ya da alt işlemin ortamında
`TWITTER_AUTH_TOKEN` ve `TWITTER_CT0` değerlerini açıkça ayarlaman gerekir. Tarayıcı Cookie'sinin otomatik okunmasına güvenme.

## Cookie'yi elle ayarlama

`auth_token` ve `ct0` değerlerini zaten biliyorsan:

1. twitter-cli'yi kur (kurulu değilse): `pipx install twitter-cli`

2. Ortam değişkenlerini ayarla:

```bash
export TWITTER_AUTH_TOKEN="senin_auth_token_degerin"
export TWITTER_CT0="senin_ct0_degerin"
```

3. Test et:

```bash
twitter search "test" -n 1
```

## Proxy ayarı

> twitter-cli proxy'yi ortam değişkenleriyle destekler:

```bash
export HTTP_PROXY="http://user:pass@host:port"
export HTTPS_PROXY="http://user:pass@host:port"
twitter search "test" -n 1
```

Genel bir proxy aracı da kullanabilirsin:

```bash
proxychains twitter search "test" -n 1
```

## Yedek: bird CLI

[bird CLI](https://www.npmjs.com/package/@steipete/bird) zaten kuruluysa (`npm install -g @steipete/bird`) o da çalışır. Agent Reach kurulu bird'ü kendiliğinden tespit edip kullanır. İkisinin işlevi benzer; şu an önerilen twitter-cli'dir.
