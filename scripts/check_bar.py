import sys, numpy as np
v = sys.argv[1]
txt = open(f'cases/00_bar/run_{v}/1/sigma').read()
seg = txt.split('internalField')[1].split('boundaryField')[0]   # только internalField
if 'nonuniform' in seg:
    body = seg[seg.index('(')+1 : seg.rindex(')')]
    rows = [l.strip().strip('()').split() for l in body.splitlines()]
    s = np.array([[float(x) for x in r] for r in rows if len(r) == 6])
else:  # uniform
    t = seg[seg.index('(')+1 : seg.index(')')].split()
    s = np.array([[float(x) for x in t]])
print(v, 'sigma_xx,yy,zz MPa =',
      round(s[:,0].mean()/1e6,1), round(s[:,3].mean()/1e6,1), round(s[:,5].mean()/1e6,1))