import feedparser
import re
import os
from datetime import datetime

# CONFIGURAÇÕES DE AFILIADO (MANTIDAS)
AMAZON_TAG = "eduardohen00f-20"
SHOPEE_ID = "18368470403"
LINK_GRUPO = "#" # Link do seu WhatsApp/Telegram futuro

def limpar_titulo(titulo):
    return re.sub(r'[^\w\s]', '', titulo).replace(' ', '+')

def identificar_categorias(titulo):
    t = titulo.lower()
    cats = []
    # Mapeamento de Áreas de Estudo
    mapeamento_areas = {
        'Nível Médio': ['médio', 'medio', 'fundamental'],
        'Nível Superior': ['superior', 'graduação', 'graduacao'],
        'Policial': ['polícia', 'policia', 'militar', 'gcm', 'segurança', 'detran', 'prf', 'pf'],
        'Saúde': ['saúde', 'saude', 'médico', 'medico', 'enfermeiro', 'hospital', 'sus'],
        'Tribunais': ['tribunal', 'tj', 'tre', 'trf', 'tse', 'stj', 'stf'],
        'Educação': ['educação', 'educacao', 'professor', 'sme', 'ensino', 'mec']
    }
    for nome, palavras in mapeamento_areas.items():
        if any(p in t for p in palavras): 
            cats.append(f"area-{nome.replace(' ', '-').lower()}")
    
    # Mapeamento de Estados (Detecção Automática no Título)
    estados_mapeados = {
        'sp': 'São Paulo', 'rj': 'Rio de Janeiro', 'mg': 'Minas Gerais', 
        'df': 'Distrito Federal', 'rs': 'Rio Grande do Sul', 'pr': 'Paraná', 
        'sc': 'Santa Catarina', 'ba': 'Bahia', 'pe': 'Pernambuco', 'ce': 'Ceará',
        'es': 'Espírito Santo', 'go': 'Goiás', 'ma': 'Maranhão', 'mt': 'Mato Grosso',
        'ms': 'Mato Grosso do Sul', 'pa': 'Pará', 'pb': 'Paraíba', 'pi': 'Piauí',
        'rn': 'Rio Grande do Norte', 'ro': 'Rondônia', 'rr': 'Roraima', 'se': 'Sergipe',
        'to': 'Tocantins', 'al': 'Alagoas', 'am': 'Amazonas', 'ap': 'Amapá', 'ac': 'Acre'
    }
    
    for sigla, nome_full in estados_mapeados.items():
        # Busca a sigla isolada (ex: " SP" ou "-SP") ou o nome do estado
        if f" {sigla}" in t or f"-{sigla}" in t or nome_full.lower() in t:
            cats.append(f"estado-{sigla}")

    tag_html = ""
    if "aberto" in t or "inscrições" in t or "publicado" in t: 
        tag_html = '<span class="tag tag-aberto">Aberto</span>'
    elif "previsto" in t or "autorizado" in t or "anunciado" in t: 
        tag_html = '<span class="tag tag-previsto">Previsto</span>'
    else: 
        tag_html = '<span class="tag tag-news">Notícia</span>'
    
    return cats, tag_html

# 1. LER NOTÍCIAS (BUSCA AMPLIADA)
rss_url = "https://news.google.com/rss/search?q=concurso+público+edital+aberto+previsto+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
feed = feedparser.parse(rss_url)

# 2. PROCESSAR NOTÍCIAS
lista_cards = []
lista_destaques = []
filtros_area = {} # Nome: Classe
filtros_estado = {} # Sigla: Classe

for i, entry in enumerate(feed.entries):
    cats, status_html = identificar_categorias(entry.title)
    termo = limpar_titulo(entry.title)
    
    # Organiza os botões dinâmicos com base no que existe hoje
    for c in cats:
        if "area-" in c:
            nome_limpo = c.replace("area-", "").replace("-", " ").title()
            filtros_area[nome_limpo] = c
        if "estado-" in c:
            sigla_uf = c.replace("estado-", "").upper()
            filtros_estado[sigla_uf] = c
    
    classes_css = " ".join(cats)
    link_amz = f"https://www.amazon.com.br/s?k=apostila+{termo}&tag={AMAZON_TAG}"
    link_shp = f"https://shopee.com.br/search?keyword=apostila%20{termo}"
    
    # Criar Card
    card = f"""
    <article class="card {classes_css}" data-titulo="{entry.title.lower()}">
        {status_html}
        <h2>{entry.title}</h2>
        <p class="data">🕒 {entry.published}</p>
        <div class="buttons-container">
            <a href="{entry.link}" class="btn-link" target="_blank" rel="nofollow">🔗 Ver Edital Oficial</a>
            <a href="{link_amz}" class="btn btn-amazon" target="_blank">🛒 Apostilas Amazon</a>
            <a href="{link_shp}" class="btn btn-shopee" target="_blank">🛍️ Apostilas Shopee</a>
        </div>
    </article>
    """
    
    # Destaques (Top 3 notícias que correm na barra)
    if i < 3:
        lista_destaques.append(f'<div class="destaque-item">🔥 <b>URGENTE:</b> {entry.title[:85]}...</div>')
    
    lista_cards.append(card)

# Gerador de Botões para o Menu
def montar_menu(dicionario_filtros):
    html = ""
    for nome, classe in sorted(dicionario_filtros.items()):
        html += f'<button class="filter-btn" onclick="filtrar(\'{classe}\')">{nome}</button>'
    return html

# 3. HTML FINAL
template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alerta Concursos Hoje | Portal Automático 2026</title>
    <style>
        :root {{ --primary: #2c3e50; --accent: #e74c3c; --amazon: #f39c12; --shopee: #ee4d2d; --bg: #f4f7f6; }}
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); }}
        header {{ background: linear-gradient(135deg, #000 0%, #2c3e50 100%); color: white; padding: 30px; text-align: center; border-bottom: 4px solid var(--accent); }}
        
        /* Barra de Destaques Correndo */
        .barra-destaques {{ background: #fffbe6; border-bottom: 1px solid #ffe58f; padding: 10px; font-size: 13px; overflow: hidden; }}
        .destaque-container {{ display: flex; animation: slide 30s linear infinite; gap: 60px; white-space: nowrap; }}
        @keyframes slide {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
        
        .container {{ max-width: 900px; margin: auto; padding: 20px; }}
        
        /* Box de Alerta WhatsApp */
        .cta-box {{ background: #27ae60; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 25px; font-weight: bold; box-shadow: 0 4px 10px rgba(39,174,96,0.2); }}
        .cta-box a {{ color: white; border: 1px solid white; padding: 5px 15px; border-radius: 20px; text-decoration: none; margin-left: 10px; transition: 0.3s; }}
        .cta-box a:hover {{ background: white; color: #27ae60; }}

        /* Menu de Filtros */
        .filter-section {{ background: white; padding: 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
        .filter-group {{ margin-bottom: 15px; }}
        .filter-group label {{ font-size: 11px; font-weight: bold; color: #999; text-transform: uppercase; display: block; margin-bottom: 8px; letter-spacing: 1px; }}
        .filter-bar {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .filter-btn {{ padding: 6px 14px; border: 1px solid #eee; border-radius: 20px; cursor: pointer; background: #fafafa; font-size: 13px; transition: 0.2s; }}
        .filter-btn:hover {{ background: #eee; }}
        .filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
        
        /* Notícias */
        .card {{ background: white; padding: 25px; margin-bottom: 25px; border-radius: 12px; border-left: 6px solid #ddd; transition: 0.3s; }}
        .card.hidden {{ display: none; }}
        .card:hover {{ border-left-color: var(--accent); transform: translateY(-3px); box-shadow: 0 6px 15px rgba(0,0,0,0.05); }}
        .card h2 {{ font-size: 1.4em; margin: 10px 0; color: var(--primary); line-height: 1.3; }}
        
        .tag {{ padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; color: white; text-transform: uppercase; }}
        .tag-aberto {{ background: #27ae60; }} .tag-previsto {{ background: #f1c40f; color: #000; }} .tag-news {{ background: #3498db; }}
        
        .buttons-container {{ display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }}
        .btn {{ flex: 1; min-width: 160px; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; text-align: center; color: white; font-size: 13px; }}
        .btn-amazon {{ background: var(--amazon); }} .btn-shopee {{ background: var(--shopee); }}
        .btn-link {{ color: var(--primary); border: 1px solid var(--primary); padding: 12px; flex: 1; text-align: center; text-decoration: none; border-radius: 6px; font-size: 13px; }}
        
        footer {{ text-align: center; padding: 50px 20px; background: #1a1a1a; color: #666; font-size: 13px; margin-top: 40px; }}
        footer a {{ color: #999; text-decoration: none; }}
    </style>
</head>
<body>
    <header>
        <h1>📍 Alerta Concursos Hoje</h1>
        <p>Atualizado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
    </header>

    <div class="barra-destaques">
        <div class="destaque-container">{" ".join(lista_destaques)}</div>
    </div>

    <main class="container">
        <div class="cta-box">
            🔔 Alertas no WhatsApp? <a href="{LINK_GRUPO}">ENTRAR NO GRUPO GRATUITO</a>
        </div>

        <section class="filter-section">
            <div class="filter-group">
                <label>📍 Filtrar por Estado:</label>
                <div class="filter-bar">
                    <button class="filter-btn active" onclick="filtrar('todos')">Todos os Estados</button>
                    {montar_menu(filtros_estado)}
                </div>
            </div>
            <div class="filter-group">
                <label>🎓 Filtrar por Área / Nível:</label>
                <div class="filter-bar">
                    {montar_menu(filtros_area)}
                </div>
            </div>
        </section>

        <div id="noticias">{" ".join(lista_cards)}</div>
    </main>

    <footer>
        <p><b>Alerta Concursos Hoje</b> &copy; {datetime.now().year}</p>
        <p><a href="privacidade.html">Política de Privacidade</a> | <a href="index.html">Início</a></p>
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
