#!/usr/bin/env python3
"""news-23-b12-numbers-led: draw the 23 Nov 2026 front page (1024x1024)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (176, 42, 32)
BLUE = (31, 78, 121)
TEAL = (14, 110, 110)
GOLD = (176, 124, 20)
GREY = (90, 88, 82)
LIGHT = (233, 228, 216)
LINE = (200, 194, 178)

F_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, f, fill, leading=None, spacing=0):
    if leading is None:
        leading = f.size + 2
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def chip(d, x, y, label, fill, fg=(255, 255, 255), f=None):
    f = f or font(F_B, 9)
    w = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill=fg)
    return w


def hline(d, y, x0=12, x1=1012, fill=INK, w=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


# ---------------------------------------------------------------- data
NUMBERS = [
    ("-3.3%", "KOSPI ROUT — AI SELL-OFF SPREADS FROM WALL ST", RED),
    ("5.3", "US–CHINA POWER GAP, NARROWEST SINCE 2018", BLUE),
    ("11,762", "EBOLA CASES IN THE DRC OUTBREAK", TEAL),
    ("10T won", "SEOUL STABILISATION FUND READIED", GOLD),
    ("2%", "BILLIONAIRE TAX BACKED IN PARIS", BLUE),
    ("$450M", "SKUBAL TO THE METS — RECORD PITCHER DEAL", RED),
    ("165", "RUSSIAN MISSILES FIRED AT UKRAINE IN A WEEK", BLUE),
    ("12,000", "CLEARED IN MANCHESTER AFTER SUBSTANCE SCARE", TEAL),
    ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", RED),
    ("$107.3B", "ANTHROPIC IPO — LARGEST EVER", GOLD),
]

REGIONS = [("ASIA-PACIFIC", 7, BLUE), ("AMERICAS", 8, RED),
           ("EUROPE", 5, TEAL), ("MIDDLE EAST", 6, GOLD),
           ("AFRICA", 3, (110, 60, 120)), ("WORLD", 2, GREY)]

UTC = [
    ("~02:00", "Seoul opens: KOSPI dives, intraday -5.8%"),
    ("~05:30", "Guterres opens AI summit in Bridgetown"),
    ("~08:00", "Asia Power Index: US 78.9, China 73.6"),
    ("~11:00", "Paris rally backs 2% billionaire tax"),
    ("~15:00", "Kyiv: 165 Russian missiles in seven days"),
    ("~20:30", "Anthropic debut closes at $97.17"),
]

HEROES = [
    dict(kick="MARKETS · ASIA", col=RED, title="AI ROUT HITS ASIA",
         body="Kospi closes 4,708.54, down 3.3% and 161 points after an intraday plunge of 5.8%. Samsung -3.1%, SK Hynix -2.5% as the AI sell-off spreads from Wall Street.",
         src="REUTERS", scene="chart"),
    dict(kick="UNITED NATIONS", col=BLUE, title="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="The UN chief urges global AI safety rules at the Bridgetown summit. 150 delegates back a risk framework — a blueprint, not a treaty.",
         src="AP", scene="podium"),
    dict(kick="POWER INDEX 2026", col=TEAL, title="US LEAD OVER CHINA AT RECORD LOW",
         body="Asia Power Index 2026: US 78.9, China 73.6 — a gap of 5.3, the narrowest since 2018. US diplomatic influence falls 6 to 76.7. India third at 40.5.",
         src="BLOOMBERG", scene="bars"),
]

CARDS = [
    ("WASHINGTON", RED, "Bessent demands Nvidia answers", "Treasury chief wants to know of violations over China sales.", "REUTERS"),
    ("FBI", BLUE, "FBI probes hack of police database", "The NCIC system, used by police nationwide, is breached.", "AP"),
    ("WHITE HOUSE", RED, "Trump: Iran strikes may resume", "President says strikes could resume in the New Year.", "REUTERS"),
    ("SPORT", GOLD, "Skubal signs $450M Mets deal", "Two-time Cy Young winner, largest ever for a pitcher.", "AP"),
    ("MARKETS", GOLD, "Anthropic IPO: $107.3B", "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.", "BLOOMBERG"),
    ("EUROPE", TEAL, "Poland: 3 Russian missiles crossed airspace", "Kyiv says three Kh-101 cruise missiles entered Poland on Friday.", "AP"),
    ("PARIS", BLUE, "100+ back 2% billionaire tax", "Economists, politicians and unions rally behind the plan.", "REUTERS"),
    ("BRITAIN", TEAL, "Manchester: 12,000 cleared", "Crowds cleared after a substance scare in the city centre.", "AP"),
    ("KYIV", BLUE, "Zelenskyy: 165 missiles in a week", "Moscow fired 165 missiles in seven days as US delays Patriots.", "REUTERS"),
    ("CLIMATE", TEAL, "COP31: the day after", "Sunday's collapse — 194 nations reject the Antalya Pact — draws fury.", "AP"),
]

ALSO = [
    "Tom Jackson dies at 75 — Broncos linebacker, ESPN",
    "10 states sue SpaceX over AI safety claims",
    "Intel: Russian nuclear satellite, launch next month — CLAIM",
    "Benghazi: UN demands probe of port attacks — CLAIM",
    "Israel unity talks resume after Sunday stall",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks hit villages",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg of explosives",
    "Bahrain: Iranian strike hits plant, 2 hurt",
    "Sudan air defences down drones over Khartoum — CLAIM",
    "DRC: fighting traps Ebola teams in Ituri",
    "Bangladesh: Hasina will be jailed if she returns",
    "Seoul minister quits over AI exam chaos",
    "SK Telecom -7.3% as Anthropic hype cools",
    "China eases margin rules to calm rout",
    "Seoul readies 10T-won stabilisation fund",
    "US futures jump 3% into holiday week",
]

# ---------------------------------------------------------------- scenes
def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 30, 44))
    for i in range(5):
        yy = y + 12 + i * (h - 24) // 4
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(60, 70, 95), width=1)
    pts = [(x + 10, y + 18), (x + w * 0.3, y + 30), (x + w * 0.5, y + 26),
           (x + w * 0.7, y + 52), (x + w - 12, y + h - 14)]
    d.line(pts, fill=(230, 70, 50), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 120, 100))
    d.text((x + 10, y + h - 22), "-3.3%", font=font(F_B, 20), fill=(255, 150, 130))


def scene_podium(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 84))
    d.ellipse([x + w // 2 - 90, y + 14, x + w // 2 + 90, y + 110], fill=(120, 170, 220))
    d.ellipse([x + w // 2 - 62, y + 28, x + w // 2 + 62, y + 96], fill=(170, 205, 235))
    d.rectangle([x + w // 2 - 34, y + h - 52, x + w // 2 + 34, y + h - 8], fill=(90, 60, 30))
    d.rectangle([x + w // 2 - 46, y + h - 62, x + w // 2 + 46, y + h - 52], fill=(120, 80, 40))
    d.ellipse([x + w // 2 - 12, y + h - 92, x + w // 2 + 12, y + h - 62], fill=(240, 200, 160))
    d.polygon([(x + w // 2 - 12, y + h - 62), (x + w // 2 + 12, y + h - 62),
               (x + w // 2 + 26, y + h - 22), (x + w // 2 - 26, y + h - 22)], fill=(40, 40, 40))
    d.text((x + 10, y + 8), "BRIDGETOWN", font=font(F_B, 12), fill=(255, 255, 255))


def scene_bars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 240))
    bx, bw = x + 40, 62
    h1 = int((h - 40) * 0.789)
    h2 = int((h - 40) * 0.736)
    d.rectangle([bx, y + h - 20 - h1, bx + bw, y + h - 20], fill=BLUE)
    d.rectangle([bx + 100, y + h - 20 - h2, bx + 100 + bw, y + h - 20], fill=RED)
    d.text((bx + 4, y + h - 20 - h1 - 20), "78.9", font=font(F_B, 15), fill=BLUE)
    d.text((bx + 104, y + h - 20 - h2 - 20), "73.6", font=font(F_B, 15), fill=RED)
    d.text((bx - 4, y + h - 18), "US", font=font(F_B, 12), fill=INK)
    d.text((bx + 96, y + h - 18), "CHINA", font=font(F_B, 12), fill=INK)
    d.text((x + w - 78, y + 8), "GAP 5.3", font=font(F_B, 15), fill=RED)


SCENES = {"chart": scene_chart, "podium": scene_podium, "bars": scene_bars}

# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 7], fill=INK)

    # masthead
    f_mast = font(F_B, 46)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 12), t, font=f_mast, fill=INK)
    d.text((12, 62), "MONDAY, 23 NOVEMBER 2026", font=font(F_B, 15), fill=RED)
    r = "THE DAY IN ONE PAGE  ·  31 STORIES"
    d.text(((W - 12 - d.textlength(r, font=font(F_B, 15))), 62), r,
           font=font(F_B, 15), fill=INK)
    hline(d, 82)

    # numbers grid
    d.text((12, 88), "THE DAY IN NUMBERS", font=font(F_B, 13), fill=INK)
    d.text(((W - 12 - d.textlength("EVERY FIGURE, ONE LINE OF NEWS", font=font(F_R, 11))), 90),
           "EVERY FIGURE, ONE LINE OF NEWS", font=font(F_R, 11), fill=GREY)
    cw, ch, gx, gy = 195, 72, 6, 6
    x0, y0 = 12, 104
    for i, (num, lab, col) in enumerate(NUMBERS):
        cx = x0 + (i % 5) * (cw + gx)
        cy = y0 + (i // 5) * (ch + gy)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(255, 255, 255),
                    outline=LINE, width=1)
        d.rectangle([cx, cy, cx + 4, cy + ch], fill=col)
        d.text((cx + 12, cy + 5), num, font=font(F_B, 25), fill=col)
        lines = wrap(d, lab, font(F_B, 10), cw - 20)
        text_block(d, cx + 12, cy + 36, lines[:2], font(F_B, 10), INK, leading=12)

    # region bar
    ry = 260
    d.rectangle([12, ry, 1012, ry + 24], fill=INK)
    x = 22
    for name, n, col in REGIONS:
        lab = "%s %d" % (name, n)
        w = int(d.textlength(lab, font=font(F_B, 12))) + 14
        d.rounded_rectangle([x, ry + 4, x + w, ry + 20], radius=3, fill=col)
        d.text((x + 7, ry + 6), lab, font=font(F_B, 12), fill=(255, 255, 255))
        x += w + 10
    d.text((x + 4, ry + 6), "31 STORIES · 6 REGIONS", font=font(F_B, 12), fill=(255, 255, 255))

    # UTC strip — flowing inline segments, two lines max
    uy = 290
    d.text((12, uy), "THE DAY IN UTC", font=font(F_B, 12), fill=RED)
    d.text(((W - 12 - d.textlength("~ = APPROXIMATE TIME", font=font(F_R, 10))), uy + 1),
           "~ = APPROXIMATE TIME", font=font(F_R, 10), fill=GREY)
    hline(d, uy + 17, fill=LINE, w=1)
    segs = []
    for tm, ev in UTC:
        segs.append((tm + "  ", font(F_B, 11), RED))
        segs.append((ev + "   ·   ", font(F_R, 10), INK))
    xx, yy = 12, uy + 22
    for txt, f, col in segs:
        wseg = d.textlength(txt, font=f)
        if xx + wseg > 1012 and xx > 12:
            xx, yy = 12, yy + 12
        d.text((xx, yy), txt, font=f, fill=col)
        xx += wseg
    hline(d, 334, fill=LINE, w=1)

    # heroes
    hy, hh, hw = 338, 186, 324
    for i, h in enumerate(HEROES):
        hx = 12 + i * (hw + 8)
        d.rectangle([hx, hy, hx + hw, hy + hh], fill=(255, 255, 255), outline=LINE, width=1)
        SCENES[h["scene"]](d, hx + 1, hy + 1, hw - 2, 80)
        d.text((hx + 10, hy + 88), h["kick"], font=font(F_B, 10), fill=h["col"])
        lines = wrap(d, h["title"], font(F_B, 15), hw - 20)
        yy = text_block(d, hx + 10, hy + 102, lines[:2], font(F_B, 15), INK, leading=17)
        bl = wrap(d, h["body"], font(F_R, 10), hw - 20)
        text_block(d, hx + 10, yy + 1, bl[:3], font(F_R, 10), INK, leading=11)
        d.text((hx + 10, hy + hh - 13), "SOURCE: " + h["src"], font=font(F_B, 9), fill=GREY)

    # cards
    cy0 = 530
    d.text((12, cy0), "MORE OF THE DAY", font=font(F_B, 13), fill=INK)
    hline(d, cy0 + 18, fill=LINE, w=1)
    ccw, cch = 195, 100
    for i, (kick, col, title, body, src) in enumerate(CARDS):
        cx = 12 + (i % 5) * (ccw + 6)
        cy = cy0 + 24 + (i // 5) * (cch + 6)
        d.rectangle([cx, cy, cx + ccw, cy + cch], fill=(255, 255, 255), outline=LINE, width=1)
        d.rectangle([cx, cy, cx + ccw, cy + 22], fill=col)
        d.text((cx + 8, cy + 5), kick, font=font(F_B, 10), fill=(255, 255, 255))
        tl = wrap(d, title, font(F_B, 12), ccw - 16)
        yy = text_block(d, cx + 8, cy + 28, tl[:2], font(F_B, 12), INK, leading=14)
        bl = wrap(d, body, font(F_R, 10), ccw - 16)
        text_block(d, cx + 8, yy + 2, bl[:2], font(F_R, 10), INK, leading=12)
        d.text((cx + 8, cy + cch - 14), "SOURCE: " + src, font=font(F_B, 8), fill=GREY)

    # map + also
    my = 766
    d.text((12, my), "WHERE IT HAPPENED", font=font(F_B, 13), fill=INK)
    d.text((452, my), "ALSO ON MONDAY", font=font(F_B, 13), fill=INK)
    hline(d, my + 18, fill=LINE, w=1)
    mx, mw, mh = 12, 424, 128
    d.rectangle([mx, my + 24, mx + mw, my + 24 + mh], fill=(214, 226, 232), outline=LINE, width=1)
    for gx_ in range(1, 7):
        xx = mx + gx_ * mw // 7
        d.line([(xx, my + 24), (xx, my + 24 + mh)], fill=(190, 205, 212), width=1)
    for gy_ in range(1, 4):
        yy = my + 24 + gy_ * mh // 4
        d.line([(mx, yy), (mx + mw, yy)], fill=(190, 205, 212), width=1)
    # rough continents
    cont = [
        [(30, 30), (90, 22), (118, 34), (112, 62), (78, 74), (52, 66), (28, 52)],
        [(108, 92), (140, 88), (150, 116), (132, 150), (112, 128)],
        [(212, 26), (238, 20), (246, 38), (228, 52), (210, 44)],
        [(212, 62), (244, 58), (256, 84), (244, 122), (224, 108), (208, 82)],
        [(250, 18), (330, 14), (360, 34), (352, 62), (318, 78), (268, 66), (250, 40)],
        [(318, 122), (352, 118), (356, 136), (326, 142)],
    ]
    for poly in cont:
        d.polygon([(mx + a, my + 24 + b) for a, b in poly], fill=(168, 188, 158),
                  outline=(120, 140, 115))
    pins = [(330, 42, "1"), (108, 82, "2"), (100, 55, "3"), (228, 32, "4"),
            (214, 38, "5"), (228, 100, "6")]
    for px, py, n in pins:
        d.ellipse([mx + px - 8, my + 24 + py - 8, mx + px + 8, my + 24 + py + 8],
                  fill=RED, outline=(255, 255, 255), width=2)
        d.text((mx + px - 3, my + 24 + py - 6), n, font=font(F_B, 9), fill=(255, 255, 255))
    d.text((mx + 6, my + 24 + mh - 16), "1 SEOUL  2 BRIDGETOWN  3 WASHINGTON  4 KYIV  5 PARIS  6 KINSHASA",
           font=font(F_B, 9), fill=INK)
    # also list, two columns
    ax = 452
    for i, item in enumerate(ALSO):
        col_i = i % 2
        row_i = i // 2
        xx = ax + col_i * 284
        yy = my + 26 + row_i * 15
        d.text((xx, yy), "·", font=font(F_B, 11), fill=RED)
        lines = wrap(d, item, font(F_R, 10), 272)
        text_block(d, xx + 10, yy, lines[:1], font(F_R, 10), INK, leading=12)

    # date check
    dy = 924
    d.rectangle([12, dy, 1012, dy + 62], outline=RED, width=2, fill=(255, 244, 242))
    d.text((22, dy + 6), "DATE CHECK", font=font(F_B, 12), fill=RED)
    d.text((130, dy + 7), "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY",
           font=font(F_B, 10), fill=INK)
    d.text((22, dy + 24),
           "LEFT OUT (NOT 23 NOV): Democrats reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo captured (22 Nov)",
           font=font(F_R, 10), fill=INK)
    d.text((22, dy + 38),
           "EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)",
           font=font(F_R, 10), fill=INK)
    d.text((22, dy + 50),
           "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating Ebola staff",
           font=font(F_R, 10), fill=INK)

    # footer
    fy = 992
    hline(d, fy, fill=LINE, w=1)
    d.text((12, fy + 6),
           "SOURCES: REUTERS · AP · BLOOMBERG · YONHAP · UN NEWS · ASIA POWER INDEX 2026 — CHIPS: REPORTED = confirmed · CLAIM = alleged, unverified · ONGOING = developing",
           font=font(F_R, 9), fill=GREY)
    d.text((12, fy + 19),
           "Scenes are drawn illustrations, not photographs. All figures as reported on 23 November 2026.",
           font=font(F_R, 10), fill=GREY)
    d.text(((W - 12 - d.textlength("THE WORLD TODAY — 23 NOV 2026", font=font(F_B, 10))), fy + 19),
           "THE WORLD TODAY — 23 NOV 2026", font=font(F_B, 10), fill=INK)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
