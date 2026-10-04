from __future__ import annotations
import re
from app.models import Publication
from app.intelligence.organizer_rules import infer_category
CVE=re.compile(r'CVE-\d{4}-\d{4,7}',re.I); CVSS=re.compile(r'CVSS(?:\s*(?:score|[:=]))?\s*(10(?:\.0)?|[0-9](?:\.\d)?)',re.I)

def technical_card(pub: Publication) -> dict:
    text=f'{pub.title} {pub.text}'; category=infer_category(pub)
    cves=sorted(set(x.upper() for x in CVE.findall(text))); m=CVSS.search(text)
    exploit=bool(re.search(r'\b(exploit|poc|proof of concept|эксплойт)\b',text,re.I))
    card={'category':category,'cve':cves,'cvss':float(m.group(1)) if m else None,'exploit_available':exploit}
    if category=='Атака': card.update({'iocs_present':bool(re.search(r'\b(?:IOC|hash|domain|ip address|индикатор)\b',text,re.I))})
    return card

TAG_RULES={
'В РФ':r'\b(росси\w*|рф)\b','Вне РФ':r'\b(europe|usa|norway|европ|сша|норвег)\w*',
'Крупные финансовые потери':r'(млн|миллиард|убыт|потер.*(?:руб|доллар|евро)|profit)',
'Нарушение работы критической инфраструктуры':r'(critical infrastructure|кии|scada|дамб|энергосистем|аэропорт)',
'Энергетика':r'(энергет|energy|power grid|scada)','Промышленность':r'(промышлен|industrial|manufactur|машиностро)',
'Имиджевые потери':r'(репутац|имидж|reputation)','Утечки чувствительной информации':r'(утеч|leak|data breach|персональн.*данн)',
'Госсектор и правовое поле':r'(минцифр|гос|government|закон|штраф|регулят)','Массово используемый сервис':r'(массов|popular service|windows|android|telegram)',
'Трудовой ресурс/мероприятия':r'(сотрудник|персонал|конференц|мероприят)','Может быть интересно':r'(исследован|тренд|обзор)'}

def executive_tags(pub: Publication) -> list[str]:
    text=f'{pub.title} {pub.text}'.lower(); return [tag for tag,pat in TAG_RULES.items() if re.search(pat,text,re.I)]
