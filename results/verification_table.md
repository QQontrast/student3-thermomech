# Таблица верификации — фактические прогоны (ТЗ 8.1, 12)

| Код | Вывод проверки | Отклонение / порог | Статус |
|---|---|---|---|
| A1 1D | `1D sigma_xx,yy,zz MPa = -252.0 0.0 0.0` | max 0.00% (порог 1%) | **PASS** |
| A1 2D | `2D sigma_xx,yy,zz MPa = -360.0 -360.0 -0.0` | max 0.00% (порог 1%) | **PASS** |
| A1 3D | `3D sigma_xx,yy,zz MPa = -630.0 -630.0 -630.0` | max 0.00% (порог 1%) | **PASS** |
| A2 | `A2 delta_tip mm = 0.0013  (ref 0.375) \| max sigmaEq MPa = 119.328  (<=5)` | delta 99.7% (порог 2%); sigma 119.3 МПа (порог 5) | **FAIL** |
| A3 | `A3 bore MPa = -126.1  ref -179.3 \| outer = 117.1  ref 164.8` | bore 29.7%, outer 28.9% (порог 3%) | **FAIL** |
| A4 | `A4 delta_d mm = 0.6604  (ref 0.660) \| max sigmaEq MPa = 193.852  (<=2)` | delta_d 0.06% (порог 1%); sigma 193.9 МПа (порог 2) | **FAIL** |
| A5 | `t=   0.0 s \| forward@nodes=1.68e-03 K \| rel_max=0.6556 rel_int=0.0043 \| worst r=0.2755 phi=0.0 z=0.020 T_in=2007.2 T_back=883.4` | rel_int 0.43% (порог 2%) | **PASS** |
| A5 | `t=   7.0 s \| forward@nodes=1.99e-03 K \| rel_max=0.2773 rel_int=0.0019 \| worst r=0.2750 phi=15.0 z=0.020 T_in=573.8 T_back=496.0` | rel_int 0.19% (порог 2%) | **PASS** |
| A5 | `t=  30.0 s \| forward@nodes=9.34e-03 K \| rel_max=0.6471 rel_int=0.0042 \| worst r=0.2755 phi=30.0 z=0.020 T_in=1211.5 T_back=617.3` | rel_int 0.42% (порог 2%) | **PASS** |
| A5 | `t= 200.0 s \| forward@nodes=1.04e-05 K \| rel_max=0.6471 rel_int=0.0043 \| worst r=0.2755 phi=30.0 z=0.020 T_in=294.2 T_back=293.5` | rel_int 0.43% (порог 2%) | **PASS** |
| A5 интеграл max | `worst rel_int = 0.0043` | порог 2% | **PASS** |
| C17 | `unit test ovality: 1.200e-04 expected 1.200e-04 -> PASS` | юнит-тест 4A | **PASS** |
| T freeze (4.5) | `max\|T-100\| = 0 K (min 100, max 100)` | поле T не эволюционировало | **PASS** |
| FIP integrity | `FIP RESULT: OK` | манифест без изменений | **PASS** |

Расхождения >1% объяснены в doc/report.md (раздел 4) и issues/question-01-solver-limitation.md.
