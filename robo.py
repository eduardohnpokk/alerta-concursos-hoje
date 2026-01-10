import feedparser
import re
import os
from datetime import datetime

# CONFIGURAÇÕES DE AFILIADO (MANTIDAS)
AMAZON_TAG = "eduardohen00f-20"
SHOPEE_ID = "18368470403"

def limpar_titulo(titulo):
    return re.sub(r'[^\w\s]', '', titulo).replace(' ', '+')

# 1. LER NOTÍCIAS
rss_url = "https://news.google.com/rss/search?q=inscrições+abertas+concurso+edital+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
feed = feedparser.parse(rss_url)

# 2. MONTAR O HTML DAS NOTÍCIAS
html_dinamico = ""
for i, entry in enumerate(feed.entries):
    termo = limpar_titulo(entry.title)
    link_amz = f"https://www.amazon.com.br/s?k=apostila+{termo}&tag={AMAZON_TAG}"
    link_shp = f"https://shopee.com.br/search?keyword=apostila%20{termo}"
    
    html_dinamico += f"""
    <div class="card">
        <span class="tag">NOVIDADE</span>
        <h3>{entry.title}</h3>
        <p class="data">🕒 Postado em: {entry.published}</p>
        <div class="links-uteis">
            <a href="{entry.link}" class="link-original" target="_blank">🔗 Ler Notícia Completa</a>
        </div>
        <div class="buttons-container">
            <a href="{link_amz}" class="btn btn-amazon" target="_blank">🛒 Apostilas Amazon</a>
            <a href="{link_shp}" class="btn btn-shopee" target="_blank">🛍️ Apostilas Shopee</a>
        </div>
    </div>
    """
    
    # Inserir um anúncio a cada 3 notícias
    if i == 2:
        html_dinamico += '<div class="ads-space">--- ESPAÇO PARA GOOGLE ADS (MEIO) ---</div>'

# 3. TEMPLATE VISUAL COMPLETO (CSS PROFISSIONAL)
template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alerta Concursos Hoje | Editais e Vagas</title>
    <style>
        :root {{
            --primary: #2c3e50;
            --accent: #e74c3c;
            --amazon: #f39c12;
            --shopee: #ee4d2d;
            --bg: #f8f9fa;
        }}
        body {{ font-family: 'Segoe UI', Roboto, sans-serif; margin: 0; background: var(--bg); color: #333; }}
        header {{ background: linear-gradient(135deg, #2c3e50 0%, #000000 100%); color: white; padding: 40px 20px; text-align: center; border-bottom: 5px solid var(--accent); }}
        header h1 {{ margin: 0; font-size: 2.5em; letter-spacing: -1px; }}
        header p {{ opacity: 0.8; margin-top: 10px; }}
        
        .container {{ max-width: 900px; margin: 20px auto; padding: 0 20px; }}
        
        .ads-space {{ background: #eee; border: 2px dashed #ccc; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px; font-size: 12px; color: #888; }}
        
        .card {{ background: white; padding: 25px; margin-bottom: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: transform 0.2s; border-left: 5px solid #ddd; }}
        .card:hover {{ transform: translateY(-5px); border-left-color: var(--accent); }}
        .card h3 {{ margin-top: 0; color: var(--primary); line-height: 1.3; }}
        .card .tag {{ background: var(--accent); color: white; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; text-transform: uppercase; }}
        .card .data {{ font-size: 13px; color: #888; }}
        
        .buttons-container {{ display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }}
        .btn {{ flex: 1; min-width: 200px; text-align: center; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; transition: opacity 0.2s; }}
        .btn-amazon {{ background: var(--amazon); color: white; }}
        .btn-shopee {{ background: var(--shopee); color: white; }}
        .btn:hover {{ opacity: 0.9; }}
        
        .link-original {{ color: #3498db; text-decoration: none; font-size: 14px; font-weight: 500; }}
        .link-original:hover {{ text-decoration: underline; }}

        footer {{ background: #222; color: #888; padding: 40px 20px; text-align: center; margin-top: 50px; font-size: 14px; }}
        footer b {{ color: white; }}
    </style>
</head>
<body>
    <header>
        <h1>📍 Alerta Concursos Hoje</h1>
        <p>Sua central automática de editais, vagas e materiais de estudo</p>
    </header>

    <div class="container">
        <div class="ads-space">--- ESPAÇO PARA GOOGLE ADS (TOPO) ---</div>
        
        <p style="text-align:right; font-size: 12px; color: #666;">
            🔄 Atualizado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
        </p>

        <div id="noticias">
            {html_dinamico}
        </div>

        <div class="ads-space">--- ESPAÇO PARA GOOGLE ADS (RODAPÉ) ---</div>
    </div>

    <footer>
        <p><b>Alerta Concursos Hoje</b> &copy; {datetime.now().year}</p>
        <p>Este site é um agregador automático de notícias públicas. Não possuímos vínculo com os órgãos oficiais.</p>
        <p>As ofertas de produtos são geradas através de programas de afiliados (Amazon e Shopee).</p>
    </footer>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(template)
