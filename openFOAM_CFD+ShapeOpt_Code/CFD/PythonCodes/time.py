import time,re
import os.path
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

def write(filename,f,t='i'):
    thefile = open('%s'%filename, 'w')
    if t=='f':
        thefile.write("%f" %f)
    if t=='i':
        thefile.write("%i" %f)
    thefile.close()

def dirCheck(s):
    import os
    cwd = os.getcwd()
    fold='/'
    cwd+=fold
    z=cwd.find(s)
    t=0
    while 1:
        if fold in cwd[z:z+len(s)+t]:
            z1=cwd[z+len(s):z+len(s)+t-1]
            break
        else:
            t+=1
            continue
    return z1
#[int(s) for s in str.split() if s.isdigit()]


Process=['Meshing_Start\t','Meshing_Done\t','Simulation_Start','Simulation_Done','PostProcessing_Done']
gen='Generation_'
spc='Specie_'


if not os.path.isfile("run"):
    t1=time.time()
    i=0
    write('run',i)  
    write('runTime',t1,'f')
else:
    t1=read_integers('runTime','f')
    i=read_integers('run','i')
    if i==5:
        os.remove('run')
        os.remove('runTime')
    else:
        print "%s%s\t"%(gen,dirCheck(gen)),"%s%s\t"%(spc,dirCheck(spc)),Process[i],"\tRun Time %.2fs" %(time.time()-t1)
        i+=1
        write('run',i)  
        write('runTime',time.time())
        
