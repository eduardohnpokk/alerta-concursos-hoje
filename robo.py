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
    # Lógica de mapeamento de palavras-chave para Categorias
    mapeamento = {
        'Nível Médio': ['médio', 'medio', 'fundamental'],
        'Nível Superior': ['superior', 'graduação', 'graduacao'],
        'Policial': ['polícia', 'policia', 'militar', 'gcm', 'segurança', 'pcdf', 'pcsp', 'pcrj'],
        'Saúde': ['saúde', 'saude', 'médico', 'medico', 'enfermeiro', 'hospital', 'sus'],
        'Tribunais': ['tribunal', 'tj', 'tre', 'trf', 'tse', 'judiciário'],
        'Educação': ['educação', 'educacao', 'professor', 'sme', 'ensino'],
        'Administrativo': ['adm', 'administrativo', 'prefeitura', 'câmara', 'camara']
    }
    
    for nome_exibicao, palavras in mapeamento.items():
        if any(p in t for p in palavras):
            cats.append(nome_exibicao)
    
    # Status
    status_tag = ""
    if "aberto" in t or "inscrições" in t:
        status_tag = '<span class="tag tag-aberto">Aberto</span>'
    elif "previsto" in t or "autorizado" in t:
        status_tag = '<span class="tag tag-previsto">Previsto</span>'
    else:
        status_tag = '<span class="tag tag-news">Notícia</span>'
    
    return cats, status_tag

# 1. LER NOTÍCIAS
rss_url = "https://news.google.com/rss/search?q=concurso+público+edital+aberto+previsto+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
feed = feedparser.parse(rss_url)

# 2. PROCESSAR NOTÍCIAS E COLETAR CATEGORIAS EXISTENTES
lista_cards = []
categorias_encontradas = set()

for entry in feed.entries:
    cats_nome, status_html = identificar_categorias(entry.title)
    termo = limpar_titulo(entry.title)
    
    # Adiciona as categorias encontradas ao nosso "banco" de botões do dia
    for c in cats_nome:
        categorias_encontradas.add(c)
    
    # Criar a classe CSS para o filtro (ex: "Policial" vira "cat-policial")
    classes_css = " ".join([f"cat-{c.replace(' ', '-').lower()}" for c in cats_nome])
    
    link_amz = f"https://www.amazon.com.br/s?k=apostila+{termo}&tag={AMAZON_TAG}"
    link_shp = f"https://shopee.com.br/search?keyword=apostila%20{termo}"
    
    card = f"""
    <div class="card {classes_css}" data-titulo="{entry.title.lower()}">
        {status_tag}
        <h3>{entry.title}</h3>
        <p class="data">🕒 {entry.published}</p>
        <div class="buttons-container">
            <a href="{entry.link}" class="btn-link" target="_blank">🔗 Ver Notícia</a>
            <a href="{link_amz}" class="btn btn-amazon" target="_blank">🛒 Apostilas Amazon</a>
            <a href="{link_shp}" class="btn btn-shopee" target="_blank">🛍️ Apostilas Shopee</a>
        </div>
    </div>
    """
    lista_cards.append(card)

# Criar os botões do menu baseados no que foi encontrado hoje
botoes_html = '<button class="filter-btn active" onclick="filtrar(\'todos\')">Todos</button>'
for cat in sorted(categorias_encontradas):
    classe_filtro = f"cat-{cat.replace(' ', '-').lower()}"
    botoes_html += f'<button class="filter-btn" onclick="filtrar(\'{classe_filtro}\')">{cat}</button>'

# 3. GERAR O SITE
template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alerta Concursos Hoje</title>
    <style>
        :root {{ --primary: #2c3e50; --accent: #e74c3c; --amazon: #f39c12; --shopee: #ee4d2d; --bg: #f4f7f6; }}
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); color: #333; }}
        header {{ background: #000; color: white; padding: 30px; text-align: center; border-bottom: 4px solid var(--accent); }}
        .container {{ max-width: 900px; margin: auto; padding: 20px; }}
        .filter-bar {{ background: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .filter-btn {{ padding: 7px 15px; border: 1px solid #ddd; border-radius: 20px; cursor: pointer; background: white; font-size: 13px; transition: 0.3s; }}
        .filter-btn.active {{ background: var(--primary); color: white; }}
        .card {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 12px; border-left: 6px solid #ddd; }}
        .card.hidden {{ display: none; }}
        .tag {{ padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; color: white; text-transform: uppercase; }}
        .tag-aberto {{ background: #27ae60; }} .tag-previsto {{ background: #f1c40f; color: #000; }} .tag-news {{ background: #3498db; }}
        .buttons-container {{ display: flex; gap: 8px; margin-top: 15px; flex-wrap: wrap; }}
        .btn {{ flex: 1; padding: 10px; border-radius: 5px; text-decoration: none; font-weight: bold; text-align: center; color: white; font-size: 13px; }}
        .btn-amazon {{ background: var(--amazon); }} .btn-shopee {{ background: var(--shopee); }}
        .btn-link {{ color: var(--primary); border: 1px solid var(--primary); flex: 1; text-align: center; text-decoration: none; border-radius: 5px; padding: 10px; font-size: 13px; }}
        footer {{ text-align: center; padding: 40px; color: #888; font-size: 13px; }}
    </style>
</head>
<body>
    <header><h1>📍 Alerta Concursos Hoje</h1><p>Atualizado automaticamente em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p></header>
    <div class="container">
        <div class="filter-bar">{botoes_html}</div>
        <div id="noticias">{" ".join(lista_cards)}</div>
    </div>
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
