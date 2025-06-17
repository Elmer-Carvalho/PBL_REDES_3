from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from web3 import Web3
import os
from solcx import compile_standard, install_solc
import json
from typing import List, Dict
import time
import logging
from datetime import datetime, timedelta
import random

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Postos de Abastecimento",
    description="API para gerenciamento de postos de abastecimento usando blockchain",
    version="1.0.0"
)

CONTRACT_ADDRESS_FILE = "/app/contract_address.txt"

def get_contract_address():
    if os.path.exists(CONTRACT_ADDRESS_FILE):
        with open(CONTRACT_ADDRESS_FILE, "r") as f:
            return f.read().strip()
    return None

def save_contract_address(address):
    with open(CONTRACT_ADDRESS_FILE, "w") as f:
        f.write(address)

# Configuração do Web3
w3 = Web3(Web3.HTTPProvider(os.getenv('HARDHAT_URL')))

# Instalar compilador Solidity
install_solc("0.8.19")

def formatar_data_hora(timestamp: int) -> Dict[str, str]:
    """
    Formata um timestamp Unix para data e hora no padrão brasileiro (Brasília)
    
    Args:
        timestamp (int): Timestamp Unix em segundos
        
    Returns:
        Dict[str, str]: Dicionário com data e hora formatadas
    """
    # Converter timestamp para datetime em UTC
    dt = datetime.fromtimestamp(timestamp)
    
    # Ajustar para horário de Brasília (UTC-3)
    dt_brasilia = dt - timedelta(hours=3)
    
    # Formatar data e hora
    data_formatada = dt_brasilia.strftime("%d/%m/%Y")
    hora_formatada = dt_brasilia.strftime("%H:%M:%S")
    
    return {
        "data": data_formatada,
        "hora": hora_formatada
    }

def deploy_contract():
    try:
        logger.info("Iniciando deploy do contrato...")
        
        # Compilar o contrato
        with open('/app/contracts/PostosAbastecimento.sol', 'r') as file:
            contract_source = file.read()

        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"PostosAbastecimento.sol": {"content": contract_source}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                },
            },
            solc_version="0.8.19",
        )

        # Obter bytecode e ABI
        bytecode = compiled_sol["contracts"]["PostosAbastecimento.sol"]["PostosAbastecimento"]["evm"]["bytecode"]["object"]
        abi = json.loads(compiled_sol["contracts"]["PostosAbastecimento.sol"]["PostosAbastecimento"]["metadata"])["output"]["abi"]

        # Criar contrato
        PostosAbastecimento = w3.eth.contract(abi=abi, bytecode=bytecode)

        # Obter nonce
        nonce = w3.eth.get_transaction_count(os.getenv('DEPLOYMENT_ADDRESS'))

        # Construir transação
        transaction = PostosAbastecimento.constructor().build_transaction({
            'chainId': int(os.getenv('NETWORK_ID')),
            'gas': int(os.getenv('GAS_LIMIT')),
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        # Assinar transação
        signed_txn = w3.eth.account.sign_transaction(transaction, os.getenv('DEPLOYMENT_PRIVATE_KEY'))

        # Enviar transação
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        logger.info(f"Contrato deployado com sucesso no endereço: {tx_receipt.contractAddress}")
        return w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    except Exception as e:
        logger.error(f"Erro durante deploy do contrato: {str(e)}")
        raise

async def popular_dados_teste(contract):
    """
    Popula o sistema com dados de teste
    """
    try:
        logger.info("Iniciando população de dados de teste...")
        
        # Lista de nomes de postos
        nomes_postos = [
            "Posto Central",
            "Posto Express",
            "Posto 24 Horas",
            "Posto Premium",
            "Posto Econômico",
            "Posto VIP",
            "Posto Shell",
            "Posto Ipiranga",
            "Posto BR",
            "Posto Petrobras"
        ]
        
        # Lista de nomes de clientes
        nomes_clientes = [
            "João Silva",
            "Maria Santos",
            "Pedro Oliveira",
            "Ana Costa",
            "Carlos Souza"
        ]
        
        # Lista de nomes de carros
        nomes_carros = [
            "Gol",
            "Uno",
            "Civic",
            "Corolla",
            "HB20",
            "Onix",
            "Celta",
            "Palio",
            "Sandero",
            "Cobalt"
        ]
        
        # Criar postos
        for nome_posto in nomes_postos:
            try:
                nonce = w3.eth.get_transaction_count(os.getenv('DEPLOYMENT_ADDRESS'))
                transaction = contract.functions.adicionarPosto(nome_posto).build_transaction({
                    'chainId': int(os.getenv('NETWORK_ID')),
                    'gas': int(os.getenv('GAS_LIMIT')),
                    'gasPrice': w3.eth.gas_price,
                    'nonce': nonce,
                })
                
                signed_txn = w3.eth.account.sign_transaction(transaction, os.getenv('DEPLOYMENT_PRIVATE_KEY'))
                tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                w3.eth.wait_for_transaction_receipt(tx_hash)
                
                logger.info(f"Posto {nome_posto} criado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao criar posto {nome_posto}: {str(e)}")
        
        # Criar reservas (apenas para os 5 primeiros postos)
        for i in range(5):
            try:
                nome_cliente = random.choice(nomes_clientes)
                nome_carro = random.choice(nomes_carros)
                nome_posto = nomes_postos[i]
                
                nonce = w3.eth.get_transaction_count(os.getenv('DEPLOYMENT_ADDRESS'))
                transaction = contract.functions.criarReserva(
                    nome_cliente,
                    nome_carro,
                    nome_posto
                ).build_transaction({
                    'chainId': int(os.getenv('NETWORK_ID')),
                    'gas': int(os.getenv('GAS_LIMIT')),
                    'gasPrice': w3.eth.gas_price,
                    'nonce': nonce,
                })
                
                signed_txn = w3.eth.account.sign_transaction(transaction, os.getenv('DEPLOYMENT_PRIVATE_KEY'))
                tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                w3.eth.wait_for_transaction_receipt(tx_hash)
                ''''''
                logger.info(f"Reserva criada com sucesso para {nome_cliente} no posto {nome_posto}")
            except Exception as e:
                logger.error(f"Erro ao criar reserva: {str(e)}")
        
        logger.info("População de dados de teste concluída com sucesso")
    except Exception as e:
        logger.error(f"Erro durante população de dados de teste: {str(e)}")

# Lógica para deploy ou conexão ao contrato
contract_address = get_contract_address()
abi = None
contract = None

if contract_address:
    # Conectar ao contrato já existente
    with open('/app/contracts/PostosAbastecimento.sol', 'r') as file:
        contract_source = file.read()
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"PostosAbastecimento.sol": {"content": contract_source}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.19",
    )
    abi = json.loads(compiled_sol["contracts"]["PostosAbastecimento.sol"]["PostosAbastecimento"]["metadata"])["output"]["abi"]
    contract = w3.eth.contract(address=contract_address, abi=abi)
else:
    if os.getenv("API_DEPLOYER", "false").lower() == "true":
        # Só a api1 faz o deploy
        contract = deploy_contract()
        save_contract_address(contract.address)
    else:
        # Outras instâncias aguardam o deploy
        while not os.path.exists(CONTRACT_ADDRESS_FILE):
            print("Aguardando deploy do contrato pela instância principal...")
            time.sleep(2)
        contract_address = get_contract_address()
        with open('/app/contracts/PostosAbastecimento.sol', 'r') as file:
            contract_source = file.read()
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"PostosAbastecimento.sol": {"content": contract_source}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                },
            },
            solc_version="0.8.19",
        )
        abi = json.loads(compiled_sol["contracts"]["PostosAbastecimento.sol"]["PostosAbastecimento"]["metadata"])["output"]["abi"]
        contract = w3.eth.contract(address=contract_address, abi=abi)

# Popular dados de teste
@app.on_event("startup")
async def startup_event():
    await popular_dados_teste(contract)

class Posto(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do posto de abastecimento")

class PostoResponse(BaseModel):
    nome: str
    dataCadastro: str
    ocupado: bool

class Reserva(BaseModel):
    nomeCliente: str = Field(..., min_length=1, max_length=100, description="Nome do cliente")
    nomeCarro: str = Field(..., min_length=1, max_length=100, description="Nome do carro")
    nomePosto: str = Field(..., min_length=1, max_length=100, description="Nome do posto")

class ReservaResponse(BaseModel):
    nomeCliente: str
    nomeCarro: str
    nomePosto: str
    dataReserva: str
    horaReserva: str

class PagamentoResponse(BaseModel):
    id: int
    nomeCliente: str
    nomeCarro: str
    nomePosto: str
    valor: int
    data: str
    hora: str

@app.post("/postos", response_model=Dict[str, str])
async def adicionar_posto(posto: Posto):
    """
    Adiciona um novo posto de abastecimento.
    
    Args:
        posto (Posto): Dados do posto a ser adicionado
        
    Returns:
        Dict[str, str]: Mensagem de sucesso e hash da transação
    """
    try:
        logger.info(f"Adicionando posto: {posto.nome}")
        
        # Preparar transação
        nonce = w3.eth.get_transaction_count(os.getenv('DEPLOYMENT_ADDRESS'))
        transaction = contract.functions.adicionarPosto(posto.nome).build_transaction({
            'chainId': int(os.getenv('NETWORK_ID')),
            'gas': int(os.getenv('GAS_LIMIT')),
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        # Assinar e enviar transação
        signed_txn = w3.eth.account.sign_transaction(transaction, os.getenv('DEPLOYMENT_PRIVATE_KEY'))
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        logger.info(f"Posto adicionado com sucesso. Hash: {tx_hash.hex()}")
        return {"message": "Posto adicionado com sucesso", "transaction_hash": tx_hash.hex()}
    except Exception as e:
        logger.error(f"Erro ao adicionar posto: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/postos", response_model=List[PostoResponse])
async def listar_postos():
    """
    Lista todos os postos de abastecimento cadastrados.
    
    Returns:
        List[PostoResponse]: Lista de postos cadastrados
    """
    try:
        logger.info("Listando postos...")
        postos = contract.functions.listarPostos().call()
        
        resultado = []
        for posto in postos:
            data_formatada = formatar_data_hora(posto[1])
            resultado.append(PostoResponse(
                nome=posto[0],
                dataCadastro=data_formatada["data"],
                ocupado=posto[2]
            ))
        
        logger.info(f"Encontrados {len(resultado)} postos")
        return resultado
    except Exception as e:
        logger.error(f"Erro ao listar postos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reservas", response_model=Dict[str, str])
async def criar_reserva(reserva: Reserva):
    """
    Cria uma nova reserva para um posto de abastecimento.
    
    Args:
        reserva (Reserva): Dados da reserva a ser criada
        
    Returns:
        Dict[str, str]: Mensagem de sucesso e hash da transação
    """
    try:
        logger.info(f"Criando reserva para posto: {reserva.nomePosto}")
        
        # Preparar transação
        nonce = w3.eth.get_transaction_count(os.getenv('DEPLOYMENT_ADDRESS'))
        transaction = contract.functions.criarReserva(
            reserva.nomeCliente,
            reserva.nomeCarro,
            reserva.nomePosto
        ).build_transaction({
            'chainId': int(os.getenv('NETWORK_ID')),
            'gas': int(os.getenv('GAS_LIMIT')),
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        # Assinar e enviar transação
        signed_txn = w3.eth.account.sign_transaction(transaction, os.getenv('DEPLOYMENT_PRIVATE_KEY'))
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        logger.info(f"Reserva criada com sucesso. Hash: {tx_hash.hex()}")
        return {"message": "Reserva criada com sucesso", "transaction_hash": tx_hash.hex()}
    except Exception as e:
        logger.error(f"Erro ao criar reserva: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reservas", response_model=List[ReservaResponse])
async def listar_reservas():
    """
    Lista todas as reservas realizadas.
    
    Returns:
        List[ReservaResponse]: Lista de reservas realizadas
    """
    try:
        logger.info("Listando reservas...")
        reservas = contract.functions.listarReservas().call()
        
        resultado = []
        for reserva in reservas:
            data_formatada = formatar_data_hora(reserva[3])
            resultado.append(ReservaResponse(
                nomeCliente=reserva[0],
                nomeCarro=reserva[1],
                nomePosto=reserva[2],
                dataReserva=data_formatada["data"],
                horaReserva=data_formatada["hora"]
            ))
        
        logger.info(f"Encontradas {len(resultado)} reservas")
        return resultado
    except Exception as e:
        logger.error(f"Erro ao listar reservas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pagamentos", response_model=List[PagamentoResponse])
async def listar_pagamentos():
    """
    Lista todos os pagamentos realizados.
    
    Returns:
        List[PagamentoResponse]: Lista de pagamentos realizados
    """
    try:
        logger.info("Listando pagamentos...")
        pagamentos = contract.functions.listarPagamentos().call()
        
        resultado = []
        for pagamento in pagamentos:
            data_formatada = formatar_data_hora(pagamento[5])
            resultado.append(PagamentoResponse(
                id=pagamento[0],
                nomeCliente=pagamento[1],
                nomeCarro=pagamento[2],
                nomePosto=pagamento[3],
                valor=pagamento[4],
                data=data_formatada["data"],
                hora=data_formatada["hora"]
            ))
        
        logger.info(f"Encontrados {len(resultado)} pagamentos")
        return resultado
    except Exception as e:
        logger.error(f"Erro ao listar pagamentos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Verifica a saúde da API e da conexão com a blockchain.
    
    Returns:
        Dict: Status da API e da blockchain
    """
    try:
        return {
            "status": "healthy",
            "blockchain_connected": w3.is_connected(),
            "contract_deployed": contract is not None,
            "block_number": w3.eth.block_number if w3.is_connected() else None
        }
    except Exception as e:
        logger.error(f"Erro no health check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)