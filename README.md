# Sistema de Postos de Abastecimento com Blockchain

Este projeto implementa um sistema de gerenciamento de postos de abastecimento utilizando blockchain, com uma API REST para interação e um contrato inteligente para armazenamento dos dados.

## 🚀 Tecnologias Utilizadas

- **Backend**: Python com FastAPI
- **Blockchain**: Hardhat (Ethereum)
- **Contrato Inteligente**: Solidity
- **Containerização**: Docker e Docker Compose
- **Web3**: Web3.py para interação com a blockchain

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Python 3.8+ (para desenvolvimento local)

## 🔧 Instalação e Execução

1. Clone o repositório:

```bash
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_DIRETÓRIO]
```

2. Execute o projeto usando Docker Compose:

```bash
docker-compose up --build
```

O sistema estará disponível em:

- API (Nginx - balanceador): http://localhost:8000
- API 1: http://localhost:8001
- API 2: http://localhost:8002
- API 3: http://localhost:8003
- Hardhat Network: http://localhost:8545

## 🏗️ Estrutura do Projeto

```
.
├── app/
│   └── main.py           # API FastAPI
├── contracts/
│   └── PostosAbastecimento.sol  # Contrato Inteligente
├── hardhat/              # Configuração do Hardhat
├── docker-compose.yml    # Configuração dos containers
├── Dockerfile           # Configuração do container da API
└── requirements.txt     # Dependências Python
```

## 🖥️ Nova Arquitetura com Múltiplos Servidores

Agora o sistema está configurado para rodar múltiplos servidores de API (api1, api2, api3), cada um em seu próprio container e porta:

- **api1:** http://localhost:8001
- **api2:** http://localhost:8002
- **api3:** http://localhost:8003
- **Nginx (balanceador):** http://localhost:8000

O Nginx faz o balanceamento de carga entre as APIs, permitindo requisições simultâneas e alta disponibilidade.

### Como funciona a lógica de deploy e concorrência

- Apenas a **api1** faz o deploy do contrato na blockchain e salva o endereço em um arquivo compartilhado (`contract_address.txt`).
- As outras APIs (api2, api3) aguardam esse arquivo ser criado e então conectam ao mesmo contrato já deployado.
- Todas as APIs compartilham o diretório `/app` via volume Docker, garantindo acesso ao mesmo endereço de contrato.
- Assim, **vários servidores podem fazer requisições ao mesmo tempo para a blockchain**.

### Concorrência está funcionando?

Sim! O que foi implementado permite que múltiplos servidores (containers) façam requisições simultâneas para a blockchain. O controle de concorrência real é feito pelo próprio blockchain, que garante a ordem e integridade das transações. Ou seja:

- Você pode testar a concorrência fazendo várias requisições ao mesmo tempo (por exemplo, usando diferentes abas ou ferramentas como Postman/curl).
- O blockchain irá processar as transações de forma segura, mesmo que cheguem ao mesmo tempo de diferentes servidores.
- O sistema está pronto para cenários reais de concorrência e alta disponibilidade.

## 📝 Funcionalidades

O sistema permite:

- Cadastro de postos de abastecimento
- Consulta de postos
- Atualização de informações
- Remoção de postos
- Interação com a blockchain para armazenamento seguro dos dados
- Teste de concorrência real com múltiplos servidores

## 🔐 Variáveis de Ambiente

O projeto utiliza as seguintes variáveis de ambiente:

- `HARDHAT_URL`: URL do nó Hardhat
- `DEPLOYMENT_PRIVATE_KEY`: Chave privada para deploy
- `DEPLOYMENT_ADDRESS`: Endereço do deploy
- `NETWORK_ID`: ID da rede
- `GAS_LIMIT`: Limite de gás para transações
- `API_DEPLOYER`: Define se a instância da API fará o deploy do contrato (true apenas para api1)

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit de suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
