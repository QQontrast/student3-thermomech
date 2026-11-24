import sys, glob, numpy as np
def field(p):
    t=open(p).read(); seg=t.split('internalField')[1].split('boundaryField')[0]
    if 'nonuniform' in seg:
        body=seg[seg.index('(')+1:seg.rindex(')')]
        rows=[l.strip().strip('()').split() for l in body.splitlines() if l.strip().strip('()')]
        return np.array([[float(x) for x in r] for r in rows])
    if '(' in seg: return np.array([[float(x) for x in seg[seg.index('(')+1:seg.index(')')].split()]])
    return np.array([[float(seg.split()[1])]])
def centres(d):
    return field(sorted(glob.glob(d+'/*/C'))[-1])
a,b,E,nu,al,dT=0.275,0.291,210e9,0.3,12e-6,100.0
def ring(r):
    L=np.log(b/a); C=al*E*dT/(2*(1-nu)*L); k=a*a/(b*b-a*a)
    return C*(1-np.log(b/r)-k*(1+b*b/r**2)*L)
w=sys.argv[1]
if w=='bending':
    D=field('cases/01_bending/1/D'); s=field('cases/01_bending/1/sigmaEq')
    print('A2 delta_tip mm =',round(D[:,2].max()*1e3,4),' (ref 0.375) | max sigmaEq MPa =',round(s.max()/1e6,3),' (<=5)')
else:
    d='cases/'+('02_ring_gradient' if w=='grad' else '03_ring_free')
    C=centres(d); r=np.hypot(C[:,0],C[:,1]); phi=np.arctan2(C[:,1],C[:,0])
    i,j=np.argmin(r),np.argmax(r)
    if w=='grad':
        s=field(d+'/1/sigma')
        st=s[:,0]*np.sin(phi)**2+s[:,3]*np.cos(phi)**2-2*s[:,1]*np.sin(phi)*np.cos(phi)
        print('A3 bore MPa =',round(st[i]/1e6,1),' ref',round(ring(r[i])/1e6,1),
              '| outer =',round(st[j]/1e6,1),' ref',round(ring(r[j])/1e6,1))
    else:
        D=field(d+'/1/D'); s=field(d+'/1/sigmaEq')
        ur=D[i,0]*np.cos(phi[i])+D[i,1]*np.sin(phi[i])
        print('A4 delta_d mm =',round(2*ur*1e3,4),' (ref 0.660) | max sigmaEq MPa =',round(s.max()/1e6,3),' (<=2)')
