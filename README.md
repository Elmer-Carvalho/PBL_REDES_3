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

- API: http://localhost:8000
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

## 📝 Funcionalidades

O sistema permite:

- Cadastro de postos de abastecimento
- Consulta de postos
- Atualização de informações
- Remoção de postos
- Interação com a blockchain para armazenamento seguro dos dados

## 🔐 Variáveis de Ambiente

O projeto utiliza as seguintes variáveis de ambiente:

- `HARDHAT_URL`: URL do nó Hardhat
- `DEPLOYMENT_PRIVATE_KEY`: Chave privada para deploy
- `DEPLOYMENT_ADDRESS`: Endereço do deploy
- `NETWORK_ID`: ID da rede
- `GAS_LIMIT`: Limite de gás para transações

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit de suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
