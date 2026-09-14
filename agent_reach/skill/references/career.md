# Kariyer ve iş ilanları

LinkedIn.

## LinkedIn

```bash
# Kişi profilini getir
mcporter call linkedin.get_person_profile linkedin_username="username" sections="experience,education"

# Kişi ara
mcporter call linkedin.search_people keywords="AI engineer" location="Shanghai"

# Şirket profilini getir
mcporter call linkedin.get_company_profile company_name="openai" sections="posts,jobs"

# İş ilanı ara
mcporter call linkedin.search_jobs keywords="software engineer" location="Remote" max_pages=2
```

> **Giriş gerekir**: İlk kullanımdan önce `uvx mcp-server-linkedin@latest --login` çalıştırıp
> geçerli bir oturum kaydet.

### Yedek yöntem

MCP kullanılamıyorsa Jina Reader ile oku:

```bash
curl -s "https://r.jina.ai/https://linkedin.com/in/username"
```

Giriş duvarına takılırsa [opencli-fallback.md](opencli-fallback.md) merdivenini izle.
