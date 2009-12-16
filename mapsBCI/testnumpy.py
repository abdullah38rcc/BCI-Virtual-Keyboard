x = array([30,40])
x2 = array([[30,40]])

y = zeros((x[0],x[1]),bool)
y2 = zeros( (x2[0,0],x2[0,1]),bool)

z = [3,2]
q = [4,8]
h = [5,7]
x = []
x.append(z)
x.append(q)
x.append(h)
#print len(x)
x = array(x)
sm = 10.2
#print sum(x[:,0], axis=0)
#print floor(x[:,0]* sm)
#print x[:,0]* sm
#f = z * ones((1,5))
f = []
for i in range(1,5):
	f.append(z)
f = array(f)
print f
print f[:,0]
