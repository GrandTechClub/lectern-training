from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE, "GTC-AV-Handout.pdf")
LOGO = os.path.join(BASE, "images", "GTC-logo.png")
QR = os.path.join(BASE, "images", "QR-code.png")

# GTC brand colors
DARK_BLUE  = colors.HexColor("#0e2247")
MED_BLUE   = colors.HexColor("#1a3a6b")
LIGHT_BLUE = colors.HexColor("#4a90d9")
GREEN      = colors.HexColor("#3a8a2e")
LIGHT_GRAY = colors.HexColor("#f0f4f8")
TEXT_DARK  = colors.HexColor("#1a3a6b")

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.6*inch,
    bottomMargin=0.6*inch,
)

styles = {
    "title": ParagraphStyle("title",
        fontName="Helvetica-Bold", fontSize=20,
        textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=4),
    "subtitle": ParagraphStyle("subtitle",
        fontName="Helvetica", fontSize=11,
        textColor=LIGHT_BLUE, alignment=TA_CENTER, spaceAfter=16),
    "heading": ParagraphStyle("heading",
        fontName="Helvetica-Bold", fontSize=12,
        textColor=GREEN, spaceBefore=10, spaceAfter=4),
    "body": ParagraphStyle("body",
        fontName="Helvetica", fontSize=10.5,
        textColor=TEXT_DARK, leading=15, spaceAfter=4),
    "bullet": ParagraphStyle("bullet",
        fontName="Helvetica", fontSize=10.5,
        textColor=TEXT_DARK, leading=15,
        leftIndent=16, firstLineIndent=-12, spaceAfter=4),
    "qr_label": ParagraphStyle("qr_label",
        fontName="Helvetica-Bold", fontSize=11,
        textColor=DARK_BLUE, alignment=TA_CENTER, spaceBefore=8),
    "qr_sub": ParagraphStyle("qr_sub",
        fontName="Helvetica", fontSize=9,
        textColor=LIGHT_BLUE, alignment=TA_CENTER),
}

story = []

# Logo
if os.path.exists(LOGO):
    logo = Image(LOGO, width=2.8*inch, height=1.39*inch)
    logo.hAlign = "CENTER"
    story.append(logo)
    story.append(Spacer(1, 6))

# Title
story.append(Paragraph("Lectern A/V Training Guide", styles["title"]))

# Two-column layout: tips on left, QR on right
tips_content = [
    Paragraph("Getting Started", styles["heading"]),
    Paragraph("•  <b>First time?</b> We recommend starting with the <b>Lectern PC</b> or <b>Lectern Mac</b> to get comfortable with the system before trying your own device.", styles["bullet"]),
    Paragraph("•  Once you're comfortable with the Lectern PC or Mac, feel free to try connecting your own laptop, phone, or tablet.", styles["bullet"]),
    Spacer(1, 10),
    Paragraph("What to Expect", styles["heading"]),
    Paragraph("•  At this time, <b>one device</b> can be displayed at a time. Your content will appear on <b>all three TVs</b> and the <b>lectern monitor</b> simultaneously.", styles["bullet"]),
    Paragraph("•  We are currently not showing different devices on different TVs.", styles["bullet"]),
    Spacer(1, 10),
    Paragraph("Important Tips", styles["heading"]),
    Paragraph("•  When tapping the <b>ClickShare touch panel</b> or any button on the <b>audio console</b>, always use a <b>gentle tap</b> — not a long press.", styles["bullet"]),
    Paragraph("•  A long press may trigger a different menu or setting than the one you need.", styles["bullet"]),
]

qr_img = Image(QR, width=2.0*inch, height=2.0*inch) if os.path.exists(QR) else Paragraph("[QR Code]", styles["qr_label"])

qr_cell = [
    qr_img,
    Paragraph("Scan to open the\nStep-by-Step Guide", styles["qr_label"]),
]

tips_table_data = [[tips_content, qr_cell]]
tips_table = Table(
    tips_table_data,
    colWidths=[4.5*inch, 2.4*inch],
    style=TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN",  (1,0), (1,0),  "CENTER"),
        ("LEFTPADDING",  (0,0), (0,0), 0),
        ("RIGHTPADDING", (0,0), (0,0), 12),
        ("LEFTPADDING",  (1,0), (1,0), 8),
    ])
)
story.append(Spacer(1, 20))
story.append(tips_table)

story.append(Spacer(1, 14))

doc.build(story)
print(f"PDF created: {OUTPUT}")
