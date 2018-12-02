import csv, random, re, sys, os, math, numpy, time, subprocess, shutil
import matplotlib.pyplot as plt 
from multiprocessing import Pool
from distutils.dir_util import copy_tree
import scipy.interpolate as si


def read_integers(filename,t):
    with open(filename) as f:
        if t=='f':
            z=[float(x) for x in f]
            if len(z)==1:
                return z[0]
            else:
                return z
        if t=='i':
            z=[int(x) for x in f]
            if len(z)==1:
                return z[0]
            else:
                return z
        if t=='fxy':
            x=[];y=[]
            for i in f:
                row = i.split()
                x.append(float(row[0]))
                y.append(float(row[1]))

            return x,y
p=[]
r=read_integers('../Generation',"i")

def Cost(e):
    #time.sleep(1)

    #print r,g
    #print "The Directory is ======",os.getcwd(),r,e
    copy_tree("../CFD", "../Results/Generation_%d/Specie_%d/CFD" %(r,e))
    #sys.path.append("../Results/Generation_%d/Specie_%d/CFD" %(r,e))
    os.chdir("../Results/Generation_%d/Specie_%d/CFD" %(r,e))

    #subprocess.call('./Allclean')
    #subprocess.call('ls')
    #os.chdir('CFD/')
    subprocess.call(['./All'])
    os.chdir('../')
    #import CFD
    #CFD.run(e)
    #r=read_integers('../Generation',"i")
    
    os.chdir("../../../GA")
    shutil.rmtree("../Results/Generation_%d/Specie_%d/CFD" %(r,e))
    #print r,e,read_integers("../Results/Generation_%d/Specie_%d/Pitch" %(r,e),"f")
    #print r,e,"Time taken=",time.time()-t1
    return read_integers("../Results/Generation_%d/Specie_%d/Power" %(r,e),"f")
    

def Gen1(nPop0):
    import Gen1
    Gen1.Gen1_run(nPop0)
    #return read_integers("../Results/Generation_%d/Specie_%d/Pitch" %(r,e))

def takeSecond(elem):
    return elem.Cost

def randf(x,y):
    a=10
    return float(random.randrange(x*a,y*a))/a

def myRound(x,base,prec=2):
    return round(base * round(float(x)/base),prec)

def cartesian(R,A):
    coorArrX=[];coorArrY=[]
    for i in range(len(R)):
        coorArrX.append(R[i]*math.cos(math.radians(A[i])))
        coorArrY.append(R[i]*math.sin(math.radians(A[i])))
    return coorArrX,coorArrY

def polar(X,Y):
    R=[];A=[]
    for i in range(len(X)):
        R.append((X[i]**2+Y[i]**2)**0.5)
        A.append(math.degrees(math.atan(float(Y[i])/X[i])))
    return R,A

def new(R,A,sigma):
    
    R,A=polar(R,A)
    from Constants import *

    if Type=='l':
        i=0
        if A[i]==Amax:
            R[i]=R[i]+(Rmax-Rmin)*sigma*randf(-1,1)
            R[i]=max(R[i],Rmin)
            R[i]=min(R[i],Rmax)
            R[i]=myRound(R[i],R_Lc)
        elif R[i]==Rmax or R[i]==Rmin:
            Amax1=Amax#*(1+per)
            Amin1=Amax*0.3

            A[i]=A[i]+(Amax1-Amin1)*sigma*randf(-1,1)
            A[i]=max(A[i],Amin1)
            A[i]=min(A[i],Amax1)
            A[i]=myRound(A[i],A_Lc)
        i+=1
        j=0
        while i <(len(R)-1):
            Amax1=Amax-(Amax-Amin)/l*j#+per*Amax
            Amin1=Amax-(Amax-Amin)/l*(j+1)#-per*Amin
            Rmax1=Rmax#*(1+per)
            Rmin1=Rmin#*(1-per)  
            R[i]=R[i]+(Rmax-Rmin)*sigma*randf(-1,1)
            R[i]=max(R[i],Rmin)
            R[i]=min(R[i],Rmax)
            R[i]=myRound(R[i],R_Lc)
            A[i]=A[i]+(Amax1-Amin1)*sigma*randf(-1,1)
            A[i]=max(A[i],Amin1)
            A[i]=min(A[i],Amax1)
            A[i]=myRound(A[i],A_Lc)
            i+=1
            j+=1

        if A[i]==Amin:
            R[i]=R[i]+(Rmax-Rmin)*sigma*randf(-1,1)
            R[i]=max(R[i],Rmin)
            R[i]=min(R[i],Rmax)
            R[i]=myRound(R[i],R_Lc)

        elif R[i]==Rmax or R[i]==Rmin:
            Amax1=Amin*0.3
            Amin1=Amin
            A[i]=A[i]+(Amax1-Amin1)*sigma*randf(-1,1)
            A[i]=max(A[i],Amin1)
            A[i]=min(A[i],Amax1)
            A[i]=myRound(A[i],A_Lc)

    if Type=='t':
    
        i=0
        #if R[i]==Rmax or R[i]==Rmin:
        
        A[i]=A[i]+(Amax)*sigma*randf(-1,1)
        A[i]=max(A[i],Amin)
        A[i]=min(A[i],Amax)
        A[i]=myRound(A[i],A_Lc)
        i+=1
        j=0
        while i <(len(R)-1):
            
            Amax1=Amax#*(1+per)
            Amin1=Amin#*(1+per)
            Rmax1=Rmax-((Rmax-Rmin)/t)*j#+per*Rmax
            Rmin1=Rmax-((Rmax-Rmin)/t)*(j+1)#-per*Rmin
            
            R[i]=R[i]+(Rmax1-Rmin1)*sigma*randf(-1,1)
            R[i]=max(R[i],Rmin1)
            R[i]=min(R[i],Rmax1)
            R[i]=myRound(R[i],R_Lc)
            A[i]=A[i]+Amax*sigma*randf(-1,1)
            A[i]=max(A[i],Amin)
            A[i]=min(A[i],Amax)

            
            A[i]=myRound(A[i],A_Lc) 
            i+=1
            j+=1
        #if R[i]==Rmax or R[i]==Rmin:
        
        A[i]=A[i]+Amax*sigma*randf(-1,1)
        A[i]=max(A[i],Amin)
        A[i]=min(A[i],Amax)
        
        A[i]=myRound(A[i],A_Lc)
    
    #print R,A 
    return cartesian(R,A)


class Pop(object):
    
    def __init__(self, R=[],A=[], Cost=0) :
        self.R = R
        self.A = A
        self.Cost = Cost
    

def Popread():
    r=read_integers('../Generation',"i")
    r=r-1
    global p
    p=[]
    g=0
    if r==0:
        while os.path.isdir("../Results/Generation_%i/Specie_%i" %(r,g)):
            x,y =read_integers("../Results/Generation_%i/Specie_%i/Genes" %(r,g),'fxy')
            z=read_integers("../Results/Generation_%i/Specie_%i/Power" %(r,g),'f')
            p.append(Pop(x,y,z))                
    else:
        while os.path.isdir("../Results/Generation_%i/Population/Specie_%i" %(r,g)):
            x,y =read_integers("../Results/Generation_%i/Population/Specie_%i/Genes" %(r,g),'fxy')
            z=read_integers("../Results/Generation_%i/Population/Specie_%i/Power" %(r,g),'f')
            p.append(Pop(x,y,z))            

def Write_Iteration():
    global r
    thefile=open('../Generation','w')
    thefile.write('%i'%r)
    thefile.close()



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

def graph(coorArrX,coorArrY,r,I,f='No'):
    from Constants import *
    #Rmax,Rmin,Amax,Amin,R_Lc,A_Lc,per,l,t,Type=Constants(["Rmax","Rmin","Amax","Amin","R_Lc","A_Lc","per",'l','t',"Type"])
    n=len(coorArrX)
    numSteps = 500    
    XY=bspline(numpy.array(zip(coorArrX,coorArrY)),numSteps,2)
    #print XY
    x1=[XY[i][0] for i in range(len(XY))]
    y1=[XY[i][1] for i in range(len(XY))]
    
    #print R,A


    #print x,y
    plt.xlim(-100,500)  
    plt.ylim(-300,300) 
    plt.scatter(coorArrX,coorArrY,s=2)
    plt.scatter(coorArrX[0],coorArrY[0],c='k',s=2)
    plt.scatter(coorArrX[n-1],coorArrY[n-1],c='k',s=2)
    #n=["%s" %i for i in range(len(coorArrX))]
    #for i, txt in enumerate(n):
    #    plt.annotate(txt, (coorArrX[i],coorArrY[i]),size="10")
    
    x=[];y=[]
    res=1000
    R=[Rmin for i in range(res+1)]
    A=[(Amax-Amin)*z/res+Amin for z in range(res+1)]

    
    for i in range(len(R)):
        x.append(R[i]*math.cos(math.radians(A[i])))
        y.append(R[i]*math.sin(math.radians(A[i])))
    plt.plot(x,y,c='r', linewidth=0.5)
    
    x=[];y=[]
    R=[Rmax for i in range(res+1)]
    A=[(Amax-Amin)*i/res+Amin for i in range(res+1)]
    for i in range(len(R)):
        x.append(R[i]*math.cos(math.radians(A[i])))
        y.append(R[i]*math.sin(math.radians(A[i])))
    plt.plot(x,y,c='r', linewidth=0.5)
    
    x=[];y=[]
    R=[(Rmax-Rmin)*i/res+Rmin for i in range(res+1)]
    A=[Amin for i in range(res+1)]
    for i in range(len(R)):
        x.append(R[i]*math.cos(math.radians(A[i])))
        y.append(R[i]*math.sin(math.radians(A[i])))
    plt.plot(x,y,c='r', linewidth=0.5)

    x=[];y=[]
    R=[(Rmax-Rmin)*i/res+Rmin for i in range(res+1)]
    A=[Amax for i in range(res+1)]
    for i in range(len(R)):
        x.append(R[i]*math.cos(math.radians(A[i])))
        y.append(R[i]*math.sin(math.radians(A[i])))
    plt.plot(x,y,c='r', linewidth=0.5)
        

    plt.plot(x1,y1,c='k', linewidth=1)
    if f=='No':
        thefile = open('../Results/Generation_0/Specie_%i/Points'%I, 'a+')
        for i in range(len(x1)):
            
            thefile.write("%.6f %.6f\n" %(x1[i],y1[i]))#randf(random.randrange(random.randrange(-150,-145),-70),0))
            
        thefile.close()
        
        plt.savefig('../Results/Generation_%i/Fig%i.svg'%(r,I))
        plt.close()
    elif f=='Yes':
        plt.savefig('../GA/Figure%i.svg'%I)
        plt.close()




if __name__ == "__main__":
    t2=time.time()
    
    global g,r,p
    from Constants import *
    if r==0:
        t1=time.time()
        Gen1(nPop0)
        x=[];y=[]
        for i in range(nPop0):
            x1,y1=read_integers('../Results/Generation_0/Specie_%d/Genes' %i, "fxy")
            x.append(x1) #float(random.randrange((VarMin*a),(VarMax*a)))/a)
            y.append(y1)
        
        ypool= Pool(nPop0)
        result = ypool.map(Cost,range(nPop0))
        ypool.close()
        ypool.join()
        for i in range(nPop0):
            p.append(Pop(x[i],y[i],result[i]))
        
        for i in range(len(p)):
            print i,p[i].Cost
        thefile=open('../Results/Generation_%d/Costs'%(r),"w")
        for i in range(len(p)):  
            thefile.write("%f\n" %p[i].Cost)
        thefile.close()
        
        print "\nGeneration=",r,"\nNet Time=",time.time()-t1
        r+=1
        #Write_Iteration()


    #IWO Main Loop
    
    BestCosts=[]
    while r<(MaxIt+1):
        t1=time.time()
        #Popread()
        
        #Update Standard Deviation
        sigma = (((MaxIt - float(r))/(MaxIt - 1))**Exponent )* (sigma_initial - sigma_final) + sigma_final;
        
        #Get Best and Worst Cost Values
        Costs=[]
        for t in range(len(p)):
            Costs.append(p[t].Cost)

        BestCost = min(Costs);
        
        WorstCost = max(Costs);
        
        #Initialize Offsprings Population
        
        pn=[]
        X=[]
        Y=[]
        #Reproduction
        g=0

        def reproduction(i):            
            global g
            ratio = (p[i].Cost - WorstCost)/(BestCost - WorstCost)
            S = int(Smin + (Smax - Smin)*ratio)
            if S>0:
                for j in range(S):
                    
                    #print r,S,j,g
                    #Initialize Offspring
                    if(not os.path.isdir("../Results/Generation_%i/Specie_%i" %(r,g))):
                        os.makedirs("../Results/Generation_%i/Specie_%i/" %(r,g))
                    thefile = open('../Results/Generation_%i/Specie_%i/Genes' %(r,g), 'w')
                    #import Graph
                    
                    #Generate Random Location
                    #print "\nSpecie%i,%i"%(i,j)

                    X1,Y1=new(p[i].R,p[i].A,sigma)
                    for t in range(len(X1)):
                        thefile.write("%.1f\t%.1f\n" %(X1[t],Y1[t]))
                    '''
                    while t<nVar: # in range(nVar):
                        a=(p[i].Genes[t]+sigma*randf(-1,1))  
                        a=max(a,VarMin)
                        a=min(a,VarMax)
                        A.append(round(a,2))
                        
                        t+=1
                    '''
                    #print A            
                    X.append(X1)
                    Y.append(Y1)
                    #Graph.Graph(A,r,g)
                    thefile.close()
                    g+=1
            

        for x in range(len(p)):
            reproduction(x)      


        y = Pool(g)
        result = y.map(Cost,range(g))
        y.close()
        y.join()    
        
        #print "\n",g,result
        for j in range(g):    
            #print Z[j]
            p1=[]
            p1.append(Pop(X[j],Y[j],result[j]))               
            #Add Offpsring to the New Population
            pn=pn+p1
        #for i in range(len(pn)):
        #    print r,g,i,"Genes",pn[i].Cost
                    
        p=p+pn
        #Merge Populations
            
        #Sort Population
        p.sort(key=takeSecond)

        p2=[]
        if len(p)>nPop:
            for i in range(nPop):
                p2.append(p[i])
            p=[]
            p=p2    
        subprocess.call(['clear'])
        print "\nGeneration=",r,g,"\nNet Time=",time.time()-t1,"\t%f"%sigma
        for i in range(len(p)):
            print i,"Genes",p[i].Cost
            os.makedirs("../Results/Generation_%i/Population/Specie_%i" %(r,i))
            thefile = open('../Results/Generation_%i/Population/Specie_%i/Genes' %(r,i), 'w')
            for j in range(len(p[i].R)):
                thefile.write("%.1f\t%.1f\n" %(p[i].R[j],p[i].A[j]))
            thefile = open('../Results/Generation_%i/Population/Specie_%i/Power' %(r,i), 'w')
            thefile.write("%.3f" %(p[i].Cost))
            thefile.close()
            thefile.close()
            #graph(p[i].R,p[i].A,r,i)
        
        #Store Best Solution Ever Found
        BestSol=p[0]
        
        #Store Best Cost History
        BestCosts.append(BestSol.Cost)
        
        #Display Iteration Information
        #print("Iteration--- %s\n" %r)
        #print("Best Cost--- %s" %BestCosts[r])
        #thefile = open('../BestCosts', 'w')
        #thefile.write("%s\t" %BestCosts[r])
        
        thefile=open('../Results/Generation_%i/Costs'%(r),"w")
        for i in range(len(p)):  
            thefile.write("%f\n" %p[i].Cost)
        thefile.close()
        #Write_Iteration()
        
        r+=1
        #Write_Iteration()
        

    #print "actual Cost",Cost1(0,0,f)
    print "Function             ---",
    #print "Minima at Coordinates---", p[0].Genes
    #BestCosts.sort()
    print "Solution at minima   ---", min(BestCosts)
    #print BestCosts
    Total=0
    for i in range(len(BestCosts)):

        Cost=read_integers('../Results/Generation_%d/Costs' %i, 'f')
        s=0;s1=0;Cost1=[]
        if i>=1:
            while s==0:
                if (os.path.isdir("../Results/Generation_%d/Specie_%d/" %(i,s1))):
                    Cost1=(read_integers('../Results/Generation_%d/Specie_%d/Power' %(i,s1), 'f'))
                    s1+=1
                    plt.scatter(i,Cost1,s=0.1,label='Species',c='blue')
                else:
                    s+=1
            print "number of Species",i,s1
            Total=Total+s1
        x=[i for j in range(len(Cost))]
        plt.scatter(x,Cost,s=2,label='Species',c='yellow')
    plt.title('Objective Function')
    plt.xlabel("Generations")
    plt.ylabel("Cost")
    plt.savefig('../Figure1.svg')
    
    plt.close()
    print "Total Species:",Total
    
    '''
    for i in range(len(BestCosts)):
        x=[]
        Cost=read_integers('../Results/Generation_%d/Cost' %i, 'f')
        for j in range(len(Cost)):
            x.append(i)    
        plt.scatter(x,Cost,label='Species')
    plt.title('Objective Function')
    plt.savefig('Figure1.svg')
    
    plt.close()
    '''
    
    thefile = open('../GA/FinalGenes', 'w')
    for i in range(len(p[0].R)):
        thefile.write("%.1f\t%.1f\n" %(p[0].R[i],p[0].A[i]))
    thefile.close()    
    graph(p[0].R,p[0].A,0,0,'Yes')
    x,y=read_integers('../GA/Genes','fxy')
    graph(x,y,0,1,'Yes')
    '''
    plt.plot(numpy.fabs(BestCosts))
    plt.savefig('Figure.svg')
    plt.show()
    '''
