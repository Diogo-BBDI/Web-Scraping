import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
import time

# Headers para simular um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

# Lista de URLs para serem processadas
urls = [  # URLs fornecidas
    'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_0_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_49_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_98_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_147_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_196_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_245_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_294_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_343_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_392_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_441_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_490_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_539_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_588_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_637_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_686_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_735_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_784_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_833_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_882_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_931_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_980_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1029_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1078_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1127_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1176_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1225_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1274_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1323_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1372_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1421_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1470_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1519_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1568_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1617_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1666_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1715_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1764_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1813_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1862_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1911_NoIndex_True',
'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1960_NoIndex_True',

]

# Função para extrair dados de uma URL
def extrair_dados(url):
    dados = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Erro ao acessar {url}, Status Code: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra todos os itens de produto na página
        for item in soup.find_all('div', class_='ui-search-result__content-wrapper'):
            titulo = item.find('h2', class_='ui-search-item__title')
            link = item.find('a', class_='ui-search-link')['href']
            
            if titulo and link:
                dados.append([titulo.text.strip(), link])
        
        # Verifica se há uma próxima página
        next_page = soup.find('a', class_='andes-pagination__link ui-search-link')
        url = next_page['href'] if next_page else None
        
        # Aguarde entre as requisições
        time.sleep(2)

    return dados

# Arquivo CSV para salvar os dados extraídos
with open('mercadolivre_lcd.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Título', 'Link'])

    # Usando tqdm para exibir uma barra de progresso
    for url in tqdm(urls, desc='Processando URLs', unit='URL'):
        dados = extrair_dados(url)
        writer.writerows(dados)

print("Extração concluída e dados salvos em 'mercadolivre_lcd.csv'")
