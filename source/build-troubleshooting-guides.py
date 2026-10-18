from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader
import shutil
out=Path(__file__).resolve().parents[1]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BrandSM',fontName='Helvetica-Bold',fontSize=15,leading=18,textColor=colors.HexColor('#252729'),spaceAfter=20))
styles.add(ParagraphStyle(name='TitleSM',fontName='Helvetica-Bold',fontSize=22,leading=27,spaceAfter=14))
styles.add(ParagraphStyle(name='HeadingSM',fontName='Helvetica-Bold',fontSize=12,leading=16,spaceBefore=15,spaceAfter=7,textColor=colors.HexColor('#28744b')))
styles.add(ParagraphStyle(name='BodySM',fontName='Helvetica',fontSize=10.5,leading=15,spaceAfter=7))
styles.add(ParagraphStyle(name='SmallSM',fontName='Helvetica',fontSize=8,leading=11,spaceAfter=5,textColor=colors.HexColor('#65696c')))
def para(t,sty='BodySM'):return Paragraph(t,styles[sty])
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#dadeda'));c.line(44,48,568,48)
 c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#65696c'))
 c.drawString(44,34,'Simply Michigan Infotainment | simplymichigan.co/install')
 c.drawRightString(568,34,'Updated October 18, 2026 | '+str(doc.page))
def build(name,title,sections):
 story=[para('SIMPLY MICHIGAN<br/><font size="9">I N F O T A I N M E N T</font>','BrandSM'),para(title,'TitleSM')]
 for heading,body in sections:
  if heading:story.append(para(heading,'HeadingSM'))
  for t in body:story.append(para(*t) if isinstance(t,tuple) else para(t))
 dest=out/name
 SimpleDocTemplate(str(dest),pagesize=letter,rightMargin=44,leftMargin=44,topMargin=38,bottomMargin=62,title=title,author='Simply Michigan Infotainment').build(story,onFirstPage=footer,onLaterPages=footer)
 assert len(PdfReader(dest).pages)==1,(name,len(PdfReader(dest).pages))
common_start='Use these steps for a frozen or unresponsive system. Start with a soft reset. If the issue remains and you can use the Settings menu, try a master reset. A reset that does not help does not prove the hardware has failed.'
for generation in (2,3):
 master=['1. Open <b>Settings</b>, then <b>System</b>, and select <b>Master Reset</b>.','2. Review the warning and confirm only if you are ready to erase your saved information.','3. Allow the system to finish and restart. Pair your phone again and restore your preferences.'] if generation==2 else ['1. Select <b>Settings</b> on the bottom feature bar, then <b>General</b>.','2. Scroll to <b>Master Reset</b> and select it.','3. Review the warning and select <b>Continue</b> if you are ready to erase your saved information.','4. Wait for the reset and restart to finish. This can take several minutes. Pair your phone again and restore your preferences.']
 source='https://www.fordservicecontent.com/Ford_Content/Catalog/owner_information/SYNC-2-MyFord-MyLincoln-Touch-Supplement-version-1_sycsy_EN-US_05_2015.pdf' if generation==2 else 'https://www.india.ford.com/owner/sync-support/3/perform-master-reset/'
 build(f'sync-{generation}-reset-instructions.pdf',f'Sync {generation} Reset Instructions',[
 ('',[common_start,'Park safely before starting. If the engine is running, keep the vehicle outdoors. Do not perform these steps while driving.']),
 ('1 / Soft reset - keeps your saved settings',['Press and hold the radio <b>Power</b> and <b>Seek Up / Next Track</b> buttons together until the display goes black, then release. Allow the system time to restart (about 1-2 minutes). If the controls or behavior do not match, stop and contact us.']),
 ('2 / Master reset - erases saved information',['<b>This deletes paired phones and personal settings.</b> Note any saved information you need first and disconnect USB devices. If the screen is black or touch does not work, do not attempt to navigate the menu blindly. Tell us you cannot access it.']+master),
 ('If the issue remains',['Record whether the reset helped, made no difference, or helped only temporarily. Contact us with the vehicle year/model and your results.','<b>Battery or APIM connector disconnection:</b> contact us for vehicle-specific guidance before attempting a power-disconnection reset. Do not disconnect the battery or 54-pin APIM connector as a routine next step from this guide.']),
 ('Need help?',['<link href="https://simplymichigan.co/contact-us" color="#28744b">simplymichigan.co/contact-us</link> | nick@simplymichigan.co',(f'Reference: <link href="{source}" color="#28744b">Ford Sync {generation} guidance</link>. Menu appearance may vary by vehicle and software.','SmallSM')])])
build('speaker-walk-around-self-test-instructions.pdf','Speaker Walk Around Self Test',[
 ('Before you begin',['For compatible Sync 3 systems with the physical controls described below. Park safely. If the engine is running, keep the vehicle outdoors. <b>Test tones can be loud or high-pitched.</b>','This procedure requires the radio to turn on and FM to be selected. If Audio will not open, FM cannot be selected, or the controls do not match, stop and contact us. An unavailable test is not a failed speaker test.']),
 ('Run the test',['1. Turn on the radio and select an FM station. Exit CarPlay or Android Auto so you are testing the vehicle radio.','2. Hold the <b>right seek / next track</b> button on the steering wheel and the <b>right seek / next track</b> button on the dashboard/HVAC panel together for about five seconds.','3. When the test starts, listen to each tone and record the named speaker position shown on the display. Use the diagnostic menu to exit or rerun the speaker test if needed. Do not change other diagnostic settings.','4. If the test will not start or you are unsure how to read the result, record that and ask for help.']),
 ('What to record',['<b>Some positions silent:</b> record each silent position. The speaker, wiring, or amplifier output may be responsible. The test alone does not identify which component failed.','<b>No tones heard:</b> report that result. It does not prove that all speakers, the ACM, or the amplifier have failed. Power, connections, and correct test operation need review.','<b>All tested positions played:</b> record whether normal AM/FM, phone playback, or calls still have a problem. Working tones do not prove that the normal playback path is working.']),
 ('Send us your results',['Include the vehicle year/model, audio package (standard, Sony, B&amp;O, THX, Revel, or aftermarket), affected sources, and the speaker positions you recorded.','<link href="https://simplymichigan.co/contact-us" color="#28744b">simplymichigan.co/contact-us</link> | nick@simplymichigan.co'])])
print('Built three one-page guides. Copy to smi-assets/instructions/pdfs before publishing both repositories.')
