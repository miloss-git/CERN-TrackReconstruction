import make_plots.illustrateData as ild
import networkx as nx
from sparse_matrix import sparseMatrix as sm
import math
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from semi_rings.maxPlus import MyNumber as MyNumber
from semi_rings.maxPlus import zero as zero

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DATA_DIR = PROJECT_ROOT / "data"

SPS_PATH = DATA_DIR / "quad_mu_1GeV_sps.csv"
TRI_PATH = DATA_DIR / "quad_mu_1GeV_tri.csv" 

sps = pd.read_csv(SPS_PATH)
tri = pd.read_csv(TRI_PATH)

def plotBiggestPaths(tri, sps, zero=zero):
    paths = extractPaths(tri=tri, sps=sps, zero=zero)
    merged_paths = nx.DiGraph()

    for path in paths:
        merged_paths.add_edges_from(path.edges(data=True))

    positions = getrzPositions(merged_paths, sps)
    #positions = nx.spring_layout(merged_paths)
    nx.draw(merged_paths, pos=positions, with_labels=False, node_color='skyblue', edge_color='gray', node_size=40, arrows=True)
    edge_labels = nx.get_edge_attributes(merged_paths, 'weight')
    nx.draw_networkx_edge_labels(merged_paths, pos=positions, edge_labels=edge_labels, label_pos=0.5, font_size=6, font_color='red')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

#data tri to adjacency
def graphToSparseAdj(G, zero = 0):
    #G = ild.illustrateTriData(tri, sps)[0] if i wanted from tri to sparse
    n = nx.number_of_nodes(G)
    nodes = list(G.nodes())
    node_to_index = {node: i for i, node in enumerate(nodes)} #dictionary

    v = []
    col_ind = []
    row_ind = [0]

    for i in range(n):
        u = nodes[i]
        successors = sorted(G.successors(u), key=lambda node: node_to_index[node])

        for v_node in successors:
            if G.has_edge(u, v_node):
                j = node_to_index[v_node]
                weight = G[u][v_node].get('weight', zero)
                v.append(MyNumber(weight))
                col_ind.append(j)
        row_ind.append(len(v))
    
    return {
        'v': v,
        'col_ind': col_ind,
        'row_ind': row_ind,
        'shape': (n, n)
    }

def extractRoots(G):
    roots = []

    for u in G.nodes():
        if (len(list(G.predecessors(u))) == 0 and len(list(G.successors(u))) > 0):
            roots.append(u)

    return roots

def extractSubgraph(G, root):
    H = nx.DiGraph()
    weights = nx.get_edge_attributes(G, 'weight')
    
    H.add_node(root)
    H = fillSubgraph(G, H, root, weights)
    
    return H

def fillSubgraph(G, H, root, weights): #there are no "true cycles" in the graph representation of the data
    if len(list(G.successors(root))) == 0:
        return H
    
    for u in G.successors(root):
        edge = (root, u)
        weight = weights[edge]
        H.add_edge(root, u, weight=weight)
        fillSubgraph(G, H, u, weights)
    
    return H

def extractPaths(tri, sps, zero=0):
    G = ild.illustrateTriData(tri, sps)[0]
    roots = extractRoots(G)
    subgraphs = []

    for root in roots:
        H = extractSubgraph(G, root)
        subgraphs.append(H)
    
    #weights = nx.get_edge_attributes(G, 'weight')
    paths = []
    for H, root in zip(subgraphs, roots):
        best_info, best_weight, predecessors = biggestPathInfo(H, zero=zero)
        path_indices = findPath(predecessors, best_info[0], best_info[1], best_info[2])
        path = reconstructPath(H, path_indices)
        paths.append(path)
    print(len(paths))
    return paths

def biggestPathInfo(H, zero=0, max_iter=100): #in general, max_iter = number of nodes
    A = graphToSparseAdj(H, zero=zero)
    A_k = A
    A_start = A
    best_weight = zero
    best_info = None #(i, j, k); i and j are indices of start and end node, and k is number of edges in i-j path
    predecessors = []

    for k in range(1, max_iter + 1):
        v = A_k['v']
        row_ind = A_k['row_ind']
        col_ind = A_k['col_ind']

        for idx, w in enumerate(v):
            if w > best_weight:
                i = next(r for r in range(len(row_ind) - 1) if row_ind[r] <= idx < row_ind[r + 1])
                j = col_ind[idx]
                best_weight = w
                best_info = (i, j, k)
        A_k, preds_k = sm.multiplicationWithPred(A_k, A_start, zero=zero)
        predecessors.append(preds_k)

        if A_k['v'] == []:
            break
    
    return best_info, best_weight, predecessors

def findPath(predecessors, i, j, k):
    path_indices = [j]
    for step in reversed(range(k - 1)): #! predecessors[k] corresponds to A^(k+2)
        key = (i, j)
        j = predecessors[step][key]
        path_indices.append(j)
    path_indices.append(i)
    path_indices.reverse()
    return path_indices

def reconstructPath(H, path_indices): #outputs graph
    nodes = list(H.nodes())
    path = nx.DiGraph()
    for i in range(len(path_indices) - 1):
        u = nodes[path_indices[i]]
        v = nodes[path_indices[i + 1]]
        w = nx.get_edge_attributes(H, 'weight').get((u, v))
        path.add_edge(u, v, weight=w)

    return path

def getrzPositions(G, sps):
    x = sps['x']
    y = sps['y']
    z = sps['z'] 

    positions = {}
    for node in G.nodes():
        i, j = node
        z_avg = (z[i] + z[j]) / 2
        r_i = math.sqrt(x[i] ** 2 + y[i] ** 2)
        r_j = math.sqrt(x[j] ** 2 + y[j] ** 2)
        r_avg = (r_i + r_j) / 2
        positions[node] = (z_avg, r_avg)

    return positions

def plotPathsAsDublets(tri, sps, zero=zero):
    paths = extractPaths(tri=tri, sps=sps, zero=zero)
    merged_paths = nx.DiGraph()

    for path in paths:
        merged_paths.add_edges_from(path.edges(data=True))
    
    dub_graph = nx.DiGraph()
    positions = {}
    for (i, j) in merged_paths.nodes():
        dub_graph.add_edge(i, j)

    x = sps['x']
    y = sps['y']
    z = sps['z']
    for i in dub_graph.nodes():
        positions[i] = (z[i], math.sqrt(x[i] ** 2 + y[i] ** 2))
    nx.draw(dub_graph, pos=positions, with_labels=False, node_color='skyblue', edge_color='gray', node_size=40, arrows=True)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__ main__":
    plotBiggestPaths(tri, sps)
    plotPathsAsDublets(tri, sps, zero=zero)