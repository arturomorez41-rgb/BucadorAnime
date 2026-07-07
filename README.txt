# 🚀 Anime Hub - Buscador Multi-idioma para Crunchyroll

Una herramienta ligera diseñada para filtrar el catálogo de Crunchyroll por sus pistas de audio de doblaje
(Español Latino, Castellano, Inglés, etc.). Ideal para usuarios que buscan contenido doblado de forma rápida y visual.

![Versión](https://shields.io)
![Licencia](https://shields.io)
![PopOS](https://shields.io)

## ✨ Características
- 🔍 **Buscador Instantáneo**: Filtra por título en tiempo real.
- 🌍 **Soporte Multi-idioma**: Pestañas para filtrar por doblaje Latino, España, Inglés, Portugués y Francés.
- 🎲 **Anime Aleatorio**: Botón inteligente para descubrir series al azar según el filtro seleccionado.
- 📱 **Diseño Responsivo**: Estética oscura (Dark Mode) optimizada para escritorio y móviles.
- 🚀 **Modo Mantenimiento**: Spinner de carga visual mientras se sincroniza el catálogo.

## 🛠️ Tecnologías Utilizadas
- **Frontend**: HTML5, CSS3 (Flexbox/Grid), JavaScript Vanilla.
- **Backend (Scraper)**: Python 3.12, Playwright, BeautifulSoup4.
- **Seguridad**: Playwright con evasión de detección (Evasión de huella digital).

## 📥 Instalación y Uso (Local)

1. **Clonar el repositorio**:
   ```bash
   git clone github.com
   cd BucadorAnime
   ```

2. **Configurar el entorno**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install playwright beautifulsoup4
   playwright install chromium
   ```

3. **Ejecutar el Extractor**:
   ```bash
   python3 extractor_pro_v2.py
   ```

4. **Lanzar la Web**:
   ```bash
   python3 -m http.server 8080
   ```
   Luego visita `http://localhost:8080`.

## ⚖️ Disclaimer (Aviso Legal)
Este proyecto es una herramienta de filtrado independiente y **no recolecta datos personales** de los usuarios. No aloja ningún contenido audiovisual; todas las redirecciones apuntan al sitio oficial de Crunchyroll. Es necesario contar con una suscripción activa en la plataforma oficial para visualizar el contenido.

---
Desarrollado con ❤️ en Pop!_OS.
