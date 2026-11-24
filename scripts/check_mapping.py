import sys, numpy as np
sys.path.insert(0, 'scripts')
import map_thermal as mt
from scipy.interpolate import RegularGridInterpolator
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

slot = 'thermal_input/stage1_fixture'
times, T, p = mt.load_slot(slot)
canon = p[['x_m','y_m','z_m']].values
rc = np.hypot(canon[:,0], canon[:,1])
pc = np.mod(np.arctan2(canon[:,1], canon[:,0]), 2*np.pi)
q = np.column_stack([rc, pc, canon[:,2]])
T0 = 293.15

# staggered "механические" центры: тот же шаг, что канон, сдвиг пол-ячейки
r  = 0.275 + 0.000125 + np.arange(24)*0.00025
ph = np.deg2rad(2.5 + np.arange(72)*5.0)
z  = 0.001 + np.arange(20)*0.002
R,P,Z = np.meshgrid(r, ph, z, indexing='ij')
cent = np.column_stack([(R*np.cos(P)).ravel(), (R*np.sin(P)).ravel(), Z.ravel()])
ph_ext = np.concatenate([ph[:1]-2*np.pi, ph, ph[-1:]+2*np.pi])  # шов с обеих сторон

ks = [0, int(np.argmin(abs(times-7.0))), int(np.argmin(abs(times-30.0))), len(times)-1]
worst = None
for k in ks:
    Trow = np.asarray(T[k], dtype=float)
    fwd = mt.ring_interp(Trow)
    node_err = float(np.max(np.abs(fwd(canon) - Trow)))     # проверка 1: прямой в узлах
    Tc = fwd(cent).reshape(24,72,20)
    Tg = np.concatenate([Tc[:, -1:, :], Tc, Tc[:, :1, :]], axis=1)
    rev = RegularGridInterpolator((r, ph_ext, z), Tg, bounds_error=False, fill_value=None)
    Tb = rev(q)
    e = np.abs(Tb - Trow)
    den = max(np.max(np.abs(Trow - T0)), 1.0)
    rel_max = float(e.max()/den)
    rel_int = float((e*rc).sum()/max((np.abs(Trow-T0)*rc).sum(), 1e-12))
    i = int(np.argmax(e))
    print('t=%6.1f s | forward@nodes=%.2e K | rel_max=%.4f rel_int=%.4f | worst r=%.4f phi=%.1f z=%.3f T_in=%.1f T_back=%.1f'
          % (times[k], node_err, rel_max, rel_int, rc[i], np.degrees(pc[i]), canon[i,2], Trow[i], Tb[i]))
    if worst is None or rel_int > worst[0]:
        worst = (rel_int, times[k], e)

rel_int, tw, e = worst
np.save('results/mapping_error_R01.npy', e)
plt.figure()
sc = plt.scatter(np.degrees(pc), rc, c=e, s=2, cmap='viridis')
plt.colorbar(sc, label='|T_back - T_in|, K')
plt.xlabel('phi, deg'); plt.ylabel('r, m')
plt.title('A5 mapping error R01, t=%g s (rel_int=%.4f)' % (tw, rel_int))
plt.tight_layout(); plt.savefig('results/fig_mapping_error_R01.png', dpi=300)
print('saved results/fig_mapping_error_R01.png ; integral <=0.02:', 'PASS' if rel_int <= 0.02 else 'FAIL')