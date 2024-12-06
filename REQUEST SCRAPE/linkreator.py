import re
import csv

def gerar_links_incrementados(links, output_file):
    # Regex para capturar o valor "Desde" e identificar onde ele aparece
    regex = re.compile(r"(_Desde_)(\d+)")
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Links"])  # Cabeçalho do CSV

        for link in links:
            match = regex.search(link)
            if match:
                prefixo = link[:match.start(2)]  # Tudo antes do número "Desde"
                desde = int(match.group(2))     # Captura o valor de "Desde"
                sufixo = link[match.end(2):]   # Tudo depois do número "Desde"

                # Geração dos links incrementados
                for i in range(0, desde + 1, 49):  # Incrementos de 49
                    novo_link = f"{prefixo}{i}{sufixo}"
                    writer.writerow([novo_link])

# Exemplo de uso:
links = [
   'https://lista.mercadolivre.com.br/informatica/portateis-acessorios/pecas-partes-notebooks/baterias/bateria-para-notebook_Desde_1969_NoIndex_True',
]

output_file = "links_gerados.csv"
gerar_links_incrementados(links, output_file)
