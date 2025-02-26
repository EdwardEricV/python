import os
import time
import json
from random import random
from datetime import datetime
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

# Captando a taxa CDI do site do BCB
try:
    response = requests.get(url=URL)
    response.raise_for_status()
    if response.text.strip():
        dados_json = json.loads(response.text)
        if dados_json:
            dado = dados_json[-1]['valor']
        else:
            print("Resposta da API está vazia.")
            dado = None
    else:
        print("Resposta da API está vazia.")
        dado = None
except requests.HTTPError:
    print("Dado não encontrado, continuando.")
    dado = None
except json.JSONDecodeError:
    print("Erro ao decodificar JSON, resposta inválida.")
    dado = None
except Exception as exc:
    print("Erro, parando a execução.")
    raise exc

# Verificando se o arquivo "taxa-cdi-analise.csv" existe
if not os.path.exists('./taxa-cdi-analise.csv'):
    with open('./taxa-cdi-analise.csv', 'w', encoding='utf8') as fp:
        fp.write('data,hora,taxa\n')

# Captura de dados e gravação no CSV
for _ in range(10):
    data_e_hora = datetime.now()
    data = data_e_hora.strftime('%Y/%m/%d')
    hora = data_e_hora.strftime('%H:%M:%S')
    cdi = float(dado) + (random() - 0.5) if dado else None
    
    with open('./taxa-cdi-analise.csv', 'a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{cdi}\n')
    
    time.sleep(1)

print("Sucesso na captura dos dados!")

# Gerando o gráfico
print("Gerando gráfico...")
df = pd.read_csv('./taxa-cdi-analise.csv')
grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
grafico.set_xticklabels(labels=df['hora'], rotation=90)
plt.savefig("visualizacao-analise.png")
print("Gráfico salvo como visualizacao-analise.png")
