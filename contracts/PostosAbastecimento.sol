// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title PostosAbastecimento
 * @dev Contrato para gerenciamento de postos de abastecimento
 */
contract PostosAbastecimento {
    /**
     * @dev Estrutura que representa um posto de abastecimento
     */
    struct Posto {
        string nome;        // Nome do posto
        uint256 dataCadastro; // Data de cadastro em timestamp
        bool ocupado;      // Status de ocupação do posto
    }

    /**
     * @dev Estrutura que representa uma reserva
     */
    struct Reserva {
        string nomeCliente;    // Nome do cliente
        string nomeCarro;      // Nome do carro
        string nomePosto;      // Nome do posto
        uint256 dataReserva;   // Data da reserva em timestamp
    }

    /**
     * @dev Estrutura que representa um pagamento
     */
    struct Pagamento {
        uint256 id;            // ID do pagamento
        string nomeCliente;    // Nome do cliente
        string nomeCarro;      // Nome do carro
        string nomePosto;      // Nome do posto
        uint256 valor;         // Valor do pagamento
        uint256 data;          // Data do pagamento
        uint256 hora;          // Hora do pagamento
    }

    // Array que armazena todos os postos
    Posto[] private postos;
    
    // Array que armazena todas as reservas
    Reserva[] private reservas;

    // Array que armazena todos os pagamentos
    Pagamento[] private pagamentos;

    // Contador para IDs de pagamento
    uint256 private pagamentoIdCounter;

    // Mapeamento para facilitar a busca de postos por nome
    mapping(string => uint256) private postoPorNome;
    
    /**
     * @dev Evento emitido quando um novo posto é adicionado
     * @param id Índice do posto no array
     * @param nome Nome do posto
     * @param dataCadastro Data de cadastro
     */
    event PostoAdicionado(uint256 indexed id, string nome, uint256 dataCadastro);

    /**
     * @dev Evento emitido quando uma nova reserva é feita
     * @param id Índice da reserva no array
     * @param nomeCliente Nome do cliente
     * @param nomeCarro Nome do carro
     * @param nomePosto Nome do posto
     * @param dataReserva Data da reserva
     */
    event ReservaCriada(uint256 indexed id, string nomeCliente, string nomeCarro, string nomePosto, uint256 dataReserva);

    /**
     * @dev Evento emitido quando um novo pagamento é registrado
     * @param id ID do pagamento
     * @param nomeCliente Nome do cliente
     * @param nomeCarro Nome do carro
     * @param nomePosto Nome do posto
     * @param valor Valor do pagamento
     * @param data Data do pagamento
     * @param hora Hora do pagamento
     */
    event PagamentoRegistrado(
        uint256 indexed id,
        string nomeCliente,
        string nomeCarro,
        string nomePosto,
        uint256 valor,
        uint256 data,
        uint256 hora
    );

    /**
     * @dev Adiciona um novo posto
     * @param _nome Nome do posto a ser adicionado
     */
    function adicionarPosto(string memory _nome) public {
        require(bytes(_nome).length > 0, "Nome do posto nao pode ser vazio");
        require(postoPorNome[_nome] == 0, "Posto com este nome ja existe");
        
        uint256 dataCadastro = block.timestamp;
        uint256 id = postos.length;
        postos.push(Posto(_nome, dataCadastro, false));
        postoPorNome[_nome] = id + 1; // +1 para diferenciar de 0 (não encontrado)
        
        emit PostoAdicionado(id, _nome, dataCadastro);
    }

    /**
     * @dev Retorna a lista de todos os postos
     * @return Array com todos os postos cadastrados
     */
    function listarPostos() public view returns (Posto[] memory) {
        return postos;
    }

    /**
     * @dev Cria uma nova reserva para um posto
     * @param _nomeCliente Nome do cliente
     * @param _nomeCarro Nome do carro
     * @param _nomePosto Nome do posto
     * @return bool Indicando se a reserva foi bem sucedida
     */
    function criarReserva(string memory _nomeCliente, string memory _nomeCarro, string memory _nomePosto) public returns (bool) {
        require(bytes(_nomeCliente).length > 0, "Nome do cliente nao pode ser vazio");
        require(bytes(_nomeCarro).length > 0, "Nome do carro nao pode ser vazio");
        require(bytes(_nomePosto).length > 0, "Nome do posto nao pode ser vazio");
        
        uint256 postoId = postoPorNome[_nomePosto];
        require(postoId > 0, "Posto nao encontrado");
        postoId--; // Ajusta o índice
        
        require(!postos[postoId].ocupado, "Posto ja esta ocupado");
        
        uint256 dataReserva = block.timestamp;
        uint256 id = reservas.length;
        
        reservas.push(Reserva(_nomeCliente, _nomeCarro, _nomePosto, dataReserva));
        postos[postoId].ocupado = true;

        // Gerar valor aleatório para o pagamento (entre 1 e 1000)
        uint256 valorPagamento = uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao))) % 1000 + 1;
        
        // Registrar o pagamento
        uint256 dataAtual = block.timestamp;
        uint256 horaAtual = (dataAtual % 86400) / 3600; // Extrai a hora do timestamp
        
        pagamentos.push(Pagamento(
            pagamentoIdCounter,
            _nomeCliente,
            _nomeCarro,
            _nomePosto,
            valorPagamento,
            dataAtual,
            horaAtual
        ));

        emit ReservaCriada(id, _nomeCliente, _nomeCarro, _nomePosto, dataReserva);
        emit PagamentoRegistrado(
            pagamentoIdCounter,
            _nomeCliente,
            _nomeCarro,
            _nomePosto,
            valorPagamento,
            dataAtual,
            horaAtual
        );

        pagamentoIdCounter++;
        return true;
    }

    /**
     * @dev Retorna a lista de todas as reservas
     * @return Array com todas as reservas realizadas
     */
    function listarReservas() public view returns (Reserva[] memory) {
        return reservas;
    }

    /**
     * @dev Retorna a lista de todos os pagamentos
     * @return Array com todos os pagamentos realizados
     */
    function listarPagamentos() public view returns (Pagamento[] memory) {
        return pagamentos;
    }
} 