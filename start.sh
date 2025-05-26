#!/bin/bash

# Full Extractor API - Script de Inicialização

echo "🚀 Full Extractor API - Iniciando..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instalando dependências Python..."
    
    # Verificar se Python está instalado
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+."
        exit 1
    fi
    
    # Instalar dependências
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
    
    # Executar aplicação
    echo "🎯 Iniciando aplicação..."
    python3 main.py
    
else
    echo "🐳 Docker encontrado. Usando Docker Compose..."
    
    # Verificar se docker-compose está instalado
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose não encontrado. Usando Docker..."
        docker build -t full-extractor-api .
        docker run -p 8000:8000 full-extractor-api
    else
        echo "🎯 Iniciando com Docker Compose..."
        docker-compose up --build
    fi
fi 