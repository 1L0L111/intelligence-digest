"""Golden benchmark distilled from the organizer-provided XLSX.

This module intentionally stores normalized labels rather than depending on Excel at runtime.
The original workbook should remain in data/reference/ for auditability.
"""
from __future__ import annotations

from dataclasses import dataclass

TECHNICAL_OUTPUT_FIELDS = {
    "Атака": ["victim_country", "threat_actor", "attack_date", "affected_sectors", "initial_access", "tools", "vulnerabilities", "iocs_present"],
    "Уязвимость": ["vulnerability_name", "affected_product", "description", "patch", "workaround", "exploit_available", "cve", "cvss", "cvss_vector", "impact"],
    "Инфо": ["summary", "referenced_links"],
}

TECHNICAL_PRIORITY_RULES = {
    "Атака": {"Высокий": "РФ + энергетика", "Средний": "РФ + другие сектора", "Низкий": "не РФ"},
    "Уязвимость": {"Высокий": "есть публичный эксплойт", "Средний": "нет эксплойта"},
    "Инфо": {"Новости ТГ": "релевантная новость из Telegram"},
}

EXECUTIVE_TAGS = [
    "В РФ", "Вне РФ", "Крупные финансовые потери", "Нарушение работы критической инфраструктуры",
    "Энергетика", "Промышленность", "Имиджевые потери", "Утечки чувствительной информации",
    "Госсектор и правовое поле", "Массово используемый сервис", "Трудовой ресурс/мероприятия",
    "Может быть интересно",
]

@dataclass(frozen=True)
class GoldenExample:
    audience: str
    category: str
    priority: str | None
    title: str
    url: str
    tags: tuple[str, ...] = ()

# 10 technical + 11 executive examples from the organizer workbook.
GOLDEN_EXAMPLES = [
    GoldenExample("technical", "Атака", "Высокий", "Атака PhantomCore на организации промышленного сектора РФ", "https://www.f6.ru/blog/phantomcore-newtools/"),
    GoldenExample("technical", "Атака", "Высокий", "Атаки Head Mare на организации образования, научных учреждений, энергетики РФ", "https://securelist.ru/head-mare-campaign-phantompxpigeon-backdoor-and-trueconf-software/114998/"),
    GoldenExample("technical", "Атака", "Высокий", "Атака Silver Dragon на государственные учреждения Европы и Юго-Восточной Азии", "https://research.checkpoint.com/2026/silver-dragon-targets-organizations-in-southeast-asia-and-europe/"),
    GoldenExample("technical", "Уязвимость", "Высокий", "Уязвимость Axios", "https://dbugs.ptsecurity.com/vulnerability/PT-2023-8832"),
    GoldenExample("technical", "Уязвимость", "Высокий", "Уязвимость Confluence", "https://dbugs.ptsecurity.com/vulnerability/PT-2021-7092"),
    GoldenExample("technical", "Уязвимость", "Средний", "Уязвимость Red OS", "https://dbugs.ptsecurity.com/vulnerability/PT-2026-30609"),
    GoldenExample("technical", "Уязвимость", "Средний", "Уязвимость WSUS", "https://securelist.ru/cve-2025-59287-wsus-exploitation-detection-in-ngfw-kes-kata-edr/114105/"),
    GoldenExample("technical", "Инфо", "Новости ТГ", "Windows Defender: три уязвимости и PoC", "https://t.me/true_secator/8113"),
    GoldenExample("technical", "Инфо", "Новости ТГ", "WebClient/SCCM и NTLM relay", "https://t.me/purpleshift/174"),
    GoldenExample("technical", "Инфо", "Новости ТГ", "Pack2TheRoot CVE-2026-41651", "https://t.me/proxy_bar/3343"),
    GoldenExample("executive", "Событие", None, "Что известно про хакерскую атаку на «Аэрофлот»?", "https://cisoclub.ru/chto-izvestno-pro-hakerskuju-ataku-na-ajeroflot/", ("В РФ", "Крупные финансовые потери", "Нарушение работы критической инфраструктуры", "Имиджевые потери", "Утечки чувствительной информации", "Массово используемый сервис")),
    GoldenExample("executive", "Событие", None, "Атаки на российских топ-менеджеров", "https://cisoclub.ru/novyj-android-trojan-maskiruetsja-pod-antivirus-fsb-i-atakuet-rossijskih-top-menedzherov/", ("В РФ", "Массово используемый сервис")),
    GoldenExample("executive", "Событие", None, "Атака на цифровую платформу «Инвестиционные проекты»", "https://www.tadviser.ru/index.php/Компания:Investprojects_%28Инвестиционные_проекты%29", ("В РФ", "Имиджевые потери", "Утечки чувствительной информации", "Массово используемый сервис")),
    GoldenExample("executive", "Событие", None, "Парализована работа целого штата Невада", "https://www.anti-malware.ru/news/2025-09-04-111332/47220", ("Вне РФ", "Нарушение работы критической инфраструктуры", "Утечки чувствительной информации", "Госсектор и правовое поле")),
    GoldenExample("executive", "Событие", None, "Хакерские атаки против России достигли рекордного уровня", "https://cisoclub.ru/sberbank-zafiksiroval-trillionnye-ubytki-ot-hakerskih-atak-i-predupredil-o-masshtabnoj-kibervojne-protiv-jekonomiki-rossii/", ("В РФ", "Крупные финансовые потери", "Госсектор и правовое поле", "Трудовой ресурс/мероприятия")),
    GoldenExample("executive", "Событие", None, "Офисная «эпидемия» нового времени – заражение 7644%", "https://cisoclub.ru/ofisnaja-jepidemija-novogo-vremeni-zarazhenie-7644/", ("В РФ", "Может быть интересно")),
    GoldenExample("executive", "Событие", None, "Минцифры планирует ввести оборотные штрафы за нарушение сроков перехода КИИ", "https://cisoclub.ru/mincifry-planiruet-vvesti-oborotnye-shtrafy-za-narushenie-srokov-perehoda-kii-na-otechestvennye-it-reshenija/", ("В РФ", "Госсектор и правовое поле")),
    GoldenExample("executive", "Событие", None, "Минус 90% прибыли из-за кибератаки", "https://www.securitylab.ru/news/565676.php", ("Вне РФ", "Крупные финансовые потери", "Имиджевые потери", "Утечки чувствительной информации")),
    GoldenExample("executive", "Событие", None, "Атаки на SCADA-системы выросли на 27% — чаще всего страдает энергетика", "https://www.anti-malware.ru/news/2025-07-25-111332/46789", ("В РФ", "Энергетика", "Промышленность")),
    GoldenExample("executive", "Событие", None, "Scaly Wolf снова атакует российский машиностроительный сектор", "https://xakep.ru/2025/08/14/scaly-wolf/", ("В РФ", "Промышленность")),
    GoldenExample("executive", "Событие", None, "Норвежская спецслужба обвинила российских хакеров в кибератаке на дамбу", "https://www.kommersant.ru/doc/7959198", ("Вне РФ", "Нарушение работы критической инфраструктуры", "Энергетика")),
]
