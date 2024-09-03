#Coding:utf-8
import numpy as np

x0=-2.7
xN=2.7
t0=0
tK=3

tau=0.0005
h=0.1

tlist = [0,0.5,1,1.2,1.7,2,2.5,3] # перечень моментов времени, когда нужен 2д график

def u0(x):
    return np.exp(-x**2)

def createMat(uarray): # слой без границ при t0
    global x0, xN, t0, tK, tau, h
    startmat = np.eye(int(np.round((xN-x0-h)/h)))
    for i in range(int(np.round((xN-x0-h)/h))):
        for j in range(int(np.round((xN-x0-h)/h))):
            if i==j+1:
                startmat[i, j]=tau/(2*h)*uarray[i]
            if i==j-1:
                startmat[i, j]=-tau/(2*h)*uarray[i]
    #print(startmat)
    return np.linalg.inv(startmat)

def createField(): # слои без границ от t0 до tK включительно
    global x0, xN, t0, tK, tau, h, tlist
    with open("graphic3d.txt", "w") as g3d, open("graphics2d.txt", "w") as g2d:
        arr = []
        g3dt = "ListPlot3D[{"
        g2dt = ""
        currcoords="{" # координаты для 2-графика, обновляются с изменением времени
        i = x0+h
        while i<=xN-h+h/2:
            arr=arr+[u0(i)]
            g3dt = g3dt + "{" + str(np.round(i,4)) + ", " + "0, " + str(np.round(u0(i),4)) + "}, "
            i+=h
        field=[np.array(arr)]
        layer=t0+tau
        while layer<=tK+tau/2:
            field = field + [createMat(field[-1]).dot(field[-1])]
            i=1
            while x0+i*h<=xN-h+h/2:
                g3dt = g3dt + "{" + str(np.round(x0+i*h,4)) + ", " + str(np.round(layer,4)) + ", " + str(np.round(field[-1][i-1],4)) + "}, "
                i+=1
            layer+=tau
        for t in tlist:
            it = int((t-t0)/tau)
            currcoords="{"
            for ix in range(1, int((xN-x0)/h)):
                print(ix,it)
                currcoords=currcoords + "{" + str(x0+ix*h) + ", " + str(np.round(field[it][ix-1],4)) + "}, "
            currcoords=currcoords[:-2] + "}"
            g2dt = g2dt + "u" + str(it) + " = Interpolation[" + currcoords + "]\n" + "Plot[u" + str(it) + "[x], {x, " + str(x0) + ", " + str(xN) + "}, ImageSize -> Large, Background -> Black, LabelStyle -> {White, Medium, Italic}, PlotStyle -> Blue, LabelStyle -> {White, Italic, Large}, AxesLabel -> {\"x\", \"u(x, " + str(t) + ")\"},\n" + "Epilog ->\n" + "{Red, Point[" + currcoords + "]}]\n"
        g3dt = g3dt[:-2] + "}, PlotStyle -> Orange, PlotRange -> {0, 1.1}]"
        g3d.write(g3dt)
        g2d.write(g2dt)
    print("end")
    return field


createField()