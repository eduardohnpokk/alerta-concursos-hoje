import feedparser
import re
import os
from datetime import datetime

# CONFIGURAÇÕES DE AFILIADO
AMAZON_TAG = "eduardohen00f-20"
SHOPEE_ID = "18368470403"

def limpar_titulo(titulo):
    return re.sub(r'[^\w\s]', '', titulo).replace(' ', '+')

def identificar_status(titulo):
    t = titulo.lower()
    if "aberto" in t or "inscrições" in t or "edital publicado" in t:
        return '<span class="tag tag-aberto">Aberto</span>'
    if "previsto" in t or "autorizado" in t or "anunciado" in t:
        return '<span class="tag tag-previsto">Previsto</span>'
    return '<span class="tag tag-news">Notícia</span>'

# 1. LER NOTÍCIAS (Expandido para pegar mais notícias)
rss_url = "https://news.google.com/rss/search?q=concurso+público+edital+aberto+previsto+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
feed = feedparser.parse(rss_url)

# 2. MONTAR O HTML DAS NOTÍCIAS
html_dinamico = ""
for i, entry in enumerate(feed.entries):
    termo = limpar_titulo(entry.title)
    status = identificar_status(entry.title)
    link_amz = f"https://www.amazon.com.br/s?k=apostila+{termo}&tag={AMAZON_TAG}"
    link_shp = f"https://shopee.com.br/search?keyword=apostila%20{termo}"
    
    html_dinamico += f"""
    <div class="card" data-titulo="{entry.title.lower()}">
        {status}
        <h3>{entry.title}</h3>
        <p class="data">🕒 {entry.published}</p>
        <div class="buttons-container">
            <a href="{entry.link}" class="btn-link" target="_blank">🔗 Ver Edital/Notícia</a>
            <a href="{link_amz}" class="btn btn-amazon" target="_blank">🛒 Apostilas Amazon</a>
            <a href="{link_shp}" class="btn btn-shopee" target="_blank">🛍️ Apostilas Shopee</a>
        </div>
    </div>
    """

# 3. TEMPLATE COM SISTEMA DE FILTRO (JAVASCRIPT INCLUÍDO)
template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alerta Concursos Hoje | Filtro Inteligente</title>
    <style>
        :root {{ --primary: #2c3e50; --accent: #e74c3c; --amazon: #f39c12; --shopee: #ee4d2d; --bg: #f8f9fa; }}
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); }}
        header {{ background: #000; color: white; padding: 30px; text-align: center; border-bottom: 4px solid var(--accent); }}
        .container {{ max-width: 900px; margin: auto; padding: 20px; }}
        
        /* Menu de Filtros */
        .filter-bar {{ background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }}
        .filter-btn {{ padding: 8px 15px; border: 1px solid #ddd; border-radius: 20px; cursor: pointer; background: white; font-size: 14px; transition: 0.3s; }}
        .filter-btn:hover, .filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
        
        .card {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-left: 5px solid #ccc; }}
        .tag {{ padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; color: white; }}
        .tag-aberto {{ background: #27ae60; }}
        .tag-previsto {{ background: #f1c40f; color: #333; }}
        .tag-news {{ background: #3498db; }}
        
        .buttons-container {{ display: flex; gap: 8px; margin-top: 15px; flex-wrap: wrap; }}
        .btn {{ flex: 1; padding: 10px; border-radius: 5px; text-decoration: none; font-weight: bold; font-size: 13px; text-align: center; color: white; }}
        .btn-amazon {{ background: var(--amazon); }}
        .btn-shopee {{ background: var(--shopee); }}
        .btn-link {{ color: var(--primary); border: 1px solid var(--primary); padding: 10px; flex: 1; text-align: center; text-decoration: none; border-radius: 5px; font-size: 13px; }}
        
        footer {{ text-align: center; padding: 40px; color: #888; font-size: 13px; }}
    </style>
</head>
<body>
    <header>
        <h1>📍 Alerta Concursos Hoje</h1>
        <p>Filtre por editais abertos, previstos ou por estado</p>
    </header>

    <div class="container">
        <div class="filter-bar">
            <button class="filter-btn active" onclick="filtrar('todos')">Todos</button>
            <button class="filter-btn" onclick="filtrar('aberto')">Editais Abertos</button>
            <button class="filter-btn" onclick="filtrar('previsto')">Previstos</button>
            <button class="filter-btn" onclick="filtrar('sp')">São Paulo</button>
            <button class="filter-btn" onclick="filtrar('rj')">Rio de Janeiro</button>
            <button class="filter-btn" onclick="filtrar('mg')">Minas Gerais</button>
            <button class="filter-btn" onclick="filtrar('federal')">Federais</button>
        </div>

        <div id="noticias">
            {html_dinamico}
        </div>
    </div>

    <script>
        function filtrar(termo) {{
            const cards = document.querySelectorAll('.card');
            const botoes = document.querySelectorAll('.filter-btn');
            
            botoes.forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');

            cards.forEach(card => {{
                const texto = card.getAttribute('data-titulo');
                if (termo === 'todos') {{
                    card.style.display = 'block';
                }} else if (texto.includes(termo)) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
    </script>

    <footer>
        <p><b>Alerta Concursos Hoje</b> &copy; {datetime.now().year}</p>
        <p>As informações são atualizadas automaticamente via Google News.</p>
    </footer>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(template)
