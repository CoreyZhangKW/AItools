---
name: stock-comparison-table
description: Generates a color-coded, ranked side-by-side comparison table for a list of stocks using real-time Yahoo Finance data. Use when the user asks to compare stocks, generate a stock comparison table, or rank stocks based on financial metrics like P/E, PEG, margins, and analyst ratings.
license: Complete terms in LICENSE.txt
---

# Stock Comparison Table Generator

This skill provides a standardized workflow and Python script to fetch comprehensive financial metrics for a list of stocks, resolve missing data, rank the stocks by value and sentiment, and generate a high-quality, color-coded comparison table image.

## When to Use

Use this skill whenever a user requests:
- A side-by-side comparison of multiple stocks
- A ranked table of stocks based on valuation or growth metrics
- A visual comparison of financial metrics (P/E, PEG, margins, FCF yield) across a sector or theme

## Workflow

1. **Understand the Request:** Identify the list of ticker symbols the user wants to compare.
2. **Execute the Script:** Run the bundled Python script, passing the comma-separated list of tickers as an argument.
3. **Review the Output:** The script will output a JSON file with the raw data and a high-resolution PNG image of the ranked comparison table.
4. **Deliver to User:** Present the generated image to the user along with a brief markdown summary of the rankings and key takeaways.

## Bundled Resources

### `scripts/generate_comparison.py`

This is the core script that handles data fetching, N/A resolution, ranking, and image generation.

**Usage:**
```bash
python3 /home/ubuntu/skills/stock-comparison-table/scripts/generate_comparison.py TICKER1,TICKER2,TICKER3
```
*Example:* `python3 /home/ubuntu/skills/stock-comparison-table/scripts/generate_comparison.py NVDA,AMD,INTC,TSM`

**What the script does:**
1. **Fetches Data:** Uses `yfinance` to pull current price, forward P/E, PEG, margins, growth rates, FCF yield, and analyst targets.
2. **Resolves N/A Values:** Automatically computes missing PEG ratios using forward P/E and growth estimates, and calculates FCF yield from cash flow statements if the primary field is missing.
3. **Ranks Stocks:** Ranks the stocks from best to worst using a composite score prioritizing low Forward P/E, low PEG ratio, and strong analyst Buy ratings. Pre-profit companies (negative P/E) are automatically ranked lower.
4. **Generates Image:** Creates a matplotlib-based table (`/home/ubuntu/stock_comparison_ranked.png`) with conditional color-coding (green for excellent, red for poor) and clear rank direction annotations.

## Best Practices

- **Handling Errors:** If the script encounters a connection error (e.g., curl 56), simply re-run the script. `yfinance` can occasionally drop connections.
- **Pre-Profit Companies:** The script handles negative P/E ratios by labeling them "Pre-Profit" and ranking them appropriately.
- **Presentation:** Always arrange the table by prioritizing stocks with lower forward P/E, lower PEG ratio, and higher buy ratings on the left side, and progressively less favorable stocks towards the right. The bundled script handles this automatically.
