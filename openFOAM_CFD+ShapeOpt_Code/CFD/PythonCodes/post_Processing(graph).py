import re, numpy, os,operator,time,math
import matplotlib.pyplot as plt
from multiprocessing import Pool

global Fx,Fy,Fz,Mx,My,Mz,T
		
def function(I):

	t2=time.time()

	#file = open('../postProcessing/forces%i/0/forces.dat'%I, 'r')

	file = open('../postProcessing/forces%i/0/forces.dat'%I, 'r')
	file = file.read()
	s=map(float, re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', file))
	X=numpy.array(s)
	a=[]
	for i in s:
		if i!=0.0:	
			a.append(i)

	Fx=[]; Fy=[]; Fz=[]
	Mx=[]; My=[]; Mz=[]
	T=[]
	
	omega=10.0*math.pi

	i=0
	while i<=(len(a)-12):
		T.append(a[i]);			i+=1
		Fx.append(a[i]+a[i+3]);	i+=1
		Fy.append(a[i]+a[i+3]);	i+=1
		Fz.append(a[i]+a[i+3]);	i+=4
		
		Mx.append(a[i]+a[i+3]);	i+=1
		My.append(a[i]+a[i+3]);	i+=1
		Mz.append(a[i]+a[i+3]);	i+=4
	

	T1=[]
	T1.append(T[0])
	for i in range(len(T)-1):
		T1.append(float(T[i+1]-T[i]))

	#print T1[0:20], len(T1)

	deltaT=sum(T1)/len(T1)
	#print deltaT

	#X = numpy.round(numpy.array(Fx),6)
	#Y = numpy.round(numpy.array(Fy),6)
	#Z = numpy.round(numpy.array(Mz),6)

	thefile1=open('../../%i.Forces'%I,'w')
	thefile2=open('../../%i.Moments'%I,'w')
	for i in range(len(Fx)):
		thefile1.write("%.6f\t%.6f\n"%(Fx[i],Fy[i]))
		thefile2.write("%.6f\n"%(Mz[i]))
	thefile1.close()
	thefile2.close()


	def Fourier(F,no,l,deltaT,Name,S="No"):
		F1=[]
		F1[:] = [x - numpy.mean(F[no:l]) for x in F]
		
		Fbar=numpy.fft.fft(F1[no:l])
		freq=numpy.fft.fftfreq(len(Fbar))

		if S!="No":
			l1=plt.semilogx(freq[0:len(freq)/2]/deltaT,numpy.abs(Fbar[0:len(Fbar)/2])**0.7)
			plt.setp(l1, linewidth=0.6, color='k')
			plt.grid(True)
			i=numpy.argmax(numpy.abs(Fbar[0:len(Fbar)/2]))
			frequency=freq[i]/deltaT
			plt.title('Max Freq %.2fHz'%frequency,loc='right',fontsize=15)
			plt.savefig('%s.svg'%Name, bbox_inches='tight')
			plt.close()

		return Fbar,freq

	def Plot(Fx,T,no,l,deltaT,Name,Fy=None,S="No"):
		Fx1=[]
		Fx1[:] = [x - numpy.mean(Fx[no:l]) for x in Fx]
		x = numpy.arange(0, l-no, 1)
		
		lines = plt.plot(T[no:l], Fx[no:l], T[no:l], Fx1[no:l])
		l1, l2 = lines
		plt.grid(True)
		plt.setp(l1, linewidth=0.8, color='k')  
		plt.setp(l2, linewidth=0.1, color='b')
		
		if (Fy!=None):
			
			Fy1=[]
			Fy1[:] = [i - numpy.mean(Fy[no:l]) for i in Fy]
			
			lines = plt.plot(T[no:l], Fy[no:l], T[no:l], Fy1[no:l])
			l1, l2 = lines
			plt.grid(True)
			plt.setp(l1, linewidth=0.1, color='g')  
			plt.setp(l2, linewidth=0.7, color='g')

		if S!="No":
			plt.title('%s'%Name,loc='right',fontsize=15)
			plt.savefig('%s.svg'%Name, bbox_inches='tight')
			plt.close()




	no=200#int(0.5*len(Fx))
	l=int(1*len(Fx))

	#Plot(Mz,T,no,l,deltaT,"MomentZ%i"%I,S="Yes")
	#Fourier(Mz,no,l,deltaT,"Fourier_Mz%i"%I,S="Yes")


	def run(a):

		global Fx,Fy,Fz,Mx,My,Mz,T
		
		if a==1:
			Plot(Fx,T,no,l,deltaT,"ForcesX%i"%I,S="Yes")
		elif a==2:
			Plot(Fy,T,no,l,deltaT,"ForcesY%i"%I,S="Yes")
		elif a==3:
			Plot(Fx,T,no,l,deltaT,"ForcesXY",Fy,S="Yes")
		elif a==4:
			Plot(Mz,T,no,l,deltaT,"MomentZ%i"%I,S="Yes")
		elif a==5:
			Fourier(Fx,no,l,deltaT,"Fourier_Fx",S="Yes")
		elif a==6:
			Fourier(Fy,no,l,deltaT,"Fourier_Fy",S="Yes")
		elif a==7:
			Fourier(Mz,no,l,deltaT,"Fourier_Mz",S="Yes")

	arr=[1,4,7]
	
	
	t1=time.time()
	'''
	y = Pool()
	result = y.map(run,arr)
	y.close()
	y.join()    
	'''
	'''
	for i in range(len(arr)):
		#print "%i"%x,time.time()-t1
		run(arr[i])
	'''
	#print "Total",time.time()-t1
	        





	#Fourier(Fx,no,l,deltaT,"Fx")
	'''
	MzBar,MzBarfreq=Fourier(Mz,no,l,deltaT,"MzBar%i"%I,S="Yes")
	i=numpy.argmax(numpy.abs(MzBar[0:len(MzBar)/2]))
	MzBarfrequency=MzBarfreq[i]/deltaT
	print MzBarfrequency


	turns=(omega/(MzBarfrequency*2*math.pi))
	'''
	turns=1
	n=turns*(2*math.pi/(omega*deltaT))

	z=len(T)/n

	#print turns,n,z

	z=z-0
	s=3


	#x=numpy.round(x,4)
	#x=[]
	#x=[float(i*deltaT) for i in range(n)]

	#print [ x[i] for i in range(len(x))]
	F=[0 for j in range(int(n)+1)]
	Fx1=[]
	#print len(x),len(Fx[int(i*n):int((i+1)*n)]),len(F)

	i=s
	while i <int(z):
		for j in range(int(n)+1):
			Fx1.append(Mz[i*int(n)+j]+i)
		i+=1
	a=1
	i=s
	while i <int(z):
		x = numpy.arange(0.0,(len(Mz[int(i*n):int((i+1)*n)]))*deltaT,deltaT)
		a+=1
		lines = plt.plot(x,Mz[int(i*n):int((i+1)*n)])
		F=[Mz[i*int(n)+j]+F[j] for j in range(int(n)+1)]
		l1 = lines
		plt.setp(l1, linewidth=0.1,color='k')  
		i+=1


	#print a, z-s
	x = numpy.arange(0.0,(n+1)*deltaT,deltaT)
	F=[F[j]/(int(z)-s) for j in range(len(F))]

	#print len(F)
	
	l2 =plt.plot(x[1:len(x)-0],F[0:])
	plt.setp(l2, linewidth=0.5,color='r')  	
	
	##plt.plot(Fx1)
	plt.ylim(-0.5, 0.5)
	
	#print min(F), max(F)
	
	Torque=sum([F[j] for j in range(len(F))])/len(F)
	Power=Torque*omega/0.02
	
	plt.title('%i %i Torque %.5fNm    Power %.2fW'%(s,z,Torque,Power),fontsize=15)
			
	plt.savefig('REP_Mz%i.svg'%I, bbox_inches='tight')	
	#plt.show()
	plt.close()


	return F
	F1=[]

	for i in range(int(z)+2):
		for j in range(len(F)):
			F1.append(F[j])

	#print len(F1)

ar=[1,2,3]


y = Pool()
result= y.map(function,ar)

y.close()	
y.join() 

'''
result=[]
for i in range(len(ar)):
	result.append(function(ar[i]))
'''

deltaT=0.0001
turns=1
omega=10*math.pi

n=turns*(2*math.pi/(omega*deltaT))
z=0.02

x = numpy.arange(0.0,(n+1)*deltaT,deltaT)
Power=[]
Torque=[]
for i in range(len(ar)):
	Torque.append(sum([result[i][j] for j in range(len(result[i]))])/len(result[i]))#/len(result[i]))
	Power.append(Torque[i]*omega/z)
PowerC=sum(Power)
TorqueC=sum(Torque)

thefile = open('../../Power', 'w')
thefile.write("%.3f"%(-1*PowerC))
thefile.close()
#print "Power per unit length =", sum(Power)
#print Torque



#print len(result[0]),len(result[1]),len(result[2]),len(x)

for i in range(len(ar)):
	#plt.plot(result[i][1][1:len(result[i][1])-0],result[i][0])
	plt.plot(x[0:len(result[i])],result[i],linewidth=0.3)
	
	#plt.setp(l2, linewidth=0.5,color='r')  	

#All=[result[0][0][i]+result[1][0][i]+result[2][0][i]+result[3][0][i] for i in range(len(result[0][0]))]
re=min([len(result[i]) for i in range(len(ar))])
#print re
#len_result=min(len(result[0]),len(result[1]),len(result[2]))
All=[result[0][i]+result[1][i]+result[2][i] for i in range(re)]
	
#plt.plot(result[0][1][1:len(result[0][1])-0],All,color='K')

plt.plot(x[0:re],All,color='K',linewidth=2)
plt.title('Torque %.5fNm    Power %.2fW'%(TorqueC,-PowerC),fontsize=15)
	 	
plt.grid(color='k',linestyle='--', linewidth=0.2)
plt.ylim(-0.5,0.5)	
plt.savefig('REP_MzCombined.svg', bbox_inches='tight')	
	
