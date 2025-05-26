# Contribuindo para o Full Extractor API

Obrigado por considerar contribuir para o Full Extractor API! Este documento fornece diretrizes para contribuição.

## 🚀 Como contribuir

### 1. Fork do projeto
```bash
git clone https://github.com/seu-usuario/full-extractor-api.git
cd full-extractor-api
```

### 2. Criar uma branch
```bash
git checkout -b feature/nova-funcionalidade
```

### 3. Configurar ambiente de desenvolvimento

#### Com Docker (Recomendado)
```bash
# Modo desenvolvimento com reload automático
docker-compose --profile dev up
```

#### Sem Docker
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar em modo desenvolvimento
python main.py
```

### 4. Fazer suas alterações

- Mantenha o código limpo e bem documentado
- Siga as convenções PEP 8 para Python
- Adicione docstrings nas funções
- Teste suas mudanças

### 5. Testar

```bash
# Testar endpoint de saúde
curl http://localhost:5555/health

# Testar extração (com PDF válido)
curl -X POST "http://localhost:5555/extract-skus" \
     -H "Content-Type: application/json" \
     -d '{"pdf_base64": "SEU_PDF_BASE64", "filename": "test.pdf"}'
```

### 6. Commit e Push

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/nova-funcionalidade
```

### 7. Abrir Pull Request

- Descreva claramente as mudanças
- Inclua exemplos de uso se aplicável
- Referencie issues relacionadas

## 📝 Padrões de Commit

Use conventional commits:

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `style:` formatação (sem mudança de código)
- `refactor:` refatoração de código
- `test:` adição de testes
- `chore:` tarefas de manutenção

## 🐛 Reportar Bugs

Ao reportar bugs, inclua:

1. Descrição clara do problema
2. Passos para reproduzir
3. Comportamento esperado vs atual
4. Versão do Python/Docker
5. Logs de erro (se houver)

## 💡 Sugerir Funcionalidades

Para sugerir novas funcionalidades:

1. Verifique se já não existe uma issue similar
2. Descreva o problema que resolve
3. Proponha uma solução
4. Considere alternativas

## 🔧 Estrutura do Código

```
full-extractor-api/
├── main.py              # FastAPI app principal
├── sku_extractor.py     # Lógica de extração
├── config.py            # Configurações
├── requirements.txt     # Dependências
├── Dockerfile           # Container config
├── docker-compose.yml   # Orquestração
└── tests/              # Testes (futuro)
```

## 📋 Checklist para PR

- [ ] Código segue padrões PEP 8
- [ ] Funcionalidade testada manualmente
- [ ] Documentação atualizada
- [ ] Commit messages seguem padrão
- [ ] Sem breaking changes (ou documentado)

## 🤝 Código de Conduta

- Seja respeitoso e profissional
- Aceite feedback construtivo
- Foque no problema, não na pessoa
- Colabore de forma inclusiva

## 📞 Contato

Para dúvidas sobre contribuição, abra uma issue ou entre em contato.

Obrigado pela sua contribuição! 🎉 