// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProductsOriginChain {
    // Estrutura com dados do produto
    struct Product {
        bool exists;
        string product_id;
        string product_name;
        string batch_number;
        string product_chain_id;
        string manufacture_date;
        string manufacturer;
        string manufacturing_location;
        string brief_description;
        string capture_date;
    }

    // Mapeamento do nome para os dados de produtos
    mapping(string => Product) private products;

    // Evento de registro de produto
    event ProductRegistered(bool exists,
        string product_id,
        string product_name,
        string batch_number,
        string product_chain_id,
        string manufacture_date,
        string manufacturer,
        string manufacturing_location,
        string brief_description,
        string capture_date
        );

    event Test(string messsage);

    // Função para registrar um produto
    function register(string memory _product_id,
                    string memory _product_name,
                    string memory _batch_number,
                    string memory _product_chain_id,
                    string memory _manufacture_date,
                    string memory _manufacturer,
                    string memory _manufacturing_location,
                    string memory _brief_description,
                    string memory _capture_date)public {
        
        require(!products[_product_chain_id].exists,"Product with this chain ID already exists");

        products[_product_chain_id] = Product(true,
                                            _product_id,
                                            _product_name,
                                            _batch_number,
                                            _product_chain_id,
                                            _manufacture_date,
                                            _manufacturer,
                                            _manufacturing_location,
                                            _brief_description,
                                            _capture_date);
        emit Test("Teste funcionou");
        emit ProductRegistered(true,
                            _product_id,
                            _product_name,
                            _batch_number,
                            _product_chain_id,
                            _manufacture_date,
                            _manufacturer,
                            _manufacturing_location,
                            _brief_description,
                            _capture_date
                            );
    }

    // Função para obter os dados de um produto pelo id criado
    function getProduct(string memory _product_chain_id) public view returns (bool, string memory, string memory, string memory, string memory, string memory, string memory, string memory, string memory, string memory) {
        Product memory p = products[_product_chain_id];
        if (!p.exists) {
        return (p.exists,
                p.product_id,
                p.product_name,
                p.batch_number,
                p.product_chain_id,
                p.manufacture_date,
                p.manufacturer,
                p.manufacturing_location,
                p.brief_description,
                p.capture_date);
        } else {
                 return (false, "", "", "", "", "", "", "", "", "");
             }
    }
    
}
