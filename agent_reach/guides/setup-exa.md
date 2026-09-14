# Exa Search kurulum rehberi

## Ne işe yarar?
Exa, anlama göre arama yapan bir yapay zekâ arama motorudur. MCP üzerinden bağlanır: **ücretsiz, API anahtarı gerekmez.** Kurulunca şunlar açılır:
- İnternette anlamsal arama
- Reddit araması (`site:reddit.com` ile)
- Twitter araması (`site:x.com` ile)

## Ajanın kendi yapabileceği adımlar

Kullanıcı açıkça izin verdikten sonra `agent-reach install --env=auto --system` aşağıdaki adımları yapar.
`--system` olmadan çalışan varsayılan komut sadece kontrol eder, hiçbir şeyi değiştirmez.

### 1. mcporter'ı kur
```bash
npm install -g mcporter
```

### 2. Exa MCP'yi kaydet
```bash
mcporter config add exa https://mcp.exa.ai/mcp --scope home
```

### 3. Doğrula
```bash
agent-reach doctor | grep "Search"
mcporter call exa.web_search_exa query="test" numResults=1
```

## Kullanıcının elle yapması gerekenler

**Hiçbir şey.** Exa MCP ile bağlanır; ücretsizdir, kayıt ve API anahtarı gerekmez.

`agent-reach install --system` ağ sorunu yüzünden Exa'yı ayarlayamadıysa yukarıdaki iki komutu elle çalıştırman yeterli.

## Sık sorulanlar

**S: Arama sayısı sınırı var mı?**
C: MCP adresi Exa'nın kendisi tarafından sağlanıyor (mcp.exa.ai) ve şu an ücretsiz, sınırsız. İleride değişirse agent-reach güncellemesiyle uyarlanır.

**S: mcporter nedir?**
C: MCP protokolü için bir komut satırı köprüsü; MCP sunucularını çağırmaya yarar. Agent Reach bunu Exa ve XiaoHongShu'ya bağlanmak için kullanır.
