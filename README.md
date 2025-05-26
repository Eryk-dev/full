# Full Extractor API

API para extrair SKUs e quantidades de PDFs de preparação de envio do Mercado Livre.

## 🚀 Funcionalidades

- Extração automática de SKUs e quantidades de PDFs
- Recebe PDFs via base64
- Retorna dados estruturados em JSON
- Validação de conteúdo do PDF
- API REST com documentação automática
- Suporte a CORS

## 📋 Pré-requisitos

- Python 3.8+
- pip

## 🔧 Instalação

### Opção 1: Usando Docker (Recomendado)

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/full-extractor-api.git
cd full-extractor-api
```

2. Execute com Docker Compose:
```bash
# Produção
docker-compose up -d

# Desenvolvimento (com reload automático)
docker-compose --profile dev up
```

A API estará disponível em: `http://localhost:5555`

### Opção 2: Instalação Manual

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🚀 Execução

### Docker
```bash
# Build da imagem
docker build -t full-extractor-api .

# Executar container
docker run -p 5555:5555 full-extractor-api
```

### Manual
```bash
# Modo desenvolvimento
python main.py

# Modo produção
uvicorn main:app --host 0.0.0.0 --port 5555
```

A API estará disponível em: `http://localhost:5555`

## 📖 Documentação

Acesse a documentação interativa da API:
- Swagger UI: `http://localhost:5555/docs`
- ReDoc: `http://localhost:5555/redoc`

## 🛠 Endpoints

### GET /
Informações gerais da API

### GET /health
Verificação do status da API

### POST /extract-skus
Extrai SKUs de um PDF enviado em base64

**Request Body:**
```json
{
    "pdf_base64": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPD4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQovUmVzb3VyY2VzIDw8Ci9Gb250IDw8Ci9GMSA0IDAgUgo+Pgo+PgovQ29udGVudHMgNSAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9MZW5ndGggNDQKPj4Kc3RyZWFtCkJUCi9GMSAxMiBUZgoxMDAgNzAwIFRkCihIZWxsbyBXb3JsZCkgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagp4cmVmCjAgNgowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1OCAwMDAwMCBuIAowMDAwMDAwMTE1IDAwMDAwIG4gCjAwMDAwMDAyNDUgMDAwMDAgbiAKMDAwMDAwMDMxMCAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9TaXplIDYKL1Jvb3QgMSAwIFIKPj4Kc3RhcnR4cmVmCjQwMQolJUVPRgo=",
    "filename": "documento.pdf"
}
```

**Response:**
```json
{
    "metadata": {
        "total_skus": 38,
        "total_unidades": 266,
        "data_extracao": "2024-01-15T10:30:00.123456",
        "fonte": "documento.pdf",
        "header_info": {
            "produtos": 38,
            "unidades": 266
        }
    },
    "skus": [
        {
            "sku": "CAR002",
            "quantidade": 40
        },
        {
            "sku": "ESC014-P",
            "quantidade": 6
        }
    ]
}
```

### POST /extract-skus/simple
Versão simplificada que retorna apenas a lista de SKUs

**Response:**
```json
[
    {
        "sku": "CAR002",
        "quantidade": 40
    },
    {
        "sku": "ESC014-P",
        "quantidade": 6
    }
]
```

## 🧪 Exemplo de uso com curl

```bash
curl -X POST "http://localhost:5555/extract-skus" \
     -H "Content-Type: application/json" \
     -d '{
       "pdf_base64": "SEU_PDF_EM_BASE64_AQUI",
       "filename": "test.pdf"
     }'
```

## 🧪 Exemplo de uso com Python

```python
import requests
import base64

# Ler PDF e converter para base64
with open("documento.pdf", "rb") as f:
    pdf_base64 = base64.b64encode(f.read()).decode('utf-8')

# Fazer requisição
response = requests.post(
    "http://localhost:5555/extract-skus",
    json={
        "pdf_base64": pdf_base64,
        "filename": "documento.pdf"
    }
)

result = response.json()
print(f"Total de SKUs: {result['metadata']['total_skus']}")
for sku_item in result['skus']:
    print(f"SKU: {sku_item['sku']} - Quantidade: {sku_item['quantidade']}")
```

## ⚠️ Limitações

- Tamanho máximo do arquivo: 50MB
- Apenas arquivos PDF são suportados
- O PDF deve conter tabelas estruturadas com SKUs

## 🛡️ Tratamento de Erros

A API retorna códigos de status HTTP apropriados:

- `200`: Sucesso
- `400`: Erro no formato dos dados (ex: base64 inválido)
- `422`: PDF válido mas sem SKUs encontrados
- `500`: Erro interno do servidor

## 🔧 Configuração

As configurações podem ser alteradas no arquivo `config.py` ou via variáveis de ambiente:

- `API_HOST`: Host da API (default: 0.0.0.0)
- `API_PORT`: Porta da API (default: 5555)
- `MAX_FILE_SIZE_MB`: Tamanho máximo do arquivo (default: 50MB)
- `LOG_LEVEL`: Nível de log (default: INFO)

## 📝 Estrutura do Projeto

```
full-extractor-api/
├── main.py              # Aplicação FastAPI principal
├── sku_extractor.py     # Módulo de extração de SKUs
├── config.py            # Configurações da aplicação
├── requirements.txt     # Dependências Python
├── Dockerfile           # Configuração Docker
├── docker-compose.yml   # Orquestração Docker
├── .dockerignore        # Arquivos ignorados no build
├── env.example          # Exemplo de variáveis de ambiente
└── README.md           # Documentação
```

## 🐳 Docker

### Build manual
```bash
docker build -t full-extractor-api .
```

### Executar
```bash
# Produção
docker run -p 5555:5555 full-extractor-api

# Com variáveis de ambiente
docker run -p 5555:5555 -e API_DEBUG=true -e LOG_LEVEL=DEBUG full-extractor-api
```

### Docker Compose
```bash
# Produção
docker-compose up -d

# Desenvolvimento
docker-compose --profile dev up

# Logs
docker-compose logs -f

# Parar
docker-compose down
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request 