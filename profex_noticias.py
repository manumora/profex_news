import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Configuración
url = "https://profex.educarex.es/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
output_dir = "./"

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Obtener el contenido de la página
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Verificar si la solicitud fue exitosa
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Buscar el contenedor principal
    target_div = soup.find("div", class_="portlet-boundary portlet-boundary_101_ portlet-static portlet-static-end portlet-borderless portlet-asset-publisher")
    
    # Generar HTML personalizado
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Noticias Profex</title>
        <style>
            :root {{
                --primary-color: #0071e3;
                --text-primary: #1d1d1f;
                --text-secondary: #86868b;
                --background-primary: #ffffff;
                --background-secondary: #f5f5f7;
                --card-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                --transition: all 0.3s ease;
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif; 
                margin: 0; 
                padding: 0;
                background: var(--background-secondary);
                color: var(--text-primary);
                line-height: 1.5;
            }}
            
            .container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            
            h1 {{
                font-weight: 600;
                font-size: 32px;
                letter-spacing: -0.5px;
                color: var(--text-primary);
                margin-bottom: 16px;
            }}
            
            .actualizado {{ 
                color: var(--text-secondary);
                font-size: 14px;
                font-weight: 400;
            }}
            
            .noticias-grid {{
                display: grid;
                gap: 16px;
                grid-template-columns: 1fr;
            }}
            
            .noticia {{ 
                background: var(--background-primary);
                border-radius: 12px;
                padding: 20px;
                transition: var(--transition);
                box-shadow: var(--card-shadow);
                border: 1px solid rgba(0,0,0,0.04);
            }}
            
            .noticia:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12);
            }}
            
            .info-linea {{
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }}
            
            .fecha {{
                color: var(--text-secondary);
                font-size: 14px;
                font-weight: 500;
            }}
            
            .separador {{
                margin: 0 8px;
                color: var(--text-secondary);
            }}
            
            .categoria {{
                color: var(--primary-color);
                font-weight: 600;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .titulo {{ 
                color: var(--text-primary);
                font-size: 16px;
                font-weight: 500;
                line-height: 1.4;
            }}
            
            @media (min-width: 768px) {{
                .noticias-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
                
                h1 {{
                    font-size: 36px;
                }}
            }}
            
            @media (prefers-color-scheme: dark) {{
                :root {{
                    --primary-color: #2997ff;
                    --text-primary: #f5f5f7;
                    --text-secondary: #a1a1a6;
                    --background-primary: #1d1d1f;
                    --background-secondary: #000000;
                    --card-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Noticias PROFEX</h1>
                <div class="actualizado">Actualizado: {datetime.now().strftime("%d/%m/%Y %H:%M")}</div>
            </div>
            <div class="noticias-grid">
    """

    if target_div:
        # Buscar la lista de noticias
        news_list = target_div.find("ul", class_="listado-noticias")
        
        if news_list:
            # Obtener todas las noticias (elementos li)
            noticias = news_list.find_all("li", class_="d-table")
            
            for noticia in noticias:
                # Extraer fecha
                fecha_elem = noticia.find("span", class_="fecha")
                fecha = fecha_elem.text.strip() if fecha_elem else "Sin fecha"
                
                # Extraer enlace y contenido
                enlace_elem = noticia.find("a", class_="contenido-noticia")
                
                if enlace_elem:
                    # Obtener URL completa
                    href = enlace_elem.get("href", "")
                    if href and not href.startswith(("http://", "https://")):
                        href = url.rstrip("/") + href
                    
                    # Extraer categoría
                    categoria_elem = enlace_elem.find("div", class_="categoria-noticia")
                    categoria = categoria_elem.text.strip() if categoria_elem else "General"
                    
                    # Extraer título
                    titulo_elem = enlace_elem.find("div", class_="titular-noticia")
                    titulo = titulo_elem.text.strip() if titulo_elem else "Sin título"
                    
                    html_content += f"""
                    <div class="noticia">
                        <div class="info-linea">
                            <div class="fecha">{fecha}</div>
                            <div class="separador">•</div>
                            <div class="categoria">{categoria}</div>
                        </div>
                        <div class="titulo">{titulo}</div>
                    </div>
                    """
        else:
            html_content += "<p>No se encontró la lista de noticias.</p>"
    else:
        html_content += "<p>No se encontró el contenedor de noticias.</p>"

    html_content += """
            </div>
        </div>
        <script>
            // Auto-refresh de la página cada 30 minutos
            setTimeout(function() {
                location.reload();
            }, 30 * 60 * 1000);
        </script>
    </body>
    </html>
    """

    # Guardar el archivo
    output_path = os.path.join(output_dir, "profex_noticias.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Archivo HTML generado correctamente en: {output_path}")

except Exception as e:
    print(f"Error al procesar la página: {e}")
