from sparse_matrix import sparseMatrix as sm

'''
from minPlus import MyNumber as MyNumber
from minPlus import zero as zero'''
'''
from maxMin import MyNumber as MyNumber
from maxMin import zero as zero'''

from semi_rings.maxMult import MyNumber as MyNumber
from semi_rings.maxMult import zero as zero

T1 = {
    'v': [MyNumber(0.1), MyNumber(0.6), MyNumber(0.3), MyNumber(0.4), MyNumber(0.7), MyNumber(0.2), MyNumber(0.9)],
    'col_ind': [1, 4, 2, 3, 5, 6, 7],
    'row_ind': [0, 2, 4, 4, 5, 7, 7, 7, 7],
    'shape': (8, 8)
}

T2 = {
    'v': [MyNumber(0.1), MyNumber(0.6), MyNumber(0.3), MyNumber(0.4), MyNumber(0.7), MyNumber(0.2), MyNumber(0.9), MyNumber(0.8)],
    'col_ind': [1, 4, 2, 3, 5, 6, 7, 8],
    'row_ind': [0, 2, 4, 4, 5, 7, 8, 8, 8, 8],
    'shape': (9, 9)
}

if __name__ == "__main__":
    T_res = sm.power(T2, 3, zero)
    print(T_res)
    sm.gl.drawWeightedGraph(sm.sta.toAdj(T_res, zero))