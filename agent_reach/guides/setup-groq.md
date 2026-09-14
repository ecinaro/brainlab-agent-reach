# Groq Whisper kurulum rehberi

## Ne işe yarar?
YouTube/Bilibili videosunun altyazısı yoksa sesi Groq'un Whisper API'si ile yazıya döker. Groq ücretsiz kota verir.

## Ajanın kendi yapabileceği adımlar

1. Zaten ayarlı mı kontrol et:
```bash
agent-reach doctor | grep -i "groq\|whisper"
```

2. Kullanıcı anahtarı verdiyse ayara yaz:
```python
from agent_reach.config import Config
c = Config()
c.set("groq_api_key", "KULLANICININ_VERDIGI_ANAHTAR")
```

3. Test et (isteğe bağlı):
```bash
curl -s https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer KULLANICININ_VERDIGI_ANAHTAR" \
  -o /dev/null -w "%{http_code}"
```
200 dönerse = çalışıyor

## Kullanıcının elle yapması gerekenler

Kullanıcıya şunu söyle:

> Videodaki konuşmayı yazıya dökmek için bir Groq API anahtarı lazım (ücretsiz).
>
> Adımlar:
> 1. https://console.groq.com adresini aç
> 2. Google hesabınla ya da e-postanla kayıt ol
> 3. Soldaki "API Keys"e tıkla
> 4. "Create API Key"e tıkla
> 5. Oluşan anahtarı kopyala ve bana ver
>
> Groq ücretsiz kota veriyor, günlük kullanım için fazlasıyla yeterli.

## Ajan anahtarı aldıktan sonra

1. Ayara yaz: `config.set("groq_api_key", key)`
2. API'nin çalıştığını test et
3. Kullanıcıya söyle: "✅ Sesi yazıya dökme açıldı! Artık altyazısı olmayan videoların içeriğini de çıkarabilirim."
