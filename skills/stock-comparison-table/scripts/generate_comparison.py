import sys, json, math, time
import yfinance as yf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

if len(sys.argv) < 2:
    print("Usage: python3 generate_comparison.py TICKER1,TICKER2,...")
    sys.exit(1)

tickers = [t.strip().upper() for t in sys.argv[1].split(",") if t.strip()]
print(f"Fetching data for: {tickers}")

def safe(val):
    if val is None: return None
    try:
        f = float(val)
        return None if math.isnan(f) else f
    except: return None

def fmt(val, mode="num", dp=1):
    v = safe(val)
    if v is None: return "N/A"
    if mode == "pct":  return f"{v*100:.{dp}f}%"
    if mode == "usd":  return f"${v:.2f}"
    if mode == "int":  return str(int(v))
    return f"{v:.{dp}f}"

results = {}
for t in tickers:
    print(f"\nFetching {t}...")
    for attempt in range(3):
        try:
            tk = yf.Ticker(t)
            info = tk.info

            price         = safe(info.get("currentPrice")) or safe(info.get("regularMarketPrice"))
            fwd_pe        = safe(info.get("forwardPE"))
            peg           = safe(info.get("pegRatio"))
            gross_margin  = safe(info.get("grossMargins"))
            net_margin    = safe(info.get("profitMargins"))
            ebitda_margin = safe(info.get("ebitdaMargins"))
            rev_growth    = safe(info.get("revenueGrowth"))
            earn_growth   = safe(info.get("earningsGrowth"))
            eps_fwd       = safe(info.get("forwardEps"))
            fcf           = safe(info.get("freeCashflow"))
            mktcap        = safe(info.get("marketCap"))
            target_mean   = safe(info.get("targetMeanPrice"))
            target_high   = safe(info.get("targetHighPrice"))
            target_low    = safe(info.get("targetLowPrice"))
            rec_key       = info.get("recommendationKey", "N/A")
            rec           = rec_key.replace("_", " ").title() if rec_key else "N/A"
            num_analysts  = safe(info.get("numberOfAnalystOpinions"))
            upside        = ((target_mean - price) / price) if (target_mean and price) else None

            fcf_yield = None
            if fcf and mktcap:
                fcf_yield = fcf / mktcap

            # Fallback PEG
            fwd_eps_growth_est = None
            try:
                ge = tk.growth_estimates
                if ge is not None and not ge.empty and "+1y" in ge.index:
                    fwd_eps_growth_est = safe(float(ge.loc["+1y", ge.columns[0]]))
            except: pass

            if peg is None and fwd_pe and fwd_eps_growth_est and fwd_eps_growth_est > 0:
                peg = round(fwd_pe / (fwd_eps_growth_est * 100), 2)

            # Fallback FCF
            if fcf_yield is None:
                try:
                    cf = tk.cashflow
                    if cf is not None and not cf.empty and "Free Cash Flow" in cf.index:
                        fcf_stmt = safe(float(cf.loc["Free Cash Flow", cf.columns[0]]))
                        if fcf_stmt and mktcap:
                            fcf_yield = fcf_stmt / mktcap
                except: pass

            results[t] = {
                "price": price, "fwd_pe": fwd_pe, "peg": peg,
                "gross_margin": gross_margin, "net_margin": net_margin, "ebitda_margin": ebitda_margin,
                "rev_growth": rev_growth, "earn_growth": earn_growth, "eps_fwd": eps_fwd,
                "fcf_yield": fcf_yield, "rec": rec, "num_analysts": num_analysts,
                "target_mean": target_mean, "target_low": target_low, "target_high": target_high,
                "upside": upside
            }
            print(f"  [OK] fwdPE={fmt(fwd_pe)} | PEG={fmt(peg)} | Rec={rec}")
            break
        except Exception as e:
            print(f"  [ERR] attempt {attempt+1}: {e}")
            time.sleep(2)
    else:
        results[t] = {"error": "Failed to fetch"}

with open("/home/ubuntu/stock_comparison_data.json", "w") as f:
    json.dump(results, f, indent=2)

# ── Ranking
rating_score = {"Strong Buy": 4, "Buy": 3, "Hold": 2, "Underperform": 1, "Sell": 0}

def rank_score(t):
    d = results[t]
    if "error" in d: return 9999
    pe  = safe(d.get("fwd_pe"))
    peg = safe(d.get("peg"))
    rat = rating_score.get(d.get("rec", "Hold"), 2)
    if pe is None or pe < 0: pe = 500
    if peg is None or peg < 0: peg = 50
    return 0.4 * pe + 0.4 * peg - 0.2 * rat * 10

ranked = sorted(tickers, key=rank_score)
print("\nRanking (best → worst):", ranked)

# ── Table Generation
rows = [
    ("Price (USD)",           "price",         "usd"),
    ("Forward P/E",           "fwd_pe",        "num"),
    ("PEG Ratio",             "peg",           "num"),
    ("Gross Margin",          "gross_margin",  "pct"),
    ("Net Margin",            "net_margin",    "pct"),
    ("EBITDA Margin",         "ebitda_margin", "pct"),
    ("Rev Growth (TTM)",      "rev_growth",    "pct"),
    ("EPS Growth (TTM)",      "earn_growth",   "pct"),
    ("Forward EPS",           "eps_fwd",       "usd"),
    ("FCF Yield",             "fcf_yield",     "pct"),
    ("Analyst Rating",        "rec",           "str"),
    ("# Analysts",            "num_analysts",  "int"),
    ("Price Target (Mean)",   "target_mean",   "usd"),
    ("Price Target (Low)",    "target_low",    "usd"),
    ("Price Target (High)",   "target_high",   "usd"),
    ("Upside to Mean Target", "upside",        "pct"),
]

def cell_text(t, key, mode):
    d = results[t]
    if "error" in d: return "ERR"
    if mode == "str": return str(d.get(key, "N/A"))
    if mode == "int":
        v = safe(d.get(key))
        return str(int(v)) if v is not None else "N/A"
    v = safe(d.get(key))
    if key == "fwd_pe" and (v is None or v < 0): return "Pre-Profit"
    if key == "peg" and (v is None or v < 0): return "N/A"
    return fmt(v, mode)

cell_data = [[cell_text(t, key, mode) for t in ranked] for _, key, mode in rows]

def c_pe(v):
    if v is None or v < 0: return "#e8daef"
    if v < 20: return "#a9dfbf"
    if v < 30: return "#d5f5e3"
    if v < 45: return "#fef9e7"
    if v < 60: return "#fdebd0"
    return "#fadbd8"

def c_peg(v):
    if v is None or v < 0: return "#f0f0f0"
    if v < 1: return "#a9dfbf"
    if v < 1.5: return "#d5f5e3"
    if v < 2.5: return "#fef9e7"
    if v < 3.5: return "#fdebd0"
    return "#fadbd8"

def c_margin(v, hi=40, lo=15):
    if v is None: return "#f0f0f0"
    p = v * 100
    if p >= hi: return "#a9dfbf"
    if p >= lo: return "#d5f5e3"
    if p >= 0: return "#fef9e7"
    return "#fadbd8"

def c_growth(v):
    if v is None: return "#f0f0f0"
    p = v * 100
    if p >= 50: return "#a9dfbf"
    if p >= 15: return "#d5f5e3"
    if p >= 0: return "#fef9e7"
    return "#fadbd8"

def c_fcf(v):
    if v is None: return "#f0f0f0"
    p = v * 100
    if p >= 3: return "#a9dfbf"
    if p >= 1: return "#d5f5e3"
    if p >= 0: return "#fef9e7"
    return "#fadbd8"

def c_rating(v):
    m = {"Strong Buy": "#a9dfbf", "Buy": "#d5f5e3", "Hold": "#fef9e7", "Underperform": "#fadbd8", "Sell": "#fadbd8"}
    return m.get(str(v), "#f0f0f0")

def c_upside(v):
    if v is None: return "#f0f0f0"
    p = v * 100
    if p >= 20: return "#a9dfbf"
    if p >= 5: return "#d5f5e3"
    if p >= -5: return "#fef9e7"
    return "#fadbd8"

color_fn_map = {
    "Forward P/E": lambda rv, _: c_pe(rv),
    "PEG Ratio": lambda rv, _: c_peg(rv),
    "Gross Margin": lambda rv, _: c_margin(rv, 50, 25),
    "Net Margin": lambda rv, _: c_margin(rv, 20, 10),
    "EBITDA Margin": lambda rv, _: c_margin(rv, 30, 15),
    "Rev Growth (TTM)": lambda rv, _: c_growth(rv),
    "EPS Growth (TTM)": lambda rv, _: c_growth(rv),
    "FCF Yield": lambda rv, _: c_fcf(rv),
    "Analyst Rating": lambda rv, cv: c_rating(cv),
    "Upside to Mean Target": lambda rv, _: c_upside(rv),
}

cell_colors = []
for ri, (label, key, mode) in enumerate(rows):
    row_colors = []
    for ci, t in enumerate(ranked):
        raw_val = results[t].get(key) if "error" not in results[t] else None
        cell_val = cell_data[ri][ci]
        if label in color_fn_map:
            row_colors.append(color_fn_map[label](raw_val, cell_val))
        else:
            row_colors.append("#f9f9f9")
    cell_colors.append(row_colors)

fig_w = 2.5 + len(ranked) * 1.8
fig_h = 1.2 + len(rows) * 0.46
fig, ax = plt.subplots(figsize=(fig_w, fig_h))
ax.axis("off")

tbl = ax.table(
    cellText=cell_data, rowLabels=[r[0] for r in rows], colLabels=ranked,
    cellLoc="center", rowLoc="right", loc="center", cellColours=cell_colors
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1, 1.4)

colors = ["#1a6faf", "#7d3c98", "#1e8449", "#c0392b", "#d35400", "#2471a3", "#717d7e"]
for j, t in enumerate(ranked):
    cell = tbl[0, j]
    cell.set_facecolor(colors[j % len(colors)])
    cell.set_text_props(color="white", fontweight="bold", fontsize=10)

for i in range(len(rows)):
    cell = tbl[i+1, -1]
    cell.set_facecolor("#1c2833")
    cell.set_text_props(color="white", fontweight="bold", fontsize=9)
    cell.set_width(0.25)

ax.annotate("◀  Best Value / Strongest Buy", xy=(0.06, 0.97), xycoords="axes fraction", fontsize=9, color="#1a5276", fontstyle="italic", fontweight="bold")
ax.annotate("Weakest Relative Value  ▶", xy=(0.72, 0.97), xycoords="axes fraction", fontsize=9, color="#922b21", fontstyle="italic", fontweight="bold")

fig.suptitle(f"Stock Comparison: {', '.join(tickers)}\nSorted: Lowest Fwd P/E + Lowest PEG + Strongest Buy Rating", fontsize=11, fontweight="bold", y=0.998)

out = "/home/ubuntu/stock_comparison_ranked.png"
plt.tight_layout(rect=[0, 0.02, 1, 0.97])
plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
print(f"\nSaved image to {out}")
