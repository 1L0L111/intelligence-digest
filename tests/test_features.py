from app.intelligence.extraction import technical_card,executive_tags
from app.intelligence.feedback import apply_feedback
from app.models import Publication,UserProfile

def test_structured_extraction():
 p=Publication(id='1',title='CVE-2026-12345 critical SCADA vulnerability',url='https://x',source='x',text='CVSS 9.8 public exploit PoC in energy')
 c=technical_card(p);assert c['cve']==['CVE-2026-12345'];assert c['exploit_available'];assert c['cvss']==9.8

def test_feedback_updates_profile():
 p=apply_feedback(UserProfile(interests=['CVE']),['SCADA'],True);assert 'SCADA' in p.interests;assert p.priorities['SCADA']>1
