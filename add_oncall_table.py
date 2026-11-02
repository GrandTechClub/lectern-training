import io, csv, urllib.request
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas

INPUT  = r"C:\Users\carol\OneDrive\Documents\Claude.AI Apps\Lectern Training\Documents and Handouts\GTC-AV-Handout-v2.pdf"
OUTPUT = r"C:\Users\carol\OneDrive\Documents\Claude.AI Apps\Lectern Training\Documents and Handouts\GTC-AV-Handout-Final.pdf"

# ── Paste your published Google Sheet CSV URL here ─────────────────────────
SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRJx54rBeNqbQh0fNXQKwvtCh5spY3L5reEllMWxbVAUe0x0LarlAVAgnnBMQrS7R0wsea4TBXuzjmB/pub?gid=0&single=true&output=csv'

GTC_GREEN = HexColor('#3A7A3A')
ALT_BG    = HexColor('#F2F2F2')
GRID_CLR  = HexColor('#BBBBBB')
NOTE_CLR  = HexColor('#555555')

# ── Load schedule ──────────────────────────────────────────────────────────
if SHEET_CSV_URL:
    print('Fetching schedule from Google Sheet...')
    with urllib.request.urlopen(SHEET_CSV_URL) as resp:
        raw = resp.read().decode('utf-8')
    reader = csv.reader(raw.splitlines())
    all_rows = list(reader)
    # Columns: Date | Time | Class Title | Instructor | Support Person | Support Cell | Backup Person | Backup Cell
    from datetime import datetime, timedelta
    today = datetime.today().date()
    week_start = today
    week_end   = today + timedelta(days=14)
    collected = []
    for row in all_rows[1:]:
        if len(row) < 5 or not row[0].strip():
            continue
        date, time_, class_title, instructor, support, support_cell = (row + ['','','','','',''])[:6]
        backup      = row[6].strip() if len(row) > 6 else ''
        backup_cell = row[7].strip() if len(row) > 7 else ''
        if backup.upper() == 'N/A':
            backup = backup_cell = ''
        if not support.strip():
            continue
        if 'cancel' in class_title.lower():
            continue
        # Parse date+time for sorting and filtering
        dt = None
        for fmt in ('%m/%d/%y %I:%M %p', '%m/%d/%Y %I:%M %p'):
            try: dt = datetime.strptime(f'{date.strip()} {time_.strip()}', fmt); break
            except: pass
        if dt is None or not (week_start <= dt.date() <= week_end):
            continue
        collected.append((dt, date.strip(), time_.strip(), class_title.strip(),
                          support.strip(), support_cell.strip(), backup.strip(), backup_cell.strip()))
    # Sort by datetime
    collected.sort(key=lambda x: x[0])
    dates = [f'{r[1]} {r[2]}' for r in collected]
    parsed_dts = [r[0].date() for r in collected]
    data = [[r[3], r[4], r[5], r[6], r[7]] for r in collected]
    # Determine week label from date range
    if parsed_dts:
        mn, mx = min(parsed_dts), max(parsed_dts)
        mn_dt = datetime.combine(mn, datetime.min.time())
        mx_dt = datetime.combine(mx, datetime.min.time())
        WEEK_LABEL = mn_dt.strftime('%B') + ' ' + str(mn.day) + ('–' + str(mx.day) if mn.month == mx.month else '–' + mx_dt.strftime('%B') + ' ' + str(mx.day)) + ', ' + str(mx.year)
    else:
        WEEK_LABEL = 'This Week'
    # Build display dates (short form)
    display_dates = []
    for d in dates:
        for fmt in ('%m/%d/%y %I:%M %p', '%m/%d/%Y %I:%M %p'):
            try:
                dt = datetime.strptime(d, fmt)
                display_dates.append(dt.strftime('%-m/%-d  %-I:%M %p'))
                break
            except: pass
        else:
            display_dates.append(d)
    has_backup = any(r[3] for r in data)
else:
    print('No Google Sheet URL set — using hardcoded data below.')
    WEEK_LABEL = 'October 28\u201330, 2026'
    display_dates = [
        '10/28  9:00 AM', '10/28  10:30 AM', '10/28  3:30 PM',
        '10/29  9:00 AM', '10/29  10:30 AM', '10/29  1:00 PM',
        '10/29  3:30 PM', '10/30  10:30 AM',
    ]
    data = [
        ['Libby Library App',                              'AnneMette Lavery', '623-330-3079', '', ''],
        ['Photoshop Elements Guided Edits',               'AnneMette Lavery', '623-330-3079', '', ''],
        ['Intro to Canva',                                'Ann Hopperstad',   '623-606-6041', '', ''],
        ['Customizing the Control Center on iPhone/iPad', 'Carol Gontko',     '630-423-2255', '', ''],
        ['iPad Basics',                                   'Ann Hopperstad',   '623-606-6041', '', ''],
        ['iPhone - The Next Step',                        'Ann Hopperstad',   '623-606-6041', '', ''],
        ['Apple Find My App',                             'Ann Hopperstad',   '623-606-6041', '', ''],
        ['All About iCloud',                              'Ira Simmons',      '925-360-4700', '', ''],
    ]
    has_backup = False

# ── Build table rows ───────────────────────────────────────────────────────
if has_backup:
    header_row = ['Date/Time', 'Class/Lab', 'Support Person', 'Cell', 'Backup Person', 'Cell']
    rows = [header_row] + [
        [display_dates[i], d[0], d[1], d[2], d[3], d[4]]
        for i, d in enumerate(data)
    ]
    COL_W = [72, 128, 86, 72, 76, 70]
else:
    header_row = ['Date/Time', 'Class/Lab', 'Support Person', 'Cell']
    rows = [header_row] + [
        [display_dates[i], d[0], d[1], d[2]]
        for i, d in enumerate(data)
    ]
    COL_W = [76, 236, 116, 76]

# ── Table style ────────────────────────────────────────────────────────────
n_cols = len(header_row)
style_cmds = [
    ('BACKGROUND',    (0, 0), (-1, 0),  GTC_GREEN),
    ('TEXTCOLOR',     (0, 0), (-1, 0),  white),
    ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0, 0), (-1, 0),  7),
    ('ALIGN',         (0, 0), (-1, 0),  'CENTER'),
    ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE',      (0, 1), (-1, -1), 7),
    ('ALIGN',         (0, 1), (0, -1),  'CENTER'),
    ('ALIGN',         (n_cols-1, 1), (n_cols-1, -1), 'CENTER'),
    ('ALIGN',         (1, 1), (n_cols-2, -1), 'LEFT'),
    ('GRID',          (0, 0), (-1, -1), 0.5, GRID_CLR),
    ('TOPPADDING',    (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ('LEFTPADDING',   (0, 0), (-1, -1), 5),
    ('RIGHTPADDING',  (0, 0), (-1, -1), 5),
    ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
]
for i in range(1, len(rows)):
    if i % 2 == 0:
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), ALT_BG))

TABLE_W = sum(COL_W)
table = Table(rows, colWidths=COL_W)
table.setStyle(TableStyle(style_cmds))

# ── Build overlay ──────────────────────────────────────────────────────────
packet = io.BytesIO()
c = canvas.Canvas(packet, pagesize=letter)

LEFT_X    = 54
SECTION_Y = 278

c.setFont('Helvetica-Bold', 11)
c.setFillColor(GTC_GREEN)
c.drawString(LEFT_X, SECTION_Y + 2, f'On-Call Support \u2014 {WEEK_LABEL}')

c.setStrokeColor(GTC_GREEN)
c.setLineWidth(0.75)
c.line(LEFT_X, SECTION_Y - 2, LEFT_X + TABLE_W, SECTION_Y - 2)

table.wrapOn(c, TABLE_W, 400)
table_h = table._height
TABLE_TOP = SECTION_Y - 8
table.drawOn(c, LEFT_X, TABLE_TOP - table_h)

note_y = TABLE_TOP - table_h - 11
c.setFont('Helvetica-Oblique', 8)
c.setFillColor(NOTE_CLR)
c.drawString(LEFT_X, note_y, 'Text only, no calls please')

c.save()
packet.seek(0)

# ── Merge onto original PDF ────────────────────────────────────────────────
reader  = PdfReader(INPUT)
overlay = PdfReader(packet)
writer  = PdfWriter()

page = reader.pages[0]
page.merge_page(overlay.pages[0])
writer.add_page(page)

with open(OUTPUT, 'wb') as f:
    writer.write(f)

print(f'Saved: {OUTPUT}')
