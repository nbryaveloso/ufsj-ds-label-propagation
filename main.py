import numpy as np
import networkx as nx
import csv
import matplotlib.pyplot as plt

def carregar_grafo(caminho_arquivo):
    # Funcao para ler o csv
    G = nx.Graph()

    with open(caminho_arquivo, 'r') as f:
        leitor = csv.reader(f)
        next(leitor) # Pula o cabeçalho 'origem, destino'
        
        for linha in leitor:
            origem, destino = int(linha[0]), int(linha[1])
            G.add_edge(origem, destino) 
            
    nos_ordenados = sorted(G.nodes()) 
    A = nx.to_numpy_array(G, nodelist=nos_ordenados, dtype=int) 
    
    return G, A, nos_ordenados

def calcular_moda(rotulos_vizinhos): 
    # Funcao que conta qual rotulo aparece mais e resolve empates com cara ou coroa.
    valores_unicos, contagens = np.unique(rotulos_vizinhos, return_counts=True)
    max_contagem = np.max(contagens)
    
    rotulos_frequentes = valores_unicos[contagens == max_contagem]
    return np.random.choice(rotulos_frequentes)

def propagar_rotulos(A, N, max_iteracoes=100):
    # Funcao que executa o laco principal ate as comunidades se formarem.
    rotulos = np.arange(N) 
    iteracao = 0
    mudou = True
    
    while iteracao < max_iteracoes and mudou:
        mudou = False
        ordem_vertices = np.random.permutation(N) 
        
        for i in ordem_vertices:
            vizinhos = np.where(A[i] == 1)[0] 
            
            if len(vizinhos) > 0:
                rotulos_vizinhos = rotulos[vizinhos]
                novo_rotulo = calcular_moda(rotulos_vizinhos)
                
                if novo_rotulo != rotulos[i]:
                    rotulos[i] = novo_rotulo
                    mudou = True 
                    
        iteracao += 1
        
    return rotulos, iteracao

def plotar_comunidades(G, rotulos_finais, caminho):
    # Funcao que gera e exibe o grafico colorido das comunidades.
    print("\nGráfico gerado. Feche-o para encerrar.")
    
    plt.figure(figsize=(8, 6))
    
    nome_arquivo = caminho.split('/')[-1] # Extrai apenas o nome do arquivo.
    plt.title(f"Label Propagation - {nome_arquivo}")
    
    # Plota o grafo usando os rotulos para definir as cores.
    nx.draw(
        G, 
        with_labels=True, 
        node_color=rotulos_finais, 
        cmap=plt.cm.Set2,
        node_size=800,
        font_color="black",
        font_weight="bold"
    )
    plt.show()

if __name__ == "__main__":
    caminho = 'data/rede1_duas_comunidades.csv'
    print(f"Processando: {caminho}")
    
    G, A, lista_nos = carregar_grafo(caminho)
    N = len(lista_nos)
    
    print("\nMatriz de Adjacência (A):")
    print(A)
    
    rotulos_finais, total_iteracoes = propagar_rotulos(A, N)
    
    print(f"\nConvergência alcançada em {total_iteracoes} iterações.")
    print("Rótulos Finais (Comunidades):", rotulos_finais)

    # Chama a funcao de visualizacao
    plotar_comunidades(G, rotulos_finais, caminho)