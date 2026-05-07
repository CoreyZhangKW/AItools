---
name: ipo-company-research
description: Conducts comprehensive background research on pre-IPO or listed companies for capital markets lawyers and sponsors. Use when a user asks to research a company for an IPO pitch, prepare background materials for management meetings, or analyze a company's core business, market position, financial performance, and potential risks for listing purposes.
---

# IPO Company Research Skill

This skill guides Manus in conducting deep, structured background research on companies (especially those preparing for IPOs or already listed) to help capital markets lawyers and sponsors prepare for management pitches and meetings.

## Core Workflow

When asked to research a company for an IPO project, follow these sequential steps:

### 1. Initial Information Gathering (Broad Search & Disclosures)
- Search for the company's official website, Baidu Baike/Wikipedia, and recent news.
- Identify the company's exact legal name, founding history, registered capital, and recent major corporate events (e.g., restructuring, M&A).
- **Crucial for Listed/Delisted Companies**: If the company is currently listed or was previously listed (A-share, HKEX, US markets), you MUST search for and review its public disclosures, specifically the latest Annual Reports (年报), Semi-Annual Reports (半年报), and its original IPO Prospectus (招股书).

### 2. Deep Dive into Core Business & Market Position
- Research the specific business models, major clients, and suppliers.
- Find industry rankings, market share data, and competitive advantages.
- Identify the company's core assets (e.g., specific mines, patents, key infrastructure) and their operational status.

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
- Look for ESG-related risks (e.g., environmental issues, labor disputes, international sanctions).
- Identify industry-specific risks (e.g., export restrictions, commodity price fluctuations).
- *Note: Because this section can be negative, it is placed at the end of the report after the strategic analysis.*

### 6. Report Generation (Markdown & Word)
- Synthesize all findings into a highly structured, professional Markdown report.
- **Language**: Always write the final report in **Chinese** (unless explicitly requested otherwise), as it is the standard working language for HK/Mainland IPO pitches.
- **Format**: Use clear headings, full paragraphs (avoid excessive bullet points), and Markdown tables for financial data and use of proceeds recommendations.
- **Output**: The report must be generated in both Markdown (`.md`) and Word (`.docx`) formats.
- Use the provided script `python /home/ubuntu/skills/ipo-company-research/scripts/md_to_docx.py <input.md> <output.docx>` to convert the Markdown report to Word format.
- Deliver both the `.md` and `.docx` files to the user. Do NOT generate a PDF.

## Output Structure Template

Your final report MUST follow this structure (or a highly similar one tailored to the specific company):

1. **摘要 (Executive Summary)**: Brief overview of the company and its IPO readiness.
2. **公司概况与历史沿革 (Company Overview & History)**: Basic facts, restructuring, capital. Include insights from past prospectuses or annual reports if applicable.
3. **核心业务与核心资产 (Core Business & Assets)**: Detailed breakdown of segments and key assets.
4. **市场地位与竞争优势 (Market Position & Competitive Edges)**: Rankings, market share, moats.
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
