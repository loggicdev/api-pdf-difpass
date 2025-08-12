# Deploy no Dokploy

Este documento descreve como fazer deploy da API PDF DIFPASS no Dokploy.

## 📋 Pré-requisitos

- Dokploy configurado na VPS
- Acesso ao repositório GitHub
- Domínio configurado (opcional)

## 🚀 Deploy via Dokploy

### 1. Criar Aplicação no Dokploy

1. Acesse o painel do Dokploy
2. Clique em "New Application"
3. Escolha "GitHub Repository"
4. Selecione o repositório: `loggicdev/api-pdf-difpass`
5. Configure:
   - **Nome**: `api-pdf-difpass`
   - **Branch**: `main`
   - **Build Type**: `Docker`
   - **Dockerfile Path**: `./Dockerfile`

### 2. Configurações de Environment

Configure as seguintes variáveis de ambiente no Dokploy:

```bash
# Porta da aplicação
PORT=8000

# Host binding (manter como 0.0.0.0 para Docker)
HOST=0.0.0.0

# Indicador de container Docker
DOCKER_CONTAINER=true

# Python
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### 3. Configurações de Rede

- **Porta interna**: 8000
- **Porta externa**: 80 ou 443 (HTTPS)
- **Domínio**: Configure seu domínio personalizado

### 4. Deploy

1. Clique em "Deploy" no Dokploy
2. Aguarde o build e deploy automático
3. Verifique os logs para confirmação

## 🔍 Verificação

Após o deploy, verifique:

- **API Docs**: `https://seu-dominio.com/docs`
- **ReDoc**: `https://seu-dominio.com/redoc`
- **Health Check**: `https://seu-dominio.com/`

## 📊 Monitoramento

O Dokploy fornece:
- Logs em tempo real
- Métricas de CPU/Memória
- Status da aplicação
- Builds automáticos via webhook

## 🔄 Atualizações

Para atualizar a aplicação:
1. Faça push das mudanças para o repositório
2. O Dokploy fará rebuild automático (se webhook configurado)
3. Ou clique em "Rebuild" manualmente no painel

## 🐛 Troubleshooting

### Problemas Comuns

**1. Build falha por dependências:**
```bash
# Verificar se todas as dependências estão no requirements.txt
pip freeze > requirements.txt
```

**2. Aplicação não responde:**
- Verificar se a porta 8000 está exposta
- Verificar variáveis de ambiente
- Verificar logs da aplicação

**3. Erro de permissão de arquivos:**
- O Dockerfile usa usuário não-root para segurança
- Verificar permissões dos arquivos assets/

### Logs Úteis

```bash
# Ver logs da aplicação no Dokploy
# Ou via linha de comando na VPS:
docker logs <container-id>
```

## 📁 Estrutura de Deploy

```
api-pdf-difpass/
├── Dockerfile              # Configuração do container
├── docker-compose.yml      # Para desenvolvimento local
├── .dockerignore           # Arquivos ignorados no build
├── requirements.txt        # Dependências Python
├── api_pdf.py              # Aplicação principal
├── assets/                 # Recursos estáticos
└── DOKPLOY.md              # Este arquivo
```

## 🌐 URLs de Produção

- **API**: `https://seu-dominio.com`
- **Documentação**: `https://seu-dominio.com/docs`
- **ReDoc**: `https://seu-dominio.com/redoc`
