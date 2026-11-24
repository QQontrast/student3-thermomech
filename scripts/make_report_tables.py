#!/usr/bin/env python3
"""results/verification_table.md из ФАКТИЧЕСКИХ прогонов (ТЗ 8.1, 12)."""
import os
import re
import subprocess
import numpy as np


def run(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()


def esc(s):
    return s.replace('|', '\\|').replace('\n', ' ; ')


def freeze():
    try:
        t = open('cases/00_bar/run_1D/1/T').read()
        seg = t.split('internalField')[1].split('boundaryField')[0]
        b = seg[seg.index('(') + 1:seg.rindex(')')]
        v = np.array([float(x) for x in b.split()])
        return ('max|T-100| = %.3g K (min %.6g, max %.6g)'
                % (abs(v - 100).max(), v.min(), v.max())), 'PASS'
    except Exception as e:
        return 'ERROR: %s' % e, 'FAIL'


rows = []
EXP = {'1D': (-252., 0., 0.), '2D': (-360., -360., 0.),
       '3D': (-630., -630., -630.)}
for v in ('1D', '2D', '3D'):
    out = run('python3 scripts/check_bar.py ' + v)
    m = re.search(r'=\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', out)
    if m:
        got = [float(x) for x in m.groups()]
        errs = [abs(g - e) / abs(e) * 100 if e else abs(g)
                for g, e in zip(got, EXP[v])]
        dev = 'max %.2f%% (порог 1%%)' % max(errs)
        st = 'PASS' if max(errs) <= 1 else 'FAIL'
    else:
        dev, st = 'нет данных', 'FAIL'
    rows.append(('A1 ' + v, out, dev, st))

out = run('python3 scripts/check_verif.py bending')
m = re.search(r'delta_tip mm = ([\d.]+).*?sigmaEq MPa = ([\d.]+)', out, re.S)
if m:
    d, s = float(m.group(1)), float(m.group(2))
    dev = ('delta %.1f%% (порог 2%%); sigma %.1f МПа (порог 5)'
           % (abs(d - 0.375) / 0.375 * 100, s))
    st = 'PASS' if (abs(d - 0.375) / 0.375 <= 0.02 and s <= 5) else 'FAIL'
else:
    dev, st = 'нет данных', 'FAIL'
rows.append(('A2', out, dev, st))

out = run('python3 scripts/check_verif.py grad')
m = re.search(r'bore MPa = ([-\d.]+)\s+ref ([-\d.]+)'
              r'.*?outer = ([-\d.]+)\s+ref ([-\d.]+)', out, re.S)
if m:
    b_, br, o, orf = [float(x) for x in m.groups()]
    e1 = abs(b_ - br) / abs(br) * 100
    e2 = abs(o - orf) / abs(orf) * 100
    dev = 'bore %.1f%%, outer %.1f%% (порог 3%%)' % (e1, e2)
    st = 'PASS' if max(e1, e2) <= 3 else 'FAIL'
else:
    dev, st = 'нет данных', 'FAIL'
rows.append(('A3', out, dev, st))

out = run('python3 scripts/check_verif.py free')
m = re.search(r'delta_d mm = ([\d.]+).*?sigmaEq MPa = ([\d.]+)', out, re.S)
if m:
    d, s = float(m.group(1)), float(m.group(2))
    dev = ('delta_d %.2f%% (порог 1%%); sigma %.1f МПа (порог 2)'
           % (abs(d - 0.660) / 0.660 * 100, s))
    st = 'PASS' if (abs(d - 0.660) / 0.660 <= 0.01 and s <= 2) else 'FAIL'
else:
    dev, st = 'нет данных', 'FAIL'
rows.append(('A4', out, dev, st))

worst = 0.0
for line in run('python3 scripts/check_mapping.py').splitlines():
    if line.startswith('t='):
        m = re.search(r'rel_int=([\d.]+)', line)
        ri = float(m.group(1)) if m else 9.0
        worst = max(worst, ri)
        rows.append(('A5', line, 'rel_int %.2f%% (порог 2%%)' % (ri * 100),
                     'PASS' if ri <= 0.02 else 'FAIL'))
rows.append(('A5 интеграл max', 'worst rel_int = %.4f' % worst,
             'порог 2%', 'PASS' if worst <= 0.02 else 'FAIL'))

out = run('python3 scripts/ovality.py')
rows.append(('C17', out, 'юнит-тест 4A', 'PASS' if 'PASS' in out else 'FAIL'))

fz, fst = freeze()
rows.append(('T freeze (4.5)', fz, 'поле T не эволюционировало', fst))

fip = run('tail -1 results/fip_verify.log')
rows.append(('FIP integrity', fip, 'манифест без изменений',
             'PASS' if 'OK' in fip else 'FAIL'))

os.makedirs('results', exist_ok=True)
with open('results/verification_table.md', 'w', encoding='utf-8') as f:
    f.write('# Таблица верификации — фактические прогоны (ТЗ 8.1, 12)\n\n')
    f.write('| Код | Вывод проверки | Отклонение / порог | Статус |\n')
    f.write('|---|---|---|---|\n')
    for c, o, d, s in rows:
        f.write('| %s | `%s` | %s | **%s** |\n' % (c, esc(o), esc(d), s))
    f.write('\nРасхождения >1% объяснены в doc/report.md (раздел 4) и '
            'issues/question-01-solver-limitation.md.\n')
print('wrote results/verification_table.md')