"""Build the Ragsak handbook and reusable vector/PNG diagrams from local evidence."""
from pathlib import Path
import csv
import html
import json
import math
import re
import shutil
import subprocess
import textwrap

from PIL import Image as PILImage
from pypdf import PdfReader
from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon
from reportlab.graphics import renderPDF, renderSVG
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, Preformatted, KeepTogether, CondPageBreak,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / 'Docs'
BUILD = DOCS / '.build'
DIAGRAMS = DOCS / 'diagrams'
EVIDENCE = DOCS / 'evidence'
REFERENCE = DOCS / 'reference'
for directory in [BUILD, DIAGRAMS, EVIDENCE, REFERENCE]:
    directory.mkdir(parents=True, exist_ok=True)

INK = colors.HexColor('#3c1c16')
ORANGE = colors.HexColor('#fa681e')
RED = colors.HexColor('#7b211c')
CREAM = colors.HexColor('#fff4df')
MUTED = colors.HexColor('#705d54')
PALE = colors.HexColor('#fbf7f1')
LINE = colors.HexColor('#e4d8cb')


def register_fonts():
    paths = {
        'Body': 'C:/Windows/Fonts/segoeui.ttf',
        'BodyBold': 'C:/Windows/Fonts/segoeuib.ttf',
        'BodyItalic': 'C:/Windows/Fonts/segoeuii.ttf',
        'Mono': 'C:/Windows/Fonts/consola.ttf',
        'Display': 'C:/Windows/Fonts/georgia.ttf',
    }
    if all(Path(value).exists() for value in paths.values()):
        for name, filename in paths.items():
            pdfmetrics.registerFont(TTFont(name, filename))
        pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='BodyItalic', boldItalic='BodyBold')
        return 'Body', 'BodyBold', 'BodyItalic', 'Mono', 'Display'
    return 'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Courier', 'Times-Roman'


BODY, BOLD, ITALIC, MONO, DISPLAY = register_fonts()


def find_renderer():
    discovered = shutil.which('pdftoppm')
    if discovered:
        return discovered
    bundled = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
    if bundled.exists():
        return str(bundled)
    raise RuntimeError('Install Poppler or add its pdftoppm executable to PATH to render diagrams.')


RENDERER = find_renderer()


class Diagram:
    def __init__(self, title, subtitle, height=650):
        self.width, self.height = 1200, height
        self.drawing = Drawing(self.width, self.height)
        self.drawing.add(Rect(0, 0, self.width, self.height, fillColor=CREAM, strokeColor=None))
        self.text(40, 38, title, 30, BOLD)
        self.text(40, 76, subtitle, 19, BODY, MUTED)

    def text(self, x, y, value, size=19, font=BODY, color=INK):
        self.drawing.add(String(x, self.height - y, value, fontName=font, fontSize=size, fillColor=color))

    def node(self, x, y, title, detail, width=300, height=115, dark=False):
        bottom = self.height - y - height
        self.drawing.add(Rect(x, bottom, width, height, rx=14, ry=14, fillColor=INK if dark else colors.white, strokeColor=INK if dark else LINE, strokeWidth=2))
        color = CREAM if dark else INK
        self.text(x+20, y+34, title, 23, BOLD, color)
        for index, line in enumerate(detail.split('\n')):
            self.text(x+20, y+65+index*25, line, 19, BODY, color)

    def arrow(self, points, label='', label_at=None, dashed=False):
        converted = [(x, self.height-y) for x, y in points]
        for (x1,y1),(x2,y2) in zip(converted, converted[1:]):
            self.drawing.add(Line(x1,y1,x2,y2, strokeColor=ORANGE, strokeWidth=3, strokeDashArray=[7,5] if dashed else None))
        x1,y1 = converted[-2]
        x2,y2 = converted[-1]
        angle = math.atan2(y2-y1,x2-x1)
        length, spread = 13, 6
        left=(x2-length*math.cos(angle)+spread*math.sin(angle), y2-length*math.sin(angle)-spread*math.cos(angle))
        right=(x2-length*math.cos(angle)-spread*math.sin(angle), y2-length*math.sin(angle)+spread*math.cos(angle))
        self.drawing.add(Polygon([x2,y2,*left,*right], fillColor=ORANGE, strokeColor=None))
        if label and label_at:
            x,y = label_at
            self.text(x,y,label,18,BODY,MUTED)

    def footer(self, value):
        self.text(40, self.height-30, value, 18, BODY, MUTED)

    def save(self, stem):
        # Vector PDF is a temporary render source; PNG and SVG are the final diagrams.
        renderSVG.drawToFile(self.drawing, str(DIAGRAMS / f'{stem}.svg'))
        temporary = BUILD / f'{stem}.pdf'
        renderPDF.drawToFile(self.drawing, str(temporary))
        prefix = DIAGRAMS / stem
        subprocess.run([RENDERER,'-singlefile','-r','180','-png',str(temporary),str(prefix)],check=True,capture_output=True)


def build_diagrams():
    d=Diagram('System architecture','Static site delivery; local tooling and hosted access are separate boundaries.')
    d.node(40,240,'Working checkout','dist/ + scripts/ + tests/\nRecorded official content',dark=True)
    d.node(450,140,'Source + version','Git commit and archive\nSaved hosting version')
    d.node(450,390,'Sites / Cloudflare','Private host access\nStatic HTTPS delivery')
    d.node(860,390,'Visitor browser','HTML + CSS + local assets\nOptional reveal script')
    d.node(860,140,'External destinations','Maps, phone handler\nFacebook and Instagram')
    d.arrow([(340,270),(450,195)],'checked source',(255,205))
    d.arrow([(340,330),(400,330),(400,445),(450,445)],'static archive',(170,402))
    d.arrow([(600,255),(600,390)],'publish',(615,330))
    d.arrow([(750,445),(860,445)],'HTTPS',(772,426))
    d.arrow([(1010,390),(1010,255)],'chosen links',(1027,325))
    d.footer('No application database, custom production server, embedded social feed, or runtime AI service.')
    d.save('system-architecture')

    d=Diagram('Conceptual content model','These are content relationships, not implemented database tables.',height=760)
    d.node(450,130,'Cafe','Identity, visit details\nOfficial social references',dark=True)
    d.node(40,335,'Page section','Heading, copy, actions\nHTML landmark and ID')
    d.node(450,335,'Menu item','Verified name + description\nManual HTML content')
    d.node(860,335,'Asset','WebP / WOFF2 variants\nAlt text, dimensions, crop')
    d.node(40,560,'Action','Anchor, image, phone\nMap or social destination')
    d.node(450,560,'Release','Source SHA + archive\nVersion, status, audience')
    d.node(860,560,'Source evidence','Original URL + observation\nOwner-review status')
    d.arrow([(450,190),(190,335)],'contains',(255,235))
    d.arrow([(340,390),(450,390)],'displays',(352,374))
    d.arrow([(750,390),(860,390)],'uses',(782,374))
    d.arrow([(190,450),(190,560)],'offers',(205,514))
    d.arrow([(1010,450),(1010,560)],'attributed to',(1020,514))
    d.arrow([(600,560),(600,450)],'snapshots source',(612,514))
    d.footer('A release fixes the source state; it does not establish that business facts remain current.')
    d.save('content-model')

    d=Diagram('Visitor and runtime flow','Core reading and navigation work before optional enhancement.',height=690)
    d.node(40,155,'1. Request website','Host checks private access\nReturns static page',dark=True)
    d.node(450,155,'2. Render content','Local CSS, fonts, images\nResponsive layout + links')
    d.node(860,155,'3. Optional enhancement','Copyright year\nMotion/API availability')
    d.node(40,425,'Readable fallback','No site JS / API failure\nCards remain visible')
    d.node(450,425,'Visitor chooses action','Section, menu, call\nDirections or source post')
    d.node(860,425,'Reveal behavior','Viewport or keyboard focus\nReduced motion restores all')
    d.arrow([(340,212),(450,212)],'HTTPS',(355,190))
    d.arrow([(750,212),(860,212)],'deferred JS',(762,190))
    d.arrow([(600,270),(600,425)],'links available',(615,351))
    d.arrow([(1010,270),(1010,425)],'when enabled',(1025,351))
    d.arrow([(880,270),(880,310),(190,310),(190,425)],'unsupported or failed enhancement',(200,336),dashed=True)
    d.footer('Outbound actions delegate to the browser/device; no visitor record is written by this application.')
    d.save('runtime-flow')

    d=Diagram('Development and deployment workflow','Recorded implementation process and repeatable update loop.',height=690)
    d.node(40,155,'1. Research','Brief + official profiles\nRecord evidence and gaps',dark=True)
    d.node(450,155,'2. Prepare assets','Official photos to WebP\nFont subsets to WOFF2')
    d.node(860,155,'3. Implement','Semantic HTML + CSS\nOptional accessible JS')
    d.node(860,425,'4. Validate','Source checks + 8 tests\nBrowser/mobile/text review')
    d.node(450,425,'5. Publish exact source','Commit + push + archive\nSave/deploy existing Site')
    d.node(40,425,'6. Confirm + retain','Native succeeded result\nVersion/SHA for recovery')
    d.arrow([(340,212),(450,212)],'sources',(355,190))
    d.arrow([(750,212),(860,212)],'local assets',(762,190))
    d.arrow([(1010,270),(1010,425)],'review',(1026,350))
    d.arrow([(860,482),(750,482)],'passes',(773,466))
    d.arrow([(450,482),(340,482)],'result',(365,466))
    d.footer('If validation fails, return to implementation. Local edits and public sharing are separate from deployment.')
    d.save('development-workflow')


def capture_evidence():
    for name in ['desktop.png','mobile.png','deployment.json','responsive.json','text-200.json','navigation.json']:
        source=ROOT/'artifacts'/name
        if source.exists():
            shutil.copy2(source,EVIDENCE/name)
    for name in ['OWNER-REVIEW.md','REVIEW-REPORT.md','DEPLOYMENT-GUIDE.md']:
        shutil.copy2(ROOT/name,REFERENCE/name)
    rows=[]
    for asset in sorted((ROOT/'dist/assets').iterdir()):
        if not asset.is_file(): continue
        row={'file':asset.name,'bytes':asset.stat().st_size,'format':asset.suffix.lstrip('.'),'width':'','height':''}
        if asset.suffix=='.webp':
            with PILImage.open(asset) as image:
                row.update(width=image.width,height=image.height)
        rows.append(row)
    with (EVIDENCE/'asset-inventory.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['file','bytes','format','width','height'])
        writer.writeheader();writer.writerows(rows)
    return rows


PAGE_W,PAGE_H=A4
MARGIN=46
CONTENT_W=PAGE_W-2*MARGIN
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TextBody',fontName=BODY,fontSize=10,leading=15,textColor=INK,spaceAfter=8,wordWrap='LTR',splitLongWords=True))
styles.add(ParagraphStyle(name='Chapter',fontName=DISPLAY,fontSize=25,leading=31,textColor=RED,spaceBefore=0,spaceAfter=17,keepWithNext=True))
styles.add(ParagraphStyle(name='Subheading',fontName=BOLD,fontSize=12.3,leading=17,textColor=INK,spaceBefore=13,spaceAfter=7,keepWithNext=True))
styles.add(ParagraphStyle(name='CaptionSmall',fontName=BODY,fontSize=8.2,leading=11.5,textColor=MUTED,spaceAfter=10))
styles.add(ParagraphStyle(name='TableBody',fontName=BODY,fontSize=8.6,leading=12.1,textColor=INK,wordWrap='CJK',splitLongWords=True))
styles.add(ParagraphStyle(name='TableHead',fontName=BOLD,fontSize=8.8,leading=12.2,textColor=CREAM,wordWrap='CJK'))
styles.add(ParagraphStyle(name='ListBody',parent=styles['TextBody'],leftIndent=16,firstLineIndent=-13,spaceAfter=6))
styles.add(ParagraphStyle(name='CodeBody',fontName=MONO,fontSize=8.7,leading=13,textColor=INK,backColor=PALE,borderPadding=10,spaceBefore=5,spaceAfter=12))
styles.add(ParagraphStyle(name='ContentsEntry',fontName=BODY,fontSize=10.5,leading=19,textColor=INK,leftIndent=0,firstLineIndent=0,spaceBefore=5))


def formatted(value):
    value=html.escape(value)
    value=re.sub(r'`([^`]+)`',lambda m:f'<font name="{MONO}">{m[1]}</font>',value)
    value=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',value)
    return value


def para(value,style='TextBody'):
    return Paragraph(formatted(value),styles[style])


class Handbook(BaseDocTemplate):
    def __init__(self,filename):
        super().__init__(filename,pagesize=A4,leftMargin=MARGIN,rightMargin=MARGIN,topMargin=58,bottomMargin=49,title='Ragsak Manila Cafe - Technical Documentation',author='Ragsak project documentation',allowSplitting=True)
        self.addPageTemplates(PageTemplate(id='handbook',frames=Frame(MARGIN,49,CONTENT_W,PAGE_H-107,id='normal',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=self.decorate))

    def decorate(self,c,doc):
        c.saveState()
        if doc.page>1:
            c.setFillColor(MUTED);c.setFont(BOLD,8)
            c.drawString(MARGIN,PAGE_H-32,'RAGSAK MANILA CAFE')
            c.setFont(BODY,8);c.drawRightString(PAGE_W-MARGIN,PAGE_H-32,'SYSTEM DESIGN / BUILD / OPERATIONS')
            c.setStrokeColor(LINE);c.line(MARGIN,PAGE_H-41,PAGE_W-MARGIN,PAGE_H-41)
        c.setStrokeColor(LINE);c.line(MARGIN,34,PAGE_W-MARGIN,34)
        c.setFillColor(MUTED);c.setFont(BODY,8)
        c.drawString(MARGIN,20,'October 4, 2026  |  Recorded private release v3')
        c.drawRightString(PAGE_W-MARGIN,20,f'{doc.page:02d}')
        c.restoreState()

    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name=='Chapter':
            label=flowable.getPlainText()
            key='section-'+re.sub(r'[^a-zA-Z0-9]','-',label)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(label,key,level=0,closed=False)
            self.notify('TOCEntry',(0,label,self.page,key))


def cover(rows):
    flow=[]
    flow.append(Spacer(1,15))
    flow.append(Paragraph('RAGSAK / PROJECT HANDBOOK',ParagraphStyle('Kicker',fontName=BOLD,fontSize=10,leading=16,textColor=RED,spaceAfter=22)))
    flow.append(Paragraph('From cafe brief<br/>to cloud website.',ParagraphStyle('CoverTitle',fontName=DISPLAY,fontSize=37,leading=44,textColor=INK,spaceAfter=20)))
    flow.append(para('System model, design decisions, research, image preparation, implementation, verification, deployment, and maintenance.'))
    flow.append(Spacer(1,8))
    summary=Table([
        [para('PROJECT','TableHead'),para('Ragsak Manila Cafe','TableBody')],
        [para('STACK','TableHead'),para('Static HTML, CSS, JavaScript; local WebP and WOFF2 assets','TableBody')],
        [para('RELEASE','TableHead'),para('Recorded version 3 / succeeded / private owner access','TableBody')],
        [para('WORKSPACE','TableHead'),para(r'C:\KELVIN\Ragsak','TableBody')],
    ],colWidths=[94,CONTENT_W-94])
    summary.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),INK),('BACKGROUND',(1,0),(1,-1),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    flow.extend([summary,Spacer(1,22)])
    screenshot=EVIDENCE/'desktop.png'
    if screenshot.exists():
        with PILImage.open(screenshot) as im:
            ratio=im.height/im.width
        width=CONTENT_W
        flow.append(Image(str(screenshot),width=width,height=width*ratio))
        flow.append(Spacer(1,5))
        flow.append(para('Reviewed desktop screenshot retained as release evidence.','CaptionSmall'))
    flow.append(PageBreak())
    flow.append(Paragraph('Handbook map',styles['Chapter']))
    flow.append(para('Read the chapters in order for the complete build account, or use the chapter links below to reach a specific task.'))
    toc=TableOfContents();toc.levelStyles=[styles['ContentsEntry']]
    flow.extend([toc,Spacer(1,20),para('Scope: this is a documented snapshot of the source and recorded release. Exact AI model settings and every historical command are not recorded. Future features are described as options, not as shipped capabilities.','CaptionSmall'),PageBreak()])
    return flow


def make_table(raw):
    rows=[]
    for index,line in enumerate(raw):
        cells=[value.strip() for value in line.strip().strip('|').split('|')]
        if all(re.fullmatch(r':?-{3,}:?',cell) for cell in cells): continue
        style='TableHead' if not rows else 'TableBody'
        rows.append([para(cell,style) for cell in cells])
    count=len(rows[0])
    if count==2: widths=[CONTENT_W*.32,CONTENT_W*.68]
    elif count==3: widths=[CONTENT_W*.26,CONTENT_W*.35,CONTENT_W*.39]
    else: widths=[CONTENT_W/count]*count
    table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),INK),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[PALE,colors.white]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LINEBELOW',(0,0),(-1,0),.7,INK),
        ('LINEBELOW',(0,1),(-1,-1),.4,LINE),
    ]))
    return [table,Spacer(1,12)]


def markdown_flow(source):
    lines=source.splitlines();flow=[];index=0;has_chapter=False
    while index<len(lines):
        line=lines[index].strip()
        if not line:
            index+=1;continue
        if line.startswith('## '):
            if has_chapter:
                chapter_number = int(line[3:5])
                if chapter_number <= 6:
                    flow.append(PageBreak())
                else:
                    flow.extend([CondPageBreak(300), Spacer(1, 24)])
            has_chapter=True
            flow.append(Paragraph(formatted(line[3:]),styles['Chapter']));index+=1;continue
        if not has_chapter:
            index+=1;continue
        if line.startswith('### '):
            flow.append(para(line[4:],'Subheading'));index+=1;continue
        if line.startswith('!['):
            match=re.fullmatch(r'!\[([^]]+)\]\(([^)]+)\)',line)
            if match:
                filename=DOCS/match[2]
                with PILImage.open(filename) as im: ratio=im.height/im.width
                flow.append(Image(str(filename),width=CONTENT_W,height=CONTENT_W*ratio))
                flow.append(Spacer(1,5));flow.append(para(match[1]+'. Standalone PNG and SVG copies are in diagrams/.','CaptionSmall'))
            index+=1;continue
        if line.startswith('```'):
            block=[];index+=1
            while index<len(lines) and not lines[index].strip().startswith('```'):
                block.append(lines[index]);index+=1
            flow.append(Preformatted('\n'.join(block),styles['CodeBody'],maxLineLength=85))
            index+=1;continue
        if line.startswith('|'):
            rows=[]
            while index<len(lines) and lines[index].strip().startswith('|'):
                rows.append(lines[index]);index+=1
            flow.extend(make_table(rows));continue
        if re.match(r'^\d+\. ',line) or line.startswith('- '):
            flow.append(para(line,'ListBody'));index+=1;continue
        paragraph=[line];index+=1
        while index<len(lines) and lines[index].strip() and not re.match(r'^(#{2,3} |\| |\|[^ ]|```|!\[|\d+\. |- )',lines[index].strip()):
            paragraph.append(lines[index].strip());index+=1
        flow.append(para(' '.join(paragraph)))
    return flow


def build_pdf(rows):
    filename=DOCS/'Ragsak-Technical-Documentation.pdf'
    source=(DOCS/'Ragsak-Technical-Documentation.md').read_text(encoding='utf-8')
    document=Handbook(str(filename))
    document.multiBuild(cover(rows)+markdown_flow(source))
    reader=PdfReader(str(filename))
    texts=[page.extract_text() or '' for page in reader.pages]
    expected=[line[3:] for line in source.splitlines() if line.startswith('## ')]
    joined='\n'.join(texts)
    for chapter in expected:
        if chapter not in joined:
            raise AssertionError(f'Missing PDF chapter: {chapter}')
    if any('\ufffd' in value or '\u25a0' in value for value in texts):
        raise AssertionError('Unexpected missing glyph in extracted text')
    print(json.dumps({'pdf':str(filename),'pages':len(reader.pages),'chapters':len(expected),'diagrams':4,'bytes':filename.stat().st_size,'textVerification':'passed'},indent=2))


if __name__=='__main__':
    capture_evidence()
    build_diagrams()
    rows=capture_evidence()
    build_pdf(rows)
    # Remove only this builder's known intermediate files, all inside Docs/.build.
    for stem in ['system-architecture','content-model','runtime-flow','development-workflow']:
        (BUILD/f'{stem}.pdf').unlink(missing_ok=True)
    if not any(BUILD.iterdir()): BUILD.rmdir()
