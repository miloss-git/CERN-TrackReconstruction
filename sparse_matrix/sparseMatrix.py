import sparse_matrix.sparseToAdj as sta
import make_plots.graphPlot as gl
import numpy as nmp

#CSR format implemented:
'''
M = {
    v = [],
    col_ind = [],
    row_ind = [],
    spahe = (m, n)
    }
'''

def addition(M1, M2, zero = 0):
    if(M1['shape'] != M2['shape']):
        print("Invalid matrix dimensions")
        return

    v1 = M1['v']
    col_ind1 = M1['col_ind']
    row_ind1 = M1['row_ind']
    v2 = M2['v']
    col_ind2 = M2['col_ind']
    row_ind2 = M2['row_ind']

    v_res = []
    col_ind_res = []
    row_ind_res = [0]

    m = M1['shape'][0]
    n = M1['shape'][1]
    nnz = 0

    for row in range(m):
        row_dict = {}

        for i in range(row_ind1[row], row_ind1[row + 1]):
            col = col_ind1[i]
            val = v1[i]
            row_dict[col] = row_dict.get(col, zero) + val

        for i in range(row_ind2[row], row_ind2[row + 1]):
            col = col_ind2[i]
            val = v2[i]
            row_dict[col] = row_dict.get(col, zero) + val

        for col in sorted(row_dict):
            val = row_dict[col]
            if val != zero:
                v_res.append(val)
                col_ind_res.append(col)
                nnz += 1
        
        row_ind_res.append(nnz)

    return {
        'v': v_res, 
        'col_ind': col_ind_res,
        'row_ind': row_ind_res,
        'shape': (m, n)
    }

def transpose(M):
    m, n = M['shape']
    v = M['v']
    col_ind = M['col_ind']
    row_ind = M['row_ind']

    nnz = len(v)
    count = [0]*n #counting nonzero entires in each column of M <-> each row of A^T
    for i in range(m):
        rs, re = row_ind[i], row_ind[i + 1]
        for p in range(rs, re):
            j = col_ind[p]
            count[j] += 1
    
    row_ind_T = [0]*(n + 1)
    for j in range(n):
        row_ind_T[j + 1] = row_ind_T[j] + count[j]

    v_T = [None]*nnz
    col_ind_T = [0]*nnz
    next_slot = row_ind_T[:]

    for i in range(m):
        rs, re = row_ind[i], row_ind[i+1]
        for p in range(rs, re):
            j = col_ind[p]
            pos = next_slot[j]
            v_T[pos] = v[p]
            col_ind_T[pos] = i
            next_slot[j] += 1

    return {
        'v': v_T,
        'col_ind': col_ind_T,
        'row_ind': row_ind_T,
        'shape': (n, m)
    }

def multiplication(M1, M2, zero = 0):
    m, n = M1['shape']
    k, l = M2['shape']
    if (n != k):
        print("invalid dims for multiplication")
        return
    
    M_t = transpose(M2)
    v1 = M1['v']
    col_ind1 = M1['col_ind']
    row_ind1 = M1['row_ind']
    v2 = M_t['v']
    col_ind2 = M_t['col_ind']
    row_ind2 = M_t['row_ind']

    v_res = []
    col_ind_res = []
    row_ind_res = [0]
    nnz = 0

    for row in range(m): #extracting the sparsed row of the first matrix
        row_start1 = row_ind1[row]
        row_end1 = row_ind1[row + 1]

        for row_t in range(l): #and then of the second matrix
            row_start2 = row_ind2[row_t] 
            row_end2 = row_ind2[row_t + 1]

            i = row_start1
            j = row_start2
            val = zero

            while i < row_end1 and j < row_end2:
                c1 = col_ind1[i]
                c2 = col_ind2[j]
                if c1 == c2:
                    val = val + ( v1[i] * v2[j] )
                    i += 1
                    j += 1
                elif c1 < c2:
                    i += 1
                else:
                    j += 1
            
            if val != zero:
                nnz += 1
                v_res.append(val)
                col_ind_res.append(row_t)
        row_ind_res.append(nnz)
    

    return {
        'v': v_res,
        'col_ind': col_ind_res,
        'row_ind': row_ind_res,
        'shape': (m, l)
    }


def multiplicationWithPred(M1, M2, zero = 0):
    m, n = M1['shape']
    k, l = M2['shape']
    if (n != k):
        print("invalid dims for multiplication")
        return
    
    M_t = transpose(M2)
    v1 = M1['v']
    col_ind1 = M1['col_ind']
    row_ind1 = M1['row_ind']
    v2 = M_t['v']
    col_ind2 = M_t['col_ind']
    row_ind2 = M_t['row_ind']

    v_res = []
    col_ind_res = []
    row_ind_res = [0]
    nnz = 0
    preds = {} #(i, j) -> k meaning that the best path from i to j goes through node k

    for row in range(m):
        row_start1 = row_ind1[row]
        row_end1 = row_ind1[row + 1]

        for row_t in range(l):
            row_start2 = row_ind2[row_t]
            row_end2 = row_ind2[row_t + 1]

            i = row_start1
            j = row_start2
            val = zero
            best_k = None

            while i < row_end1 and j < row_end2:
                c1 = col_ind1[i]
                c2 = col_ind2[j]

                if c1 == c2:
                    temp = v1[i] * v2[j]
                    if val == zero or temp > val:
                        val = val + temp    #specifically val = temp cause we already know that temp > val and
                        best_k = c1         #only max.+ is used with this function
                    i += 1
                    j += 1
                elif c1 < c2:
                    i += 1
                else:
                    j += 1
            
            if val != zero:
                nnz += 1
                v_res.append(val)
                col_ind_res.append(row_t)
                preds[(row, row_t)] = best_k

        row_ind_res.append(nnz)
    res =  {
        'v': v_res,
        'col_ind': col_ind_res,
        'row_ind': row_ind_res,
        'shape': (m, l)
    }

    return res, preds

def vectorMult(M, vector, zero):
    m, n = M['shape']
    l = len(vector)
    if (n != l):
        print("invalid dimensions for Mxv multiplication")
        return
    
    v = M['v']
    col_ind = M['col_ind']
    row_ind = M['row_ind']

    vector_res = []
    for row in range(m):
        row_start = row_ind[row]
        row_end = row_ind[row + 1]

        val = zero
        for i in range(row_start, row_end):
            col = col_ind[i]
            val = ( v[i] * vector[col] ) + val
        
        vector_res.append(val)

    return vector_res

def power(M, k, zero = 0):
    if k < 1 or (not isinstance(k, int)):
        print("Invalid exponent")
        return
    
    result = M
    k -= 1
    while k > 0:
        if k % 2 == 1:
            result = multiplication(result, M, zero)
        M = multiplication(M, M, zero)
        k //= 2
    
    return result

M1 = {
    'v': [1, 1, 2, 1],
    'col_ind': [0, 0, 1, 2],
    'row_ind': [0, 1, 3, 4],
    'shape': (3, 3)
}

M2 = {
    'v': [1, 1, 1],
    'col_ind': [1, 0, 2],
    'row_ind': [0, 1, 2, 3],
    'shape': (3, 3)
}

M3 = {
    'v': [0.8, 0.1, 0.2, 0.3, 0.4],
    'col_ind': [1, 0, 2, 0, 1],
    'row_ind': [0, 1, 3, 5],
    'shape': (3, 3)
}

M4 = {
    'v': [0.5, 0.7, 0.4, 0.1],
    'col_ind': [2, 2, 0, 1],
    'row_ind': [0, 1, 2, 4],
    'shape': (3, 3)
}

M = {
    'v': [1, 2, 3],
    'col_ind': [0, 2, 1],
    'row_ind': [0, 2, 3],
    'shape': (2, 3)
}

vector = [4, 5, 6]

if __name__ == "__main__":
    M = multiplication(M3, M4)
    print(M)
    print(sta.toAdj(M))
    gl.drawWeightedGraph(sta.toAdj(M))
    print(vectorMult(M, vector))