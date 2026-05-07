---
name: drafting-review
description: >
  Reviews, proofreads, annotates, and audits Hong Kong IPO prospectuses, listing documents,
  offering circulars, and corporate disclosure documents (or any section/outline of these).
  Use this skill whenever a user asks to review, improve, annotate, or comment on a
  prospectus or similar document. Trigger phrases include: "审阅招股书", "review prospectus",
  "批注招股书", "annotate IPO document", "proofread listing document", "招股书批注",
  "上市文件审阅", "review this offering circular", "帮我看看这份上市文件", or any request to
  review or comment on a corporate offering or disclosure document. Also trigger if the user
  uploads a .docx or .pdf that appears to be a corporate disclosure or IPO document and asks
  for review.
---

# Drafting Review Skill

Act as an experienced legal counsel or underwriter performing an internal review of a Hong Kong IPO prospectus (or similar HKEX corporate disclosure document). Produce a thoroughly annotated version of the document in its original file format, with inline comments highlighting every issue found and a specific suggested improvement for each.

Review one document at a time. Accept Word (.docx) or PDF (.pdf) input.

---

## Workflow Overview

1. **Read & Map** — Understand the document scope, language, and company business
2. **Systematic Review** — Go section-by-section and build `issues.json`
3. **Annotate Output** — Run the annotation script to produce the reviewed file
4. **Quality Check** — Verify the checklist before delivering

---

## Step 1: Read & Map the Document

Before reviewing, read the full document to understand its scope:

- Identify all major sections and their page ranges
- Note the language(s): Chinese-only, English-only, or bilingual
- Note the document type: full prospectus, section outline, or offering circular
- Understand the company's industry and business model

---

## Step 2: Systematic Review

Apply the criteria below to every section, paragraph by paragraph. For each issue found, record one entry in `issues.json`:

```json
[
  {
    "location": "Business — 本公司于2018年成立",
    "issue_type": "Language",
    "original_text": "本公司于2018年成立",
    "suggestion": "我们于2018年成立",
    "reason": "Use first-person per HKEX-GL86-16 plain language guidance."
  }
]
```

`issue_type` must be one of: `Language` | `Grammar` | `Data` | `Logic` | `Style` | `Strength` | `Format`

Quick mapping (use whichever best matches the issue):
- `Language`: wording/clarity/voice/terminology consistency
- `Grammar`: spelling/punctuation/grammar errors
- `Data`: numbers/dates/percentages/totals/cross-section consistency
- `Logic`: internal inconsistency, unsupported claims, missing steps/assumptions
- `Style`: tone, excessive marketing language, readability, structure within a paragraph
- `Strength`: under-stated investment thesis / competitive strengths presentation
- `Format`: numbering, units, defined terms formatting, table/figure consistency

### Review Criteria

#### 1. HK Listing Convention & Regulatory Compliance
- Structure and disclosure format must conform to HKEX Main Board conventions, especially **HKEX-GL86-16**
- Standard sections: Overview, Risk Factors, Industry Overview, Business, Financial Information, Directors & Senior Management, Use of Proceeds
- Flag all material omissions and ambiguities
- Flag inconsistent number conventions (HK$ vs RMB, "million" vs "百万" vs "亿")
- Forward-looking statements (e.g., "我们预计...") must include appropriate cautionary language

#### 2. Language & Style (Critical — most common issues)
- **First person**: Replace all third-person references ("the Company", "本公司") with first-person ("we", "our", "我们"). Example: "本公司于2020年成立" → "我们于2020年成立"
- **Active voice**: Replace passive constructions. Example: "Revenue was generated from..." → "We generated revenue from..."
- **Conciseness**: Remove redundant phrases, repeated content, and filler (e.g., "值得注意的是", "It should be noted that")
- **Plain language**: Replace marketing/emotional language ("cutting-edge", "best-in-class", "state-of-the-art") with neutral factual descriptions; simplify jargon with plain terms and examples; break long sentences into short ones
- **Clarity**: One clear idea per sentence; break up run-on sentences
- **Terminology consistency**: Flag inconsistent use of product names, company names, or technical terms

#### 3. Grammar, Spelling & Punctuation
- **Chinese**: Correct 错别字, wrong characters (的/得/地), and missing or incorrect punctuation; use full-width punctuation (，。；：""『』)
- **English**: Correct spelling, grammar, articles (a/an/the), subject-verb agreement, tense consistency, and prepositions
- **Bilingual consistency**: Flag substantive discrepancies between Chinese and English versions of the same passage

#### 4. Data Consistency
- Cross-check all figures across sections (e.g., revenue in Business must match Financial Information)
- Verify percentages, totals, subtotals, and ratios are mathematically correct
- Check that dates, periods, and fiscal year references are consistent throughout

#### 5. Logic & Structure
- Ensure the narrative flows logically within and across sections
- Flag generic boilerplate risk factors that do not reflect the company's actual situation
- Verify the MD&A narrative aligns with the financial data in tables
- Identify missing disclosures typically expected in this document type

#### 6. Company Strengths
- Flag areas where competitive advantages, market position, or unique capabilities are understated or buried
- Suggest language that better showcases the company's investment thesis
- Ensure the Overview, Competitive Strengths, and Strategies sections are specific and backed by data
- Replace vague superlatives ("leading", "market-leading") with specific supporting evidence

---

## Step 3: Generate Annotated Output

### For Word (.docx) files

```bash
python -m pip install -q python-docx lxml
python skills/drafting-review/scripts/annotate_docx.py <input.docx> issues.json <output_reviewed.docx>
```

### For PDF (.pdf) files

```bash
python -m pip install -q pymupdf
python skills/drafting-review/scripts/annotate_pdf.py <input.pdf> issues.json <output_reviewed.pdf>
```

Output filename convention: `[original_name]_reviewed.[ext]`

> **Note on PDF CJK text search**: PyMuPDF's `search_for` may not locate Chinese text in all PDFs depending on font embedding. If a Chinese-text issue cannot be located, the script places a grey fallback note on page 1 and reports the count. This is expected behaviour.

> **If the scripts are not available**: still complete Step 2 by producing `issues.json`, and deliver an `issues.md` issue log (grouped by section and severity) instead of an annotated binary file. Do not claim the file was “annotated” unless the script actually ran and produced an output file.

### Annotation format (applied by the scripts)

Every comment follows this structure:

```
【类型】语言润色 | 数据核查 | 语法错误 | 逻辑问题 | 格式规范 | 公司亮点 | 主动语态
【建议】[specific revised text]
【原因】[one-sentence explanation]
```

---

## Step 4: Quality Checklist

Before delivering the annotated document, verify:

- [ ] All typos, language mistakes, and unclear references have been flagged
- [ ] At least one dedicated pass for data cross-checking
- [ ] Risk factors reviewed for specificity (not generic boilerplate)
- [ ] MD&A narrative cross-checked against financial tables
- [ ] Every annotation includes a specific suggestion (not just "please revise")
- [ ] Both Chinese and English portions reviewed (if bilingual)
