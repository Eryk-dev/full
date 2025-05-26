from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import tempfile
import os
from typing import List, Dict, Any
import json
from datetime import datetime

from sku_extractor import extract_skus_from_pdf

# Inicializar FastAPI
from config import Settings

settings = Settings()

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PDFRequest(BaseModel):
    """Modelo para requisição com PDF em base64"""
    pdf_base64: str
    filename: str = "documento.pdf"

class SKUItem(BaseModel):
    """Modelo para um item SKU"""
    sku: str
    quantidade: int

class SKUResponse(BaseModel):
    """Modelo para resposta da extração de SKUs"""
    metadata: Dict[str, Any]
    skus: List[SKUItem]

@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Full Extractor API",
        "version": settings.API_VERSION,
        "description": "API para extrair SKUs e quantidades de PDFs",
        "endpoints": {
            "POST /extract-skus": "Extrai SKUs de um PDF em base64",
            "GET /health": "Verifica status da API"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint para verificar saúde da API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/extract-skus", response_model=SKUResponse)
async def extract_skus(request: PDFRequest):
    """
    Extrai SKUs e quantidades de um PDF enviado em base64
    
    Args:
        request: Objeto contendo o PDF em base64 e nome do arquivo
    
    Returns:
        Objeto com metadata e lista de SKUs encontrados
    """
    try:
        # Decodificar base64
        try:
            pdf_data = base64.b64decode(request.pdf_base64)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao decodificar base64: {str(e)}")
        
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_data)
            temp_file_path = temp_file.name
        
        try:
            # Extrair SKUs do PDF
            result = extract_skus_from_pdf(temp_file_path, request.filename)
            
            if not result:
                raise HTTPException(status_code=422, detail="Nenhum SKU foi encontrado no PDF")
            
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")
        
        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/extract-skus/simple")
async def extract_skus_simple(request: PDFRequest):
    """
    Versão simplificada que retorna apenas a lista de SKUs
    
    Args:
        request: Objeto contendo o PDF em base64 e nome do arquivo
    
    Returns:
        Lista simples de objetos {sku, quantidade}
    """
    try:
        result = await extract_skus(request)
        return result.skus
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT) 