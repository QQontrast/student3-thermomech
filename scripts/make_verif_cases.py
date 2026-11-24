#!/usr/bin/env python3
import os
H='FoamFile{version 2.0; format ascii; class %s; object %s;}\n'
FS=H%('dictionary','fvSchemes')+'''ddtSchemes{default Euler;}
d2dt2Schemes{default steadyState;}
gradSchemes{default Gauss linear;}
divSchemes{default Gauss linear;}
laplacianSchemes{default Gauss linear corrected;}
interpolationSchemes{default linear;}
snGradSchemes{default corrected;}
'''
FV=H%('dictionary','fvSolution')+'''solvers{
D{solver PCG;preconditioner DIC;tolerance 1e-09;relTol 0;}
DFinal{$D;relTol 0;}
T{solver PCG;preconditioner DIC;tolerance 1e-09;relTol 0;}
TFinal{$T;relTol 0;}}
stressAnalysis{nCorrectors 2000;D 1e-09;T 1e-09;compactNormalStress yes;}
'''
CD=H%('dictionary','controlDict')+'''application solidDisplacementFoam;startFrom startTime;startTime 0;
stopAt endTime;endTime 1;deltaT 1;writeControl runTime;writeInterval 1;
writeFormat ascii;purgeWrite 0;runTimeModifiable yes;
'''
def base(d,plane):
    for s in ('0','constant','system'): os.makedirs(d+'/'+s,exist_ok=True)
    open(d+'/system/fvSchemes','w').write(FS); open(d+'/system/fvSolution','w').write(FV)
    open(d+'/system/controlDict','w').write(CD)
    open(d+'/constant/mechanicalProperties','w').write(H%('dictionary','mechanicalProperties')+
      'rho{type uniform;value 7850;}\nnu{type uniform;value 0.3;}\nE{type uniform;value 2.1e11;}\nplaneStress %s;\n'%plane)
    open(d+'/constant/thermalProperties','w').write(H%('dictionary','thermalProperties')+
      'C{type uniform;value 470;}\nk{type uniform;value 1e-12;}\nalpha{type uniform;value 12e-6;}\nthermalStress yes;\n')
def setT(d,expr):
    open(d+'/system/setExprFieldsDict','w').write(H%('dictionary','setExprFieldsDict')+
      'expressions ( T { field T; expression "%s"; } );\n'%expr)
TR='type tractionDisplacement;traction uniform (0 0 0);pressure uniform 0;value uniform (0 0 0);'
# --- 01_bending ---
d='cases/01_bending'; base(d,'no')
b=['scale 1;','vertices ((0 0 0)(0.1 0 0)(0.1 0.01 0)(0 0.01 0)(0 0 0.016)(0.1 0 0.016)(0.1 0.01 0.016)(0 0.01 0.016));',
   'blocks (hex (0 1 2 3 4 5 6 7) (100 10 16) simpleGrading (1 1 1));','edges ();','boundary (']
F={'x0':'(0 4 7 3)','x1':'(1 2 6 5)','y0':'(0 1 5 4)','y1':'(3 7 6 2)','z0':'(0 3 2 1)','z1':'(4 5 6 7)'}
for f,fc in F.items(): b.append(f' {f} {{type patch;faces ({fc});}}')
b.append(');'); open(d+'/system/blockMeshDict','w').write(H%('dictionary','blockMeshDict')+'\n'.join(b))
D=H%('volVectorField','D')+'dimensions [0 1 0 0 0 0 0];\ninternalField uniform (0 0 0);\nboundaryField{'
T=H%('volScalarField','T')+'dimensions [0 0 0 1 0 0 0];\ninternalField uniform 0;\nboundaryField{'
for f in F:
    D += ('x0{type fixedValue;value uniform (0 0 0);}' if f=='x0' else f'{f}{{{TR}}}')
    T += f'{f}{{type zeroGradient;}}'
open(d+'/0/D','w').write(D+'}'); open(d+'/0/T','w').write(T+'}')
setT(d,'100*((pos() & vector(0,0,1))/0.016 - 0.5)')

RING=['scale 1;','vertices ((0.275 0 0)(0.291 0 0)(0 0.291 0)(0 0.275 0)(0.275 0 0.001)(0.291 0 0.001)(0 0.291 0.001)(0 0.275 0.001));',
 'blocks (hex (0 1 2 3 4 5 6 7) (24 96 1) simpleGrading (3 1 1));',
 'edges (arc 1 2 (0.2057681 0.2057681 0) arc 0 3 (0.1944544 0.1944544 0) arc 5 6 (0.2057681 0.2057681 0.001) arc 4 7 (0.1944544 0.1944544 0.001));',
 'boundary (bore{type patch;faces ((0 4 7 3));} outer{type patch;faces ((1 2 6 5));} phi0{type symmetryPlane;faces ((0 1 5 4));} phi90{type symmetryPlane;faces ((3 7 6 2));} frontAndBack{type empty;faces ((0 3 2 1)(4 5 6 7));});']
for name,uniform,expr in (('02_ring_gradient',False,'100*log(0.291/mag(pos()))/log(0.291/0.275)'),
                          ('03_ring_free',True,None)):
    d='cases/'+name; base(d,'yes')
    open(d+'/system/blockMeshDict','w').write(H%('dictionary','blockMeshDict')+'\n'.join(RING))
    D=H%('volVectorField','D')+'dimensions [0 1 0 0 0 0 0];\ninternalField uniform (0 0 0);\nboundaryField{'
    T=H%('volScalarField','T')+'dimensions [0 0 0 1 0 0 0];\ninternalField uniform %s;\nboundaryField{'%('100' if uniform else '0')
    for f in ('bore','outer','phi0','phi90','frontAndBack'):
        if f in ('phi0','phi90'): Db='type symmetryPlane;'; Tb='type symmetryPlane;'
        elif f=='frontAndBack': Db='type empty;'; Tb='type empty;'
        else: Db=TR; Tb='type zeroGradient;'
        D+=f'{f}{{{Db}}}'; T+=f'{f}{{{Tb}}}'
    open(d+'/0/D','w').write(D+'}'); open(d+'/0/T','w').write(T+'}')
    if expr: setT(d,expr)
print('built 01_bending, 02_ring_gradient, 03_ring_free')