import json
import math
import heapq 

def carregar_grafo():

    with open("grafo.json", 'r') as f:
        grafo = json.load(f)
        print("Arquivo 'grafo.json' carregado com sucesso!")
        return grafo


def heuristica(pos1, pos2):
    return math.dist(pos1, pos2)

def a_star(grafo, no_origem, no_destino):
    fila = [(0, no_origem)]
    
    anterior = {}
    custo_g = {}
    custo_f = {}
    
    for no in grafo:
        custo_g[no] = float('inf')
    custo_g[no_origem] = 0
    
    for no in grafo:
        custo_f[no] = float('inf')
    custo_f[no_origem] = heuristica(grafo[no_origem]['posicao'], grafo[no_destino]['posicao'])

    while fila:
        _, no_atual = heapq.heappop(fila)
        
        if no_atual == no_destino:
            caminho_total = []
            temp = no_atual
            while temp in anterior:
                caminho_total.append(temp)
                temp = anterior[temp]
            caminho_total.append(no_origem)
            
            return caminho_total[::-1], custo_g[no_destino]


        for aresta in grafo[no_atual]['arestas']:
            vizinho = aresta['no']
            custo_aresta = aresta['custo']
            
            custo_g_atual = custo_g[no_atual] + custo_aresta
            
            if custo_g_atual < custo_g[vizinho]:
                anterior[vizinho] = no_atual
                custo_g[vizinho] = custo_g_atual
                custo_f[vizinho] = custo_g_atual + heuristica(grafo[vizinho]['posicao'], grafo[no_destino]['posicao'])
                
                heapq.heappush(fila, (custo_f[vizinho], vizinho))
    return None, 0

def main():

    grafo = carregar_grafo()
    if not grafo:
        return

    nos_disponiveis = list(grafo.keys())
    print(f"\nNós disponíveis no grafo: {nos_disponiveis}")

    origem = input("Digite o nó de origem: ")
    destino = input("Digite o nó de destino: ")
    

    caminho, custo = a_star(grafo, origem, destino)
    

    print("\n--- Resultado ---")
    if caminho:
        print(f"O menor caminho de '{origem}' para '{destino}' é:")
        for no in caminho:
            print(f"{no} -> ", end="")
        print(f"Custo total do caminho: {custo:.2f}")
    else:
        print(f"Não foi possível encontrar um caminho de '{origem}' para '{destino}'.")

if __name__ == "__main__":
    main()