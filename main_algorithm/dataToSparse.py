from collections import defaultdict

def formSparseMatrices(tri, MyNumber=float):
    nodes = []
    edges = defaultdict(list)
    
    in_degree = defaultdict(int)
    has_outgoing = defaultdict(bool)

    for l in range(len(tri['point1'])): #O(n), n = len(tri)
        i = tri['point1'][l]
        j = tri['point2'][l]
        k = tri['point3'][l]
        w = tri['weight'][l]

        if (i, j) not in nodes:
            nodes.append((i, j))
        if (j, k) not in nodes:
            nodes.append((j, k))
        
        idx_start = next(d for d, node in enumerate(nodes) if node == (i, j))
        idx_end = next(d for d, node in enumerate(nodes) if node == (j, k))
        edges[idx_start].append((idx_end, w))

        in_degree[idx_end] += 1
        has_outgoing[idx_start] = True
    #now i just plan to access my dictionary one by one and fill the components for my sparse matrix...
    #the indices in nodes and dictionary are aligned id say!
    v = []
    col_ind = []
    row_ind = [0]
    nnz = 0

    for idx_start in range(len(nodes)): #forst case - complete graph: O(n^2), e.i. n*(n-1)
        if idx_start in edges:
            idx_ends = edges[idx_start]
            for idx_end, w in idx_ends:
                v.append(MyNumber(w))
                col_ind.append(idx_end)
                nnz += 1
        row_ind.append(nnz)
    
    sparse = {'v': v,
                  'col_ind': col_ind,
                  'row_ind': row_ind, 
                  'shape': (len(nodes), len(nodes))}

    roots_idx = [] #i dont even need roots anymore but lets leave them for now...
    for idx in range(len(nodes)):
        if in_degree[idx] == 0 and has_outgoing[idx]:
            roots_idx.append(idx)

    return sparse, nodes, roots_idx

def formSparseMatrices1(tri, MyNumber=float):
    nodes = []
    edges = defaultdict(list)
    
    in_degree = defaultdict(int)
    has_outgoing = defaultdict(bool)

    for l in range(len(tri['point1'])):
        i = tri['point1'][l]
        j = tri['point2'][l]
        k = tri['point3'][l]
        w = tri['weight'][l]

        if (i, j) not in nodes:
            nodes.append((i, j))
        if (j, k) not in nodes:
            nodes.append((j, k))
        
        idx_start = next(d for d, node in enumerate(nodes) if node == (i, j))
        idx_end = next(d for d, node in enumerate(nodes) if node == (j, k))
        edges[idx_start].append((idx_end, w))

        in_degree[idx_start] += 1 #idx_end
        has_outgoing[idx_start] = True
    #now i just plan to access my dictionary one by one and fill the components for my sparse matrix...
    #the indices in nodes and dictionary are aligned id say!
    v = []
    col_ind = []
    row_ind = [0]
    nnz = 0

    for idx_start in range(len(edges)): #range(len(nodes)) == nodes
        idx_ends = edges[idx_start]
        for idx_end, w in idx_ends:
            v.append(MyNumber(w))
            col_ind.append(idx_end)
            nnz += 1
        row_ind.append(nnz)
    
    sparse = {'v': v,
                  'col_ind': col_ind,
                  'row_ind': row_ind, 
                  'shape': (len(nodes), len(nodes))}

    roots_idx = [] #i dont even need roots anymore but lets leave them for now...
    for idx in range(len(nodes)):
        if in_degree[idx] == 0 and has_outgoing[idx]:
            roots_idx.append(idx)

    return sparse, nodes, roots_idx