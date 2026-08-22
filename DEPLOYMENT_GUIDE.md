# 🚀 GUÍA DE DESPLIEGUE PÚBLICO — RADAR CHILE 2035

Esta guía te permite publicar la plataforma en internet con **1 solo comando** o mediante Git para que cualquier persona (inversionistas, clientes, comités) pueda acceder directamente desde su navegador o teléfono móvil sin instalar nada.

---

## 🌟 Opción 1: Railway (Recomendada — 1 Solo Servicio Fullstack)

Railway construye automáticamente el contenedor Docker, compila el Frontend React y ejecuta la API FastAPI en **un único enlace público** (ej. `https://radar-chile-2035.up.railway.app`).

### Pasos:
1. **Opción A (Con CLI en tu terminal)**:
   ```bash
   ./deploy.sh
   # Elige la opción 2
   ```
2. **Opción B (Desde la web de Railway)**:
   - Ve a [railway.app](https://railway.app) y haz clic en **`New Project`** → **`Deploy from GitHub repo`**.
   - Selecciona el repositorio de `radar_chile`.
   - Railway detectará el archivo `Dockerfile` y `railway.json` automáticamente.
   - En *Variables de Entorno* (opcional), añade tus API Keys:
     - `FRED_API_KEY`: `97466e891b73c0383011ec23cc26e7cd`
     - `GEMINI_API_KEY`: `AIzaSyD51_bg8ko3PsMEIKehlGukwasrwYvib6E`
   - Haz clic en **`Generate Domain`** y obtendrás tu URL pública lista para compartir.

---

## ⚡ Opción 2: Vercel (Frontend Ultra-Rápido)

Vercel aloja la interfaz web en su red CDN global con despliegue instantáneo.

### Pasos:
1. Abre tu terminal en `apps/web`:
   ```bash
   cd apps/web
   npx vercel --prod
   ```
2. Sigue las preguntas en pantalla (presiona Enter para los defaults).
3. Obtendrás un enlace público instantáneo como `https://radar-chile-web.vercel.app`.

> **Nota:** Si tienes el backend en Railway o Cloud Run, en el panel de Vercel agrega la variable de entorno:
> `VITE_API_BASE_URL=https://tu-backend-en-railway.app/api/v1`

---

## ☁️ Opción 3: Google Cloud Run (Producción GCP)

Si deseas alojarlo en la infraestructura corporativa de Google Cloud:

```bash
# 1. Autenticar en GCP
gcloud auth login
gcloud config set project TU_PROYECTO_GCP

# 2. Desplegar con el script automático
./deploy.sh
# Elige la opción 3
```

---

## 🐳 Opción 4: Contenedor Docker Local

Para verificar que la imagen empaquetada funciona idéntica a producción:

```bash
docker build -t radar-chile-2035 .
docker run -p 8000:8000 -e PORT=8000 radar-chile-2035
```
Abre en tu navegador: [http://localhost:8000](http://localhost:8000)

---

## 📱 ¿Cómo compartirlo como Demo?

Una vez desplegado en **Railway** o **Vercel**:
1. Copia tu URL pública generada (ej: `https://radar-chile.up.railway.app`).
2. Compártela directamente por WhatsApp, LinkedIn, correo o presentación.
3. Los usuarios podrán:
   - Simular proyectos en el **Siting Optimizer**.
   - Descargar modelos financieros en **Excel (`.xls`)**.
   - Imprimir el **Memorándum de Inversión (PDF)**.
   - Explorar el mapa de las 30 barras del SEN y pronósticos de Machine Learning.
