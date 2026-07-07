import asyncio
import json
import os
import random
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

URL_ALFABETICO = "https://crunchyroll.com"
ARCHIVO_SALIDA = "catalogo_multiidioma.json"
PERFIL_DIR = os.path.join(os.getcwd(), "perfil_pro_crunchy")

IDIOMAS_OBJETIVO = {
    "Latino": "Español (América Latina)",
    "Castellano": "Español (España)",
    "English": "English",
    "Portuguese": "Português (Brasil)",
    "French": "Français (France)"
}

async def extraer():
    async with async_playwright() as p:
        print("🚀 Iniciando navegador optimizado...")
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PERFIL_DIR,
            headless=False,
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        
        await page.route("**/*.{woff,woff2,ttf,otf,analytics,google-analytics,doubleclick}", lambda route: route.abort())

        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print(f"🔗 Conectando a: {URL_ALFABETICO}")
        await page.goto(URL_ALFABETICO, wait_until="domcontentloaded", timeout=60000)
        
        print("\n📢 CONTROL MANUAL: Resuelve Cloudflare si aparece.")
        input("👉 Presiona ENTER cuando veas el catálogo cargado...")

        print("\n⏳ Escaneando catálogo completo...")
        for i in range(50): 
            await page.evaluate("window.scrollBy(0, 1500);")
            await page.wait_for_timeout(900) # Ajustado para fluidez
            if i % 10 == 0:
                print(f"   📊 Scroll en progreso ({i}/50)...")

        html_principal = await page.content()
        soup_principal = BeautifulSoup(html_principal, 'html.parser')
        
        # Captura de enlaces única y limpia
        links = {f"https://www.crunchyroll.com{a['href']}" for a in soup_principal.find_all('a', href=True) 
                 if "/series/" in a['href'] and all(x not in a['href'] for x in ["/watch/", "/reviews", "/comments"])}
        
        lista_animes = list(links)
        print(f"\n✅ Se analizarán {len(lista_animes)} series.")

        resultados = []
        for index, url in enumerate(lista_animes, start=1):
            print(f"🔎 [{index}/{len(lista_animes)}] -> {url.split('/')[-1]}")
            
            try:
                # OPTIMIZACIÓN 2: Espera inteligente basada en DOM (más rápido que NetworkIdle)
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                # Pausa mínima para que se inyecten los datos de idioma
                await page.wait_for_timeout(4500) 
                
                detail_soup = BeautifulSoup(await page.content(), 'html.parser')

                # OPTIMIZACIÓN 3: Filtro de imagen avanzado
                imagen_url = "https://placeholder.com"
                todas_las_imgs = detail_soup.find_all("img", src=True)
                
                for img in todas_las_imgs:
                    src = img.get('src', '')
                    # Excluimos logo y banners para asegurar el póster vertical
                    es_basura = any(x in src.lower() for x in ["blur", "logo", "avatar", "user", "transparent", "banner"])
                    if not es_basura and src.startswith("http"):
                        imagen_url = src
                        break

                titulo = detail_soup.find("h1").get_text(strip=True) if detail_soup.find("h1") else "Sin título"
                
                # Búsqueda de idiomas
                etiqueta = detail_soup.find(attrs={"data-t": "details-item-description"})
                texto_idiomas = etiqueta.get_text() if etiqueta else detail_soup.get_text()

                doblajes = [clave for clave, nombre in IDIOMAS_OBJETIVO.items() if nombre.lower() in texto_idiomas.lower()]

                if doblajes:
                    resultados.append({
                        "titulo": titulo,
                        "url": url,
                        "imagen": imagen_url,
                        "doblajes": doblajes
                    })
                    print(f"   ✅ {titulo} | {doblajes}")
                    
                    # Guardado atómico
                    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
                        json.dump(resultados, f, ensure_ascii=False, indent=4)
                else:
                    print(f"   ❌ Solo Sub")

            except Exception as e:
                print(f"   ⚠️ Error: {str(e)[:50]}... Reintentando.")
                continue
            
            # Pausa humana aleatoria para evitar detección
            await page.wait_for_timeout(random.uniform(2000, 4000))

        await context.close()
        print(f"🎉 ¡Proceso finalizado! Revisa {ARCHIVO_SALIDA}")

if __name__ == "__main__":
    asyncio.run(extraer())
