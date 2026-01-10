import feedparser
import re
import os
from datetime import datetime

# CONFIGURAÇÕES DE AFILIADO
AMAZON_TAG = "eduardohen00f-20"
SHOPEE_ID = "18368470403"

def limpar_titulo(titulo):
    return re.sub(r'[^\w\s]', '', titulo).replace(' ', '+')

def identificar_categorias(titulo):
    t = titulo.lower()
    cats = []
    mapeamento = {
        'Nível Médio': ['médio', 'medio', 'fundamental'],
        'Nível Superior': ['superior', 'graduação', 'graduacao'],
        'Policial': ['polícia', 'policia', 'militar', 'gcm', 'segurança'],
        'Saúde': ['saúde', 'saude', 'médico', 'medico', 'enfermeiro', 'hospital'],
        'Tribunais': ['tribunal', 'tj', 'tre', 'trf', 'tse'],
        'Educação': ['educação', 'educacao', 'professor', 'sme', 'ensino']
    }
    for nome_exibicao, palavras in mapeamento.items():
        if any(p in t for p in palavras):
            cats.append(nome_exibicao)
    
    tag_html = ""
    if "aberto" in t or "inscrições" in t:
        tag_html = '<span class="tag tag-aberto">Aberto</span>'
    elif "previsto" in t or "autorizado" in t:
        tag_html = '<span class="tag tag-previsto">Previsto</span>'
    else:
        tag_html = '<span class="tag tag-news">Notícia</span>'
    
    return cats, tag_html

# 1. LER NOTÍCIAS
rss_url = "https://news.google.com/rss/search?q=concurso+público+edital+aberto+previsto+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
feed = feedparser.parse(rss_url)

# 2. PROCESSAR NOTÍCIAS
lista_cards = []
categorias_encontradas = set()
texto_seo = ""

for entry in feed.entries:
    cats_nome, status_html = identificar_categorias(entry.title)
    termo = limpar_titulo(entry.title)
    texto_seo += entry.title + ", "
    
    for c in cats_nome:
        categorias_encontradas.add(c)
    
    classes_css = " ".join([f"cat-{c.replace(' ', '-').lower()}" for c in cats_nome])
    link_amz = f"https://www.amazon.com.br/s?k=apostila+{termo}&tag={AMAZON_TAG}"
    link_shp = f"https://shopee.com.br/search?keyword=apostila%20{termo}"
    
    card = f"""
    <article class="card {classes_css}" data-titulo="{entry.title.lower()}">
        {status_html}
        <h2>{entry.title}</h2>
        <p class="data">🕒 Publicado em: {entry.published}</p>
        <div class="buttons-container">
            <a href="{entry.link}" class="btn-link" target="_blank" rel="nofollow">🔗 Ver Edital Oficial</a>
            <a href="{link_amz}" class="btn btn-amazon" target="_blank">🛒 Apostilas Amazon</a>
            <a href="{link_shp}" class="btn btn-shopee" target="_blank">🛍️ Apostilas Shopee</a>
        </div>
    </article>
    """
    lista_cards.append(card)

botoes_html = '<button class="filter-btn active" onclick="filtrar(\'todos\')">Todos</button>'
for cat in sorted(categorias_encontradas):
    classe_filtro = f"cat-{cat.replace(' ', '-').lower()}"
    botoes_html += f'<button class="filter-btn" onclick="filtrar(\'{classe_filtro}\')">{cat}</button>'

# 3. GERAR O SITE COM META TAGS SEO
template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alerta Concursos Hoje | Editais Abertos e Apostilas 2026</title>
    
    <meta name="description" content="Acompanhe diariamente os novos editais de concursos abertos e previstos. Encontre materiais de estudo e apostilas para {texto_seo[:150]}...">
    <meta name="keywords" content="concursos 2026, editais abertos, apostilas concurso, inscrições abertas, concurso público">
    <meta name="robots" content="index, follow">
    
    <meta property="og:title" content="📍 Alerta Concursos Hoje | Portal Automático de Editais">
    <meta property="og:description" content="Veja as vagas de hoje e prepare-se com as melhores apostilas.">
    <meta property="og:type" content="website">
    
    <style>
        :root {{ --primary: #2c3e50; --accent: #e74c3c; --amazon: #f39c12; --shopee: #ee4d2d; --bg: #f4f7f6; }}
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); color: #333; }}
        header {{ background: linear-gradient(135deg, #000 0%, #2c3e50 100%); color: white; padding: 40px 10px; text-align: center; border-bottom: 4px solid var(--accent); }}
        .container {{ max-width: 900px; margin: auto; padding: 20px; }}
        .filter-bar {{ background: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .filter-btn {{ padding: 7px 15px; border: 1px solid #ddd; border-radius: 20px; cursor: pointer; background: white; font-size: 13px; font-weight: 500; }}
        .filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
        .card {{ background: white; padding: 25px; margin-bottom: 25px; border-radius: 12px; border-left: 6px solid #ddd; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }}
        .card.hidden {{ display: none; }}
        .card h2 {{ font-size: 1.4em; margin-top: 5px; color: var(--primary); }}
        .tag {{ padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; color: white; text-transform: uppercase; }}
        .tag-aberto {{ background: #27ae60; }} .tag-previsto {{ background: #f1c40f; color: #000; }} .tag-news {{ background: #3498db; }}
        .buttons-container {{ display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap; }}
        .btn {{ flex: 1; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; text-align: center; color: white; font-size: 13px; }}
        .btn-amazon {{ background: var(--amazon); }} .btn-shopee {{ background: var(--shopee); }}
        .btn-link {{ color: var(--primary); border: 1px solid var(--primary); flex: 1; text-align: center; text-decoration: none; border-radius: 6px; padding: 12px; font-size: 13px; }}
        footer {{ text-align: center; padding: 50px 20px; color: #888; font-size: 13px; background: #eee; margin-top: 40px; }}
    </style>
</head>
<body>
    <header>
        <h1>📍 Alerta Concursos Hoje</h1>
        <p>Editais Atualizados em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
    </header>
    <main class="container">
        <nav class="filter-bar" aria-label="Filtros de notícias">{botoes_html}</nav>
        <div id="noticias">{" ".join(lista_cards)}</div>
    </main>
    <footer>
        <p><b>Alerta Concursos Hoje</b> - {datetime.now().year}</p>
        <p>As melhores oportunidades de concursos públicos reunidas automaticamente.</p>
    </footer>
    <script>
        function filtrar(classe) {{
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.card').forEach(card => {{
                if(classe === 'todos') card.classList.remove('hidden');
                else card.classList.toggle('hidden', !card.classList.contains(classe));
            }});
        }}
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(template)
