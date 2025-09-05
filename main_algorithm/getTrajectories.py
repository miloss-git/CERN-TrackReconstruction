import main_algorithm.dataToSparse as dts
import main_algorithm.findComponents as fc
import main_algorithm.obtainPath as op

import pandas as pd
import networkx as nx
import math
import matplotlib.pyplot as plt
import make_plots.illustrateData as ild
from pathlib import Path

from semi_rings.maxPlus import MyNumber as MyNumber
from semi_rings.maxPlus import zero as zero_max

from semi_rings.booleanSemiring import MyBool as MyBool
from semi_rings.booleanSemiring import zero as zero_bool

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DATA_DIR = PROJECT_ROOT / "data"

DUB_PATH = DATA_DIR / "quad_mu_1GeV_dub.csv"
SPS_PATH = DATA_DIR / "quad_mu_1GeV_sps.csv"
TRI_PATH = DATA_DIR / "quad_mu_1GeV_tri.csv" 

dub = pd.read_csv(DUB_PATH)
sps = pd.read_csv(SPS_PATH)
tri = pd.read_csv(TRI_PATH)

def getTrajectories(tri):
    sparse_bool, nodes, roots_idx = dts.formSparseMatrices(tri, MyNumber=MyBool)
    tri_components = fc.findWeakComponents(tri, sparse_bool, nodes, roots_idx)
    biggest_paths_indices = []
    local_nodes_all = []

    for tri_component in tri_components:
        sparse_max, local_nodes, _ = dts.formSparseMatrices(tri_component, MyNumber=MyNumber)
        (i, j, k), w, predecessors = op.biggestPathInfo(sparse_max, zero=zero_max)
        biggest_path = op.findPath(predecessors, i, j, k)
        
        biggest_paths_indices.append(biggest_path)
        local_nodes_all.append(local_nodes)

    return biggest_paths_indices, local_nodes_all

def plotTrajectories(tri, sps):
    biggest_paths_indices, local_nodes_all = getTrajectories(tri) #these are still just indices...
    merged_paths = nx.DiGraph()

    for path_indices, nodes in zip(biggest_paths_indices, local_nodes_all):
        path = [nodes[idx] for idx in path_indices]
        edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
        merged_paths.add_edges_from(edges)

    positions = getrzPositions(merged_paths, sps)
    #positions = nx.spring_layout(merged_paths)
    nx.draw(merged_paths, pos=positions, with_labels=False, node_color='skyblue', edge_color='gray', node_size=40, arrows=True)
    edge_labels = nx.get_edge_attributes(merged_paths, 'weight')
    nx.draw_networkx_edge_labels(merged_paths, pos=positions, edge_labels=edge_labels, label_pos=0.5, font_size=6, font_color='red')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def plotTrajectoriesAsDublets(tri, sps):
    biggest_paths_indices, local_nodes_all = getTrajectories(tri) #these are still just indices...
    merged_paths = nx.DiGraph()

    for path_indices, nodes in zip(biggest_paths_indices, local_nodes_all):
        path = [nodes[idx] for idx in path_indices]
        edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
        merged_paths.add_edges_from(edges)
    
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

def highlightPathsInDub(tri, sps, dub):

    dub_graph = nx.DiGraph()
    positions = {}
    x1 = dub['point1']
    x2 = dub['point2']
    
    for i, j in zip(x1, x2):
        dub_graph.add_edge(i, j)
    
    x = sps['x']
    y = sps['y']
    z = sps['z']
    
    for i in dub_graph.nodes():
        positions[i] = (z[i], math.sqrt(x[i] ** 2 + y[i] ** 2))
    nx.draw_networkx_nodes(dub_graph, pos=positions, node_color='skyblue', node_size=40)
    

    biggest_paths_indices, local_nodes_all = getTrajectories(tri) #these are still just indices...
    highlight_edges = set()
    for path_indices, local_nodes in zip(biggest_paths_indices, local_nodes_all):
        tuple_path = [local_nodes[idx] for idx in path_indices]
        for (u, v) in tuple_path:
            highlight_edges.add((u, v))
    
    edge_style = dict(
        pos=positions,
        arrows=True,
        arrowstyle='->', ##i added this on this plot so i should as well to other ones!!!
        min_source_margin = 0.0,
        min_target_margin = 0.0
    )
    all_edges = list(dub_graph.edges())

    nx.draw_networkx_edges(dub_graph, edgelist=all_edges, edge_color='lightgray', **edge_style)
    nx.draw_networkx_edges(dub_graph, edgelist=list(highlight_edges), edge_color='red', **edge_style)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def illustrateDub(sps, dub):

    dub_graph = nx.DiGraph()
    positions = {}
    x1 = dub['point1']
    x2 = dub['point2']
    
    for i, j in zip(x1, x2):
        dub_graph.add_edge(i, j)
    print(len(list(dub_graph.edges())))
    
    x = sps['x']
    y = sps['y']
    z = sps['z']
    
    for i in dub_graph.nodes():
        positions[i] = (z[i], math.sqrt(x[i] ** 2 + y[i] ** 2))
    nx.draw_networkx_nodes(dub_graph, pos=positions, node_color='skyblue', node_size=40)
    
    
    edge_style = dict(
        pos=positions,
        arrows=True,
        arrowstyle='->', ##i added this on this plot so i should as well to other ones!!!
        min_source_margin = 0.0,
        min_target_margin = 0.0
    )
    all_edges = list(dub_graph.edges())

    nx.draw_networkx_edges(dub_graph, edgelist=all_edges, edge_color='gray', **edge_style)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    #plotTrajectories(tri, sps)
    ###plotTrajectoriesAsDublets(tri, sps)

    highlightPathsInDub(tri, sps, dub)

    #illustrateDub(sps, dub)
