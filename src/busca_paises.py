"""
Trabalho de Estruturas de Dados 2 - Algoritmos de Busca
Consultor de Países — app que usa busca sequencial e binária como
motor de busca sobre dados reais de países.
"""
import json
import os
import random
import time
import statistics
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

def busca_binaria(vetor_ordenado, chave):
    """Busca em vetor ordenado, dividindo o espaço de busca ao meio a
    cada tentativa. Complexidade: O(log n)."""
    inicio, fim = 0, len(vetor_ordenado) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if vetor_ordenado[meio] == chave:
            return meio
        elif vetor_ordenado[meio] < chave:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1

def medir_tempo(func, vetor, chave, repeticoes=200):
    """Executa a função de busca várias vezes e retorna o tempo médio."""
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        func(vetor, chave)
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    return statistics.mean(tempos)

def rodar_experimento(nomes):
    """Compara busca sequencial e binária em vários tamanhos de entrada."""
    tamanhos = [10, 25, 50, 100, 150, 200, len(nomes)]
    tamanhos = sorted(set(t for t in tamanhos if t <= len(nomes)))

    resultados = {
        "tamanhos": [], "seq_pior_caso": [], "bin_pior_caso": [],
        "seq_medio_caso": [], "bin_medio_caso": [],
    }

    for n in tamanhos:
        subconjunto = nomes[:n]
        vetor_ordenado = sorted(subconjunto)
        chave_inexistente = "___PAIS_INEXISTENTE___"
        chave_aleatoria = random.choice(subconjunto)

        t_seq_pior = medir_tempo(busca_sequencial, subconjunto, chave_inexistente)
        t_bin_pior = medir_tempo(busca_binaria, vetor_ordenado, chave_inexistente)
        t_seq_medio = medir_tempo(busca_sequencial, subconjunto, chave_aleatoria)
        t_bin_medio = medir_tempo(busca_binaria, vetor_ordenado, chave_aleatoria)

        resultados["tamanhos"].append(n)
        resultados["seq_pior_caso"].append(t_seq_pior)
        resultados["bin_pior_caso"].append(t_bin_pior)
        resultados["seq_medio_caso"].append(t_seq_medio)
        resultados["bin_medio_caso"].append(t_bin_medio)

        print(
            f"n={n:4d} | Seq(pior)={t_seq_pior*1e6:8.2f} µs | "
            f"Bin(pior)={t_bin_pior*1e6:8.2f} µs | "
            f"Seq(médio)={t_seq_medio*1e6:8.2f} µs | "
            f"Bin(médio)={t_bin_medio*1e6:8.2f} µs"
        )

    return resultados


if __name__ == "__main__":
    nomes, info = carregar_dados()
    print(nomes[:5])
    print(info[nomes[0]])

    vetor_teste = ["Brasil", "Argentina", "Chile", "Uruguai"]
    print(busca_sequencial(vetor_teste, "Chile"))   # esperado: 2
    print(busca_sequencial(vetor_teste, "XPTO"))    # esperado: -1

    vetor_teste = sorted(["Brasil", "Argentina", "Chile", "Uruguai"])
    print(busca_binaria(vetor_teste, "Chile"))
    print(busca_binaria(vetor_teste, "XPTO"))