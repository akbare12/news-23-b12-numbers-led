[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b12-numbers-led/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b12-numbers-led/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World Today — Monday 23 November 2026

One image that sums up Monday 23 November 2026's world news, drawn as a
front page. The giant number grid leads: ten figures, each with one line of
news — the KOSPI rout (-3.3%), the US–China power gap (5.3, narrowest since
2018), 11,762 Ebola cases in the DRC, Seoul's 10T-won stabilisation fund, the
2% billionaire tax, Skubal's $450M Mets deal, 165 Russian missiles in a week,
12,000 cleared in Manchester, 264 kg of explosives seized in Lebanon, and the
$107.3B Anthropic IPO.

Below the grid: a region bar (31 stories across 6 regions), a "THE DAY IN
UTC" strip, three hero scenes (AI rout hits Asia · Guterres: regulate AI
before it's too late · US lead over China at record low), ten more stories as
small cards, a world map with numbered pins, an "ALSO ON MONDAY" list, and a
DATE CHECK box that keeps out stories from other days (Democrats reach 258,
Sparta II fire, El Chapo captured — 22 Nov; EU–Indonesia pact, Nigeria boat —
21 Nov; ICJ Myanmar ruling — 19 Nov).

Scenes are drawn illustrations, not photographs. All figures as reported on
23 November 2026. Sources: Reuters, AP, Bloomberg, Yonhap, UN News, Asia
Power Index 2026.

## Run

```sh
python3 draw.py        # regenerate entry.png (1024x1024, <1 MiB)
python3 main.py        # copy entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

`main.py` is stdlib-only: it verifies the PNG header (1024x1024), copies the
bundled image, and verifies the destination byte-for-byte. It never writes
next to itself.
