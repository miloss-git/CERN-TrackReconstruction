import pandas as pd
import make_plots.SPplot as plot
import make_plots.graphPlot as gl
import math
from sparse_matrix import sparseToAdj as sta
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DATA_DIR = PROJECT_ROOT / "data"

DUB_PATH = DATA_DIR / "quad_mu_1GeV_dub.csv"
SPS_PATH = DATA_DIR / "quad_mu_1GeV_sps.csv"
TRI_PATH = DATA_DIR / "quad_mu_1GeV_tri.csv" 

dub = pd.read_csv(DUB_PATH)
sps = pd.read_csv(SPS_PATH)
tri = pd.read_csv(TRI_PATH)

x = sps['x']
y = sps['y']
z = sps['z']

ind1 = dub['point1']
ind2 = dub['point2']
if __name__ == "__main__":
    plot.toTransversePlane(x, y, z, lines= [])
    plot.torzPlane(x, y, z, lines= [])
    plot.toTransversePlane(x, y, z, lines= zip(ind1, ind2))
    plot.torzPlane(x, y, z, lines= zip(ind1, ind2))


#lines would be my edges, n number of nodes
def adjMatrix(n, lines, zero = 0):
    A = [[zero for _ in range(n)] for _ in range(n)]
    for edge in lines:
        A[edge[0]][edge[1]] = 1
    
    return A
#! in xy plane manner
#positions = {i: (x[i], y[i]) for i in range(len(x))}

#! in rz plane manner
positions = {i: (z[i], math.sqrt((x[i] ** 2 + y[i] ** 2))) for i in range(len(x))}
A = adjMatrix(len(x), zip(ind1, ind2))

if __name__ == "__main__":
    gl.illustrateData(A, positions=positions) #illustrating doubles

def get_curvature(n, max_rad=0.4, spacing=0.05):
    rads = []
    level = 1
    while len(rads) < n:
        val = min(level * spacing, max_rad)
        rads.append(val)
        if len(rads) < n:
            rads.append(-val)
        level += 1
    return rads[:n]

def illustrateTriData(tri, sps, comp = False):
    G = nx.DiGraph()
    positions = {}

    x = sps['x']
    y = sps['y']
    z = sps['z']

    edge_to_tri_index = {}

    sgn = 1
    for l in range(len(tri['point1'])):
        i = tri['point1'][l]
        j = tri['point2'][l]
        k = tri['point3'][l]
        weight = tri['weight'][l]

        node1 = (i, j)
        node2 = (j, k)

        r1 = math.sqrt(x[i] ** 2 + y[i] ** 2)
        r2 = math.sqrt(x[j] ** 2 + y[j] ** 2)
        r3 = math.sqrt(x[k] ** 2 + y[k] ** 2)

        positions[node1] = ((z[i] + z[j] + sgn * l) / 2, (r1 + r2) / 2)
        positions[node2] = ((z[j] + z[k] + sgn * l) / 2, (r2 + r3) / 2)
        #sgn *= -1

        G.add_edge(node1, node2, weight = weight) 
        edge_to_tri_index[(node1, node2)] = l 
    
    pos = positions
    #pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=40)

    if comp:
        n = G.number_of_nodes()
        rads = get_curvature(n)
        for edge, rad in zip(G.edges(),rads):
            nx.draw_networkx_edges(G, pos, edgelist=[edge], connectionstyle=f'arc3,rad={rad}',
                                           edge_color='gray', arrows=True, arrowstyle='-|>')
            edge_labels = nx.get_edge_attributes(G, 'weight')
            label = edge_labels[edge]
            nx.draw_networkx_edge_labels(G, pos, edge_labels={edge: label}, label_pos=0.5, connectionstyle=f'arc3,rad={rad}', font_size=6, font_color='red')
    else:
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowstyle='-|>')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5, font_size=6, font_color='red')


    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    #handling components
    components = list(nx.connected_components(G.to_undirected()))
    if len(components) == 1:
        return tri
    
    components_tri = []
    for comp in components:
        tri_indices = set() #avoid duplicates
        for u in comp:
            for v in G.successors(u):
                edge = (u, v)
                if edge in edge_to_tri_index:
                    tri_indices.add(edge_to_tri_index[edge])
        components_tri.append(sorted(tri_indices))
    
    return G, components_tri

#formating data as tri DataFrame
def format_tri_subset(tri_df, indices):
    return tri_df.iloc[indices].reset_index(drop=True)

def illustrateTriDataComponents(tri, sps):
    G, components_tri = illustrateTriData(tri, sps)

    for comp_tri in components_tri:
        comp_tri_formated = format_tri_subset(tri, comp_tri)
        illustrateTriData(comp_tri_formated, sps, comp=True)

if __name__ == "__main__":
    illustrateTriDataComponents(tri, sps)
