# Use Python 3.11 slim como base
FROM python:3.11-slim as builder

# Instalar dependências do sistema necessárias para PyMuPDF
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmupdf-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage final - imagem de produção
FROM python:3.11-slim

# Instalar apenas as bibliotecas runtime necessárias
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    libfreetype6 \
    libjpeg62-turbo \
    libopenjp2-7 \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash app

# Criar diretório de trabalho e definir permissões
WORKDIR /app
RUN chown app:app /app

# Copiar dependências instaladas do builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código da aplicação
COPY --chown=app:app . .

# Mudar para usuário não-root
USER app

# Expor porta padrão
EXPOSE 8000

# Variáveis de ambiente
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Comando de inicialização
CMD ["python", "api_pdf.py"]
