import feedparser
import re
import os
from datetime import datetime

# CONFIGURAÇÕES
AMAZON_TAG = "eduardohen00f-20"
SHOPEE_ID = "18368470403"

def limpar_titulo(titulo):
    return re.sub(r'[^\w\s]', '', titulo).replace(' ', '+')

# 1. LER NOTÍCIAS
rss_url = "https://news.google.com/rss/search?q=inscrições+abertas+concurso+edital+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
feed = feedparser.parse(rss_url)

# 2. MONTAR O HTML
html_dinamico = ""
for entry in feed.entries:
    termo = limpar_titulo(entry.title)
    link_amz = f"https://www.amazon.com.br/s?k=apostila+{termo}&tag={AMAZON_TAG}"
    link_shp = f"https://shopee.com.br/search?keyword=apostila%20{termo}"
    
    html_dinamico += f"""
    <div class="card">
        <h3>{entry.title}</h3>
        <p>Publicado em: {entry.published}</p>
        <a href="{entry.link}" target="_blank">Ler Notícia</a><br><br>
        <a href="{link_amz}" class="btn" target="_blank">🛒 Apostilas Amazon</a>
        <a href="{link_shp}" class="btn" style="background:#ee4d2d" target="_blank">🛍️ Apostilas Shopee</a>
    </div>
    """

# 3. ESCREVER O ARQUIVO INDEX.HTML FINAL
template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alerta Concursos Hoje</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: auto; padding: 20px; background: #f4f4f4; }}
        .card {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .btn {{ display: inline-block; background: #27ae60; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 10px; }}
        h1 {{ color: #2c3e50; text-align: center; }}
    </style>
</head>
<body>
    <h1>📍 Alerta Concursos Hoje</h1>
    <p style="text-align:center">Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    <div id="noticias">
        {html_dinamico}
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(template)
