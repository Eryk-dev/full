import re
import json
import pdfplumber
from typing import List, Tuple, Dict, Any
from datetime import datetime

def extract_text_and_tables_from_pdf(pdf_path: str) -> Tuple[str, List]:
    """
    Extrai texto e tabelas do PDF usando pdfplumber.
    """
    all_text = ""
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extrair texto
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"
            
            # Extrair tabelas
            tables = page.extract_tables()
            if tables:
                all_tables.extend(tables)
    
    return all_text, all_tables

def extract_skus_from_tables(tables: List) -> List[Tuple[str, int, str]]:
    """Extrai SKUs e quantidades das tabelas do PDF."""
    all_skus = []
    
    for table_idx, table in enumerate(tables):
        for row_idx, row in enumerate(table):
            if not row or len(row) < 2:
                continue
                
            # Pular apenas cabeçalhos reais (primeira célula deve ser exatamente "PRODUTO")
            first_cell = str(row[0]).strip() if len(row) > 0 and row[0] else ""
            if first_cell == "PRODUTO":
                continue
                
            # Extração estruturada: coluna 0 = produto, coluna 1 = unidades
            product_cell = str(row[0]).strip() if len(row) > 0 and row[0] else ""
            units_cell = str(row[1]).strip() if len(row) > 1 and row[1] else ""
            
            # Extrair SKU da célula do produto
            sku = extract_sku_from_product_cell(product_cell)
            
            # Extrair código ML da célula do produto
            ml_code = extract_ml_code_from_product_cell(product_cell)
            
            # Extrair quantidade APENAS da coluna de unidades (não de outras células)
            quantity = None
            if units_cell:
                qty_match = re.search(r'^(\d+)$', units_cell.strip())  # Apenas números puros
                if qty_match:
                    qty = int(qty_match.group(1))
                    if 1 <= qty <= 500:
                        quantity = qty
            
            # Se encontramos SKU e quantidade válidos
            if sku and quantity:
                all_skus.append((sku, quantity, ml_code or "N/A"))
    
    return all_skus

def extract_sku_from_product_cell(product_text: str) -> str:
    """
    Extrai o SKU da célula do produto.
    Procura por 'SKU:' seguido do código na próxima linha.
    """
    if not product_text:
        return None
    
    # Procurar por padrão "SKU:" seguido do código
    sku_match = re.search(r'SKU:\s*\n?([A-Z0-9\-]+)', product_text, re.IGNORECASE)
    if sku_match:
        return sku_match.group(1).strip().upper()
    
    # Procurar por códigos após quebra de linha que começam com letras ou números
    lines = product_text.split('\n')
    for i, line in enumerate(lines):
        if 'SKU:' in line.upper() and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            # Verificar se a próxima linha contém um código válido
            if re.match(r'^[A-Z0-9\-]{3,}$', next_line):
                return next_line.upper()
    
    return None

def extract_ml_code_from_product_cell(product_text: str) -> str:
    """
    Extrai o código ML da célula do produto.
    """
    if not product_text:
        return None
    
    # Procurar por "Código ML: XXXXXXXX"
    ml_match = re.search(r'Código ML:\s*([A-Z0-9]+)', product_text)
    if ml_match:
        return ml_match.group(1).strip()
    
    return None

def extract_header_info(text: str) -> Dict:
    """
    Extrai informações do cabeçalho do PDF (total de produtos e unidades).
    """
    header_info = {}
    
    # Procurar por padrões como "Produtos do envio:32|Total de unidades:170"
    produtos_match = re.search(r'Produtos do envio:\s*(\d+)', text)
    if produtos_match:
        header_info['produtos'] = int(produtos_match.group(1))
    
    unidades_match = re.search(r'Total de unidades:\s*(\d+)', text)
    if unidades_match:
        header_info['unidades'] = int(unidades_match.group(1))
    
    # Procurar por outros padrões possíveis
    alt_pattern = re.search(r'(\d+)\s*\|\s*Total de unidades:\s*(\d+)', text)
    if alt_pattern:
        header_info['produtos'] = int(alt_pattern.group(1))
        header_info['unidades'] = int(alt_pattern.group(2))
    
    return header_info

def is_valid_sku(sku: str) -> bool:
    """Verifica se o SKU é válido."""
    if not sku or len(sku) < 3:
        return False
    
    # Aceitar qualquer combinação de letras, números e hífen com pelo menos 3 caracteres
    if re.match(r'^[A-Z0-9\-]+$', sku) and len(sku) >= 3:
        return True
    
    return False

def extract_skus_from_pdf(pdf_path: str, filename: str = "documento.pdf") -> Dict[str, Any]:
    """
    Função principal para extrair SKUs do PDF.
    
    Args:
        pdf_path: Caminho para o arquivo PDF
        filename: Nome original do arquivo (para metadata)
    
    Returns:
        Dicionário com metadata e lista de SKUs
    """
    try:
        # Extrair dados do PDF
        text, tables = extract_text_and_tables_from_pdf(pdf_path)
        
        if not tables:
            raise Exception("Nenhuma tabela encontrada no PDF")
        
        # Extrair informações do cabeçalho
        header_info = extract_header_info(text)
        
        # Extrair SKUs das tabelas
        raw_skus = extract_skus_from_tables(tables)
        
        # Filtrar apenas SKUs válidos (mas sem deduplicar)
        clean_skus = [(sku, qty, ml_code) for sku, qty, ml_code in raw_skus if is_valid_sku(sku)]
        
        if not clean_skus:
            raise Exception("Nenhum SKU válido encontrado no PDF")
        
        # Estrutura do JSON simplificada
        result = {
            "metadata": {
                "total_skus": len(clean_skus),
                "total_unidades": sum(qty for _, qty, _ in clean_skus),
                "data_extracao": datetime.now().isoformat(),
                "fonte": filename,
                "header_info": header_info
            },
            "skus": []
        }
        
        # Adicionar cada SKU com apenas SKU e quantidade
        for sku, quantity, _ in clean_skus:
            sku_data = {
                "sku": sku,
                "quantidade": quantity
            }
            result["skus"].append(sku_data)
        
        return result
        
    except Exception as e:
        raise Exception(f"Erro ao processar PDF: {str(e)}")

def validate_pdf_content(pdf_path: str) -> bool:
    """
    Valida se o PDF contém conteúdo válido para extração.
    """
    try:
        text, tables = extract_text_and_tables_from_pdf(pdf_path)
        
        # Verificar se há texto
        if not text or len(text.strip()) < 100:
            return False
        
        # Verificar se há tabelas
        if not tables or len(tables) == 0:
            return False
        
        # Verificar se há indicadores de documento de preparação
        indicators = ['Código ML:', 'SKU:', 'PRODUTO', 'UNIDADES']
        text_upper = text.upper()
        
        found_indicators = sum(1 for indicator in indicators if indicator in text_upper)
        
        return found_indicators >= 2
        
    except Exception:
        return False 