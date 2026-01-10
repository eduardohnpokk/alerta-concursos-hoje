import feedparser
import re
import os
from datetime import datetime

# CONFIGURAÇÕES DE AFILIADO DO EDUARDO
AMAZON_TAG = "eduardohen00f-20"
SHOPEE_ID = "18368470403"

def limpar_titulo(titulo):
    return re.sub(r'[^\w\s]', '', titulo).replace(' ', '+')

# LER NOTÍCIAS DE CONCURSOS (GOOGLE NEWS)
rss_url = "https://news.google.com/rss/search?q=inscrições+abertas+concurso+edital+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
feed = feedparser.parse(rss_url)

# CRIAR O CONTEÚDO PARA O SITE
print(f"Detectadas {len(feed.entries)} notícias hoje...")

for entry in feed.entries:
    termo_busca = limpar_titulo(entry.title)
    
    link_amazon = f"https://www.amazon.com.br/s?k=apostila+{termo_busca}&tag={AMAZON_TAG}"
    link_shopee = f"https://shopee.com.br/search?keyword=apostila%20{termo_busca}"

    # Aqui o robô gera o texto de cada postagem
    post_modelo = f"""
# {entry.title}
*Publicado em: {entry.published}*

Notícia completa em: {entry.link}

---
### 📚 ESTUDE PARA ESTE CONCURSO:
👉 [Ver Apostilas na AMAZON]({link_amazon})
👉 [Ver Apostilas na SHOPEE]({link_shopee})
    """
    # Exibe no log (depois faremos salvar em arquivo)
    print(f"--- Post gerado para: {entry.title}")
