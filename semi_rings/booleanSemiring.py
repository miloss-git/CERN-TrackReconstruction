from sparse_matrix import sparseMatrix as sm

class MyBool:
    def __init__(self, value):
        self.value = bool(value)
    
    def __bool__(self): #allows "if x"
        return self.value
    
    def __add__(self, o):
        if isinstance(o, MyBool):
            return MyBool(self.value or o.value)
        return MyBool(self.value or bool(o))
    
    def __mul__(self, o):
        if isinstance(o, MyBool):
            return MyBool(self.value and o.value)
        return MyBool(self.value and bool(o))
    
    def __repr__(self):
        return str(self.value)
    
    def __lt__(self, o): #needed for graph ploting
        if isinstance(o, MyBool):
            return int(self.value) < int(o.value)
        return int(self.value) < int(bool(o))
    
    def __gt__(self, o): #-||-
        if isinstance(o, MyBool):
            return int(self.value) > (o.value)
        return int(self.value) > int(bool(o))
    
    def __eq__(self, o): #for val != zero
        if isinstance(o, MyBool):
            return self.value == o.value
        # Explicitly check for bool or the integers 0 and 1
        if isinstance(o, bool):
            return self.value == o
        if o == 1 or o == 0:
            return self.value == bool(o)
        
        return False
    
    def __int__(self): #ploting
        return int(self.value)
    
    def __float__(self): #lets leave it for safety
        return float(self.value)

zero = MyBool(0)

M7 = {
    'v': [MyBool(0.1), MyBool(0.3), MyBool(0.2), MyBool(0.5), MyBool(0.1), MyBool(0.1), MyBool(0.7), MyBool(0.6)],
    'col_ind': [1, 2, 3, 4, 4, 6, 5, 5],
    'row_ind': [0, 1, 3, 4, 6, 7, 7, 8],
    'shape': (7, 7)
}

M8 = {
    'v': [MyBool(1), MyBool(1), MyBool(1), MyBool(1), MyBool(1), MyBool(1), MyBool(1), MyBool(1), MyBool(1), MyBool(1), MyBool(1), MyBool(1)],
    'col_ind': [1, 2, 5, 7, 2, 4, 6, 6, 4, 0, 2, 3],
    'row_ind': [0, 1, 4, 4, 7, 7, 8, 8, 9, 12],
    'shape': (9, 9)
}

if __name__ == "__main__":
    #biggest path of lenght 4
    A1 = sm.power(M8, 1, zero=zero)
    A2 = sm.power(M8, 2, zero=zero)
    A3 = sm.power(M8, 3, zero=zero)
    A4 = sm.power(M8, 4, zero=zero)
    R = sm.addition(A1, A2, zero=zero)
    R = sm.addition(R, A3, zero=zero)
    R = sm.addition(R, A4, zero=zero)
    print(sm.sta.toAdj(R))
