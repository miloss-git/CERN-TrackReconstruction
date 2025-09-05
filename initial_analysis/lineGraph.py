from sparse_matrix import sparseToAdj as sta
from make_plots import graphPlot as gl

def lineGraph(M, zero = 0): #this works for simple unweighted graphs
    n = M['shape'][0]
    A = sta.toAdj(M, zero)
    edges = []
    labels = {}
    k = 0

    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != zero:
                edges.append((i, j))
                labels[k] = f"$A_{{{i}}}A_{{{j}}}$"
                k += 1
    
    A_res = [[zero for _ in range(k)] for _ in range(k)]

    for i in range(k):
        u1, v1 = edges[i]
        for j in range(i + 1, k):
            u2, v2 = edges[j]
            if len({u1, v1} & {u2, v2}) > 0:
                A_res[i][j] = A[u1][v1] * A[u2][v2]
                A_res[j][i] = A[u1][v1] * A[u2][v2]
    
    return sta.toSparse(A_res), labels

def lineGraphDirected(M, zero = 0):
    n = M['shape'][0]
    A = sta.toAdj(M, zero)
    edges = []

    for i in range(n):
        for j in range(n):
            if A[i][j] != zero:
                edges.append((i, j))
    
    k = len(edges)
    A_res = [[zero for _ in range(k)] for _ in range(k)]

    for i in range(k):
        u1, v1 = edges[i]
        for j in range(k):
            if i == j: continue

            u2, v2 = edges[j]
            if v1 == u2:
                A_res[i][j] = A[u1][v1] * A[u2][v2]
    
    return sta.toSparse(A_res)

M = {
    'v': [1, 1, 1, 1],
    'col_ind': [1, 2, 0, 0],
    'row_ind': [0, 2, 3, 4],
    'shape': (3, 3)
}

M1 = {
    'v': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'col_ind': [1, 2, 3, 0, 0, 0, 5, 7, 4, 6, 5, 7, 4, 6],
    'row_ind': [0, 3, 4, 5, 6, 8, 10, 12, 14],
    'shape': (8, 8)
}

if __name__ == "__main__":
    G, labels = lineGraph(M1)
    gl.drawGraphN(sta.toAdj(M1), directed=False)
    gl.drawGraphN(sta.toAdj(G), directed=False, labels = labels)
   
   