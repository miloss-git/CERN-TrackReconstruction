import matplotlib.pyplot as plt
import math

#passing the lists of x coordinates and y, and z, so I will acommodate the data...
def toTransversePlane(x, y, z, lines = []):
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='blue', s=2)

    if lines != []:
        for i, j in lines:
            plt.plot([x[i], x[j]], [y[i], y[j]], color='gray', linewidth=1)

    ax.axhline(0, color='black', linewidth=1)  #for x-axis
    ax.axvline(0, color='black', linewidth=1)  #for y-axis

    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_aspect('equal', adjustable='datalim')
    ax.autoscale_view()

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    #plt.title("Points in the transverse plane")

    plt.show()

def torzPlane(x, y, z, lines = []):
    fig, ax = plt.subplots()

    r = []
    for xi, yi in zip(x, y):
        ri = math.sqrt(xi ** 2 + yi ** 2)
        r.append(ri)
    ax.scatter(z, r, color='blue', s=2)
    
    if lines != []:
        for i, j in lines:
            plt.plot([z[i], z[j]], [r[i], r[j]], color='gray', linewidth=1)

    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_aspect('equal', adjustable='datalim')
    ax.autoscale_view()

    ax.set_xlabel("z")
    ax.set_ylabel("r")

    plt.show()
    
#these SPs follow helical path in the space, so...
x = [1.0, 0.707, 0.0, -0.707, -1.0, -0.707, 0.0, 0.707, 1.0, 0.707]
y = [0.0, 0.707, 1.0, 0.707, 0.0, -0.707, -1.0, -0.707, 0.0, 0.707]
z = [0.0, 0.157, 0.314, 0.471, 0.628, 0.785, 0.942, 1.1, 1.257, 1.414]

if __name__ == "__main__":
    toTransversePlane(x, y, z)
    torzPlane(x, y, z)