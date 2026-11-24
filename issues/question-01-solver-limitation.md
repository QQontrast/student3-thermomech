# question-01: ограничение стокового решателя на A2–A4
Цель: закрыть fail-gates A2–A4 (по 12 их провал = задача не сдана).
Что сделал: 4 теста. A1 PASS 0%. A2 delta 0.0013 мм при sigma 119.3 МПа
(невязки корректоров стоят ~2e-5). A3 −126.1/+117.1 вместо −179.3/+164.8.
A4 delta_d 0.6604 мм (верно), но sigmaEq 193.9 МПа при planeStress+empty.
Команда: cd cases/01_bending && solidDisplacementFoam > log.run; tail -15 log.run
Лог: results/allrun.log, cases/*/log.run. Версия ПО: OpenFOAM v2406 (ESI).
Вопрос: согласовать путь закрытия A2–A4 —
(1) solids4foam на поддерживаемой версии ESI рядом (5.6), либо
(2) solidEquilibriumDisplacementFoam. Какой приоритетнее?