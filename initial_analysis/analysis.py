import initial_analysis.biggestPaths as bp
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
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

def checkTriProperty(tri, sps, zero=zero):
    paths = bp.extractPaths(tri, sps, zero=zero)
    merged_paths = nx.DiGraph()
    induced_tri = []

    for path in paths:
        merged_paths.add_edges_from(path.edges(data=True))
    
    for (u, v) in merged_paths.edges():
        (i1, j1) = u
        (i2, j2) = v
        if j1 != i2: 
            return False, []
        
        w = merged_paths[u][v].get('weight', 1)
        induced_tri.append([i1, j1, j2, w])
    induced_tri_df = pd.DataFrame(induced_tri, columns=['point1', 'point2', 'point3', 'weight'])
    print("now comes the graph")
    return True, induced_tri_df

#inverting out-tree gives an in-tree and vice versa so...
def isTree(tri, sps, zero=zero):
    paths = bp.extractPaths(tri, sps, zero=zero)
    merged_paths = nx.DiGraph()

    for path in paths:
        merged_paths.add_edges_from(path.edges(data=True))
    
    roots = bp.extractRoots(merged_paths)
    if graphIsTree(merged_paths, roots):
        return True, "out-tree"
    
    merged_paths_reversed = merged_paths.reverse()
    roots_reversed = bp.extractRoots(merged_paths_reversed)
    if graphIsTree(merged_paths_reversed, roots_reversed):
        return True, "in-tree"
    
    return False, None

#this logic is appropriate for out-trees
def graphIsTree(G, nodes):
    if len(nodes) == 0:
        return True
    
    if all(isRoot(G, node) for node in nodes):
        all_nodes = [v for node in nodes for v in G.successors(node)]
        new_nodes = list(set(all_nodes)) #removing potential duplicates
        
        H = G.copy()
        H.remove_nodes_from(nodes)
        return graphIsTree(H, new_nodes)
    
    else: return False

def isRoot(G, node):
    return len(list(G.predecessors(node))) == 0

def illustrateReversedPaths(tri, sps, zero=zero):
    paths = bp.extractPaths(tri, sps, zero=zero)
    merged_paths = nx.DiGraph()

    for path in paths:
        merged_paths.add_edges_from(path.edges(data=True))
    merged_paths_reversed = merged_paths.reverse()
    #positions = bp.getrzPositions(merged_paths_reversed, sps)
    positions = nx.spring_layout(merged_paths)
    nx.draw(merged_paths_reversed, pos=positions, with_labels=False, node_color='skyblue', edge_color='gray', node_size=40, arrows=True)
    edge_labels = nx.get_edge_attributes(merged_paths_reversed, 'weight')
    nx.draw_networkx_edge_labels(merged_paths_reversed, pos=positions, edge_labels=edge_labels, label_pos=0.5, font_size=6, font_color='red')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def reverseData(tri):
    reversed_tri = []
    for i, j, k, w in zip(tri['point1'], tri['point2'], tri['point3'], tri['weight']):
        reversed_tri.append([k, j, i, w])
    reversed_tri_df = pd.DataFrame(reversed_tri, columns=['point1', 'point2', 'point3', 'weight'])
    
    return reversed_tri_df

def getSinglePaths(tri, sps, zero=zero):
    paths = bp.extractPaths(tri, sps, zero=zero)
    merged_paths = nx.DiGraph()

    for path in paths:
        merged_paths.add_edges_from(path.edges(data=True))
    
    ok, induced_tri = checkTriProperty(tri, sps, zero=zero) #induced_tri is the subset of tri that induces the merged_paths
    if not ok:
        print("Tri property failed!")
        return
    
    induced_tri_reversed = reverseData(induced_tri)
    paths_reversed = bp.extractPaths(induced_tri_reversed, sps, zero=zero)
    
    merged_single_paths = nx.DiGraph()
    for path_reversed in paths_reversed:
        path_normal = path_reversed.reverse(copy=True)
        merged_single_paths.add_edges_from(path_normal.edges(data=True))
    
    positions = bp.getrzPositions(merged_single_paths, sps)
    nx.draw(merged_single_paths, pos=positions, with_labels=False, node_color='skyblue', edge_color='gray', node_size=40, arrows=True)
    edge_labels = nx.get_edge_attributes(merged_single_paths, 'weight')
    nx.draw_networkx_edge_labels(merged_single_paths, pos=positions, edge_labels=edge_labels, label_pos=0.5, font_size=6, font_color='red')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print(checkTriProperty(tri, sps, zero=zero)[0])
    print(isTree(tri, sps, zero=zero))
    illustrateReversedPaths(tri, sps, zero=zero)
    getSinglePaths(tri, sps, zero=zero)
