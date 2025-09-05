from sparse_matrix import sparseMatrix as sm

class MyNumber:
    def __init__(self, value):
        self.value = value

    def __add__(self, o):
        if isinstance(o, MyNumber):
            return MyNumber(min(self.value, o.value))
        return MyNumber(min(self.value, o))
    
    def __mul__(self, o):
        if isinstance(o, MyNumber):
            return MyNumber(self.value + o.value)
        return MyNumber(self.value + o)
    
    def __repr__(self):
        return str(self.value)
    
    def __lt__(self, o): #needed for graph ploting
        if isinstance(o, MyNumber):
            return self.value < o.value
        return self.value < o
    
    def __gt__(self, o): #-||-
        if isinstance(o, MyNumber):
            return self.value > o.value
        return self.value > o
    
    def __eq__(self, o): #for val != zero
        if isinstance(o, MyNumber):
            return self.value == o.value
        return self.value == o
    
    def __int__(self): #ploting
        return int(self.value)
    
    def __float__(self):
        return float(self.value)

zero = MyNumber(float('inf'))

#a = MyNumber(3)
#b = MyNumber(5)
#print(a + b)
#print(a * b)

M1 = {
    'v': [MyNumber(1), MyNumber(1), MyNumber(1), MyNumber(1), MyNumber(2)],
    'col_ind': [1, 2, 2, 0, 1],
    'row_ind': [0, 2, 3, 5],
    'shape': (3, 3)
}

M2 = {
    'v': [MyNumber(2), MyNumber(1), MyNumber(1), MyNumber(1)],
    'col_ind': [1, 0, 2, 1],
    'row_ind': [0, 1, 3, 4],
    'shape': (3, 3)
}

M3 = {
    'v':[MyNumber(0.8), MyNumber(0.2), MyNumber(0.5), MyNumber(0.3), MyNumber(0.1)],
    'col_ind': [1, 2, 0, 2, 0],
    'row_ind': [0, 2, 4, 5],
    'shape': (3, 3)
}

M4 = {
    'v': [MyNumber(0.21), MyNumber(0.11), MyNumber(0.35), MyNumber(0.7)],
    'col_ind': [1, 0, 0, 1],
    'row_ind': [0, 1, 2, 4],
    'shape': (3, 3)
}

M5 = {
    'v': [MyNumber(0.8), MyNumber(0.1), MyNumber(0.2), MyNumber(0.3), MyNumber(0.4)],
    'col_ind': [1, 0, 2, 0, 1],
    'row_ind': [0, 1, 3, 5],
    'shape': (3, 3)
}

M6 = {
    'v': [MyNumber(0.5), MyNumber(0.7), MyNumber(0.4), MyNumber(0.1)],
    'col_ind': [2, 2, 0, 1],
    'row_ind': [0, 1, 2, 4],
    'shape': (3, 3)
}

M7 = {
    'v': [MyNumber(0.1), MyNumber(0.3), MyNumber(0.2), MyNumber(0.5), MyNumber(0.1), MyNumber(0.1), MyNumber(0.7), MyNumber(0.6)],
    'col_ind': [1, 2, 3, 4, 4, 6, 5, 5],
    'row_ind': [0, 1, 3, 4, 6, 7, 7, 8],
    'shape': (7, 7)
}

if __name__ == "__main__":
    M = sm.power(M7, 3, zero=zero)
    #sm.gl.drawWeightedGraph(sm.sta.toAdj(M7))
    sm.gl.drawWeightedGraph(sm.sta.toAdj(M))

    M = sm.multiplication(M3, M4, zero)
    #print(M)
    #print(sm.sta.toAdj(M, zero))
    sm.gl.drawGraphN(sm.sta.toAdj(M, zero))
    sm.gl.drawWeightedGraph(sm.sta.toAdj(M, zero))

    M = sm.power(M5, 4, zero)
    #print(M)
    #print(sm.sta.toAdj(M, zero))
    sm.gl.drawWeightedGraph(sm.sta.toAdj(M5, zero))
    sm.gl.drawWeightedGraph(sm.sta.toAdj(M, zero))