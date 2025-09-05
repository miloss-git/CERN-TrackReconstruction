from semi_rings.booleanSemiring import MyBool as MyBool
from semi_rings.booleanSemiring import zero as zero_bool

from sparse_matrix import sparseMatrix as sm #i should implement sparse matrix as a class with all the methods, constructor, ==, SM[i][j]...
#this gives me out-components, not weakly connected components as i expected, but lets say i can leave it for now and see what happens
def findWeakComponents(tri, sparse_bool, nodes, roots_idx): #SM - sparse matrix for my data
    sparse_bool_symm = symmetrize(sparse_bool)
    R = sparse_bool_symm
    sparse_start = sparse_bool_symm

    n = sparse_bool['shape'][0] #these are sparse for adjacency matrices => always square
                        #in that sense, i could even omit the 'shape' attribute from the object
    for k in range(n):
        sparse_bool_symm = sm.multiplication(sparse_bool_symm, sparse_start, zero=zero_bool)
        R_new = sm.addition(R, sparse_bool_symm, zero=zero_bool)
        if sparseEqual(R, R_new):
            break
        R = R_new
    
    #fast access row - faster than getSMij...
    reach = [set() for _ in range(n)] #reach[i] is a conn. component that includes i
    for i in range(n):
        row_start = R['row_ind'][i]
        row_end = R['row_ind'][i + 1]
        for idx in range(row_start, row_end):
            reach[i].add(R['col_ind'][idx])

    node_to_index = {node: idx for idx, node in enumerate(nodes)}
    visited = [False for _ in range(len(nodes))] #early exit, many roots will now be in the same WCC

    tri_components = []
    for r in roots_idx: #iterating over roots of DAG is sufficient to visit every WCC
        if visited[r]:
            continue

        reachable_nodes = reach[r]
        selected_rows = []
        
        for idx, i, j, k, w in tri[['point1', 'point2', 'point3', 'weight']].itertuples(index=True):
            node1 = (i, j)
            node2 = (j, k)
            idx1 = node_to_index.get(node1)
            idx2 = node_to_index.get(node2)
            if idx1 in reachable_nodes and idx2 in reachable_nodes:
                selected_rows.append(idx)
                
        #visited[r] = True
        for j in reachable_nodes:
            visited[j] = True

        tri_subset = tri.iloc[selected_rows].reset_index(drop=True)
        tri_components.append(tri_subset)

    return tri_components

def sparseEqual(SM1, SM2):
    v1 = SM1['v']
    col_ind1 = SM1['col_ind']
    row_ind1 = SM1['row_ind']
    shape1 = SM1['shape']

    v2 = SM2['v']
    col_ind2 = SM2['col_ind']
    row_ind2 = SM2['row_ind']
    shape2 = SM2['shape']

    if(v1 == v2 and col_ind1 == col_ind2 and 
       row_ind1 == row_ind2 and shape1 == shape2):
        return True
    else:
        return False

def symmetrize(M):
    M_t = sm.transpose(M)
    return sm.addition(M, M_t, zero=zero_bool)
