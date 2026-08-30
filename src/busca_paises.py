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
import matplotlib.pyplot as plt

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

def gerar_grafico(resultados, caminho_saida="comparacao_busca.png"):
    tamanhos = resultados["tamanhos"]

    plt.figure(figsize=(9, 6))
    plt.plot(tamanhos, [t * 1e6 for t in resultados["seq_pior_caso"]],
              marker="o", label="Busca Sequencial (pior caso)")
    plt.plot(tamanhos, [t * 1e6 for t in resultados["bin_pior_caso"]],
              marker="o", label="Busca Binária (pior caso)")
    plt.plot(tamanhos, [t * 1e6 for t in resultados["seq_medio_caso"]],
              marker="s", linestyle="--", label="Busca Sequencial (caso médio)")
    plt.plot(tamanhos, [t * 1e6 for t in resultados["bin_medio_caso"]],
              marker="s", linestyle="--", label="Busca Binária (caso médio)")

    plt.xlabel("Tamanho da entrada (nº de países)")
    plt.ylabel("Tempo médio de execução (microssegundos)")
    plt.title("Busca Sequencial x Busca Binária\nDados reais: países (mledoze/countries)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=150)
    print(f"\nGráfico salvo em: {caminho_saida}")


def opcao_buscar_pais(nomes, info):
    """Deixa o usuário buscar um país por nome, escolhendo qual
    algoritmo usar, e mostra os detalhes do país encontrado."""
    nome_buscado = input("\nDigite o nome do país (em inglês, ex: Brazil): ").strip()

    print("\nQual algoritmo você quer usar?")
    print("  1 - Busca Sequencial (O(n))")
    print("  2 - Busca Binária (O(log n))")
    escolha = input("Escolha (1 ou 2): ").strip()

    inicio = time.perf_counter()
    if escolha == "2":
        vetor_ordenado = sorted(nomes)
        posicao = busca_binaria(vetor_ordenado, nome_buscado)
        algoritmo_usado = "Busca Binária"
    else:
        posicao = busca_sequencial(nomes, nome_buscado)
        algoritmo_usado = "Busca Sequencial"
    fim = time.perf_counter()

    tempo_gasto_us = (fim - inicio) * 1e6

    if posicao == -1:
        print(f"\n País '{nome_buscado}' não encontrado.")
        print(f"   ({algoritmo_usado} — tempo: {tempo_gasto_us:.2f} µs)")
        return

    detalhes = info.get(nome_buscado, {})
    print(f"\n País encontrado! ({algoritmo_usado} — tempo: {tempo_gasto_us:.2f} µs)")
    print(f"   Nome:      {nome_buscado}")
    print(f"   Capital:   {detalhes.get('capital', '?')}")
    print(f"   Região:    {detalhes.get('regiao', '?')}")
    print(f"   Sub-região:{detalhes.get('subregiao', '?')}")
    area = detalhes.get("area")
    if area:
        print(f"   Área:      {area:,.0f} km²")










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