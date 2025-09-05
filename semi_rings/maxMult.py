from sparse_matrix import sparseMatrix as sm

class MyNumber:
    def __init__(self, value):
        if (value >= 0): self.value = value   #added condition

    def __add__(self, o):
        if isinstance(o, MyNumber):
            return MyNumber(max(self.value, o.value))
        return MyNumber(max(self.value, o))
    
    def __mul__(self, o):
        if isinstance(o, MyNumber):
            return MyNumber(self.value * o.value)
        return MyNumber(self.value * o)
    
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

zero = MyNumber(float(0))

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
M = sm.power(M7, 3, zero=zero)
sm.gl.drawWeightedGraph(sm.sta.toAdj(M))

if __name__ == "__main__":
    #M = sm.multiplication(M5, M6, zero)
    M = sm.power(M5, 3, zero)
    #print(M)
    #print(sm.sta.toAdj(M, zero))
    sm.gl.drawWeightedGraph(sm.sta.toAdj(M, zero))