"""
Trabalho de Estruturas de Dados 2 - Algoritmos de Busca
Consultor de Países — app que usa busca sequencial e binária como
motor de busca sobre dados reais de países.
"""

import requests

API_URL = "https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.json"


def carregar_dados():
    """Busca a lista de países e monta duas estruturas:
    - nomes: lista de nomes (usada pelos algoritmos de busca)
    - info: dicionário com detalhes de cada país (capital, região, área)
    """
    print("Buscando dados de países no GitHub (mledoze/countries)...")
    resposta = requests.get(API_URL, timeout=15)
    resposta.raise_for_status()
    dados_brutos = resposta.json()

    nomes = []
    info = {}
    for pais in dados_brutos:
        nome = pais.get("name", {}).get("common")
        if not nome:
            continue
        nomes.append(nome)
        capitais = pais.get("capital") or ["(sem capital registrada)"]
        info[nome] = {
            "capital": capitais[0],
            "regiao": pais.get("region", "(desconhecida)"),
            "subregiao": pais.get("subregion", "(desconhecida)"),
            "area": pais.get("area"),
        }

    print(f"{len(nomes)} países obtidos.")
    return nomes, info


if __name__ == "__main__":
    nomes, info = carregar_dados()
    print(nomes[:5])
    print(info[nomes[0]])