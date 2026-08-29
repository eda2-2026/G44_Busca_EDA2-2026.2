"""
Trabalho de Estruturas de Dados 2 - Algoritmos de Busca
Consultor de Países — app que usa busca sequencial e binária como
motor de busca sobre dados reais de países.
"""
import json
import os
import requests

API_URL = "https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.json"
CACHE_FILE = "paises_cache.json"

def carregar_dados():
    if os.path.exists(CACHE_FILE):
        print(f"Carregando dados do cache local ({CACHE_FILE})...")
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            dados_salvos = json.load(f)
        return dados_salvos["nomes"], dados_salvos["info"]

    print("Buscando dados de países no GitHub (mledoze/countries)...")
    resposta = requests.get(API_URL, timeout=15)
    resposta.raise_for_status()
    dados_brutos = resposta.json()

    if not isinstance(dados_brutos, list):
        raise RuntimeError(
            "Os dados não vieram no formato esperado (lista de países). "
            f"Resposta recebida: {dados_brutos}"
        )

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

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"nomes": nomes, "info": info}, f, ensure_ascii=False, indent=2)

    print(f"{len(nomes)} países obtidos e salvos em cache.")
    return nomes, info

def busca_sequencial(vetor, chave):
    """Percorre o vetor posição por posição. Complexidade: O(n). """
    for i in range(len(vetor)):
        if vetor[i] == chave:
            return i
    return -1


if __name__ == "__main__":
    nomes, info = carregar_dados()
    print(nomes[:5])
    print(info[nomes[0]])