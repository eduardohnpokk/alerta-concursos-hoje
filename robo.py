import feedparser
import re
import os
from datetime import datetime

# CONFIGURAÇÕES DE AFILIADO (MANTIDAS)
AMAZON_TAG = "eduardohen00f-20"
SHOPEE_ID = "18368470403"

def limpar_titulo(titulo):
    return re.sub(r'[^\w\s]', '', titulo).replace(' ', '+')

def identificar_categorias(titulo):
    t = titulo.lower()
    tags = []
    # Nível
    if "médio" in t or "medio" in t: tags.append("nivel-medio")
    if "superior" in t or "graduação" in t: tags.append("nivel-superior")
    # Área
    if "polícia" in t or "policia" in t or "militar" in t or "gcm" in t: tags.append("area-policial")
    if "tribunal" in t or "tre" in t or "trj" in t or "tj" in t: tags.append("area-tribunal")
    if "saúde" in t or "saude" in t or "médico" in t or "enfermeiro" in t: tags.append("area-saude")
    if "educação" in t or "professor" in t or "sme" in t: tags.append("area-educacao")
    # Status
    status_html = ""
    if "aberto" in t or "inscrições" in t: status_html = '<span class="tag tag-aberto">Aberto</span>'
    elif "previsto" in t or "autorizado" in t: status_html = '<span class="tag tag-previsto">Previsto</span>'
    else: status_html = '<span class="tag tag-news">Notícia</span>'
    
    return " ".join(tags), status_html

# 1. LER NOTÍCIAS
rss_url = "https://news.google.com/rss/search?q=concurso+público+edital+aberto+previsto+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
feed = feedparser.parse(rss_url)

# 2. MONTAR CARDS
html_dinamico = ""
for entry in feed.entries:
    termo = limpar_titulo(entry.title)
    categorias, status_tag = identificar_categorias(entry.title)
    link_amz = f"https://www.amazon.com.br/s?k=apostila+{termo}&tag={AMAZON_TAG}"
    link_shp = f"https://shopee.com.br/search?keyword=apostila%20{termo}"
    
    html_dinamico += f"""
    <div class="card {categorias}" data-titulo="{entry.title.lower()}">
        {status_tag}
        <h3>{entry.title}</h3>
        <p class="data">🕒 {entry.published}</p>
        <div class="buttons-container">
            <a href="{entry.link}" class="btn-link" target="_blank">🔗 Ver Detalhes</a>
            <a href="{link_amz}" class="btn btn-amazon" target="_blank">🛒 Apostilas Amazon</a>
            <a href="{link_shp}" class="btn btn-shopee" target="_blank">🛍️ Apostilas Shopee</a>
        </div>
    </div>
    """

# 3. TEMPLATE VISUAL COM FILTROS AVANÇADOS
template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alerta Concursos Hoje</title>
    <style>
        :root {{ --primary: #2c3e50; --accent: #e74c3c; --amazon: #f39c12; --shopee: #ee4d2d; --bg: #f4f7f6; }}
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); }}
        header {{ background: #000; color: white; padding: 30px 10px; text-align: center; border-bottom: 4px solid var(--accent); }}
        .container {{ max-width: 1000px; margin: auto; padding: 20px; }}
        
        .filter-section {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .filter-group {{ margin-bottom: 15px; }}
        .filter-group label {{ font-weight: bold; display: block; margin-bottom: 8px; font-size: 14px; color: var(--primary); }}
        .filter-bar {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .filter-btn {{ padding: 6px 14px; border: 1px solid #ddd; border-radius: 20px; cursor: pointer; background: #fff; font-size: 13px; }}
        .filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
        
        .card {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 12px; border-left: 6px solid #ddd; }}
        .card.hidden {{ display: none; }}
        .tag {{ padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; color: white; }}
        .tag-aberto {{ background: #27ae60; }} .tag-previsto {{ background: #f1c40f; color: #000; }} .tag-news {{ background: #3498db; }}
        
        .buttons-container {{ display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap; }}
        .btn {{ flex: 1; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; text-align: center; color: white; font-size: 13px; }}
        .btn-amazon {{ background: var(--amazon); }} .btn-shopee {{ background: var(--shopee); }}
        .btn-link {{ color: var(--primary); border: 1px solid var(--primary); flex: 1; text-align: center; text-decoration: none; border-radius: 6px; padding: 12px; font-size: 13px; }}
    </style>
</head>
<body>
    <header><h1>📍 Alerta Concursos Hoje</h1><p>Central de Oportunidades e Estudos</p></header>
    <div class="container">
        <div class="filter-section">
            <div class="filter-group">
                <label>📍 Por Estado:</label>
                <div class="filter-bar">
                    <button class="filter-btn active" onclick="setFiltro('estado', 'todos')">Todos</button>
                    <button class="filter-btn" onclick="setFiltro('estado', 'sp')">SP</button>
                    <button class="filter-btn" onclick="setFiltro('estado', 'rj')">RJ</button>
                    <button class="filter-btn" onclick="setFiltro('estado', 'mg')">MG</button>
                </div>
            </div>
            <div class="filter-group">
                <label>🎓 Nível / Área:</label>
                <div class="filter-bar">
                    <button class="filter-btn" onclick="setFiltro('cat', 'nivel-medio')">Médio</button>
                    <button class="filter-btn" onclick="setFiltro('cat', 'nivel-superior')">Superior</button>
                    <button class="filter-btn" onclick="setFiltro('cat', 'area-policial')">Policial</button>
                    <button class="filter-btn" onclick="setFiltro('cat', 'area-saude')">Saúde</button>
                </div>
            </div>
        </div>
        <div id="noticias">{html_dinamico}</div>
    </div>
    <script>
        let filtros = {{ estado: 'todos', cat: 'todos' }};
        function setFiltro(tipo, valor) {{
            filtros[tipo] = valor;
            document.querySelectorAll('.filter-btn').forEach(b => {{
                if(b.innerText.toLowerCase().includes(valor)) b.classList.add('active');
            }});
            aplicarFiltros();
        }}
        function aplicarFiltros() {{
            document.querySelectorAll('.card').forEach(card => {{
                const matchEstado = filtros.estado === 'todos' || card.getAttribute('data-titulo').includes(filtros.estado);
                const matchCat = filtros.cat === 'todos' || card.classList.contains(filtros.cat);
                card.classList.toggle('hidden', !(matchEstado && matchCat));
            }});
        }}
    </script>
</body>
</html>
