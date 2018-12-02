Rmax=300
Rmin=200
Amax=30
Amin=-30
R_Lc=0.5
A_Lc=0.5
#per=0.1
l=8
t=8
Type="l"
MaxIt = 70 
nPop0 = 27    
nPop = 18
Smin = 0.5     
Smax = 3       
Exponent = 2
sigma_initial = 0.5
sigma_final = 0.01

'''
Values=[Rmax,Rmin,Amax,Amin,R_Lc,A_Lc,per,l,t,Type,MaxIt,nPop0,nPop,Smin,Smax,Exponent,sigma_initial,sigma_final]
Variables=['Rmax','Rmin','Amax','Amin','R_Lc','A_Lc','per','l','t','Type','MaxIt','nPop0','nPop','Smin','Smax','Exponent','sigma_initial','sigma_final']

#print Values,Variables
R=[]
for i in range(len(name)):
    for j in range(len(Values)):
        if name[i]==Variables[j]:
            R.append(Values[j])
'''
