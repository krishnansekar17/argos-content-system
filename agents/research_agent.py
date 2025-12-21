"""
Research Agent for Argos Content System
Handles two modes:
1. Discovery Mode - Find 5 trending topics in fragrance niche
2. Deep Research Mode - Detailed research on a selected topic
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.settings import Settings
from tools.web_search import search_web, search_fragrance_trends, discover_trending_topics
from tools.argos_products import get_products_by_style, get_products_by_season


# === SYSTEM PROMPTS ===

DISCOVERY_MODE_PROMPT = """You are a Fragrance Trend Research Specialist working for Argos Fragrances, a luxury niche perfume brand based in the USA inspired by Greek and Roman mythology.

## YOUR TASK

Analyze the search data provided and identify exactly 5 HIGH-POTENTIAL blog topics for the luxury fragrance niche.

## STRICT REQUIREMENTS

1. You must output EXACTLY 5 topics - no more, no less
2. Focus ONLY on US and Western fragrance trends
3. Each topic must be suitable for a 1800-2500 word blog article
4. Topics should naturally allow featuring Argos Fragrance products
5. DO NOT call any tools - just analyze the provided data and respond

## OUTPUT FORMAT (Follow Exactly)

TOPIC 1:
Title: [Catchy, SEO-friendly blog title - 50-60 characters]
Primary Keyword: [Main keyword to target, 2-4 words]
Secondary Keywords: [3-4 related keywords, comma separated]
Search Potential: [High/Medium]
Why Trending: [One sentence explaining why this is hot now]
Argos Angle: [How Argos products can be featured]

TOPIC 2:
[Same format]

TOPIC 3:
[Same format]

TOPIC 4:
[Same format]

TOPIC 5:
[Same format]

## TOPIC IDEAS TO CONSIDER
- Seasonal fragrance guides (winter, summer, fall, spring)
- Occasion-based recommendations (date night, office, wedding)
- Fragrance education (how to choose, layering, longevity tips)
- Trend pieces (niche vs designer, oud popularity, gourmand scents)
- Gift guides and recommendations
- Fragrance note deep-dives (oud, amber, vanilla, rose)

Now analyze the search data and provide your 5 topic recommendations.
"""

DEEP_RESEARCH_PROMPT = """You are a Senior SEO Content Researcher for Argos Fragrances, a luxury niche perfume brand based in the USA inspired by Greek and Roman mythology.

## YOUR TASK

Create a comprehensive content brief for the selected topic. DO NOT call any tools - analyze the provided data and create the brief.

## OUTPUT FORMAT (Follow Exactly)

# CONTENT RESEARCH BRIEF

## Topic Overview
- Title: [Final article title]
- Primary Keyword: [main keyword]
- Search Intent: [informational/commercial/transactional]
- Target Word Count: 1800-2500 words

## Keyword Strategy
Primary Keyword: [keyword]
Long-tail Keywords:
1. [keyword phrase]
2. [keyword phrase]
3. [keyword phrase]
4. [keyword phrase]
5. [keyword phrase]

LSI Keywords: [5-7 semantically related terms]

## Suggested Article Outline
H1: [Main title]

H2: Introduction
- Hook the reader
- What they'll learn

H2: [Section 1 title]
H3: [Subsection if needed]

H2: [Section 2 title]

H2: [Section 3 title]

H2: [Section 4 title]

H2: Argos Fragrances Recommendations
- Feature 3-4 products naturally

H2: Frequently Asked Questions
- Q1: [Question]
- Q2: [Question]
- Q3: [Question]

H2: Conclusion
- Summary and CTA

## Argos Products to Feature
1. [Product Name] - [Why it fits this article]
2. [Product Name] - [Why it fits this article]
3. [Product Name] - [Why it fits this article]

## Key Points to Cover
- [Point 1]
- [Point 2]
- [Point 3]
- [Point 4]
- [Point 5]

## SEO Notes
- Include primary keyword in: title, first paragraph, H2, conclusion
- Use secondary keywords naturally throughout
- Add internal links to Argos product pages
- Suggest 2-3 external authority links

Now create the complete research brief.
"""


def create_research_agent(mode: str = "discovery"):
    """
    Create a Research Agent for the specified mode.
    
    Args:
        mode: "discovery" for finding topics, "deep" for detailed research
    
    Returns:
        AssistantAgent configured for the specified mode
    """
    # Validate API key
    if not Settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key not configured. Please check your .env file.")
    
    # Create model client
    model_client = OpenAIChatCompletionClient(
        model=Settings.RESEARCH_AGENT_MODEL,
        api_key=Settings.OPENAI_API_KEY
    )
    
    # Select prompt based on mode
    system_prompt = DISCOVERY_MODE_PROMPT if mode == "discovery" else DEEP_RESEARCH_PROMPT
    
    # Create the agent WITHOUT tools - it analyzes provided data only
    agent = AssistantAgent(
        name="research_agent",
        model_client=model_client,
        system_message=system_prompt,
    )
    
    return agent


async def discover_topics() -> dict:
    """
    Phase 1: Discover 5 trending fragrance topics.
    Returns structured data for UI display.
    
    Returns:
        Dictionary with trending topics and metadata
    """
    print("\n🔍 Starting Topic Discovery...")
    print("-" * 40)
    
    # Step 1: Gather search data (this uses the web search tool)
    print("📡 Searching for fragrance trends...")
    trends_data = search_fragrance_trends()
    base_topics = discover_trending_topics("luxury fragrance")
    
    # Step 2: Create the agent
    agent = create_research_agent(mode="discovery")
    
    # Step 3: Prepare the task with all search data
    topics_text = "\n".join([f"- {t['topic']}: keyword '{t['keyword']}'" for t in base_topics])
    
    task = f"""
Analyze the following fragrance trend data and provide exactly 5 blog topic recommendations.

## CURRENT FRAGRANCE TRENDS (from web search):

{trends_data}

## TOPIC INSPIRATIONS:

{topics_text}

## INSTRUCTIONS:
- Review the search data above
- Identify what's trending in the US/Western fragrance market
- Create 5 unique, high-potential blog topics
- Follow the exact output format specified in your system instructions
- DO NOT call any tools - just analyze and respond

Provide your 5 topic recommendations now.
"""
    
    # Step 4: Run the agent
    print("🤖 Analyzing trends with AI...")
    result = await agent.run(task=task)
    
    # Step 5: Extract the response
    response_text = ""
    for msg in result.messages:
        if hasattr(msg, 'content') and isinstance(msg.content, str):
            response_text = msg.content
    
    print("✅ Topic discovery complete!")
    
    return {
        "status": "success",
        "raw_response": response_text,
        "search_data_used": True,
    }


async def deep_research(topic: str, keyword: str) -> dict:
    """
    Phase 2: Conduct deep research on a selected topic.
    
    Args:
        topic: The selected topic title
        keyword: The primary keyword for the topic
    
    Returns:
        Dictionary with research brief
    """
    print(f"\n📚 Starting Deep Research: {topic}")
    print("-" * 40)
    
    # Step 1: Gather search data
    print("📡 Gathering detailed information...")
    search_results = search_web(f"{keyword} guide tips 2025", max_results=5)
    
    # Step 2: Get relevant Argos products based on topic
    print("🏛️ Finding matching Argos products...")
    
    topic_lower = topic.lower()
    
    if "winter" in topic_lower or "cold" in topic_lower:
        argos_products = get_products_by_season("winter")
    elif "summer" in topic_lower or "fresh" in topic_lower:
        argos_products = get_products_by_season("summer")
    elif "date" in topic_lower or "romantic" in topic_lower:
        argos_products = get_products_by_style("romantic sensual")
    elif "oud" in topic_lower:
        argos_products = get_products_by_style("oud woody")
    elif "long lasting" in topic_lower or "lasting" in topic_lower:
        argos_products = get_products_by_style("powerful bold")
    elif "niche" in topic_lower:
        argos_products = get_products_by_style("luxury elegant")
    else:
        argos_products = get_products_by_style("luxury")
    
    # Step 3: Create the agent
    agent = create_research_agent(mode="deep")
    
    # Step 4: Prepare the task
    task = f"""
Create a comprehensive content research brief for the following topic.

## SELECTED TOPIC:
Title: {topic}
Primary Keyword: {keyword}

## WEB RESEARCH DATA:

{search_results}

## ARGOS PRODUCTS TO CONSIDER FEATURING:

{argos_products}

## INSTRUCTIONS:
- Create a detailed content brief following your system instructions format
- Include specific Argos products that match this topic
- Provide a clear article outline
- DO NOT call any tools - just analyze the data and create the brief

Create the research brief now.
"""
    
    # Step 5: Run the agent
    print("🤖 Creating research brief...")
    result = await agent.run(task=task)
    
    # Step 6: Extract response
    response_text = ""
    for msg in result.messages:
        if hasattr(msg, 'content') and isinstance(msg.content, str):
            response_text = msg.content
    
    print("✅ Deep research complete!")
    
    return {
        "status": "success",
        "topic": topic,
        "keyword": keyword,
        "research_brief": response_text,
    }


# === TEST FUNCTIONS ===

async def test_discovery():
    """Test the topic discovery function."""
    print("=" * 60)
    print("TESTING RESEARCH AGENT - DISCOVERY MODE")
    print("=" * 60)
    
    result = await discover_topics()
    
    print("\n" + "=" * 60)
    print("📋 DISCOVERY RESULTS:")
    print("=" * 60)
    print(result["raw_response"])
    
    return result


async def test_deep_research():
    """Test the deep research function."""
    print("=" * 60)
    print("TESTING RESEARCH AGENT - DEEP RESEARCH MODE")
    print("=" * 60)
    
    result = await deep_research(
        topic="Best Winter Fragrances for 2025",
        keyword="best winter fragrances 2025"
    )
    
    print("\n" + "=" * 60)
    print("📋 RESEARCH BRIEF:")
    print("=" * 60)
    print(result["research_brief"])
    
    return result


# Run tests when executed directly
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    
    print("\n🧪 Research Agent Test Menu")
    print("-" * 30)
    print("1. Test Discovery Mode (find 5 topics)")
    print("2. Test Deep Research Mode")
    print("3. Run Both Tests")
    print("-" * 30)
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        asyncio.run(test_discovery())
    elif choice == "2":
        asyncio.run(test_deep_research())
    elif choice == "3":
        asyncio.run(test_discovery())
        print("\n" + "=" * 60 + "\n")
        asyncio.run(test_deep_research())
    else:
        print("Invalid choice. Running discovery test by default.")
        asyncio.run(test_discovery())