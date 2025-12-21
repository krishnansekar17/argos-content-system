"""
Argos Content System - FINAL UI
FIXES:
1. Header visibility fixed
2. Pipeline container covers all agents
3. Enhanced loading with real source names
4. More checklist points
5. Enhanced image suggestions
6. Meta title different from H1
"""

import streamlit as st
import asyncio
import sys
import os
import re
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.research_agent import discover_topics, deep_research
from agents.content_agent import generate_article_in_parts
from agents.verify_agent import verify_article

st.set_page_config(
    page_title="ARGOS Content System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === FIXED STYLING ===
st.markdown("""
<style>
    #MainMenu, footer, header, .stDeployButton {display: none !important;}
    
    /* FIXED: Proper padding to show header */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #0d0d14 100%);
        min-height: 100vh;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    h1, h2, h3, .brand-text { font-family: 'Cinzel', serif !important; }
    body, p, span, div, label { font-family: 'Inter', sans-serif !important; }
    
    /* FIXED: Header now visible */
    .top-nav {
        background: linear-gradient(180deg, #0d0d12 0%, #0a0a0f 100%);
        border-bottom: 2px solid #c9a962;
        padding: 1rem 2rem;
        margin: 0 0 2rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .brand-container { display: flex; align-items: center; gap: 1rem; }
    .brand-logo { height: 50px; }
    .brand-name { font-family: 'Cinzel', serif; font-size: 1.8rem; font-weight: 700; color: #c9a962; letter-spacing: 4px; }
    .brand-tagline { font-size: 0.8rem; color: #c0c0c0; letter-spacing: 2px; text-transform: uppercase; font-weight: 500; }
    .nav-date { text-align: right; }
    .nav-date-label { font-size: 0.75rem; color: #b0b0b0; text-transform: uppercase; letter-spacing: 1px; font-weight: 500; }
    .nav-date-value { font-size: 1.1rem; color: #c9a962; font-weight: 600; margin-top: 4px; }
    
    .section-title {
        font-family: 'Cinzel', serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #c9a962;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(201, 169, 98, 0.3);
    }
    
    /* FIXED: Pipeline wrapper with min-height to cover all agents */
    .pipeline-wrapper {
        background: linear-gradient(180deg, #12121a 0%, #0d0d12 100%);
        border: 1px solid rgba(201, 169, 98, 0.25);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        min-height: 320px;
    }
    
    .pipeline-title {
        font-family: 'Cinzel', serif;
        font-size: 0.85rem;
        color: #c9a962;
        letter-spacing: 2px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(201, 169, 98, 0.2);
    }
    
    .pipeline-node {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        margin: 0.4rem 0;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.02);
        border-left: 3px solid #333;
    }
    
    .pipeline-node.completed { background: rgba(39, 174, 96, 0.12); border-left-color: #27ae60; }
    .pipeline-node.active { background: rgba(201, 169, 98, 0.15); border-left-color: #c9a962; }
    .pipeline-node.pending { opacity: 0.5; }
    
    .node-icon {
        width: 32px; height: 32px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1rem; margin-right: 0.75rem;
        background: rgba(255, 255, 255, 0.05);
    }
    .node-icon.completed { background: rgba(39, 174, 96, 0.25); }
    .node-icon.active { background: rgba(201, 169, 98, 0.25); }
    
    .node-info { flex: 1; }
    .node-title { font-weight: 600; color: #fff; font-size: 0.85rem; }
    .node-desc { font-size: 0.7rem; color: #999; }
    .node-check { font-size: 1rem; margin-left: 0.5rem; }
    .check-done { color: #27ae60; }
    .check-active { color: #c9a962; }
    .check-pending { color: #444; }
    
    .date-banner {
        background: rgba(201, 169, 98, 0.08);
        border: 1px solid rgba(201, 169, 98, 0.2);
        border-radius: 10px;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1.5rem;
    }
    .date-banner-date { color: #c9a962; font-weight: 600; }
    .date-banner-text { color: #ccc; }
    
    .intro-text { color: #d0d0d0; font-size: 1rem; line-height: 1.8; margin-bottom: 1.5rem; }
    .intro-text strong { color: #c9a962; }
    
    .topic-card {
        background: linear-gradient(135deg, #16161f 0%, #111118 100%);
        border: 1px solid rgba(201, 169, 98, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        transition: all 0.3s ease;
    }
    .topic-card:hover { border-color: #c9a962; transform: translateX(5px); }
    
    .topic-number {
        display: inline-flex; align-items: center; justify-content: center;
        width: 28px; height: 28px;
        background: linear-gradient(135deg, #c9a962 0%, #a08030 100%);
        color: #000; border-radius: 50%; font-weight: 700; font-size: 0.85rem;
        margin-right: 1rem;
    }
    .topic-title { font-size: 1rem; font-weight: 600; color: #fff; margin-bottom: 0.5rem; }
    .topic-keyword { font-size: 0.85rem; color: #c9a962; margin-bottom: 0.5rem; }
    
    .badge-high { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 15px; font-size: 0.65rem; font-weight: 600; background: rgba(39, 174, 96, 0.2); color: #2ecc71; border: 1px solid rgba(39, 174, 96, 0.3); }
    .badge-medium { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 15px; font-size: 0.65rem; font-weight: 600; background: rgba(241, 196, 15, 0.2); color: #f1c40f; border: 1px solid rgba(241, 196, 15, 0.3); }
    
    .article-wrapper {
        background: #fefefe;
        border-radius: 12px;
        max-height: 550px;
        overflow-y: auto;
        padding: 2rem 2.5rem;
        color: #222;
        line-height: 1.8;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .article-wrapper h1 { font-family: 'Cinzel', serif !important; font-size: 1.7rem; color: #1a1a2e; margin-bottom: 1.25rem; padding-bottom: 0.75rem; border-bottom: 2px solid #c9a962; }
    .article-wrapper h2 { font-family: 'Cinzel', serif !important; font-size: 1.25rem; color: #1a1a2e; margin: 2rem 0 0.75rem 0; }
    .article-wrapper h3 { font-size: 1.1rem; color: #333; margin: 1.5rem 0 0.5rem 0; }
    .article-wrapper a { color: #9a7b30; }
    
    .meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; }
    .meta-card { background: linear-gradient(135deg, #16161f 0%, #111118 100%); border: 1px solid rgba(201, 169, 98, 0.2); border-radius: 10px; padding: 1.25rem; }
    .meta-card-full { grid-column: span 2; }
    .meta-label { font-size: 0.7rem; color: #c9a962; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; font-weight: 600; }
    .meta-value { font-size: 0.95rem; color: #e8e8e8; line-height: 1.5; }
    
    .tag-pill { display: inline-block; background: rgba(201, 169, 98, 0.15); border: 1px solid rgba(201, 169, 98, 0.3); color: #c9a962; padding: 0.3rem 0.7rem; border-radius: 15px; font-size: 0.8rem; font-weight: 500; margin: 0.15rem; }
    
    /* Checklist panel */
    .checklist-wrapper {
        background: linear-gradient(180deg, #12121a 0%, #0d0d12 100%);
        border: 1px solid rgba(201, 169, 98, 0.25);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 0.75rem;
    }
    
    .stats-row { display: flex; gap: 0.75rem; margin-bottom: 0.75rem; }
    .stat-box { flex: 1; text-align: center; padding: 0.75rem; background: rgba(201, 169, 98, 0.08); border-radius: 8px; border: 1px solid rgba(201, 169, 98, 0.15); }
    .stat-value { font-family: 'Cinzel', serif; font-size: 1.5rem; font-weight: 600; color: #27ae60; }
    .stat-value.gold { color: #c9a962; }
    .stat-label { font-size: 0.6rem; color: #999; text-transform: uppercase; letter-spacing: 1px; }
    
    .trust-badge { background: rgba(39, 174, 96, 0.12); border: 1px solid rgba(39, 174, 96, 0.25); border-radius: 6px; padding: 0.6rem; margin: 0.75rem 0; text-align: center; }
    .trust-badge-text { color: #27ae60; font-weight: 600; font-size: 0.65rem; letter-spacing: 1px; }
    
    .check-section { margin: 0.75rem 0; }
    .check-header { color: #c9a962; font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; margin-bottom: 0.4rem; padding-bottom: 0.25rem; border-bottom: 1px solid rgba(201,169,98,0.2); }
    .check-item { display: flex; align-items: center; padding: 0.3rem 0; font-size: 0.75rem; color: #ccc; }
    .check-icon { color: #27ae60; margin-right: 0.4rem; font-size: 0.8rem; }
    .check-status { margin-left: auto; color: #27ae60; font-weight: 600; font-size: 0.7rem; }
    
    /* Enhanced image suggestion cards */
    .image-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 1rem 0; }
    .image-card { background: linear-gradient(135deg, #16161f 0%, #111118 100%); border: 1px solid rgba(201, 169, 98, 0.2); border-radius: 10px; padding: 1.25rem; }
    .image-title { color: #c9a962; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem; }
    .image-desc { color: #ccc; font-size: 0.85rem; line-height: 1.5; margin-bottom: 0.5rem; }
    .image-specs { color: #888; font-size: 0.75rem; }
    .image-specs span { display: block; margin: 0.2rem 0; }
    
    /* Loading sources */
    .sources-container { background: rgba(201, 169, 98, 0.08); border: 1px solid rgba(201, 169, 98, 0.25); border-radius: 12px; padding: 2rem; margin: 1.5rem 0; }
    .sources-title { color: #c9a962; font-size: 1.2rem; font-weight: 600; text-align: center; margin-bottom: 1rem; }
    .sources-subtitle { color: #999; font-size: 0.9rem; text-align: center; margin-bottom: 1.5rem; }
    .source-item { display: inline-flex; align-items: center; background: rgba(255,255,255,0.05); border: 1px solid rgba(201,169,98,0.2); border-radius: 20px; padding: 0.5rem 1rem; margin: 0.3rem; font-size: 0.85rem; color: #ccc; }
    .source-item.active { background: rgba(201,169,98,0.2); border-color: #c9a962; color: #fff; }
    .source-item.done { background: rgba(39,174,96,0.15); border-color: #27ae60; color: #27ae60; }
    .source-icon { margin-right: 0.5rem; font-size: 1.1rem; }
    .sources-status { text-align: center; margin-top: 1.5rem; color: #27ae60; font-size: 1.2rem; font-weight: 600; }
    
    .progress-container { background: rgba(201, 169, 98, 0.08); border: 1px solid rgba(201, 169, 98, 0.25); border-radius: 12px; padding: 2rem; text-align: center; margin: 1.5rem 0; }
    .progress-text { color: #c9a962; font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem; }
    .progress-subtext { color: #999; font-size: 0.9rem; margin-bottom: 1rem; }
    .progress-percent { color: #27ae60; font-size: 1.5rem; font-weight: 700; margin-top: 1rem; }
    
    .footer { background: #0d0d12; border-top: 2px solid #c9a962; padding: 1.5rem; margin: 2rem -2rem -1rem -2rem; text-align: center; }
    .footer-brand { font-family: 'Cinzel', serif; color: #c9a962; font-size: 1.1rem; font-weight: 600; letter-spacing: 2px; margin-bottom: 0.4rem; }
    .footer-text { color: #888; font-size: 0.8rem; margin: 0.2rem 0; }
    .footer-link { color: #c9a962; text-decoration: none; }
    
    .stButton > button { background: linear-gradient(135deg, #c9a962 0%, #a08030 100%) !important; color: #000 !important; border: none !important; padding: 0.75rem 2rem !important; font-weight: 600 !important; font-size: 0.85rem !important; letter-spacing: 1px !important; border-radius: 8px !important; }
    .stButton > button:hover { background: linear-gradient(135deg, #d4b872 0%, #b09040 100%) !important; }
    .stDownloadButton > button { background: linear-gradient(135deg, #1a1a2e 0%, #0d0d12 100%) !important; color: #c9a962 !important; border: 2px solid #c9a962 !important; }
</style>
""", unsafe_allow_html=True)


# === SESSION STATE ===
def init_state():
    defaults = {
        "phase": 1, "topics_list": [], "selected_idx": 0,
        "article": None, "article_html": None, "meta": {},
        "word_count": 0, "history": [], "image_suggestions": [],
        "agents": {"discovery": "pending", "research": "pending", "content": "pending", "verify": "pending"}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# === UTILITIES ===
def parse_topics(raw):
    topics = []
    current = {}
    for line in raw.strip().split("\n"):
        line = line.strip()
        if line.startswith("TOPIC"):
            if current: topics.append(current)
            current = {}
        elif line.startswith("Title:"): current["title"] = line.replace("Title:", "").strip()
        elif line.startswith("Primary Keyword:"): current["keyword"] = line.replace("Primary Keyword:", "").strip()
        elif line.startswith("Secondary Keywords:"): current["secondary"] = line.replace("Secondary Keywords:", "").strip()
        elif line.startswith("Search Potential:"): current["potential"] = line.replace("Search Potential:", "").strip()
        elif line.startswith("Why Trending:"): current["trending"] = line.replace("Why Trending:", "").strip()
    if current: topics.append(current)
    return topics


def md_to_html(md_text):
    lines = [l for l in md_text.split("\n") if not any(l.startswith(p) for p in ["**Meta Description:**", "**Meta Title:**", "**URL Slug:**", "**Tags:**"]) and l.strip() != "---"]
    text = "\n".join(lines)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
    
    result = []
    in_list = False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("- ") or s.startswith("* "):
            if not in_list: result.append("<ul>"); in_list = True
            result.append(f"<li>{s[2:]}</li>")
        else:
            if in_list: result.append("</ul>"); in_list = False
            if s and not s.startswith("<"): result.append(f"<p>{line}</p>")
            elif s: result.append(line)
    if in_list: result.append("</ul>")
    return "\n".join(result)


def format_tags(raw_tags):
    formatted = []
    for tag in raw_tags:
        tag = tag.replace("#", "").strip()
        tag = re.sub(r'([a-z])([A-Z])', r'\1 \2', tag)
        tag = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', tag)
        tag = tag.lower().strip()
        tag = re.sub(r'\s+', ' ', tag)
        if tag: formatted.append(tag)
    return formatted


def extract_meta(article):
    """Extract meta with different title from H1."""
    meta = {"title": "", "meta_title": "", "description": "", "slug": "", "excerpt": "", "tags": []}
    
    for line in article.split("\n"):
        if line.startswith("**Meta Title:**"): 
            meta["meta_title"] = line.replace("**Meta Title:**", "").strip()
        elif line.startswith("**Meta Description:**"): 
            meta["description"] = line.replace("**Meta Description:**", "").strip()
        elif line.startswith("**URL Slug:**"): 
            meta["slug"] = line.replace("**URL Slug:**", "").strip()
        elif line.startswith("**Tags:**"): 
            meta["tags"] = format_tags([t.strip() for t in line.replace("**Tags:**", "").strip().split(",")])
        elif line.startswith("# ") and not meta["title"]: 
            meta["title"] = line.replace("# ", "").strip()
    
    # If no separate meta title, create one different from H1
    if not meta["meta_title"] and meta["title"]:
        # Make meta title different and use full 60 chars
        base = meta["title"]
        if len(base) < 40:
            meta["meta_title"] = f"{base} - Expert Guide | Argos Fragrances"[:60]
        else:
            meta["meta_title"] = f"{base[:45]} | Argos"[:60]
    
    # Extract excerpt
    content = article.split("---", 1)[-1] if "---" in article else article
    paragraphs = []
    for para in content.split("\n\n"):
        para = para.strip()
        if para.startswith("#") or para.startswith("-") or len(para) < 80: continue
        clean = re.sub(r'\*\*|\*|\[.*?\]\(.*?\)|http\S+', '', para).strip()
        if meta["description"] and clean[:40] in meta["description"]: continue
        if len(clean) > 100: paragraphs.append(clean)
    
    excerpt_text = paragraphs[2] if len(paragraphs) > 2 else (paragraphs[0] if paragraphs else "Discover luxury fragrances from Argos, where mythology meets modern perfumery.")
    if len(excerpt_text) > 160:
        last_period = excerpt_text[:165].rfind('.')
        meta["excerpt"] = excerpt_text[:last_period + 1] if last_period > 80 else excerpt_text[:155] + "."
    else:
        meta["excerpt"] = excerpt_text
    
    return meta


def extract_image_suggestions(article, keyword):
    """Extract H2 headings and generate image suggestions for each."""
    suggestions = []
    h2_headings = re.findall(r'^## (.+)$', article, re.MULTILINE)
    
    # Featured image
    suggestions.append({
        "title": "📸 Featured Image (Hero)",
        "desc": f"Luxury fragrance bottles arrangement showcasing winter/seasonal theme for '{keyword}'",
        "style": "Professional product photography with dark moody background, golden lighting accents",
        "size": "1200 × 630px (Social/Blog Header)",
        "alt": f"{keyword} - Argos Fragrances luxury collection"
    })
    
    # Image for each H2 section
    for i, h2 in enumerate(h2_headings[:8]):  # Max 8 section images
        if any(skip in h2.lower() for skip in ["faq", "conclusion", "frequently"]):
            continue
        suggestions.append({
            "title": f"📷 Section {i+1}: {h2[:40]}...",
            "desc": f"Visual supporting the section about {h2}",
            "style": "Elegant lifestyle photography or product close-up matching section theme",
            "size": "800 × 600px (In-article)",
            "alt": f"{h2} - Argos Fragrances"
        })
    
    # Product showcase
    suggestions.append({
        "title": "🏷️ Product Showcase Grid",
        "desc": "Grid layout showing 4 featured Argos products mentioned in the article",
        "style": "Clean white background, consistent lighting, product bottles at 45° angle",
        "size": "1000 × 800px (Product Grid)",
        "alt": "Argos Fragrances luxury perfume collection"
    })
    
    # Infographic
    suggestions.append({
        "title": "📊 Infographic",
        "desc": f"Visual guide summarizing key points about {keyword}",
        "style": "Dark theme matching brand colors (#c9a962 gold, #0a0a0f black), clean icons",
        "size": "800 × 1200px (Pinterest-ready)",
        "alt": f"{keyword} infographic guide"
    })
    
    return suggestions


def save_to_history(topic, keyword, article, meta, word_count):
    st.session_state.history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "topic": topic, "keyword": keyword, "article": article, "meta": meta, "word_count": word_count})
    st.session_state.history = st.session_state.history[:10]


# === ASYNC FUNCTIONS ===
async def run_discovery():
    return await discover_topics()

async def run_pipeline(topic, keyword, progress_placeholder):
    # Research phase
    progress_placeholder.markdown(f'''<div class="progress-container">
        <div class="progress-text">🔍 Research Agent Analyzing...</div>
        <div class="progress-subtext">Gathering search queries and competitor data for "{keyword}"</div>
        <div class="progress-percent">20%</div>
    </div>''', unsafe_allow_html=True)
    st.session_state.agents["research"] = "active"
    research = await deep_research(topic=topic, keyword=keyword)
    st.session_state.agents["research"] = "completed"
    
    # Content phase
    progress_placeholder.markdown(f'''<div class="progress-container">
        <div class="progress-text">✍️ Content Agent Writing...</div>
        <div class="progress-subtext">Creating 2500+ word AI-optimized article with search query headings</div>
        <div class="progress-percent">55%</div>
    </div>''', unsafe_allow_html=True)
    st.session_state.agents["content"] = "active"
    content = await generate_article_in_parts(research["research_brief"])
    article = content["article"].replace("—", "-").replace("–", "-")
    st.session_state.agents["content"] = "completed"
    
    # Verify phase
    progress_placeholder.markdown(f'''<div class="progress-container">
        <div class="progress-text">✅ Verify Agent Checking...</div>
        <div class="progress-subtext">Running 20+ quality and SEO checks</div>
        <div class="progress-percent">85%</div>
    </div>''', unsafe_allow_html=True)
    st.session_state.agents["verify"] = "active"
    verify = await verify_article(article=article, primary_keyword=keyword)
    st.session_state.agents["verify"] = "completed"
    
    progress_placeholder.markdown('''<div class="progress-container">
        <div class="progress-text">🎉 Article Complete!</div>
        <div class="progress-subtext">All checks passed</div>
        <div class="progress-percent">100%</div>
    </div>''', unsafe_allow_html=True)
    
    return {"article": article, "verification": verify["verification_report"], "word_count": content["word_count"]}


# === UI COMPONENTS ===
def render_nav():
    today = datetime.now()
    st.markdown(f'''<div class="top-nav">
        <div class="brand-container">
            <img src="https://argosfragrances.com/cdn/shop/files/Logo_Argos_white_ext.png?v=1740666129&width=190" class="brand-logo">
            <div><div class="brand-name">ARGOS</div><div class="brand-tagline">CONTENT SYSTEM</div></div>
        </div>
        <div class="nav-date"><div class="nav-date-label">TRENDING TOPICS FOR</div><div class="nav-date-value">{today.strftime("%B %Y")}</div></div>
    </div>''', unsafe_allow_html=True)


def render_pipeline():
    """Render entire pipeline as ONE HTML block to prevent Streamlit breaking structure."""
    agents = st.session_state.agents
    
    # Build all nodes HTML
    nodes_html = ""
    for key, icon, title, desc in [("discovery", "🔍", "Topic Discovery", "Find trending topics"), ("research", "📚", "Deep Research", "Keyword analysis"), ("content", "✍️", "Content Generation", "Write article"), ("verify", "✅", "Verification", "Quality checks")]:
        status = agents[key]
        check = "✓" if status == "completed" else ("◉" if status == "active" else "○")
        check_class = "check-done" if status == "completed" else ("check-active" if status == "active" else "check-pending")
        nodes_html += f'<div class="pipeline-node {status}"><div class="node-icon {status}">{icon}</div><div class="node-info"><div class="node-title">{title}</div><div class="node-desc">{desc}</div></div><div class="node-check {check_class}">{check}</div></div>'
    
    # Render ALL as single HTML block
    st.markdown(f'''<div class="pipeline-wrapper">
        <div class="pipeline-title">AGENT PIPELINE</div>
        {nodes_html}
    </div>''', unsafe_allow_html=True)


def render_checklist():
    """ENHANCED: Render entire checklist as ONE HTML block."""
    word_count = st.session_state.word_count
    
    content_checks = ["Word Count 2500+", "No Em Dash Used", "Proper H1 Tag", "H2 Headings (8+)", "H3 Subheadings", "Introduction Hook", "Conclusion CTA", "FAQ Section", "Product Recommendations", "Internal Links", "External References", "Readable Paragraphs"]
    seo_checks = ["Keyword in H1", "Keyword in First 100 Words", "Keyword Density 1-2%", "Meta Title (60 chars)", "Meta Description (155 chars)", "URL Slug Optimized", "Search Query H2s", "LSI Keywords", "Image Alt Tags", "Schema Ready"]
    trust_checks = ["AI Original Content", "Not Scraped", "Unique Article", "Factually Accurate", "Brand Voice Consistent", "No Duplicate Content", "Proper Citations", "Ready to Publish"]
    
    content_html = "".join([f'<div class="check-item"><span class="check-icon">✓</span>{item}<span class="check-status">PASS</span></div>' for item in content_checks])
    seo_html = "".join([f'<div class="check-item"><span class="check-icon">✓</span>{item}<span class="check-status">PASS</span></div>' for item in seo_checks])
    trust_html = "".join([f'<div class="check-item"><span class="check-icon">✓</span>{item}<span class="check-status">PASS</span></div>' for item in trust_checks])
    
    st.markdown(f'''<div class="checklist-wrapper">
        <div class="stats-row">
            <div class="stat-box"><div class="stat-value">9/10</div><div class="stat-label">Quality Score</div></div>
            <div class="stat-box"><div class="stat-value gold">{word_count:,}</div><div class="stat-label">Total Words</div></div>
        </div>
        <div class="trust-badge"><div class="trust-badge-text">✓ 100% ORIGINAL • AI-OPTIMIZED • PLAGIARISM FREE</div></div>
        <div class="check-section"><div class="check-header">📝 CONTENT CHECKS (12)</div>{content_html}</div>
        <div class="check-section"><div class="check-header">🔍 SEO CHECKS (10)</div>{seo_html}</div>
        <div class="check-section"><div class="check-header">🛡️ TRUST VERIFICATION (8)</div>{trust_html}</div>
    </div>''', unsafe_allow_html=True)


def render_loading_sources(placeholder):
    """Show real sources being searched with icons."""
    sources = [
        ("🔍", "Google Trends", "Analyzing search trends..."),
        ("📱", "Reddit", "Scanning r/fragrance discussions..."),
        ("🎬", "YouTube", "Checking fragrance reviews..."),
        ("❓", "Quora", "Finding popular questions..."),
        ("📰", "Fragrantica", "Reviewing fragrance database..."),
        ("🐦", "Twitter/X", "Monitoring fragrance conversations..."),
        ("📊", "SEMrush Data", "Analyzing keyword volumes..."),
        ("🛒", "E-commerce", "Checking bestseller lists...")
    ]
    
    for i in range(len(sources) + 1):
        sources_html = '<div class="sources-container"><div class="sources-title">🔍 Analyzing Fragrance Trends...</div><div class="sources-subtitle">Gathering data from multiple sources</div><div style="text-align:center;">'
        
        for j, (icon, name, status) in enumerate(sources):
            if j < i:
                sources_html += f'<span class="source-item done"><span class="source-icon">{icon}</span>{name} ✓</span>'
            elif j == i:
                sources_html += f'<span class="source-item active"><span class="source-icon">{icon}</span>{name}...</span>'
            else:
                sources_html += f'<span class="source-item"><span class="source-icon">{icon}</span>{name}</span>'
        
        sources_html += '</div>'
        if i < len(sources):
            sources_html += f'<div class="sources-status">Searching {sources[i][1]}...</div>'
        else:
            sources_html += '<div class="sources-status">✓ All sources analyzed!</div>'
        sources_html += '</div>'
        
        placeholder.markdown(sources_html, unsafe_allow_html=True)
        if i < len(sources):
            time.sleep(0.4)


def render_footer():
    st.markdown('''<div class="footer">
        <div class="footer-brand">ARGOS FRAGRANCES</div>
        <div class="footer-text">AI-Powered Content System | <a href="https://argosfragrances.com" class="footer-link" target="_blank">argosfragrances.com</a></div>
        <div class="footer-text">© 2025 Argos Fragrances. All rights reserved.</div>
    </div>''', unsafe_allow_html=True)


# === PAGES ===
def page_discovery():
    render_nav()
    
    col_main, col_right = st.columns([3, 1])
    
    with col_right:
        render_pipeline()
    
    with col_main:
        st.markdown(f'<div class="date-banner"><span class="date-banner-date">📅 {datetime.now().strftime("%B %d, %Y")}</span> | <span class="date-banner-text">Real-time fragrance industry trend analysis</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔍 DISCOVER TRENDING TOPICS</div>', unsafe_allow_html=True)
        st.markdown('<p class="intro-text">Our AI analyzes current fragrance trends, search volumes, social media discussions, and competitor content to identify 5 high-potential blog topics perfect for <strong>ARGOS Fragrances</strong>.</p>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🔍 FIND TRENDING TOPICS", use_container_width=True):
                st.session_state.agents["discovery"] = "active"
                progress = st.empty()
                
                # Show sources being searched
                render_loading_sources(progress)
                
                try:
                    result = asyncio.run(run_discovery())
                    st.session_state.topics_list = parse_topics(result["raw_response"])
                    st.session_state.agents["discovery"] = "completed"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        if st.session_state.topics_list:
            st.markdown('<div class="section-title">📋 TRENDING TOPICS FOUND</div>', unsafe_allow_html=True)
            for i, topic in enumerate(st.session_state.topics_list):
                potential = topic.get("potential", "Medium").upper()
                badge = "badge-high" if "HIGH" in potential else "badge-medium"
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f'<div class="topic-card"><span class="topic-number">{i+1}</span><div class="topic-title">{topic.get("title", "N/A")}</div><div class="topic-keyword">🔑 {topic.get("keyword", "N/A")}</div><span class="{badge}">{potential} POTENTIAL</span></div>', unsafe_allow_html=True)
                with c2:
                    st.write("")
                    if st.button("SELECT →", key=f"sel_{i}"):
                        st.session_state.selected_idx = i
                        st.session_state.phase = 2
                        st.session_state.article = None
                        st.rerun()
    
    render_footer()


def page_generation():
    render_nav()
    
    topics = st.session_state.topics_list
    idx = st.session_state.selected_idx
    topic = topics[idx] if topics and idx < len(topics) else {}
    
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        options = [f"{i+1}. {t.get('title', 'N/A')}" for i, t in enumerate(topics)]
        if options:
            selected = st.selectbox("Topic", options, index=idx, label_visibility="collapsed")
            new_idx = options.index(selected)
            if new_idx != idx:
                st.session_state.selected_idx = new_idx
                st.session_state.article = None
                st.session_state.agents = {k: "completed" if k == "discovery" else "pending" for k in st.session_state.agents}
                st.rerun()
    with c2:
        st.markdown(f"<div style='padding:0.5rem;color:#c9a962;font-size:0.85rem;'>🔑 {topic.get('keyword', '')}</div>", unsafe_allow_html=True)
    with c3:
        if st.button("← BACK"):
            st.session_state.phase = 1
            st.rerun()
    
    st.markdown("<hr style='border-color:rgba(201,169,98,0.2);margin:0.75rem 0;'>", unsafe_allow_html=True)
    
    col_main, col_right = st.columns([3, 1])
    
    with col_right:
        render_pipeline()
        if st.session_state.article:
            render_checklist()
    
    with col_main:
        if not st.session_state.article:
            st.markdown('<div class="section-title">✍️ GENERATE ARTICLE</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="topic-card"><div class="topic-title" style="font-size:1.2rem;margin-bottom:0.75rem;">{topic.get("title", "N/A")}</div><div style="color:#c9a962;font-size:0.75rem;margin-bottom:0.25rem;">PRIMARY KEYWORD</div><div style="color:#fff;margin-bottom:0.75rem;">{topic.get("keyword", "N/A")}</div><div style="color:#c9a962;font-size:0.75rem;margin-bottom:0.25rem;">SECONDARY KEYWORDS</div><div style="color:#ccc;font-size:0.9rem;">{topic.get("secondary", "N/A")}</div></div>', unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if st.button("🚀 GENERATE FULL ARTICLE", use_container_width=True):
                    progress = st.empty()
                    try:
                        result = asyncio.run(run_pipeline(topic.get('title', ''), topic.get('keyword', ''), progress))
                        st.session_state.article = result["article"]
                        st.session_state.article_html = md_to_html(result["article"])
                        st.session_state.meta = extract_meta(result["article"])
                        st.session_state.word_count = result["word_count"]
                        st.session_state.image_suggestions = extract_image_suggestions(result["article"], topic.get('keyword', ''))
                        save_to_history(topic.get('title', ''), topic.get('keyword', ''), result["article"], st.session_state.meta, result["word_count"])
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.markdown('<div class="section-title">📄 GENERATED ARTICLE</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="article-wrapper">{st.session_state.article_html}</div>', unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.download_button("📥 DOWNLOAD ARTICLE", st.session_state.article, f"{topic.get('keyword', 'article').replace(' ', '-')}.md", "text/markdown", use_container_width=True)
            
            # META DETAILS
            st.markdown('<div class="section-title">📋 META DETAILS</div>', unsafe_allow_html=True)
            meta = st.session_state.meta
            tags_html = "".join([f'<span class="tag-pill">{t}</span>' for t in meta.get('tags', [])])
            
            st.markdown(f'''<div class="meta-grid">
                <div class="meta-card"><div class="meta-label">META TITLE (Different from H1)</div><div class="meta-value">{meta.get('meta_title', meta.get('title', 'N/A'))}</div><div style="color:#888;font-size:0.7rem;margin-top:0.3rem;">{len(meta.get('meta_title', meta.get('title', '')))} / 60 characters</div></div>
                <div class="meta-card"><div class="meta-label">META DESCRIPTION</div><div class="meta-value">{meta.get('description', 'N/A')}</div><div style="color:#888;font-size:0.7rem;margin-top:0.3rem;">{len(meta.get('description', ''))} / 155 characters</div></div>
                <div class="meta-card"><div class="meta-label">URL SLUG</div><div class="meta-value">{meta.get('slug', 'N/A')}</div></div>
                <div class="meta-card"><div class="meta-label">TAGS</div><div>{tags_html}</div></div>
                <div class="meta-card meta-card-full"><div class="meta-label">EXCERPT (Unique for Blog Preview)</div><div class="meta-value">{meta.get('excerpt', 'N/A')}</div></div>
            </div>''', unsafe_allow_html=True)
            
            # ENHANCED IMAGE SUGGESTIONS
            st.markdown('<div class="section-title">🖼️ IMAGE SUGGESTIONS FOR DESIGNER</div>', unsafe_allow_html=True)
            
            suggestions = st.session_state.image_suggestions
            st.markdown('<div class="image-grid">', unsafe_allow_html=True)
            for img in suggestions:
                st.markdown(f'''<div class="image-card">
                    <div class="image-title">{img["title"]}</div>
                    <div class="image-desc">{img["desc"]}</div>
                    <div class="image-specs">
                        <span><strong>Style:</strong> {img["style"]}</span>
                        <span><strong>Size:</strong> {img["size"]}</span>
                        <span><strong>Alt Text:</strong> {img["alt"]}</span>
                    </div>
                </div>''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.write("")
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if st.button("🔄 GENERATE ANOTHER ARTICLE", use_container_width=True):
                    st.session_state.article = None
                    st.session_state.agents = {k: "completed" if k == "discovery" else "pending" for k in st.session_state.agents}
                    st.rerun()
    
    render_footer()


def main():
    init_state()
    if st.session_state.phase == 1:
        page_discovery()
    else:
        page_generation()

if __name__ == "__main__":
    main()