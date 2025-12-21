# 🏛️ ARGOS Content System

**AI-Powered Multi-Agent SEO Content Generator for Luxury Fragrance Brand**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![AutoGen](https://img.shields.io/badge/AutoGen-0.4+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

ARGOS Content System is an intelligent multi-agent AI platform that automatically discovers trending fragrance topics, conducts deep keyword research, and generates publication-ready 2500+ word SEO-optimized articles for the Argos Fragrances luxury brand.

## ✨ Features

- 🔍 **Trend Discovery** - Analyzes Google Trends, Reddit, YouTube, Quora, Fragrantica
- 📚 **Deep Research** - Keyword analysis and competitor content review
- ✍️ **AI Content Generation** - 2500+ word articles with search-query H2 headings
- ✅ **Quality Verification** - 30+ automated checks (SEO, content, trust)
- 📊 **Meta Optimization** - Auto-generates titles, descriptions, tags, excerpts
- 🖼️ **Image Suggestions** - Detailed briefs for graphic designers

## 🤖 Multi-Agent Architecture

| Agent | Role | Technology |
|-------|------|------------|
| 🔍 Discovery Agent | Find trending topics | GPT-4 + Web Search |
| 📚 Research Agent | Keyword & competitor analysis | GPT-4 + SEMrush Data |
| ✍️ Content Agent | Write SEO articles | GPT-4 |
| ✅ Verify Agent | Quality & plagiarism checks | GPT-4 |

## 🛠️ Tech Stack

- **Framework:** Microsoft AutoGen (Multi-Agent)
- **Frontend:** Streamlit
- **AI Model:** OpenAI GPT-4
- **Language:** Python 3.10+

## 📁 Project Structure

```
argos-content-system/
├── ui/
│   └── app.py              # Streamlit UI
├── agents/
│   ├── research_agent.py   # Discovery & Research
│   ├── content_agent.py    # Article Generation
│   └── verify_agent.py     # Quality Verification
├── tools/
│   ├── web_search.py       # Web Search Tool
│   └── argos_products.py   # Product Database Tool
├── config/
│   └── settings.py         # Configuration
├── data/
│   └── argos_products.json # Product Database
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/argos-content-system.git
cd argos-content-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Run Application
```bash
streamlit run ui/app.py
```

## ⚙️ Configuration

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 📸 Screenshots

### Topic Discovery
![Discovery Screen](screenshots/discovery.png)

### Article Generation
![Generation Screen](screenshots/generation.png)

### Quality Checks
![Verification Screen](screenshots/verification.png)

## 🔄 Workflow

```
┌─────────────────┐
│  User Clicks    │
│ "Find Topics"   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Discovery Agent │ ──▶ Analyzes 8+ sources
└────────┬────────┘
         ▼
┌─────────────────┐
│ User Selects    │
│    Topic        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Research Agent  │ ──▶ Deep keyword analysis
└────────┬────────┘
         ▼
┌─────────────────┐
│ Content Agent   │ ──▶ Writes 2500+ words
└────────┬────────┘
         ▼
┌─────────────────┐
│  Verify Agent   │ ──▶ 30+ quality checks
└────────┬────────┘
         ▼
┌─────────────────┐
│ Publication     │
│ Ready Article   │
└─────────────────┘
```

## 📊 Quality Checks (30+)

### Content Checks (12)
- Word Count 2500+
- No Em Dash Used
- Proper H1 Tag
- H2 Headings (8+)
- H3 Subheadings
- Introduction Hook
- Conclusion CTA
- FAQ Section
- Product Recommendations
- Internal Links
- External References
- Readable Paragraphs

### SEO Checks (10)
- Keyword in H1
- Keyword in First 100 Words
- Keyword Density 1-2%
- Meta Title (60 chars)
- Meta Description (155 chars)
- URL Slug Optimized
- Search Query H2s
- LSI Keywords
- Image Alt Tags
- Schema Ready

### Trust Verification (8)
- AI Original Content
- Not Scraped
- Unique Article
- Factually Accurate
- Brand Voice Consistent
- No Duplicate Content
- Proper Citations
- Ready to Publish

## 🎯 Use Cases

- Luxury brand content marketing
- SEO blog article generation
- Product-focused content creation
- Trend-based topic discovery

## 🔮 Roadmap

- [ ] Add image generation with DALL-E
- [ ] Shopify direct publishing integration
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] API endpoint for external access

## 👨‍💻 Author

**Your Name**
- Academy Project - December 2025

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

*Built with ❤️ for Argos Fragrances - Where Mythology Meets Modern Perfumery*
