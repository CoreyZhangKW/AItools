# Search Methodology for Chinese Company Research

## Session: 万联证券 (Wanlian Securities) — 2026-05-07

### Proven Approaches (What Works)

#### 1. curl + Sina Finance (finance.sina.com.cn)
```bash
curl -sL -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://finance.sina.com.cn/roll/2024-10-27/doc-inctyvzy0506630.shtml" | \
  python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'&nbsp;|\s+', ' ', text)
idx = text.find('万联证券')
if idx >= 0:
    print(text[idx:idx+4000])
"
```
Sina Finance articles are NOT JS-rendered; the full article text is in the raw HTML. Use regex to strip `<script>` and `<style>` blocks, then extract with a keyword search. Works reliably for detailed Chinese financial news including shareholder structures, financial data, and management changes.

#### 2. curl + nfnews.com (南方+/南方plus)
Same pattern as Sina — direct curl with desktop UA returns clean, parseable content. Good for Guangdong/Southern China regional company coverage.

#### 3. DuckDuckGo HTML Search
`https://duckduckgo.com/html/?q=<URL-encoded query>`

- Returns clean HTML with article snippets, titles, and URLs
- Extract article links via: `re.findall(r'uddg=(https?://[^&"]+)', html)`
- **Rate limiting warning**: After 3-4 rapid queries, DuckDuckGo may return empty results. Space queries apart or rotate search terms. If you get empty results, wait 30-60 seconds before retrying.
- Good for initial discovery but not for deep content extraction

#### 4. Browser Navigation + Console Extraction
For articles behind paywalls or JS-rendered content:
```javascript
// In browser_console after browser_navigate
document.querySelector('.article-content')?.innerText || 
document.querySelector('.main-article')?.innerText || 
document.querySelector('article')?.innerText
```

Sites tested successfully:
- **jiemian.com** (界面新闻): `.article-content` — full article text extractable via console
- **cls.cn** (财联社): JS-rendered but console extraction works
- **21jingji.com** (21经济报道): May time out on initial load; try alternative sources first

#### 5. Browser Snapshot
Use `browser_navigate` + accessibility snapshot for:
- Article structure and headings
- Metadata extraction (author, date, source)
- Even when full text isn't visible, the snapshot reveals key structural elements

### What Does NOT Work (Avoid These)

| Method | Issue | Alternative |
|--------|-------|-------------|
| **Bing curl scraping** | Returns unparseable JavaScript, not HTML content | Use DuckDuckGo HTML or browser |
| **Baidu Baike direct curl** | Immediate CAPTCHA/anti-crawl page | Use browser navigation if essential |
| **Baidu search curl** | Anti-crawl protections | Use DuckDuckGo for Chinese queries |
| **Google search curl from non-US IPs** | Empty results or CAPTCHAs for Chinese queries | DuckDuckGo or browser |
| **Company official websites** | May have cert errors (e.g., wlzq.com.cn had ERR_CERT_COMMON_NAME_INVALID) | Fall back to news articles |

### Financial Data Sources (Priority Order)

1. **Sina Finance articles** — often contain detailed financial tables with YoY comparisons
2. **Company annual reports / prospectuses** — if publicly available via CSRC/exchange websites
3. **Wind data cited in news articles** — 界面新闻, 21经济报道, 券商中国 frequently cite Wind rankings
4. **东方财富 Choice data** — cited in media; direct access may require subscription
5. **Company IR pages** — try `browser_navigate` if cert issues aren't blocking

### Search Query Strategy for Chinese Companies

Build queries in Chinese using these patterns:
- Company name + IPO + 上市 + 财务数据
- Company name + 股东 + 结构
- Company name + 增资 + 估值
- Company name + 处罚 + 证监局
- Company name + 招股书 + 募资

For securities firms specifically:
- Add "Wind数据" or "排名" for industry rankings
- Search "广东证监局" / "证监会" for regulatory actions
- Check "排队IPO" for peer comparison context

### Token Packing Efficiency

DuckDuckGo HTML search returns compact results (1-2KB per query) vs browser navigation (50-200KB per page). Prefer DuckDuckGo for discovery and only use browser for articles where full text is essential.
