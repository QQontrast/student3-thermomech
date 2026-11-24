# A12: воспроизводимость (чистый клон -> Allrun -> те же таблицы)

Проверка выполнена 24.11.2026, Ubuntu 22.04 WSL2, OpenFOAM v2406 (ESI).
Проверяемый коммит: fc9a619 (git rev-parse --short HEAD на момент клонирования).
Данный файл с доказательством добавлен следующим коммитом после проверки.

Команды:
    git clone ~/cae/student3-thermomech /tmp/s3-clone
    cd /tmp/s3-clone && source ~/venvs/cae/bin/activate && ./Allrun
    diff results/verification_table.md \
         ~/cae/student3-thermomech/results/verification_table.md

Результат: diff пуст, вывод "A12: TABLES IDENTICAL" -> таблицы побайтово
идентичны. Критерий A12 подтверждён.

Клон не содержит тяжёлых данных (grid_T.npz, временные каталоги 1/, *.npy
в .gitignore). Allrun сам:
- проверяет целостность FIP (verify_fip.py -> FIP RESULT: OK);
- генерирует слот стадии 1 из FIP as-is (R01 и P01);
- строит и считает кейсы 00-03 (blockMesh, checkMesh, setExprFields, решатель);
- проверяет тракт интерполяции A5 и юнит-тест овальности C17;
- собирает results/verification_table.md.

Совпавшие ключевые числа: A1 -252.0/-360.0/-630.0 МПа; A2 delta 0.0013 мм,
sigmaEq 119.328 МПа; A3 -126.1/+117.1; A4 0.6604 мм / 193.852 МПа;
A5 rel_int <= 0.0043; C17 1.200e-04; max|T-100| = 0 K.

Логи: results/a12_clone_allrun.log (прогон в клоне), results/allrun.log (исходный).
Контрольные суммы тяжёлых файлов: results/checksums.sha256.