# PDF Shell Generator API

Uma API FastAPI para criar "shells" (molduras) personalizadas para documentos PDF, adicionando cabeçalhos com elementos visuais customizados.

## Funcionalidades

- 🖼️ Adiciona cabeçalho personalizado a documentos PDF
- 🎨 Suporte a elementos visuais: ícone, título, logo e barra decorativa
- 📄 Processa múltiplas páginas mantendo a formatação original
- 🚀 API REST simples e eficiente
- 🔧 Processamento em memória com limpeza automática de arquivos temporários

## Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **PyMuPDF (fitz)** - Manipulação de documentos PDF
- **Uvicorn** - Servidor ASGI de alta performance

## Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd api-marcao
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

### Desenvolvimento
```bash
python api_pdf.py
```

### Produção
```bash
uvicorn api_pdf:app --host 0.0.0.0 --port 8000
```

A API estará disponível em: http://localhost:8000

## Documentação da API

Acesse a documentação interativa em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Uso da API

### Endpoint Principal

**POST** `/generate-pdf/`

Gera um PDF com cabeçalho personalizado.

#### Parâmetros (form-data):
- `title` (string, opcional): Título do cabeçalho (padrão: "CRUZEIRO")
- `icon_image` (file): Imagem do ícone (PNG)
- `dif_image` (file): Logo DIFPASS (PNG)
- `input_pdf` (file): PDF original a ser processado

#### Resposta:
- PDF processado com cabeçalho personalizado e gradiente azul-laranja

### Exemplo de Uso com curl:

```bash
curl -X POST "http://localhost:8001/generate-pdf/" \
  -F "title=MEUCLUB" \
  -F "icon_image=@icon.png" \
  -F "dif_image=@logo.png" \
  -F "input_pdf=@document.pdf" \
  --output output.pdf
```

## Estrutura do Projeto

```
api-marcao/
├── api_pdf.py          # Código principal da API
├── requirements.txt    # Dependências Python
├── README.md          # Documentação
└── .github/
    └── copilot-instructions.md
```

## Layout do Cabeçalho

O cabeçalho gerado contém:

```
[Ícone] [Título]                    [Logo DIFPASS]
============== Gradiente Azul → Laranja ==============
```

- **Margens**: 40px laterais e 40px inferior
- **Ícone**: 40x40px no canto superior esquerdo
- **Título**: Texto configurável ao lado do ícone
- **Logo DIFPASS**: 100x40px no canto superior direito
- **Gradiente**: Barra horizontal azul-laranja criada programaticamente
- **Borda**: Contorno cinza claro ao redor do conteúdo original

## Desenvolvimento

### Estrutura do Código

- `create_pdf_shell_and_insert_content_core()`: Função principal de processamento
- `/generate-pdf/`: Endpoint FastAPI que gerencia uploads e resposta

### Tratamento de Erros

- Validação de arquivos PDF
- Tratamento de exceções em operações de imagem
- Limpeza automática de arquivos temporários
- Códigos de erro HTTP apropriados

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
