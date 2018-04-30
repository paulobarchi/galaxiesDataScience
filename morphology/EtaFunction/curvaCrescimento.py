import pyfits
import copy
import numpy as np
import matplotlib.pyplot as plt

f1 = pyfits.open('587722982280724639.fit')
tbdata1 = f1[0].data
f2 = pyfits.open('bcg_360_3.fits')
tbdata2 = f2[0].data


xc=float(tbdata1.shape[0])/2.
yc=float(tbdata1.shape[1])/2.
linddlist=[[],[]]
for i in range(tbdata1.shape[0]):
	for j in range(tbdata1.shape[1]):
		dist=((i-xc)**2+(j-yc)**2)**0.5
		if dist<xc:
			linddlist[0].append(dist)
			linddlist[1].append(tbdata1[i][j]-tbdata2[i][j])

fluxc=[[],[]]
fluxt=0
indlist=copy.deepcopy(linddlist)
while len(indlist[0])>0:
	if type(indlist[0].index(np.min(indlist[0])))!=int:
		imin=indlist[0].index(np.min(indlist[0]))[0]
	else:
		imin=indlist[0].index(np.min(indlist[0]))
	fluxt+=indlist[1][imin]
	fluxc[0].append(np.min(indlist[0]))
	fluxc[1].append(fluxt)
	try:
		for j in range(1000):
			indlist[0].pop(imin)
			indlist[1].pop(imin)
	except:
		pass
	print len(indlist[0])

fig1=plt.figure(figsize=(8,8))
plt.plot(fluxc[0],fluxc[1])
plt.xlabel('r (pix)')
plt.ylabel('Counts (bck corrected)')
#plt.show()
plt.savefig('growth_curve_bcg_360_3.png')
plt.close(fig1)