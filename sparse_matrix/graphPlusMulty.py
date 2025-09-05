#standard addition and multiplication primitively implemented...
import make_plots.graphPlot as gl
import numpy as np

def addition(adjMatrix1, adjMatrix2):
    n = len(adjMatrix1)
    m = len(adjMatrix1[0])

    if(n != len(adjMatrix2) or m != len(adjMatrix2[0])):
        print("Dimensions are not complementary")
        return
    
    resMatrix = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            resMatrix[i][j] = adjMatrix1[i][j] + adjMatrix2[i][j]
    return resMatrix

def multiplication(adjMatrix1, adjMatrix2):
    n = len(adjMatrix1)
    m = len(adjMatrix1[0])
    l = len(adjMatrix2[0])

    if(m != len(adjMatrix2)):
        print("Invalid dimensions")
        return
    
    resMatrix = np.zeros((n,l))
    for i in range(n):
        for j in range(l):
            for k in range(m):
                resMatrix[i][j] += adjMatrix1[i][k]*adjMatrix2[k][j]
    
    return resMatrix

adj1 = [
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
]

adj2 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0]
]

adjRes = [
    [0, 1, 1, 0, 0],
    [0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0]
]

adj3 = [
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0], 
    [0, 0, 0, 0, 0]
]

adj4 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0]
]

adj5 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0]
]

if __name__ == "__main__":
    gl.drawGraphN(adj1)
    gl.drawGraphN(adj2)
    gl.drawGraphN(addition(adj1, adj2))

    gl.drawGraphN(adj3)
    gl.drawGraphN(adj4)
    gl.drawGraphN(multiplication(adj3, adj4))

    gl.drawGraphN(adj5)
    gl.drawGraphN(multiplication(adj5, adj5))