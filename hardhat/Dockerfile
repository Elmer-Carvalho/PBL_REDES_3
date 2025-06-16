FROM node:16

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar solc
RUN pip3 install py-solc-x

# Copiar arquivos de configuração
COPY package*.json ./
RUN npm install

# Copiar código fonte
COPY . .

# Criar diretórios para volumes
RUN mkdir -p /app/cache /app/artifacts

# Expor porta do Hardhat
EXPOSE 8545

# Iniciar nó Hardhat
CMD ["npx", "hardhat", "node", "--hostname", "0.0.0.0"] 