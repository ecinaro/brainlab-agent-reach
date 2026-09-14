# Sosyal medya ve topluluklar

XiaoHongShu, Twitter/X, Bilibili, V2EX, Reddit, Facebook, Instagram.

## XiaoHongShu (çoklu backend)

XiaoHongShu'nun üç backend'i var. **Önce `agent-reach doctor --json` çalıştırıp xiaohongshu için
`active_backend` değerinin hangisi olduğuna bak**, sonra ilgili komut grubunu kullan.

> XiaoHongShu Çince bir platformdur: aramalarda Çince anahtar kelime kullan (ör. "kahve" yerine
> `咖啡`, "İstanbul seyahati" yerine `伊斯坦布尔 旅行`). Türkçe/İngilizce sorgular çok az sonuç verir.

### Backend A: OpenCLI (masaüstünde tercih edilir)

```bash
# Not ara
opencli xiaohongshu search "query" -f yaml

# Notun tam metni + etkileşim verileri (arama sonucundaki xsec_token içeren tam URL'yi kullan)
opencli xiaohongshu note "NOTE_URL" -f yaml

# Yorumlar (iç içe yanıtlar dahil)
opencli xiaohongshu comments NOTE_ID -f yaml

# Ana sayfa öneri akışı
opencli xiaohongshu feed -f yaml

# Kullanıcı profilindeki herkese açık notlar
opencli xiaohongshu user USER_ID -f yaml
```

> Chrome'un açık ve OpenCLI eklentisinin kurulu olması gerekir. OpenCLI yalnızca kullanıcının
> zaten açık ve kendi kontrolündeki Chrome oturumunu kullanır; Agent Reach kullanıcı adına giriş
> yapmaz ve tarayıcı cookie'lerini okumaz.
> `agent-reach configure xhs-cookies`, cookie'leri OpenCLI'a enjekte etmez.
> Hazır bir oturum yoksa girişi otomatikleştirme; Backend B/C'ye geç ve ilgili Cookie-Editor ile
> elle dışa aktarma akışını izle.

### Backend B: xiaohongshu-mcp (sunucu senaryosu)

```bash
# Kimlik doğrulamadan önce kullanıcıdan Cookie-Editor ile elle dışa aktarmasını iste, sonra açıkça içe aktar
agent-reach configure xhs-cookies

# Mevcut durumu salt-okunur kontrol et
mcporter call xiaohongshu.check_login_status --timeout 120000

# Arama
mcporter call xiaohongshu.search_feeds keyword="query" --timeout 120000

# Not ayrıntısı + yorumlar (feed_id ve xsec_token arama sonucundan alınır)
mcporter call xiaohongshu.get_feed_detail feed_id="..." xsec_token="..." --timeout 120000
```

> İlk çağrıda yaklaşık 150MB'lık headless tarayıcı otomatik indirilir; mutlaka
> `--timeout 120000` ekle.
> Kimlik doğrulama yalnızca Cookie-Editor ile elle dışa aktarma üzerinden yapılır; içe aktardıktan
> sonra önce `check_login_status` çalıştır.
> Bu açık komut, kullanıcının verdiği xiaohongshu.com alan adına ait cookie setini kaydeder/içe
> aktarır; kullanıcı kapsamı onaylamalıdır. xiaohongshu.com dışındaki alan adlarına ait cookie'ler
> yok sayılır.

### Backend C: xhs-cli (eski alternatif; upstream 2026-03'ten beri güncellenmiyor)

```bash
xhs search "query"          # arama
xhs read NOTE_ID_OR_URL     # notu oku (arama sonucundaki URL/ID şart, çıplak note_id olmaz)
xhs comments NOTE_ID_OR_URL # yorumlar
xhs hot                     # popüler
xhs feed                    # öneriler
```

> Bilinen kararsızlık: `xhs user` / `xhs user-posts` / `xhs favorites` API error döndürebilir
> (upstream güncellenmiyor, düzelten yok). Yeni kullanıcılar doğrudan Backend A/B'yi kullanmalı.

### Genel notlar

> **Kimlik doğrulama sınırı**: Agent Reach kullanıcı adına XiaoHongShu girişi yapamaz ve tarayıcı
> cookie'lerini okuyamaz. OpenCLI yalnızca kullanıcının zaten açık ve kendi kontrolündeki Chrome
> oturumunu kullanabilir; xiaohongshu-mcp / eski araçlar Cookie-Editor ile elle dışa aktarma kullanır.
>
> **xsec_token kısıtı**: XiaoHongShu xsec_token mekanizmasını zorunlu kılar, **çıplak note_id ile
> doğrudan okunamaz**. Doğru akış: önce arama/feed ile sonuç al, sonra sonuçtaki tam URL/ID ile oku.
> Üç backend için de aynıdır.
>
> **Hız sınırı**: Yüksek frekanslı istekler (toplu arama, yorumlarda derin gezinme) doğrulama kodu
> tetikler; platform kısıtıdır, aşılamaz. İşlemler arasında 2-3 saniye bekle.
>
> **Yazma işlemleri (paylaşım/yorum/beğeni)**: Salt-okunur kalman önerilir. xhs-cli v0.6.x yazma
> işlemleri imza sorunu yüzünden 406 döndürebilir.

## Twitter/X (twitter-cli)

### Kimlik doğrulama ön koşulu

`agent-reach configure twitter-cookies` ile gizli girişle kaydedilen cookie'ler yalnızca
`agent-reach doctor`'ın açık kimlik bilgilerinin eksiksiz olup olmadığını kontrol etmesi içindir.
`doctor`, upstream `twitter status` komutunu çalıştırmaz ve mevcut shell'i de yapılandırmaz.
Aşağıdaki herhangi bir `twitter` komutunu çalıştırmadan önce aynı shell'de veya alt süreç
ortamında şunları açıkça ver:

```bash
export TWITTER_AUTH_TOKEN="..."
export TWITTER_CT0="..."
```

> PowerShell karşılığı: `$env:TWITTER_AUTH_TOKEN = "..."` ve `$env:TWITTER_CT0 = "..."`.
> Değerleri asla loglama veya ekrana yazdırma.

### Kararlı komutlar

```bash
# Ana sayfa zaman akışı (en kararlı)
twitter feed -n 20

# Tek bir tweet'i oku (yanıtlar dahil)
twitter tweet URL_OR_ID

# Uzun yazı / X Article oku
twitter article URL_OR_ID

# Kullanıcı zaman akışı
twitter user-posts @username -n 20

# Kullanıcı profili
twitter user @username
```

### Kararsız olabilecek komutlar

```bash
# Tweet ara (Twitter GraphQL uç noktalarını sık değiştirir, 404 dönebilir)
twitter search "query" -n 10

# likes (2024'ten sonra yalnızca kendi beğenilerini görebilirsin, platform kısıtı)
twitter likes
```

### search başarısız olursa yeniden deneme zinciri (sırayla, başarılı olunca dur)

1. Doğrudan bir kez tekrar dene (ara sıra başarısızlık yaygındır): `twitter search "query" -n 10`
2. Güncelleyip tekrar dene: `pipx upgrade twitter-cli && twitter search "query" -n 10`
3. OpenCLI alternatifine geç (masaüstü, tarayıcı oturumunu kullanır): `opencli twitter search "query" -f yaml`
4. Hiçbiri olmazsa `twitter feed` / `twitter user-posts @somebody` gibi kararlı komutlarla dolaylı yoldan git

### Önemli notlar

> **Kurulum**: `pipx install twitter-cli` (v0.8.5+ olduğundan emin ol)
>
> **Kimlik doğrulama**: Yalnızca Cookie-Editor ile elle dışa aktar, sonra ortam değişkenlerini
> `TWITTER_AUTH_TOKEN` + `TWITTER_CT0` olarak açıkça ayarla; otomatik tarayıcı okumasına güvenme.
>
> **IP risk kontrolü**: VPS/veri merkezi IP'lerinden sık çağrı yapma, özellikle
> followers/following — hesap kapatılma riski var. Konut proxy'si veya yerel ortam kullan.
>
> **OpenCLI alternatifi**: Masaüstünde OpenCLI kuruluysa `opencli twitter search/article/user-posts -f yaml`
> komutlarının hepsi çalışır (tarayıcı oturumu; cookie ortam değişkeni gerekmez).
>
> **Çıktı formatı**: Yapılandırılmış çıktı için `--yaml` veya `--json` kullan; AI agent için daha uygundur.

## Bilibili

> ⚠️ **Bilibili'yi yt-dlp ile okuma** (bot koruması her şeyi 412 ile engelliyor, testlerde çözüm yok).
> bili-cli / OpenCLI kullan.

```bash
# Arama / popüler / video ayrıntısı (bili-cli, salt-okunur, giriş gerekmez)
bili search "query" --type video -n 5
bili hot -n 10
bili video BVxxx

# Altyazı (OpenCLI, masaüstü Chrome gerekir)
opencli bilibili subtitle BVxxx
```

> Ayrıntılı komutlar (ses transkripsiyonu, doğrudan API son çaresi) için bkz. [video.md](video.md).

## V2EX (herkese açık API)

Kimlik doğrulama gerekmez, herkese açık API doğrudan çağrılır.

### Popüler konular

```bash
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"
```

### Düğüm (node) konuları

```bash
# node_name örnekleri: python, tech, jobs, qna, programmers
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"
```

### Konu ayrıntısı

```bash
# topic_id URL'den alınır, ör. https://www.v2ex.com/t/1234567
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"
```

### Konu yanıtları

```bash
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"
```

### Kullanıcı bilgisi

```bash
curl -s "https://www.v2ex.com/api/members/show.json?username=USERNAME" -H "User-Agent: agent-reach/1.0"
```

> Windows PowerShell'de `curl` yerine `curl.exe` yaz.

### Python çağrı örneği

```python
from agent_reach.channels.v2ex import V2EXChannel

ch = V2EXChannel()

# Popüler gönderileri al
topics = ch.get_hot_topics(limit=10)
for t in topics:
    print(f"[{t['node_title']}] {t['title']} ({t['replies']} yanıt)")

# Düğüm gönderilerini al
node_topics = ch.get_node_topics("python", limit=5)

# Gönderi ayrıntısı + yanıtlar
topic = ch.get_topic(1234567)
print(topic["title"], "—", topic["author"])

# Kullanıcı bilgisi
user = ch.get_user("Livid")
```

> **Düğüm listesi**: https://www.v2ex.com/planes

## Reddit (çoklu backend, giriş gerekir)

**Reddit'in kurulumsuz yolu yok**: anonim `.json` uç noktaları engellendi (403), resmi API 2025-11'den
beri elle onaya tabi ve neredeyse hiç onaylanmıyor. İki backend de giriş yapılmış oturuma dayanır;
önce `agent-reach doctor --json` çalıştırıp reddit için `active_backend` değerine bak. Çin anakarasından
erişim için proxy gerekir.

### Backend A: OpenCLI (masaüstünde tercih edilir, tarayıcı oturumunu kullanır)

```bash
# Gönderi ara
opencli reddit search "query" -f yaml

# Gönderinin tam metni + yorumlar
opencli reddit read POST_ID -f yaml

# Subreddit / popüler / Popular akışına göz at
opencli reddit subreddit LocalLLaMA -f yaml
opencli reddit hot -f yaml
opencli reddit popular -f yaml

# Subreddit meta bilgisi (abone sayısı, açıklama)
opencli reddit subreddit-info LocalLLaMA -f yaml
```

> Chrome'un açık olması ve tarayıcıda reddit.com'a giriş yapılmış olması gerekir.

### Backend B: rdt-cli (eski/sunucu alternatifi; upstream 2026-03'ten beri güncellenmiyor)

```bash
rdt search "query" --limit 10   # gönderi ara
rdt read POST_ID                # gönderinin tam metni + yorumlar
rdt sub python --limit 20       # subreddit'e göz at
rdt popular --limit 10          # popüler
rdt all --limit 10              # /r/all
```

> **Kurulum**: `pipx install 'git+https://github.com/public-clis/rdt-cli.git'` (PyPI sürümü geride;
> GitHub'dan v0.4.2+ kur). Arama ve okuma için önce kullanıcının `rdt login` yapması gerekir
> (tarayıcısız sunucuda cookie elle yazılır, bkz. doctor çıktısı).
> AI agent için daha uygun olduğundan `--yaml` çıktısı önerilir.

### İleri seçenek: resmi API + PRAW (yalnızca zaten kimlik bilgisi olan kullanıcılar)

2025-11'den önce Reddit script app kaydetmiş (client_id/client_secret sahibi) kullanıcılar PRAW ile
resmi API'yi kullanabilir (100 QPM ücretsiz). Yeni başvurular elle onaylanıyor ve kişisel projeler
neredeyse hiç onaylanmıyor; **yeni kullanıcılara bu yolu önerme**.

## Facebook (OpenCLI, giriş gerekir)

Facebook, OpenCLI üzerinden kullanıcının Chrome'undaki facebook.com oturumunu kullanır. Önce
`agent-reach doctor --json` çalıştırıp facebook için `active_backend` değerine bak; normalde
`OpenCLI` olmalı. Jina/Exa/Graph API'yi varsayılan yol olarak önerme.

```bash
# Kullanıcı / sayfa / gönderi ara
opencli facebook search "query" -f yaml

# Kullanıcı veya sayfa bilgisi
opencli facebook profile zuck -f yaml

# Mevcut hesabın News Feed'i
opencli facebook feed --limit 10 -f yaml

# Mevcut hesabın görebildiği grup listesi / son etkinlikler
opencli facebook groups --limit 20 -f yaml
```

> Chrome'un açık, OpenCLI eklentisinin kurulu ve facebook.com'a giriş yapılmış olması gerekir.
> Facebook Groups için şu an yalnızca mevcut hesabın görebildiği grup listesi / son etkinlikler
> okunabilir; herhangi bir grubun gönderileri ve yorumları için API garantisi yoktur.

## Instagram (OpenCLI, giriş gerekir)

Instagram, OpenCLI üzerinden kullanıcının Chrome'undaki instagram.com oturumunu kullanır. Önce
`agent-reach doctor --json` çalıştırıp instagram için `active_backend` değerine bak; normalde
`OpenCLI` olmalı. instaloader'ı varsayılan olarak geri getirme; geçmişte cookies/401/429 sorunları
yüzünden kararsızdı.

```bash
# Kullanıcı ara (sitedeki gönderilerde anahtar kelime araması değildir)
opencli instagram search "query" -f yaml

# Kullanıcı profili
opencli instagram profile nasa -f yaml

# Kullanıcının son gönderileri
opencli instagram user nasa --limit 12 -f yaml

# Explore / Discover
opencli instagram explore --limit 20 -f yaml

# Mevcut hesabın kaydedilenleri
opencli instagram saved --limit 20 -f yaml
```

> Chrome'un açık, OpenCLI eklentisinin kurulu ve instagram.com'a giriş yapılmış olması gerekir.
> `instagram search` bir kullanıcı aramasıdır; gönderi okumak için önce username'i belirle, sonra
> `instagram user USERNAME` kullan. 429 / login required görülürse kullanıcıdan Chrome'da tekrar
> giriş yapmasını iste ve istek sıklığını azalt.

## Burada olmayan bir platform veya komut

Önce `opencli list` ile adapter var mı bak; yoksa veya erişim engelleniyorsa
[opencli-fallback.md](opencli-fallback.md) merdivenini izle.
