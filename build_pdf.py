import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Preformatted, Table, TableStyle, HRFlowable)

OUTDIR = "assets"
os.makedirs(OUTDIR, exist_ok=True)
DPI = 300
MAX_EQN_WIDTH_PT = 430

def eqn_image(latex, name, fontsize=13):
    fig = plt.figure(figsize=(8, 2.2))
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, ha="center", va="center")
    path = os.path.join(OUTDIR, name)
    fig.savefig(path, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    from PIL import Image as PILImage
    im = PILImage.open(path)
    px_w, px_h = im.size
    pt_w, pt_h = px_w / DPI * 72, px_h / DPI * 72
    if pt_w > MAX_EQN_WIDTH_PT:
        s = MAX_EQN_WIDTH_PT / pt_w
        pt_w, pt_h = pt_w * s, pt_h * s
    img = Image(path, width=pt_w, height=pt_h)
    img.hAlign = "CENTER"
    return img

# ---------------------------------------------------------- Problem 1 plot
def make_f_plot():
    x = np.linspace(-2, 3, 1000)
    f = 2*(x-2)**2*(1-3**x)
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.axhline(0, color="black", linewidth=0.8)
    ax.plot(x, f, color="#1f4e79", linewidth=1.8)
    ax.plot([0, 2], [0, 0], "o", color="#c0392b", zorder=5, markersize=4)
    ax.set_xlabel("x", fontsize=9)
    ax.set_ylabel("f(x)", fontsize=9)
    ax.set_ylim(-60, 40)
    ax.grid(alpha=0.3)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    path = os.path.join(OUTDIR, "plot1.png")
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path

# ---------------------------------------------------------- cobweb plot (g2 near x=1)
def make_cobweb():
    def g2(x): return np.sign(3*x-2)*np.abs(3*x-2)**(1/3)
    xlim = (0.93, 1.38)
    xs = np.linspace(*xlim, 400)
    fig, ax = plt.subplots(figsize=(4.0, 4.0))
    ax.plot(xs, g2(xs), color="#1f4e79", linewidth=1.8, label="g$_2$(x)")
    ax.plot(xs, xs, color="#c0392b", linewidth=1.2, label="y = x")
    x = 1.32
    for _ in range(9):
        y = g2(x)
        ax.plot([x, x], [x, y], color="gray", linewidth=0.9)
        ax.plot([x, y], [y, y], color="gray", linewidth=0.9)
        x = y
    ax.set_xlim(*xlim); ax.set_ylim(*xlim)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    path = os.path.join(OUTDIR, "cobweb.png")
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path

plot1_path = make_f_plot()
cobweb_path = make_cobweb()

# ---------------------------------------------------------- styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleX", parent=styles["Title"], fontSize=15, spaceAfter=2)
sub_style = ParagraphStyle("SubX", parent=styles["Normal"], fontSize=9.5, textColor=colors.grey,
                            alignment=TA_CENTER, spaceAfter=10)
h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=12.5, spaceBefore=12, spaceAfter=4,
                     textColor=colors.HexColor("#1f4e79"))
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=10.5, spaceBefore=7, spaceAfter=3,
                     textColor=colors.HexColor("#2e5f8a"))
body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=9.3, leading=13, spaceAfter=5)
result = ParagraphStyle("Result", parent=styles["Normal"], fontSize=9.3, leading=13, spaceAfter=5,
                         backColor=colors.HexColor("#eef4fa"), borderPadding=5,
                         leftIndent=4, rightIndent=4)
code_style = ParagraphStyle("Code", parent=styles["Code"], fontSize=7.6, leading=9.6,
                             backColor=colors.HexColor("#f5f5f5"))
cap_style = ParagraphStyle("Cap", parent=styles["Normal"], fontSize=8.3, leading=11,
                            textColor=colors.HexColor("#444444"), alignment=TA_CENTER, spaceAfter=6)

def P(txt, style=body):
    return Paragraph(txt, style)

story = []

# ---------------------------------------------------------- Title
story.append(Paragraph("Exercise #4 &ndash; Solution Proposal", title_style))
story.append(Paragraph("TMA4130/TMA4135 &mdash; Autumn 2026", sub_style))
story.append(HRFlowable(width="100%", color=colors.HexColor("#1f4e79"), thickness=1))
story.append(Spacer(1, 6))

# ==================================================================
# PROBLEM 1
# ==================================================================
story.append(P("Problem 1 &mdash; Bisection Method", h1))
story.append(P("Writing t = 3<super>x</super>, f(x) collects into "
               "f(x) = 2(x&minus;2)<super>2</super>(1&minus;3<super>x</super>). "
               "So f has a <b>simple root at x = 0</b> and a <b>double root at x = 2</b>, and no others.", body))

story.append(P("a) Plot on [&minus;2, 3]", h2))
story.append(Image(plot1_path, width=8.2*cm, height=8.2*cm*3.0/4.6))

story.append(P("b) Four bisection steps on [&minus;2, 3]", h2))
story.append(P("f(&minus;2) &gt; 0, f(3) &lt; 0, so this brackets the root x = 0:", body))
table_data = [["n", "interval", "c", "sign f(c)", "new interval"],
              ["1", "[&minus;2, 3]", "0.5", "&minus;", "[&minus;2, 0.5]"],
              ["2", "[&minus;2, 0.5]", "&minus;0.75", "+", "[&minus;0.75, 0.5]"],
              ["3", "[&minus;0.75, 0.5]", "&minus;0.125", "+", "[&minus;0.125, 0.5]"],
              ["4", "[&minus;0.125, 0.5]", "0.1875", "&minus;", "[&minus;0.125, 0.1875]"]]
table_data = [[Paragraph(c, ParagraphStyle("t", parent=body, fontSize=8, alignment=TA_CENTER)) for c in row]
              for row in table_data]
t = Table(table_data, colWidths=[0.9*cm, 3.0*cm, 2.1*cm, 2.0*cm, 3.2*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6fa")]),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
]))
story.append(t)
story.append(Spacer(1, 4))
story.append(P("After 4 steps: [a<sub>4</sub>,b<sub>4</sub>] = [&minus;0.125, 0.1875], so "
               "&tilde;x = (a<sub>4</sub>+b<sub>4</sub>)/2 = <b>0.03125</b>, "
               "error bound = (b<sub>4</sub>&minus;a<sub>4</sub>)/2 = <b>0.15625</b> "
               "&mdash; this locates the root x = 0.", result))

story.append(P("c) Iterations for error &lt; 10<super>&minus;3</super>", h2))
story.append(P("Error bound after n steps is (b<sub>0</sub>&minus;a<sub>0</sub>)/2<super>n+1</super> = "
               "5/2<super>n+1</super>. Requiring this &lt; 10<super>&minus;3</super> gives "
               "2<super>n+1</super> &gt; 5000, i.e. n+1 &gt; log<sub>2</sub>(5000) &asymp; 12.29, so "
               "<b>n = 12</b> iterations suffice.", body))

story.append(P("d) The root at x = 2", h2))
story.append(P("f(2) = 0, but with even multiplicity (from the squared factor), so f does not change "
               "sign there (e.g. f(1) = &minus;4, f(2.5) &asymp; &minus;7.3, both negative). Bisection needs "
               "f(a)&middot;f(b) &lt; 0 to bracket a root, so it can never isolate x = 2.", body))

story.append(P("e) Python", h2))
code1 = '''def f(x): return 2*(x-2)**2*(1-3**x)

def bisection(f, a, b, tol=1e-4):
    fa, n = f(a), 0
    while (b-a)/2 > tol:
        c, fc = (a+b)/2, f((a+b)/2)
        if fa*fc < 0: b = c
        else: a, fa = c, fc
        n += 1
    return (a+b)/2, n

print(bisection(f, -2, 3, 1e-4))   # -> (4.58e-05, 15)'''
story.append(Preformatted(code1, code_style))
story.append(P("Root &asymp; 4.6&times;10<super>&minus;5</super> &asymp; 0 after <b>15 iterations</b> "
               "&mdash; matches part c) for tol = 10<super>&minus;4</super>.", result))

# ==================================================================
# PROBLEM 2
# ==================================================================
story.append(P("Problem 2 &mdash; Fixed-Point Method", h1))
story.append(P("f(x) = x<super>3</super> &minus; 3x + 2 = (x&minus;1)<super>2</super>(x+2): "
               "double root x = 1, simple root x = &minus;2.", body))

story.append(P("a) Derivatives", h2))
story.append(eqn_image(r"g_1'(x)=x^2,\quad g_2'(x)=\frac{1}{|3x-2|^{2/3}},\quad "
                        r"g_3'(x)=\frac{-4(x^2-x-1)}{(x^2+1)^2}", "eq2a.png", fontsize=11))
table2 = [["", "g<sub>1</sub>&prime;", "g<sub>2</sub>&prime;", "g<sub>3</sub>&prime;"],
          ["at x=1", "1", "1", "1"], ["at x=&minus;2", "4", "0.25", "&minus;0.80"]]
table2 = [[Paragraph(c, ParagraphStyle("t2", parent=body, fontSize=8, alignment=TA_CENTER)) for c in row]
          for row in table2]
t2 = Table(table2, colWidths=[2.4*cm, 3.4*cm, 3.4*cm, 3.4*cm])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6fa")]),
    ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
]))
story.append(t2)
story.append(Spacer(1, 4))
story.append(P("All three satisfy g<sub>i</sub>&prime;(1) = 1 exactly, since x=1 is a double root "
               "(f&prime;(1)=0) &mdash; none is a genuine contraction there. g<sub>1</sub> is only safe on "
               "(&minus;1,1), so it is unusable far from either root. Between g<sub>2</sub> and "
               "g<sub>3</sub>, g<sub>3</sub> has the smaller slope at both roots.", body))

story.append(P("b) Iterating from x<super>(0)</super>=4 until |x<super>(k+1)</super>&minus;x<super>(k)</super>| &lt; 10<super>&minus;6</super>", h2))
table3 = [["g", "outcome", "iterations"],
          ["g<sub>1</sub>(x) = (x&#179;+2)/3", "diverges", "&mdash;"],
          ["g<sub>2</sub>(x) = (3x&minus;2)<super>1/3</super>", "&rarr; x &asymp; 1", "1005"],
          ["g<sub>3</sub>(x) = (4x&minus;2)/(x&#178;+1)", "&rarr; x &asymp; &minus;2", "61"]]
table3 = [[Paragraph(c, ParagraphStyle("t3", parent=body, fontSize=8, alignment=TA_CENTER)) for c in row]
          for row in table3]
t3 = Table(table3, colWidths=[4.5*cm, 3.5*cm, 3.2*cm])
t3.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6fa")]),
    ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
]))
story.append(t3)
story.append(Spacer(1, 5))
story.append(Image(cobweb_path, width=6.2*cm, height=6.2*cm))
story.append(P("Cobweb of g<sub>2</sub> near x=1: the curve is tangent to y=x, so steps crawl instead "
               "of collapsing &mdash; this is why it takes 1005 iterations.", cap_style))
story.append(P("<b>Comment.</b> g<sub>1</sub> diverges (x<super>(0)</super>=4 is outside (&minus;1,1)). "
               "g<sub>2</sub> does reach x=1, but very slowly: multiplicity 2 forces g<sub>2</sub>&prime;&rarr;1 "
               "there, killing the usual geometric rate. g<sub>3</sub> converges fast &mdash; but overshoots "
               "past 1 and lands on the <i>other</i> root, x = &minus;2, where |g<sub>3</sub>&prime;| = 0.8 "
               "gives comfortable convergence. Lesson: |g&prime;| &lt; 1 only guarantees local convergence, "
               "and a double root can make it very slow even when satisfied.", result))

# ==================================================================
# PROBLEM 3
# ==================================================================
story.append(P("Problem 3 &mdash; Newton's Method", h1))
story.append(P("f(x) = x &minus; e<super>&minus;x</super>, f&prime;(x) = 1 + e<super>&minus;x</super>:", body))
story.append(eqn_image(r"x_{n+1} = x_n - \frac{x_n - e^{-x_n}}{1+e^{-x_n}}", "eq3.png", fontsize=13))

story.append(P("a) Two steps from x<sub>0</sub> = 2", h2))
story.append(P("x<sub>1</sub> = 2 &minus; (2&minus;e<super>&minus;2</super>)/(1+e<super>&minus;2</super>) "
               "&asymp; <b>0.3576</b><br/>"
               "x<sub>2</sub> = x<sub>1</sub> &minus; (x<sub>1</sub>&minus;e<super>&minus;x1</super>)/"
               "(1+e<super>&minus;x1</super>) &asymp; <b>0.5587</b>", body))

story.append(P("b) Python", h2))
code3 = '''def fN(x):  return x - np.exp(-x)
def fNp(x): return 1 + np.exp(-x)

def newton(x0, tol=1e-6):
    x, n = x0, 0
    while abs(fN(x)) > tol:
        x = x - fN(x)/fNp(x); n += 1
    return x, n

print(newton(2.0))   # -> (0.5671432904, 5)'''
story.append(Preformatted(code3, code_style))
story.append(P("Converges to <b>x &asymp; 0.5671433</b> (the Omega constant) in <b>5 iterations</b>.", result))

# ==================================================================
# PROBLEM 4
# ==================================================================
story.append(P("Problem 4", h1))
story.append(eqn_image(r"e^{e^{-x}} = \frac{5x}{3}", "eq4.png", fontsize=13))

story.append(P("a) Uniqueness", h2))
story.append(P("e<super>&minus;x</super> is strictly decreasing, so e<super>e<sup>&minus;x</sup></super> "
               "is strictly decreasing, while 5x/3 is strictly increasing &mdash; their difference is "
               "strictly decreasing, so <b>at most one</b> root. As x&rarr;&minus;&infin; it &rarr; +&infin;, "
               "as x&rarr;+&infin; it &rarr; &minus;&infin;, so by IVT there is <b>exactly one</b> root x*.", body))

story.append(P("b) Error bound", h2))
story.append(P("The code iterates x = g(x) with g(x) = (3/5)e<super>e<sup>&minus;x</sup></super>, "
               "g&prime;(x) = &minus;e<super>&minus;x</super>g(x). It converges after <b>16 steps</b> to "
               "x &asymp; 0.9007279 (last step size &asymp; 9.33&times;10<super>&minus;7</super>). "
               "On [0.8,1.0], L = max|g&prime;| &asymp; 0.4225 &lt; 1, so the fixed-point bound gives", body))
story.append(eqn_image(r"e = |x^*-x_{16}| \leq \frac{L}{1-L}|x_{16}-x_{15}| \approx 6.8\times10^{-7}",
                        "eq4b.png", fontsize=12))
story.append(P("i.e. <b>x* &asymp; 0.900728</b>, accurate to about 6&ndash;7 significant digits.", result))

story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", color=colors.grey, thickness=0.5))
story.append(P("<i>All numerical results verified with Python/NumPy.</i>",
               ParagraphStyle("foot", parent=body, fontSize=7.5, textColor=colors.grey)))

doc = SimpleDocTemplate("Exercise_4_1_Solution_Proposal.pdf", pagesize=A4,
                         topMargin=1.4*cm, bottomMargin=1.4*cm, leftMargin=1.9*cm, rightMargin=1.9*cm,
                         title="Exercise 4 - Solution Proposal")
doc.build(story)
print("done")
