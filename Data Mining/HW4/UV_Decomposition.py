import sys
import math
import numpy as np


path  = sys.argv[1]
X =int(sys.argv[2])
Y =int(sys.argv[3])
f =int(sys.argv[4])
iters = int(sys.argv[5])

#m = np.zeros(sys.argv[1],sys.argv[2])
m = np.zeros((X,Y))
u = np.ones((X,f))
v = np.ones((f,Y))
iterations = iters
numberOfValues =0
output=[]
with open(path,'r') as values:
    for each in values:
		each = each.split(',')
		m[int(each[0])-1,int(each[1])-1] = float(each[2])
		#m[int(each[0]),int(each[1])] = float(each[2])
		numberOfValues=numberOfValues+1
    
    for i in range(iterations):
        for r in range(X):
            for s in range(f):
                add=0.0
                square =0.0
                for j in range (Y):
                    subt =0
                    if m[r,j]!=0:                
                        square = square+pow(v[s,j],2)                
                        multi=0.0
                        for k in range(f):
                            if k!=s:
                                multi = multi+(u[r,k]*v[k,j])   
                        subt = m[r,j]-multi
                    add = add+(v[s,j]*subt)
                x = add/square
                u[r,s] = x
           
        for r in range(f):
            for s in range(Y):
                add=0.0
                square =0.0
                for i in range(X):
                    subt=0
                    if m[i,s]!=0:
                        square = square + pow(u[i,r],2)
                        multi = 0
                        for k in range(f):
                            if k!=r:
                                multi = multi+(u[i,k]*v[k,s])
                        subt = m[i,s] - multi
                    add = add+(u[i,r]*subt)
                y = add/square
                v[r,s] = y
    
        p = np.dot(u,v)
        for r in range(X):
            for s in range(Y):
                if m[r,s]==0:
                    p[r,s]=0
        diff = np.subtract(m,p)
        diffSquare = np.square(diff)
        squaredSum =  np.sum(diffSquare)
        meanSquareErrror = math.sqrt(squaredSum/numberOfValues)
        output.append("%.4f" % meanSquareErrror)
        print "%.4f" % meanSquareErrror