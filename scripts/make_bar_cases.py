#!/usr/bin/env python3
import os
FACES = {'x0':'(0 4 7 3)','x1':'(1 2 6 5)','y0':'(0 1 5 4)',
         'y1':'(3 7 6 2)','z0':'(0 3 2 1)','z1':'(4 5 6 7)'}
VAR = {'1D':({'x0','x1','y0','z0'},(-252,0,0)),
       '2D':({'x0','x1','y0','y1','z0'},(-360,-360,0)),
       '3D':({'x0','x1','y0','y1','z0','z1'},(-630,-630,-630))}
H = 'FoamFile{version 2.0; format ascii; class %s; object %s;}\n'
FS = H%('dictionary','fvSchemes') + '''ddtSchemes{default Euler;}
d2dt2Schemes{default steadyState;}
gradSchemes{default Gauss linear;}
divSchemes{default Gauss linear;}
laplacianSchemes{default Gauss linear corrected;}
interpolationSchemes{default linear;}
snGradSchemes{default corrected;}
'''
FV = H%('dictionary','fvSolution') + '''solvers{
 D{solver PCG;preconditioner DIC;tolerance 1e-09;relTol 0.9;}
 DFinal{$D;relTol 0;}
 T{solver PCG;preconditioner DIC;tolerance 1e-09;relTol 0.9;}
 TFinal{$T;relTol 0;}}
stressAnalysis{nCorrectors 300;D 1e-09;T 1e-09;compactNormalStress yes;}
'''
CD = H%('dictionary','controlDict') + '''application solidDisplacementFoam;startFrom startTime;startTime 0;
stopAt endTime;endTime 1;deltaT 1;writeControl runTime;writeInterval 1;
writeFormat ascii;purgeWrite 0;runTimeModifiable yes;
'''
for v,(sym,exp) in VAR.items():
    d = f'cases/00_bar/run_{v}'
    for s in ('0','constant','system'): os.makedirs(d+'/'+s, exist_ok=True)
    open(d+'/system/fvSchemes','w').write(FS)
    open(d+'/system/fvSolution','w').write(FV)
    open(d+'/system/controlDict','w').write(CD)
    open(d+'/constant/mechanicalProperties','w').write(H%('dictionary','mechanicalProperties')+
        'rho{type uniform;value 7850;}\nnu{type uniform;value 0.3;}\nE{type uniform;value 2.1e11;}\nplaneStress no;\n')
    open(d+'/constant/thermalProperties','w').write(H%('dictionary','thermalProperties')+
        'C{type uniform;value 470;}\nk{type uniform;value 1e-12;}\nalpha{type uniform;value 12e-6;}\nthermalStress yes;\n')
    b = ['scale 1;','vertices ((0 0 0)(0.01 0 0)(0.01 0.01 0)(0 0.01 0)(0 0 0.01)(0.01 0 0.01)(0.01 0.01 0.01)(0 0.01 0.01));',
         'blocks (hex (0 1 2 3 4 5 6 7) (10 10 10) simpleGrading (1 1 1));','edges ();','boundary (']
    for f,fc in FACES.items():
        b.append(f' {f} {{type {"symmetryPlane" if f in sym else "patch"};faces ({fc});}}')
    b.append(');')
    open(d+'/system/blockMeshDict','w').write(H%('dictionary','blockMeshDict')+'\n'.join(b))
    D = H%('volVectorField','D')+'dimensions [0 1 0 0 0 0 0];\ninternalField uniform (0 0 0);\nboundaryField{'
    T = H%('volScalarField','T')+'dimensions [0 0 0 1 0 0 0];\ninternalField uniform 100;\nboundaryField{'
    for f in FACES:
        D += (f'{f}{{type symmetryPlane;}}' if f in sym else
              f'{f}{{type tractionDisplacement;traction uniform (0 0 0);pressure uniform 0;value uniform (0 0 0);}}')
        T += (f'{f}{{type symmetryPlane;}}' if f in sym else f'{f}{{type zeroGradient;}}')
    open(d+'/0/D','w').write(D+'}')
    open(d+'/0/T','w').write(T+'}')
    print(v,'expected MPa =',exp)