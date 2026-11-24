# A0: словарь — запись — смысл — единицы — где в исходнике
OpenFOAM v2406 (ESI). Путь: $FOAM_SOLVERS/stressAnalysis/solidDisplacementFoam/

| Словарь | Запись | Смысл | Единицы | Источник |
|---|---|---|---|---|
| mechanicalProperties | rho{type uniform\|field; value} | плотность | кг/м3 | readMechanicalProperties.H:16,31 |
| mechanicalProperties | E{type uniform\|field; value} | модуль Юнга | Па | :71,86 (внутр. имя Erho, dims Па; туториал 2e11) |
| mechanicalProperties | nu{type uniform\|field; value} | Пуассон | – | :137,141 |
| mechanicalProperties | planeStress yes/no | плоское напряжение | bool | :187 |
| thermalProperties | thermalStress yes/no | вкл. термочлен | bool | readThermalProperties.H:15 |
| thermalProperties | C{type uniform\|field; value} | теплоёмкость | Дж/(кг К) | :61,64 |
| thermalProperties | k{type uniform\|field; value} | теплопроводность (внутри k/rho) | Вт/(м К) | :116,119; DT=k/C |
| thermalProperties | alpha{type uniform\|field; value} | КТР, СЕКУЩИЙ | 1/К | :172,176; threeKalpha=threeK*alpha :219 |
| fvSolution | подсловарь stressAnalysis (НЕ stressControl) | управления | – | readSolidDisplacementFoamControls.H |
| fvSolution | nCorrectors | внешние корректоры | int, optional (default 1) | getOrDefault<int> |
| fvSolution | D | допуск по перемещениям | scalar, ОБЯЗАТЕЛЕН | get<scalar>("D") |
| fvSolution | compactNormalStress | форма норм. напряжений | bool, ОБЯЗАТЕЛЕН | get<bool> |
| 0/T | dimensions [0 0 0 1 0 0 0] | подаём dT = T − Tref | К (разность) | grep Tref по решателю — пусто |
| ГУ | tractionDisplacement (НЕ solidTraction) | свободная грань | – | tractionDisplacement/*.C:164,182,189 |
| ГУ | constraint-патчи (symmetryPlane, empty) требуют одноимённого ГУ для ВСЕХ полей, включая T | – | – | fatal IO error при zeroGradient на symmetryPlane |
| сборка | DEqn += fvc::grad(threeKalpha*T) | термочлен | – | solidDisplacementFoam.C:101 |
| сборка | sigma = sigma − I*(rho*threeKalpha*T) | термочлен | – | calculateStress.H:19 |
| вывод | D, T, sigma, sigmaEq | – | – | файлы 1/*, Max sigmaEq в логе |
| symmTensor | порядок xx,xy,xz,yy,yz,zz (yy = индекс 3) | – | – | проверено на тесте 1 |
| формат | подсловари type/value, НЕ плоские dimensionedScalar (шаблон ТЗ 9.2 копировать нельзя); type field позволяет alpha(T(x)), E(T(x)) | – | – | туториал plateHole/constant |

## Ответы на вопросы 5.4
1. Имена/единицы — таблица выше.
2. alpha — СЕКУЩИЙ, входит линейно как alpha*T.
3. Tref ОТСУТСТВУЕТ -> отсчёт зашивается в подаваемое dT.
4. Переключатель planeStress в mechanicalProperties.
5. stressAnalysis/nCorrectors — число внешних корректоров сегрегированного цикла;
   D — допуск; compactNormalStress — формулировка (на сошедшийся ответ не влияет).
6. Поля: D, T, sigma, sigmaEq.

## Карта материала (частично; литературная сверка — pending)
Значения FIP 2.1. km.py: CE_IIW = 0.6283; Ms_Andrews = 321.9 C.
Сверить с ASM Handbook Vol.4, EN 1011-2, Koistinen–Marburger (1959), Andrews (1965).