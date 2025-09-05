import networkx as nx
import matplotlib.pyplot as plt


def fillGraph(adjMatrix, directed):
    G = nx.DiGraph() if directed else nx.Graph()
    n = len(adjMatrix)
    m = len(adjMatrix[0])
    if(m != n):
        print("Invalid adj matrix")
        return
    for i in range(n):
        for j in range(m):
            if(adjMatrix[i][j] < 0):
                print("invalid adj matrix")
                return
            if(not directed and i > j):
                continue
            if(adjMatrix[i][j] > 0):
                for k in range(int(adjMatrix[i][j])):
                    G.add_edge(i, j)
    return G

def drawGraphN(adjMatrix, directed = True, labels = {}): #weights \in N...
    G = nx.MultiDiGraph() if directed else nx.MultiGraph()
    n = len(adjMatrix)
    m = len(adjMatrix[0])
    if(m != n):
        print("Invalid adj matrix; not a square matrix")
        return
    for i in range(n):
        for j in range(m):
            if(adjMatrix[i][j] < 0 and adjMatrix[i][j] != float('-inf')): ###
                print("invalid adj matrix; entries < 0")
                return
            if(not directed and i > j):
                continue
            if(adjMatrix[i][j] > 0 and adjMatrix[i][j] != float('inf')):   ### zero == inf not to satisfy the expression
                for k in range(int(adjMatrix[i][j])):
                    G.add_edge(i, j)
    
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=800)
    
    if labels == {}:
        labels = {i: f"$A_{{{i}}}$" for i in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels)
    else: 
        nx.draw_networkx_labels(G, pos, labels=labels)

    drawn = set()
    for (u,v) in G.edges():
        key = (u,v)
        if key not in drawn:
            count = G.number_of_edges(u,v)
            if (directed == True and G.has_edge(v,u)):
                count_opp = G.number_of_edges(v,u)
                rads_uv, rads_vu = get_curvature_directed(count, count_opp)
                
                for rad in rads_uv:
                    nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], connectionstyle=f'arc3, rad={rad}',
                                           edge_color='gray', min_source_margin=15, min_target_margin=15)
                for rad in rads_vu:
                    nx.draw_networkx_edges(G, pos, edgelist=[(v,u)], connectionstyle=f'arc3, rad={rad}',
                                           edge_color='gray', min_source_margin=15, min_target_margin=15)
                
                drawn.add((u,v))
                drawn.add((v,u))
            else:
                rads = get_curvature(count)
                for rad in rads:
                    nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], connectionstyle=f'arc3, rad={rad}',
                                           edge_color='gray', min_source_margin=15, min_target_margin=15)
                    drawn.add(key)

    plt.axis('off')
    plt.show()
    
def get_curvature(count):
    rads = []
    for k in range(count):
        if count % 2 == 1 and k == 0:
            rads.append(0.0)
        else:
            idx = (k if count % 2 == 0 else k - 1)
            direction = (-1) ** (idx + 1)
            amount = (idx // 2 + 1) / 5
            rads.append(direction * amount)
    return rads

def get_curvature_directed(count, count_opp):
    rads = []
    for k in range(count):
        rads.append((k+1) * 0.2)
    for k in range(count_opp):
        rads.append((k+1) * 0.2)
    return rads[:count], rads[count:]

def drawWeightedGraph(adjMatrix, labels = {}):
    G = nx.DiGraph()
    n = len(adjMatrix)
    m = len(adjMatrix[0])
    if(m != n):
        print("Invalid adj matrix")
        return
    
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(m):
            if(adjMatrix[i][j] < 0 and adjMatrix[i][j] != float('-inf')):
                print("invalid adj matrix")
                return
            if(adjMatrix[i][j] > 0 and adjMatrix[i][j] != float('inf')):
                G.add_edge(i,j, weight = float(adjMatrix[i][j]))
    
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=800)
    
    if labels == {}:
        labels = {i: f"$A_{{{i+1}}}$" for i in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels)
    else:
        nx.draw_networkx_labels(G, pos, labels=labels)

    drawn = set()
    for (u,v) in G.edges():
        if (u,v) in drawn:
            continue
        if G.has_edge(v,u) and (v,u) not in drawn:
            nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], connectionstyle='arc3, rad=0.2', edge_color='gray', arrows=True,
                arrowstyle='-|>', min_source_margin=15, min_target_margin=15)
            label_uv = round(nx.get_edge_attributes(G, 'weight').get((u, v)), 5)
            if label_uv is not None:
                nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): label_uv}, label_pos=0.5, connectionstyle='arc3, rad=0.2', font_size=12, font_color='red')
            
            nx.draw_networkx_edges(G, pos, edgelist=[(v,u)], connectionstyle='arc3, rad=0.2', edge_color='gray', arrows=True,
                arrowstyle='-|>', min_source_margin=15, min_target_margin=15)
            label_vu = round(nx.get_edge_attributes(G, 'weight').get((v, u)), 5)
            if label_vu is not None:
                nx.draw_networkx_edge_labels(G, pos, label_pos=0.5, edge_labels={(v, u): label_vu}, connectionstyle='arc3, rad=0.2', font_size=12, font_color='red')
            drawn.add((u,v))
            drawn.add((v,u))
        else:
            nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color='gray', arrows=True,
                arrowstyle='-|>', min_source_margin=15, min_target_margin=15)
            label_uv = round(nx.get_edge_attributes(G, 'weight').get((u, v)), 5)
            if label_uv is not None:
                nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): label_uv}, label_pos=0.5, font_size=12, font_color='red')
            drawn.add((u,v))

    plt.axis('off')
    plt.tight_layout()
    plt.show()

def illustrateData(adjMatrix, positions = {}, labels = {}):
    G = nx.DiGraph()
    n = len(adjMatrix)
    m = len(adjMatrix[0])
    if(m != n):
        print("Invalid adj matrix")
        return
    
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(m):
            if(adjMatrix[i][j] < 0 and adjMatrix[i][j] != float('-inf')):
                print("invalid adj matrix")
                return
            if(adjMatrix[i][j] > 0 and adjMatrix[i][j] != float('inf')):
                G.add_edge(i,j, weight = float(adjMatrix[i][j]))
    
    if positions == {}:
        pos = nx.spring_layout(G)
    else:
        pos = positions
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=40)
    
    '''
    if labels == {}:
        labels = {i: f"$A_{{{i}}}$" for i in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels)
    else:
        nx.draw_networkx_labels(G, pos, labels=labels)
    '''

    drawn = set()
    for (u,v) in G.edges():
        if (u,v) in drawn:
            continue
        if G.has_edge(v,u) and (v,u) not in drawn:
            nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], connectionstyle='arc3, rad=0.2', edge_color='gray', arrows=True,
                arrowstyle='-|>')
            label_uv = nx.get_edge_attributes(G, 'weight').get((u, v))
            if label_uv is not None and label_uv != 1.0:
                nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): label_uv}, label_pos=0.5, connectionstyle='arc3, rad=0.2', font_size=12, font_color='red')
            
            nx.draw_networkx_edges(G, pos, edgelist=[(v,u)], connectionstyle='arc3, rad=0.2', edge_color='gray', arrows=True,
                arrowstyle='-|>')
            label_vu = nx.get_edge_attributes(G, 'weight').get((v, u))
            if label_vu is not None and label_vu != 1.0:
                nx.draw_networkx_edge_labels(G, pos, label_pos=0.5, edge_labels={(v, u): label_vu}, connectionstyle='arc3, rad=0.2', font_size=12, font_color='red')
            drawn.add((u,v))
            drawn.add((v,u))
        else:
            nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color='gray', arrows=True,
                arrowstyle='-|>')
            label_uv = nx.get_edge_attributes(G, 'weight').get((u, v))
            if label_uv is not None and label_uv != 1.0:
                nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): label_uv}, label_pos=0.5, font_size=12, font_color='red')
            drawn.add((u,v))

    plt.axis('off')
    plt.tight_layout()
    plt.show()

def plotGraph(G):
    #pos = nx.spring_layout(G, weight=None)
    pos = nx.shell_layout(G)

    nx.draw_networkx_nodes(G, pos=pos, node_color='skyblue', node_size=40)
    nx.draw_networkx_edges(G, pos=pos, edge_color='gray', arrows=True)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, label_pos=0.5, font_size=6, font_color='red')
    path_labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos=pos, labels=path_labels, font_size=8)
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

adj = [
    [0, 3, 0],
    [0, 0, 2],
    [1, 0, 0]
]

adj1 = [
    [0, 5.3, 0],
    [1.11, 0, 3.14],
    [2.44, 0, 0]
]

if __name__ == "__main__":
    drawGraphN(adj, directed=True)
    drawWeightedGraph(adj1)


#some concrete examples for the report

def drawExample():
    G = nx.DiGraph()
    G.add_nodes_from(range(8))

    edge_list2 = [(0, 1), (1, 4), (4, 5), (5, 6)]
    edge_list3 = [(1, 2), (1, 7), (4, 2), (2, 3)]

    G.add_edges_from(edge_list2 + edge_list3)

    pos = nx.spring_layout(G, seed=40)

    nx.draw_networkx_nodes(G, pos=pos, node_color='skyblue', node_size=400)

    labels = {i: rf"$X_{{{i+1}}}$" for i in G.nodes()}
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=10)

    common = dict(pos=pos, arrows=True, arrowstyle='-|>', 
                  )

    #nx.draw_networkx_edges(G, edgelist=edge_list1, edge_color='green', connectionstyle='arc3,rad=0.0', **common)
    nx.draw_networkx_edges(G, edgelist=edge_list2, edge_color='purple', connectionstyle='arc3,rad=0.0', **common)
    nx.draw_networkx_edges(G, edgelist=edge_list3, edge_color='gray', **common)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

def drawExample1():
    G = nx.DiGraph()
    G.add_nodes_from(range(8))

    edge_list1 = [(0, 1), (1, 4), (4, 2), (2, 3)]
    edge_list3 = [(1, 2), (1, 7), (4, 5), (5, 6)]

    G.add_edges_from(edge_list1 + edge_list3)

    pos = nx.spring_layout(G, seed=40)

    nx.draw_networkx_nodes(G, pos=pos, node_color='skyblue', node_size=400)

    labels = {i: rf"$X_{{{i+1}}}$" for i in G.nodes()}
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=10)

    common = dict(pos=pos, arrows=True, arrowstyle='-|>', 
                  )

    nx.draw_networkx_edges(G, edgelist=edge_list1, edge_color='green', connectionstyle='arc3,rad=0.0', **common)
    #nx.draw_networkx_edges(G, edgelist=edge_list2, edge_color='purple', connectionstyle='arc3,rad=0.0', **common)
    nx.draw_networkx_edges(G, edgelist=edge_list3, edge_color='gray', **common)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

def drawExample2():
    G = nx.DiGraph()
    G.add_nodes_from(range(3))

    edge_list1 = [(0, 1)]
    edge_list3 = [(0, 2)]

    G.add_edges_from(edge_list1 + edge_list3)

    pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos=pos, node_color='skyblue', node_size=400)

    labels = {i: rf"$X_{{{1+3*i}}}$" for i in G.nodes()}
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=10)

    common = dict(pos=pos, arrows=True, arrowstyle='-|>', 
                  )

    nx.draw_networkx_edges(G, edgelist=edge_list1, edge_color='green', connectionstyle='arc3,rad=0.0', **common)
    #nx.draw_networkx_edges(G, edgelist=edge_list2, edge_color='purple', connectionstyle='arc3,rad=0.0', **common)
    nx.draw_networkx_edges(G, edgelist=edge_list3, edge_color='purple', **common)

    plt.axis('off')
    plt.tight_layout()
    plt.show()
