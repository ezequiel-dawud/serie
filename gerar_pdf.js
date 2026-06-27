const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

const inputFile = path.join(__dirname, 'episodios', 'ep01_producao_leonardo.md');
const outputFile = path.join(__dirname, 'episodios', 'ep01_producao_leonardo.pdf');

const md = fs.readFileSync(inputFile, 'utf8');
const lines = md.split('\n');

const doc = new PDFDocument({ margin: 50, size: 'A4' });
doc.pipe(fs.createWriteStream(outputFile));

const COLORS = {
  h1: '#1a1a2e',
  h2: '#16213e',
  h3: '#0f3460',
  h4: '#533483',
  text: '#1a1a1a',
  code: '#2d2d2d',
  codeBg: '#f4f4f4',
  blockquote: '#555555',
  hr: '#cccccc',
  tableHeader: '#1a1a2e',
  tableHeaderText: '#ffffff',
  tableRowAlt: '#f9f9f9',
};

const FONTS = {
  regular: 'Helvetica',
  bold: 'Helvetica-Bold',
  italic: 'Helvetica-Oblique',
  mono: 'Courier',
};

let inCodeBlock = false;
let codeLines = [];
let inTable = false;
let tableRows = [];

function flushCode() {
  if (codeLines.length === 0) return;
  const codeText = codeLines.join('\n');
  const blockHeight = codeLines.length * 12 + 16;

  doc.rect(50, doc.y, doc.page.width - 100, blockHeight)
     .fill(COLORS.codeBg);

  doc.fillColor(COLORS.code)
     .font(FONTS.mono)
     .fontSize(7.5)
     .text(codeText, 58, doc.y - blockHeight + 8, {
       width: doc.page.width - 116,
       lineGap: 2,
     });

  doc.moveDown(0.5);
  codeLines = [];
}

function flushTable() {
  if (tableRows.length === 0) return;

  const colCount = tableRows[0].length;
  const colWidth = (doc.page.width - 100) / colCount;
  let y = doc.y;

  tableRows.forEach((row, rowIdx) => {
    // skip separator rows (---|---|---)
    if (row.every(cell => /^[-:]+$/.test(cell.trim()))) return;

    const isHeader = rowIdx === 0;
    const rowHeight = 18;

    if (isHeader) {
      doc.rect(50, y, doc.page.width - 100, rowHeight).fill(COLORS.tableHeader);
    } else if (rowIdx % 2 === 0) {
      doc.rect(50, y, doc.page.width - 100, rowHeight).fill(COLORS.tableRowAlt);
    }

    row.forEach((cell, colIdx) => {
      doc.fillColor(isHeader ? COLORS.tableHeaderText : COLORS.text)
         .font(isHeader ? FONTS.bold : FONTS.regular)
         .fontSize(8)
         .text(cell.trim(), 54 + colIdx * colWidth, y + 4, {
           width: colWidth - 8,
           height: rowHeight - 4,
           ellipsis: true,
           lineBreak: false,
         });
    });

    y += rowHeight;
  });

  doc.y = y + 6;
  doc.moveDown(0.3);
  tableRows = [];
  inTable = false;
}

function renderLine(line) {
  // Heading 1
  if (/^# /.test(line)) {
    const text = line.replace(/^# /, '');
    doc.moveDown(0.4)
       .fillColor(COLORS.h1)
       .font(FONTS.bold)
       .fontSize(18)
       .text(text);
    doc.moveDown(0.2)
       .rect(50, doc.y, doc.page.width - 100, 1.5).fill(COLORS.h1);
    doc.moveDown(0.5);
    return;
  }

  // Heading 2
  if (/^## /.test(line)) {
    const text = line.replace(/^## /, '');
    doc.moveDown(0.5)
       .fillColor(COLORS.h2)
       .font(FONTS.bold)
       .fontSize(14)
       .text(text);
    doc.moveDown(0.1)
       .rect(50, doc.y, doc.page.width - 100, 1).fill(COLORS.h2);
    doc.moveDown(0.4);
    return;
  }

  // Heading 3
  if (/^### /.test(line)) {
    const text = line.replace(/^### /, '');
    doc.moveDown(0.4)
       .fillColor(COLORS.h3)
       .font(FONTS.bold)
       .fontSize(11.5)
       .text(text);
    doc.moveDown(0.25);
    return;
  }

  // Heading 4
  if (/^#### /.test(line)) {
    const text = line.replace(/^#### /, '');
    doc.moveDown(0.3)
       .fillColor(COLORS.h4)
       .font(FONTS.bold)
       .fontSize(10)
       .text(text);
    doc.moveDown(0.2);
    return;
  }

  // Horizontal rule
  if (/^---+$/.test(line.trim())) {
    doc.moveDown(0.3)
       .rect(50, doc.y, doc.page.width - 100, 0.5).fill(COLORS.hr);
    doc.moveDown(0.5);
    return;
  }

  // Blockquote
  if (/^> /.test(line)) {
    const text = line.replace(/^> /, '');
    doc.rect(50, doc.y, 3, 14).fill(COLORS.h3);
    doc.fillColor(COLORS.blockquote)
       .font(FONTS.italic)
       .fontSize(9)
       .text(text, 60, doc.y - 13, { width: doc.page.width - 110 });
    doc.moveDown(0.3);
    return;
  }

  // Table row
  if (/^\|/.test(line)) {
    const cells = line.split('|').slice(1, -1);
    tableRows.push(cells);
    return;
  }

  // Bullet list
  if (/^[-*] /.test(line)) {
    const text = line.replace(/^[-*] /, '');
    doc.fillColor(COLORS.text)
       .font(FONTS.regular)
       .fontSize(9)
       .text(`• ${text}`, 60, doc.y, { width: doc.page.width - 110 });
    doc.moveDown(0.1);
    return;
  }

  // Bold+italic inline, inline code — plain text fallback with basic cleanup
  if (line.trim() === '') {
    if (inTable) { flushTable(); }
    doc.moveDown(0.25);
    return;
  }

  // Regular paragraph — strip basic markdown inline
  const clean = line
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/\*(.+?)\*/g, '$1')
    .replace(/`(.+?)`/g, '$1')
    .replace(/\[CHARACTER REF.*?\]/g, '[CHARACTER REF]');

  doc.fillColor(COLORS.text)
     .font(FONTS.regular)
     .fontSize(9)
     .text(clean, { width: doc.page.width - 100 });
  doc.moveDown(0.1);
}

// Main render loop
for (const line of lines) {
  // Code block toggle
  if (/^```/.test(line)) {
    if (!inCodeBlock) {
      if (inTable) flushTable();
      inCodeBlock = true;
    } else {
      inCodeBlock = false;
      flushCode();
    }
    continue;
  }

  if (inCodeBlock) {
    codeLines.push(line);
    continue;
  }

  // If we were building a table and hit a non-table line, flush it
  if (inTable && !/^\|/.test(line)) {
    flushTable();
  }

  if (/^\|/.test(line)) inTable = true;

  renderLine(line);
}

if (inCodeBlock) flushCode();
if (inTable) flushTable();

doc.end();
console.log('PDF gerado:', outputFile);
