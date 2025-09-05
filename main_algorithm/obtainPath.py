from sparse_matrix import sparseMatrix as sm

from semi_rings.maxPlus import MyNumber as MyNumber
from semi_rings.maxPlus import zero as zero_max

def biggestPathInfo(sparse_max, zero=0): #i could optimize this max_iter somehow... we will see
    A_k = sparse_max
    A_start = sparse_max
    n = sparse_max['shape'][0]
    
    best_weight = zero
    best_info = None #(i, j, k) i and j indices of start and end node, and k # of edges in i-j path
    predecessors = [] #[[preds_1], [preds_2], ...]; predecessors[k] = preds_k; preds_k[(i, j)] = node through which the best path from i to j passes

    for k in range(1, n):
        v = A_k['v']
        row_ind = A_k['row_ind']
        col_ind = A_k['col_ind']

        for idx, w in enumerate(v):
            if w > best_weight:
                i = next(r for r in range(len(row_ind) - 1) if row_ind[r] <= idx < row_ind[r + 1]) #index of a row
                j = col_ind[idx]
                best_weight = w
                best_info = (i, j, k)
        A_k, preds_k = sm.multiplicationWithPred(A_k, A_start, zero=zero_max)
        predecessors.append(preds_k)

        if A_k['v'] == []:
            break
    
    return best_info, best_weight, predecessors

def findPath(predecessors, i, j, k): #outputs the list of indices of nodes along the biggestPath
    path_indices = [j]
    for step in reversed(range(k - 1)): #! predecessors[k] corresponds to A^(k+2)
        key = (i, j)
        j = predecessors[step][key] #j must be updated at each step loggg
        path_indices.append(j)
    path_indices.append(i)
    path_indices.reverse()
    return path_indices