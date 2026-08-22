#!/bin/bash
# ==============================================================================
# RADAR CHILE 2035 — Universal Automated Deployment Script
# Supports: Vercel (Frontend), Railway (Fullstack), Google Cloud Run, Docker Local
# ==============================================================================

set -e

echo "======================================================================"
echo "⚡ RADAR CHILE 2035 — PLATAFORMA DE INTELIGENCIA ECONÓMICA & ENERGÉTICA"
echo "======================================================================"
echo "Selecciona una opción de despliegue:"
echo "1) 🌐 Desplegar Frontend en Vercel (Gratis y ultra-rápido)"
echo "2) 🚂 Desplegar Fullstack en Railway (1 servicio unificado con backend + web)"
echo "3) ☁️ Desplegar en Google Cloud Run (Producción GCP)"
echo "4) 🐳 Probar contenedor Docker localmente (localhost:8000)"
echo "======================================================================"

read -p "Opción [1-4]: " OPTION

case $OPTION in
  1)
    echo "🚀 Desplegando Frontend en Vercel..."
    cd apps/web
    npm run build
    npx vercel --prod
    echo "✅ Frontend desplegado exitosamente en Vercel!"
    ;;
  2)
    echo "🚂 Desplegando en Railway..."
    if ! command -v railway &> /dev/null; then
      echo "Instalando Railway CLI..."
      npm install -g @railway/cli
    fi
    railway up
    echo "✅ Servicio desplegado en Railway!"
    ;;
  3)
    echo "☁️ Desplegando en Google Cloud Run..."
    read -p "Ingresa tu GCP Project ID: " GCP_PROJECT
    gcloud builds submit --tag gcr.io/${GCP_PROJECT}/radar-chile-2035
    gcloud run deploy radar-chile-2035 \
      --image gcr.io/${GCP_PROJECT}/radar-chile-2035 \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated
    echo "✅ Backend & Web desplegados en Cloud Run!"
    ;;
  4)
    echo "🐳 Construyendo imagen Docker local..."
    docker build -t radar-chile-2035 .
    echo "Iniciando contenedor en http://localhost:8000..."
    docker run -p 8000:8000 -e PORT=8000 radar-chile-2035
    ;;
  *)
    echo "Opción inválida."
    exit 1
    ;;
esac
