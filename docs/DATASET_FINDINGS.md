# Что на самом деле оценивает датасет организаторов

Разобран `organizer_examples_v4.0.xlsx`: 21 эталонный пример — 10 для технических специалистов и 11 для руководства/работников.

## 1. Это две разные задачи, а не один summarizer

### Technical digest
Организатор ожидает три класса: **Атака / Уязвимость / Инфо**.

Приоритеты явно заданы:
- атака: высокий = РФ + энергетика; средний = РФ + другие отрасли; низкий = вне РФ;
- уязвимость: высокий = есть exploit; средний = exploit отсутствует;
- инфо: отдельный поток Telegram.

Главное: технический вывод должен быть **структурированным extraction**, а не свободным summary.
Для атаки ожидаются 8 полей (страна, actor, дата, отрасли, initial access, tools, vulnerabilities, IOC).
Для уязвимости — 10 полей (product/version, description, patch/workaround, exploit, CVE/CVSS, impact).

### Executive digest
Здесь вместо технической схемы используется multi-label business taxonomy из 12 признаков: РФ/не РФ, финансовый ущерб, КИИ, энергетика, промышленность, репутация, утечки, regulation, массовые сервисы, события и unusual stories.
Форма вывода намеренно короткая: **заголовок + 3–4 строки + первоисточники**.

## 2. Event-centric clustering обязателен
Первый executive пример объединяет две публикации об атаке на Аэрофлот в одно событие с двумя ссылками. Значит dedup/event fusion — не декоративная фича, а поведение, показанное самим golden dataset.

## 3. Энергетика должна быть first-class signal
В executive golden set отдельно присутствуют SCADA/энергетика и атака на дамбу. В technical правилах энергетический сектор повышает приоритет атак до высокого.

## 4. Telegram нельзя терять
Technical dataset содержит три Telegram-примера и большой список каналов. Нужен отдельный Telegram connector/snapshot adapter, extraction внешних ссылок и нормализация obfuscated URL (`[.]`).

## 5. Что меряем
- relevance: Precision@K / Recall@K;
- ranking: NDCG@K с priority labels;
- classification: macro F1 для Атака/Уязвимость/Инфо;
- executive tagging: micro/macro F1 по 12 тегам;
- extraction: field-level exact/semantic match;
- clustering: pairwise F1 + duplicate reduction;
- groundedness: доля утверждений с evidence/source.

## Winning gate
Перед защитой нельзя ограничиваться визуальным демо. В репозитории должен лежать воспроизводимый evaluation report на frozen corpus с baseline и финальной конфигурацией.
