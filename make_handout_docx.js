const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, AlignmentType, LevelFormat, WidthType, ShadingType, VerticalAlign,
} = require("docx");

const BASE = __dirname;
const LOGO = path.join(BASE, "images", "GTC-logo.png");
const QR = path.join(BASE, "images", "QR-code.png");
const OUTPUT = path.join(BASE, "GTC-AV-Handout.docx");

// GTC brand colors (hex, no #)
const DARK_BLUE = "0E2247";
const MED_BLUE = "1A3A6B";
const LIGHT_BLUE = "4A90D9";
const GREEN = "3A8A2E";

const bulletRun = (boldText, restText) => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [
    ...(boldText ? [new TextRun({ text: boldText, bold: true, color: MED_BLUE, font: "Arial", size: 21 })] : []),
    new TextRun({ text: restText, color: MED_BLUE, font: "Arial", size: 21 }),
  ],
});

const heading = (text) => new Paragraph({
  spacing: { before: 200, after: 80 },
  children: [new TextRun({ text, bold: true, color: GREEN, font: "Arial", size: 24 })],
});

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 360, hanging: 200 } } },
        }],
      },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 864, right: 1080, bottom: 864, left: 1080 },
      },
    },
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new ImageRun({
          type: "png",
          data: fs.readFileSync(LOGO),
          transformation: { width: 202, height: 100 },
          altText: { title: "Logo", description: "Grand Tech Club logo", name: "Logo" },
        })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 240 },
        children: [new TextRun({
          text: "Lectern A/V Training Guide",
          bold: true, color: DARK_BLUE, font: "Arial", size: 40,
        })],
      }),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [6480, 2880],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                width: { size: 6480, type: WidthType.DXA },
                margins: { top: 0, bottom: 0, left: 0, right: 160 },
                borders: { top: { style: "none" }, bottom: { style: "none" }, left: { style: "none" }, right: { style: "none" } },
                verticalAlign: VerticalAlign.TOP,
                children: [
                  heading("Getting Started"),
                  bulletRun("First time? ", "We recommend starting with the Lectern PC or Lectern Mac to get comfortable with the system before trying your own device."),
                  bulletRun(null, "Once you're comfortable with the Lectern PC or Mac, feel free to try connecting your own laptop, phone, or tablet."),
                  heading("What to Expect"),
                  bulletRun("At this time, ", "one device can be displayed at a time. Your content will appear on all three TVs and the lectern monitor simultaneously."),
                  bulletRun(null, "We are currently not showing different devices on different TVs."),
                  heading("Important Tips"),
                  bulletRun(null, "When tapping the ClickShare touch panel or any button on the audio console, always use a gentle tap — not a long press."),
                  bulletRun(null, "A long press may trigger a different menu or setting than the one you need."),
                ],
              }),
              new TableCell({
                width: { size: 2880, type: WidthType.DXA },
                margins: { top: 0, bottom: 0, left: 160, right: 0 },
                borders: { top: { style: "none" }, bottom: { style: "none" }, left: { style: "none" }, right: { style: "none" } },
                verticalAlign: VerticalAlign.TOP,
                children: [
                  new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [new ImageRun({
                      type: "png",
                      data: fs.readFileSync(QR),
                      transformation: { width: 144, height: 144 },
                      altText: { title: "QR Code", description: "QR code linking to the step-by-step guide", name: "QR Code" },
                    })],
                  }),
                  new Paragraph({
                    alignment: AlignmentType.CENTER,
                    spacing: { before: 80 },
                    children: [new TextRun({
                      text: "Scan to open the Step-by-Step Guide",
                      bold: true, color: DARK_BLUE, font: "Arial", size: 22,
                    })],
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(OUTPUT, buffer);
  console.log("DOCX created:", OUTPUT);
});
