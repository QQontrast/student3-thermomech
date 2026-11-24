# student3-thermomech — S3, ТЗ v2.0

Термомеханика: T -> eps_th -> sigma -> остаточная форма -> допуски.
Материал: сталь 45 / AISI 1045. Объекты: P01 (пластина), R01 (кольцо).

## Среда
Ubuntu 22.04.5 LTS, WSL2; OpenFOAM v2406 (ESI); Python 3.10 (venv ~/venvs/cae).
Снимки среды: env/. Активация: source ~/venvs/cae/bin/activate

## Запуск всего (воспроизводимость, A12)
    ./Allrun

Allrun генерирует слот стадии 1 из FIP (as-is), строит и считает кейсы 00-03,
проверяет тракт интерполяции (A5), гоняет юнит-тест овальности (C17) и km.py,
собирает results/verification_table.md.

## Структура (ТЗ 6.1)
FIP-1.0/   входной пакет AS RECEIVED, без изменений (добавлен git add -f)
env/ thermal_input/ cases/ scripts/ src/ out/ results/ doc/ issues/
material -> FIP-1.0/material (симлинк для скриптов FIP)
thermal_input/active -> stage1_fixture

## Статус (неделя 1)
- A0: словари/единицы/тип alpha/Tref по исходнику — выполнено.
- A1 PASS 0%: -252 / -360 / -630 МПа. Заморозка T: max|T-100| = 0.
- A2-A4 FAIL: ограничение стокового сегрегированного решателя;
  числа и причина в doc/report.md и issues/question-01.
- Слот стадии 1: R01 (66,37800), P01 (71,72900), Кельвины.
- A5 PASS по интегралу <=0.43% (порог 2%), карта ошибки в results/.
- C17 PASS: юнит-тест овальности 1.2e-4 = 4A.
- Не сделано: A6-A13, уровни B/C. План — issues/weekly-1.md.

## Тяжёлые данные
Поля ([0-9]*/, *.vtk, *.npz) не в git; суммы — results/checksums.sha256.
Слот регенерируется Allrun из FIP. Данных заказчика нет: всё модельное.