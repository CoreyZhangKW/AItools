---
name: ipo-company-research
description: Conducts comprehensive background research on pre-IPO or listed companies for capital markets lawyers. Use when a user asks to research a company for an IPO pitch, prepare background materials for management meetings, or analyze a company's core business, market position, financial performance, and potential risks for listing purposes.
---

# IPO Company Research Skill

This skill guides AI workflow in conducting deep, structured background research on companies (especially those preparing for IPOs or already listed) to help capital markets lawyers prepare for management pitches and meetings.

## Source Repository

GitHub: https://github.com/CoreyZhangKW/AItools
SKILL.md: https://raw.githubusercontent.com/CoreyZhangKW/AItools/main/skills/ipo-company-research/SKILL.md

## Core Workflow

When asked to research a company for an IPO project, follow these sequential steps:

### 1. Initial Information Gathering (Broad Search & Disclosures)

- Search for the company's official website, Baidu Baike/Wikipedia/Google, and recent news.
- Identify the company's exact legal name, founding history, registered capital, and recent major corporate events (e.g., restructuring, M&A, and debt offering).
- **Crucial for Listed/Delisted Companies**: If the company is currently listed or was previously listed (A-share, HKEX, US markets), you MUST search for and review its public disclosures, specifically the latest Annual Reports (年报), Semi-Annual Reports (半年报), other regular or ad hoc reports and disclosures, and its original IPO Prospectus (招股书) in Chinese or English.

### 2. Deep Dive into Core Business & Market Position

- Research the specific business models, core products and services, business segments, major clients, and suppliers.
- Find industry rankings, industry outlook and entry barriers, the company's market share data, and competitive advantages, and a list of the company's key competitors in China and overseas
- Identify the company's core assets (e.g., specific plants, machinery, patents, key infrastructure) and their operational status.

### 3. Financial Performance & Management Structure

- Search for the latest three years of financial data (revenue, profit, total assets). Look for official announcements, SASAC (国资委) reports if state-owned, or financial news platforms.
- Identify key shareholders, ultimate controllers, and core management team members.

### 4. Strategic Analysis & IPO Recommendations (Core Section)

- **This is the core of the research report.** It must be highly detailed, specific, and supported by public data and facts.
- Analyze the company's positioning, vision, or mission.
- Summarize the company's **Core Competitive Advantages** (aim for 4-6 distinct, well-supported points).
- Formulate specific, actionable, and grounded recommendations for the company's future strategy and the "Use of Proceeds" (募集资金用途) in the potential IPO. These recommendations must align with the company's strategic goals and industry trends.

### 5. Risk Assessment & ESG Compliance

- Search specifically for major litigation, disputes, or regulatory penalties involving the company.
- Identify industry-specific risks (e.g., export restrictions, commodity price fluctuations).
- Look for compliance and ESG-related risks (e.g., environmental issues, labor disputes, international sanctions).
- *Note: Because this section can be negative, it is placed at the end of the report after the strategic analysis.*

### 6. Report Generation (Markdown & Word)

- Synthesize all findings into a highly structured, professional Markdown report.
- **Language**: Always write the final report in **Chinese** (unless explicitly requested otherwise), as it is the standard working language for the user.
- **Format**: Use clear headings, full paragraphs (avoid excessive bullet points), and Markdown tables for financial data and use of proceeds recommendations.
- **Output**: The report must be generated in both Markdown (`.md`) and Word (`.docx`) formats.
- Use the included script to convert the Markdown report to Word format:
  ```
  python3 ~/.hermes/skills/ipo-company-research/scripts/md_to_docx.py <input.md> <output.docx>
  ```
  This script requires **pandoc** (`brew install pandoc` or `apt install pandoc`). If pandoc is unavailable, use the python-docx fallback instead:
  ```
  pip3 install python-docx
  python3 ~/.hermes/skills/ipo-company-research/scripts/md_to_docx_py.py <input.md> <output.docx>
  ```
  The fallback script handles markdown headings (H1-H4), tables with styled headers and alternating row shading, bold/italic inline formatting, and Chinese font configuration (宋体 body, 黑体 headings). It does not handle images or nested lists.
- Deliver both the `.md` and `.docx` files to the user.

## Output Structure Template

Your final report MUST follow this structure (or a highly similar one tailored to the specific company):

1. **摘要 (Executive Summary)**: Brief overview of the company and its IPO readiness.
2. **公司概况与历史沿革 (Company Overview & History)**: Basic facts, restructuring, capital and shareholder structure. Include insights from past prospectuses or annual reports if applicable.
3. **核心业务与核心资产 (Core Business & Assets)**: Detailed breakdown of segments, products and services, and key assets.
4. **市场地位与竞争优势 (Market Position & Competitive Edges)**: Rankings, market share, moats and key competitors.
5. **财务表现 (Financial Performance)**: 3-year data table and analysis.
6. **股东与管理层构成 (Shareholders & Management)**: Ownership structure and key executives.
7. **业务发展策略与港股上市募资用途建议 (Development Strategy & Proposed Use of Proceeds)**: **[CORE SECTION]** Detailed analysis of positioning, vision, 4-6 core competitive advantages, and highly specific, data-backed recommendations for the use of IPO proceeds.
8. **重大诉讼、争议与主要风险 (Litigation, Disputes & Key Risks)**: Crucial for legal due diligence, placed at the end.
9. **参考文献 (References)**: List of sources used.

## Best Practices for Capital Markets Research

- **Source Credibility**: Prioritize official company websites, government/regulator portals (e.g., SASAC), authoritative financial media (e.g., Reuters, Bloomberg, Sina Finance), and industry-specific databases.
- **Data Accuracy**: Cross-check financial figures across multiple sources if possible. Always cite the year/quarter for the data.
- **Legal Focus**: Pay special attention to the "Risks" and "Litigation" sections. Lawyers need to know the "skeletons in the closet" before pitching.
- **Actionable Pitch**: The "Use of Proceeds" section should not be generic. It must tie directly to the company's stated future plans and current bottlenecks.

### Search Methodology for Chinese Companies

When researching Chinese companies, search engines and data sources behave differently than for Western companies. See `references/search-methodology.md` for detailed curl commands, browser extraction techniques, and a list of sites that work vs. don't work. Key rules of thumb:

**What works:**
- **`curl` + Sina Finance (finance.sina.com.cn)**: Directly curl article URLs with a desktop User-Agent; returns clean, parseable HTML with full article text. Best source for detailed Chinese financial news.
- **`curl` + nfnews.com (南方+)**: Similar to Sina — direct curl with desktop UA returns clean content. Good for Guangdong/Southern China company coverage.
- **DuckDuckGo HTML search** (`duckduckgo.com/html/?q=...`): Works for initial discovery of Chinese-language articles. Use `uddg=` link extraction to get clean URLs. May rate-limit after 3-4 queries; space queries apart or rotate search terms.
- **Browser (browser_navigate) + console extraction**: For articles behind paywalls or JS-rendered content. Navigate to the article, then use `browser_console` with `document.querySelector('.article-content')?.innerText` to extract full text. Jiemian (界面新闻), cls.cn (财联社), and 21jingji (21经济报道) articles work well with this method.
- **Browser (browser_navigate) + snapshot**: Use the accessibility snapshot for article structure; can extract headings and metadata even when full text isn't directly visible.

**What does NOT work (avoid):**
- **Bing curl scraping**: Bing search results are heavily JS-rendered; curl returns unparseable JavaScript, not HTML content. Do not use Bing for automated Chinese searches.
- **Baidu Baike direct curl**: Triggers CAPTCHA/anti-crawl pages immediately. Use browser navigation instead if Baike access is critical.
- **Baidu search curl**: Similar anti-crawl protections; avoid direct curl to Baidu domains.
- **Google search curl from non-US IPs**: May return empty results or CAPTCHAs for Chinese-language queries.

**Financial data sources (priority order):**
1. Sina Finance articles (finance.sina.com.cn) — often contain detailed financial tables
2. Company annual reports / prospectuses (if publicly available)
3. Wind data cited in news articles (e.g., 界面新闻, 21经济报道)
4. 东方财富 Choice data (cited in media)
5. Company official website investor relations sections

**For securities firms specifically:**
- Wind rankings are the standard industry reference for business-line rankings
- CSRC (证监会) and regional bureau (证监局) websites for regulatory actions
- Exchange filings (上交所/深交所) for IPO progress and prospectuses
