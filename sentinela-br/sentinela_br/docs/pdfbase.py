from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("Cal", F + "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("CalB", F + "Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("CalI", F + "Carlito-Italic.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Cal", normal="Cal", bold="CalB", italic="CalI", boldItalic="CalB")

ACC = colors.HexColor("#0e7490")
CINZA = colors.HexColor("#555555")
S = {
 "t": ParagraphStyle("t", fontName="CalB", fontSize=20, leading=24, spaceAfter=4),
 "st": ParagraphStyle("st", fontName="Cal", fontSize=12, leading=15, textColor=CINZA, spaceAfter=14),
 "h1": ParagraphStyle("h1", fontName="CalB", fontSize=15, leading=19, spaceBefore=14, spaceAfter=6, textColor=ACC),
 "h2": ParagraphStyle("h2", fontName="CalB", fontSize=12, leading=15, spaceBefore=8, spaceAfter=3),
 "p": ParagraphStyle("p", fontName="Cal", fontSize=11, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6),
 "b": ParagraphStyle("b", fontName="Cal", fontSize=11, leading=14.5, leftIndent=12, bulletIndent=2, spaceAfter=3, alignment=TA_LEFT),
 "c": ParagraphStyle("c", fontName="Cal", fontSize=9.5, leading=12),
 "cb": ParagraphStyle("cb", fontName="CalB", fontSize=9.5, leading=12),
 "n": ParagraphStyle("n", fontName="CalI", fontSize=9, leading=11.5, textColor=CINZA, spaceAfter=6),
 "box": ParagraphStyle("box", fontName="Cal", fontSize=11, leading=14.5, alignment=TA_JUSTIFY),
}
def P(t, s="p"): return Paragraph(t, S[s])
def B(itens): return [Paragraph(t, S["b"], bulletText="•") for t in itens]
def tabela(cab, linhas, larg, cab_cor=colors.HexColor("#eef6f8")):
    dados = [[Paragraph(c, S["cb"]) for c in cab]] + [[Paragraph(str(c), S["c"]) for c in l] for l in linhas]
    t = Table(dados, colWidths=[w * cm for w in larg], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa5ab")), ("BACKGROUND", (0, 0), (-1, 0), cab_cor),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t
def caixa(texto):
    t = Table([[Paragraph(texto, S["box"])]], colWidths=[17 * cm])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, ACC), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f2fafb")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t
def gerar(caminho, titulo, story):
    def rodape(c, d):
        c.saveState(); c.setFont("Cal", 8.5); c.setFillColor(CINZA)
        c.drawString(2 * cm, 1.2 * cm, f"pAInel Sentinela BR · {titulo}")
        c.drawRightString(19 * cm, 1.2 * cm, f"Página {d.page}"); c.restoreState()
    doc = SimpleDocTemplate(caminho, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm, title=titulo, author="pAInel Sentinela BR")
    doc.build(story, onFirstPage=rodape, onLaterPages=rodape)
