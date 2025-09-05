def toAdj(sparse, zero = 0):
    m, n = sparse['shape']
    A = [[zero for _ in range(n)] for _ in range(m)]
    
    v = sparse['v']
    col_ind = sparse['col_ind']
    row_ind = sparse['row_ind']

    for row in range(m):
        for i in range(row_ind[row], row_ind[row + 1]):
            col = col_ind[i]
            val = v[i]
            A[row][col] = val
    return A

def toSparse(adj, zero = 0):
    m = len(adj)
    n = len(adj[0])

    v = []
    col_ind = []
    row_ind = [0]

    for i in range(m):
        row_nnz = 0
        for j in range(n):
            if adj[i][j] != zero:
                v.append(adj[i][j])
                col_ind.append(j)
                row_nnz += 1
        row_ind.append(row_ind[-1] + row_nnz)
    
    return {
        'v': v,
        'col_ind': col_ind,
        'row_ind': row_ind,
        'shape': (m, n)
    }
