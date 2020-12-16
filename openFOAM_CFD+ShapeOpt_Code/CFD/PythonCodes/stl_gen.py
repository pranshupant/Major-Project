
import random, re,  subprocess, sys, os, math ,numpy,shutil
import matplotlib.pyplot as plt
import stl
from stl import mesh
from distutils.dir_util import copy_tree
from multiprocessing import Pool
import scipy.interpolate as si

def read_integers(filename,t):
    with open(filename) as f:
        if t=='f':
            return [float(x) for x in f]
        
        if t=='i':
            z=[int(x) for x in f]
            return z[0]

        if t=='fxy':
            x=[];y=[]
            for i in f:
                row = i.split()
                x.append(float(row[0]))
                y.append(float(row[1]))

            return x,y

def randf(x,y):
    a=10000000
    return float(random.randrange(int(x*a),int(y*a)))/a

def STL_Gen(x,y,I):
    res = len(x)
    x=[x[i]/1000 for i in range(len(x))]
    y=[y[i]/1000 for i in range(len(x))]
    z=0.05
    i = 0; v=[]
    while (i <res): # +ve z axis points
        v.append([x[i],y[i],z])
        i += 1
    i=0
    while (i <res): # -ve z axis points
        v.append([x[i],y[i],-z])
        i += 1
    vertices=numpy.array(v)

    i=0; f=[]
    while (i<res-1): # generating faces
        f.append([i,i+1,res+i+1])
        f.append([i,res+i+1,res+i])
        i +=1
    faces= numpy.array(f)


    suf=mesh.Mesh(numpy.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            suf.vectors[i][j]= vertices[f[j],:]
    suf.save('../constant/triSurface/VAWT%i.stl'%I, mode=stl.Mode.ASCII)

def bspline(cv, n=100, degree=2, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
                  False - Curve is open
    """

    # If periodic, extend the point array by count+degree+1
    cv = numpy.asarray(cv)
    count = len(cv)

    if periodic:
        factor, fraction = divmod(count+degree+1, count)
        cv = numpy.concatenate((cv,) * factor + (cv[:fraction],))
        count = len(cv)
        degree = numpy.clip(degree,1,degree)

    # If opened, prevent degree from exceeding count-1
    else:
        degree = numpy.clip(degree,1,count-1)


    # Calculate knot vector
    kv = None
    if periodic:
        kv = numpy.arange(0-degree,count+degree+degree-1,dtype='int')
    else:
        kv = numpy.array([0]*degree + range(count-degree+1) + [count-degree]*degree,dtype='int')

    # Calculate query range
    u = numpy.linspace(periodic,(count-degree),n)


    # Calculate result
    arange = numpy.arange(len(u))
    points = numpy.zeros((len(u),cv.shape[1]))
    for i in xrange(cv.shape[1]):
        points[arange,i] = si.splev(u, (kv,cv[:,i],degree))

    return points

def insert(coorArrX,coorArrY,R,A):
    coorArrX.append(R*math.cos(math.radians(A)))
    coorArrY.append(R*math.sin(math.radians(A)))

def dis(r1,a1,r2,a2):
    #d1=math.sqrt((r2-r1)**2+(a2-a1)**2) //Cartesian
    d1=math.sqrt(r1**2+r2**2-2*r1*r2*math.cos(math.radians(a1-a2)))
            
    return d1

def points():
    coorArrX,coorArrY=read_integers('../../Genes', "fxy")
    numSteps = 500    
    n=len(coorArrY)
    XY=bspline(numpy.array(zip(coorArrX,coorArrY)),numSteps,2)

    x1=[XY[i][0] for i in range(len(XY))]
    y1=[XY[i][1] for i in range(len(XY))]

    '''
    thefile = open('../Points', 'a+')

    for i in range(len(x1)):
        thefile.write("%.6f %.6f\n" %(x1[i],y1[i]))#randf(random.randrange(random.randrange(-150,-145),-70),0))
    thefile.close()
    '''
    return x1,y1

def run():
    x,y=points()#read_integers('Points', "fxy")
    Theta=90
    Rot=[[math.cos(math.radians(Theta)),-math.sin(math.radians(Theta))],[math.sin(math.radians(Theta)),math.cos(math.radians(Theta))]]

    x1,y1=numpy.matmul(Rot,[x,y])

    STL_Gen(x1,y1,1)


    Theta=210
    Rot=[[math.cos(math.radians(Theta)),-math.sin(math.radians(Theta))],[math.sin(math.radians(Theta)),math.cos(math.radians(Theta))]]
    x1,y1=numpy.matmul(Rot,[x,y])

    STL_Gen(x1,y1,2)

    Theta=330
    Rot=[[math.cos(math.radians(Theta)),-math.sin(math.radians(Theta))],[math.sin(math.radians(Theta)),math.cos(math.radians(Theta))]]
    x1,y1=numpy.matmul(Rot,[x,y])

    STL_Gen(x1,y1,3)


run()




