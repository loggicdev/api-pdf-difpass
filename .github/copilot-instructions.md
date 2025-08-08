<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# API de Geração de PDF com Cabeçalho Personalizado

Este é um projeto FastAPI para processamento de PDFs. A aplicação cria um "shell" (moldura) personalizada para documentos PDF existentes, adicionando elementos visuais de cabeçalho.

## Contexto do Projeto
- **Tecnologia principal**: FastAPI com PyMuPDF (fitz)
- **Propósito**: Adicionar cabeçalhos personalizados a documentos PDF
- **Elementos do cabeçalho**: Ícone, título (CRUZEIRO), logo DIFPASS, barra decorativa
- **Processamento**: Mantém o conteúdo original dentro de uma moldura com bordas

## Padrões de Código
- Use tratamento de exceções adequado para operações de arquivo
- Implemente limpeza de recursos temporários
- Mantenha logs informativos para debugging
- Valide tipos de arquivo antes do processamento

## APIs Principais
- `/generate-pdf/` - Endpoint principal para gerar PDFs com cabeçalho personalizado
