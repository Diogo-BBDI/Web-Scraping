import os
import pandas as pd
import chardet

# Defina o caminho da pasta onde estão os arquivos
pasta = "/home/diogo/Área de trabalho/Scrapy/Teclados"

# Lista todos os arquivos CSV e XLS na pasta
arquivos = [f for f in os.listdir(pasta) if f.endswith((".csv", ".xls"))]

# Cria uma lista para armazenar os DataFrames
dataframes = []

# Função para detectar o encoding de um arquivo (apenas para CSV)
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']

# Loop para ler cada arquivo e adicioná-lo à lista
for arquivo in arquivos:
    caminho_arquivo = os.path.join(pasta, arquivo)
    try:
        if arquivo.endswith(".csv"):
            # Detecta o encoding para CSV
            encoding = detect_encoding(caminho_arquivo)
            print(f"Lendo {arquivo} (CSV) com encoding: {encoding}")
            
            # Lê o arquivo CSV, pulando linhas problemáticas
            df = pd.read_csv(
                caminho_arquivo,
                encoding=encoding,
                on_bad_lines='skip',  # Pula linhas com erro
                # delimiter=';'      # Ajuste se necessário
            )
        elif arquivo.endswith(".xls"):
            print(f"Lendo {arquivo} (XLS)")
            # Lê o arquivo XLS (não precisa de encoding, é binário)
            df = pd.read_excel(caminho_arquivo, engine='xlrd')  # Usa xlrd para .xls
            
        print(f"Linhas lidas de {arquivo}: {len(df)}")
        dataframes.append(df)
    except Exception as e:
        print(f"Erro ao ler {arquivo}: {e}")
        # Para CSV, exibe as primeiras linhas como texto
        if arquivo.endswith(".csv"):
            with open(caminho_arquivo, 'r', encoding=encoding) as f:
                print(f"Primeiras 5 linhas de {arquivo}:")
                for i, line in enumerate(f.readlines()[:5], 1):
                    print(f"Linha {i}: {line.strip()}")

# Verifica se há DataFrames para concatenar
if dataframes:
    # Concatena todos os DataFrames
    df_final = pd.concat(dataframes, ignore_index=True)

    # Salva o resultado em um novo arquivo CSV
    df_final.to_csv("arquivo_concatenado.csv", index=False, encoding="utf-8")

    print(f"Arquivos mesclados com sucesso! Total de linhas: {len(df_final)}")
else:
    print("Nenhum arquivo foi lido com sucesso.")
