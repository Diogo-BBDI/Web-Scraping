import requests
from bs4 import BeautifulSoup
import csv

# Lista de URLs do site a ser raspado
urls = [
    "https://batteryempire.pt/15-baterias-para-computadores-portateis#/page-1",
    "https://batteryempire.pt/15-baterias-para-computadores-portateis#/page-2",
    "https://batteryempire.pt/15-baterias-para-computadores-portateis#/page-3",
]

# Cabeçalhos HTTP, incluindo um User-Agent para emular um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/110.0.0.0 Safari/537.36'
}

# Conjunto para armazenar URLs já processadas
processed_urls = set()

# Abre um arquivo CSV para escrita
with open('dados_tabela.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Cria um objeto escritor CSV
    csvwriter = csv.writer(csvfile)

    # Escreve o cabeçalho no CSV
    headers_csv = ["Title", "Link", "Source URL"]
    csvwriter.writerow(headers_csv)

    # Itera sobre a lista de URLs
    for url in urls:
        try:
            # Envia uma solicitação GET para a URL
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Levanta um erro se a solicitação falhar

            # Cria uma instância do BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontra todos os elementos <a> com a classe "product-name"
            links = soup.select('a.product-name')

            # Itera sobre os elementos <a> e extrai o título e o link
            for link in links:
                title = link['title']
                href = link['href']
                full_url = f"https://batteryempire.pt{href}"  # Completa a URL

                # Verifica se a URL já foi processada
                if full_url not in processed_urls:
                    # Adiciona a URL ao conjunto de URLs processadas
                    processed_urls.add(full_url)

                    # Escreve os dados no CSV
                    csvwriter.writerow([title, full_url, url])

        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP ao acessar {url}: {e}")
        except Exception as e:
            print(f"Erro ao processar {url}: {e}")

print("Dados extraídos e salvos em 'dados_tabela.csv'")