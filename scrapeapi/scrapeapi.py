import requests
import pandas as pd
from bs4 import BeautifulSoup
import math

# Cabeçalhos da requisição
headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json',
    'X-Api-Key': '5b13f80d0f024d68ae654ff1e7612cc6',
    'Magento-Environment-Id': '5b161701-1558-4979-aebc-a80bbb012878',
    'Magento-Website-Code': 'base',
    'Magento-Store-Code': 'main_website_store',
    'Magento-Store-View-Code': 'default',
}

page_size = 500
current_page = 1

# Dados da requisição GraphQL (query original)
json_data = {
    'query': """
        query productSearch(
    $phrase: String!
    $pageSize: Int
    $currentPage: Int = 1
    $filter: [SearchClauseInput!]
    $sort: [ProductSearchSortInput!]
    $context: QueryContextInput
) {
    productSearch(
        phrase: $phrase
        page_size: $pageSize
        current_page: $currentPage
        filter: $filter
        sort: $sort
        context: $context
    ) {
        total_count
        items {
            product {
                sku
                name
                canonical_url
                price_range {
                    minimum_price {
                        final_price { value currency }
                    }
                    maximum_price {
                        final_price { value currency }
                    }
                }
            }
            productView {  # Adicione o bloco productView aqui
                inStock    # Adicione o campo inStock aqui
            }
        }
        page_info {
            current_page
            page_size
            total_pages
        }
    }
}
    """,
    'variables': {
        'phrase': '',
        'pageSize': page_size,
        'currentPage': current_page,
        'filter': [
            {
                'attribute': 'categoryPath',  # Filtro por categoria
                'eq': 'teclado-para-notebook',  # Exemplo: um caminho de categoria específico
            },
            {
                'attribute': 'visibility',
                'in': ['Catalog', 'Catalog, Search'],
            },
        ],
        'sort': [{'attribute': 'position', 'direction': 'ASC'}],
        'context': {
            'customerGroup': 'b6589fc6ab0dc82cf12099d1c2d40ab994e8410c',
            'userViewHistory': None,
        },
    },
}

palavras_chave = ['Acer',	'Apple',	'Asus',	'Avell',	'CCE',	'Clevo',	'Dell',	'Exo Smart',	'Gateway',	'H-Buster',	'HP',	'Ibyte',	'Intelbras',	'Itautec',	'LG',	'Leadership',	'Lenovo',	'Login',	'MSI',	'Megaware',	'Microboard',	'Multilaser',	'Part Number',	'Philco',	'Positivo',	'QBex',	'Samsung',	'Semp Toshiba',	'Sony Vaio',	'Toshiba',]

for palavra in palavras_chave:
    produtos = [ ]
    total_count = 0
    current_page = 1
    contador = 0

    json_data['variables']['phrase'] = palavra

    response = requests.post('https://catalog-service.adobe.io/graphql', headers=headers, json=json_data)
    data = response.json()

    # print(data)  # Pode remover este print após testar

    if 'errors' in data:
        print(f"Erros na resposta da API para '{palavra}':", data['errors'])
    elif 'data' in data and data['data'] is not None and 'productSearch' in data['data']:
        total_count = data['data']['productSearch']['total_count']
        print(f"Total de produtos encontrados para '{palavra}': {total_count}")

        max_pages = math.ceil(total_count / page_size)  # Calcula o número máximo de páginas

        while len(produtos) < total_count and current_page > 0 and contador < 20 and current_page <= max_pages:  # Limita por max_pages
            json_data['variables']['currentPage'] = current_page

            response = requests.post('https://catalog-service.adobe.io/graphql', headers=headers, json=json_data)
            data = response.json()

            if 'errors' in data:
                print(f"Erros na resposta da API (página {current_page}) para '{palavra}':", data['errors'])
                break
            elif 'data' in data and data['data'] is not None and 'productSearch' in data['data'] and 'items' in data['data']['productSearch']:
                items = data['data']['productSearch']['items']

                for item in items:
                    product = item.get('product', {})
                    # Correção inStock: Verifica se productView existe e se inStock está presente
                    product_view = item.get('productView', {})  # Obtém productView
                    in_stock = product_view.get('inStock', False) if product_view else False  # Valor padrão False

                    descricao_html = product.get('description', {}).get('html', '')
                    soup = BeautifulSoup(descricao_html, 'html.parser')
                    descricao_limpa = soup.get_text(strip=True)

                    produto = {
                        'SKU': product.get('sku', ''),
                        'Nome': product.get('name', ''),
                        'Descrição': descricao_limpa,
                        'Preço Regular Mínimo': product.get('price_range', {}).get('minimum_price', {}).get('regular_price', {}).get('value', 0),
                        'Preço Final Mínimo': product.get('price_range', {}).get('minimum_price', {}).get('final_price', {}).get('value', 0),
                        'Preço Regular Máximo': product.get('price_range', {}).get('maximum_price', {}).get('regular_price', {}).get('value', 0),
                        'Preço Final Máximo': product.get('price_range', {}).get('maximum_price', {}).get('final_price', {}).get('value', 0),
                        'Disponível em Estoque': in_stock,  # Usa o valor corrigido
                        'URL': f"https://www.bringit.com.br{product.get('canonical_url', '')}"
                    }
                    produtos.append(produto)

            else:
                print(f"Estrutura inesperada na resposta da API ou dados ausentes para '{palavra}'.")
                break

            current_page += 1
            contador += 1
            print(f"Página {current_page} processada para '{palavra}'.")

        df = pd.DataFrame(produtos)
        df.to_csv(f'dados_{palavra}.csv', index=False, encoding='utf-8')
        print(f"CSV atualizado gerado com sucesso para '{palavra}'!")

    else:
        print(f"Erro: Estrutura inesperada na resposta da API para '{palavra}'.")