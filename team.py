"""
Team Integration for Argos Content System
Connects Research, Content, and Verify agents in a workflow
"""

import asyncio
import sys
import os

# Ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.research_agent import discover_topics, deep_research
from agents.content_agent import generate_article_in_parts
from agents.verify_agent import verify_article


async def phase1_discover_topics() -> dict:
    """
    Phase 1: Discover 5 trending topics.
    
    Returns:
        Dictionary with topic suggestions
    """
    print("\n" + "=" * 60)
    print("📌 PHASE 1: TOPIC DISCOVERY")
    print("=" * 60)
    
    result = await discover_topics()
    return result


async def phase2_generate_article(topic: str, keyword: str) -> dict:
    """
    Phase 2: Full article generation pipeline.
    Research Agent → Content Agent → Verify Agent
    
    Args:
        topic: Selected topic title
        keyword: Primary keyword for the topic
    
    Returns:
        Dictionary with final article and verification report
    """
    print("\n" + "=" * 60)
    print("📌 PHASE 2: ARTICLE GENERATION PIPELINE")
    print("=" * 60)
    
    # Step 1: Deep Research
    print("\n🔍 Step 1/3: Research Agent - Deep Research")
    print("-" * 40)
    research_result = await deep_research(topic=topic, keyword=keyword)
    research_brief = research_result["research_brief"]
    
    # Step 2: Content Generation
    print("\n✍️ Step 2/3: Content Agent - Writing Article")
    print("-" * 40)
    content_result = await generate_article_in_parts(research_brief)
    article = content_result["article"]
    
    # Auto-clean em dashes
    article = article.replace("—", "-").replace("–", "-")
    
    # Step 3: Verification
    print("\n🔍 Step 3/3: Verify Agent - Quality Check")
    print("-" * 40)
    verify_result = await verify_article(article=article, primary_keyword=keyword)
    
    # Combine results
    return {
        "status": verify_result["status"],
        "topic": topic,
        "keyword": keyword,
        "research_brief": research_brief,
        "article": article,
        "word_count": content_result["word_count"],
        "verification_report": verify_result["verification_report"],
        "has_em_dash": content_result["has_em_dash"],
    }


async def full_workflow_demo():
    """
    Demonstrate the complete workflow:
    1. Discover topics
    2. Select a topic (simulated)
    3. Generate article
    4. Verify and finalize
    """
    print("\n" + "=" * 60)
    print("🚀 ARGOS CONTENT SYSTEM - FULL WORKFLOW DEMO")
    print("=" * 60)
    
    # Phase 1: Discover Topics
    discovery_result = await phase1_discover_topics()
    
    print("\n" + "=" * 60)
    print("📋 DISCOVERED TOPICS:")
    print("=" * 60)
    print(discovery_result["raw_response"])
    
    # Simulate user selection (in UI, user would click a topic)
    print("\n" + "-" * 40)
    print("📌 SIMULATING USER SELECTION...")
    print("   Selected: 'Best Winter Fragrances for 2025'")
    print("-" * 40)
    
    selected_topic = "Best Winter Fragrances for 2025"
    selected_keyword = "best winter fragrances 2025"
    
    # Phase 2: Generate Article
    article_result = await phase2_generate_article(
        topic=selected_topic,
        keyword=selected_keyword
    )
    
    # Final Output
    print("\n" + "=" * 60)
    print("🎉 WORKFLOW COMPLETE!")
    print("=" * 60)
    
    print(f"\n📊 FINAL STATS:")
    print(f"   Topic: {article_result['topic']}")
    print(f"   Keyword: {article_result['keyword']}")
    print(f"   Word Count: {article_result['word_count']}")
    print(f"   Em Dash: {'❌ Found' if article_result['has_em_dash'] else '✅ Clean'}")
    print(f"   Status: {article_result['status'].upper()}")
    
    print("\n" + "=" * 60)
    print("📄 ARTICLE PREVIEW (First 2000 chars):")
    print("=" * 60)
    print(article_result["article"][:2000])
    print("\n... [Article continues] ...")
    
    print("\n" + "=" * 60)
    print("📋 VERIFICATION REPORT:")
    print("=" * 60)
    print(article_result["verification_report"])
    
    return article_result


async def quick_article_generation(topic: str, keyword: str) -> dict:
    """
    Quick method to generate an article without topic discovery.
    Useful when user already knows what topic they want.
    
    Args:
        topic: The article topic
        keyword: Primary SEO keyword
    
    Returns:
        Complete article result
    """
    return await phase2_generate_article(topic=topic, keyword=keyword)


# === TEST FUNCTIONS ===

async def test_phase1_only():
    """Test Phase 1 only (topic discovery)."""
    result = await phase1_discover_topics()
    print("\n📋 Topics discovered successfully!")
    print(result["raw_response"])
    return result


async def test_phase2_only():
    """Test Phase 2 only (article generation) with a predefined topic."""
    print("Testing Phase 2 with predefined topic...")
    
    result = await phase2_generate_article(
        topic="Best Winter Fragrances for 2025",
        keyword="best winter fragrances 2025"
    )
    
    print("\n📄 Article generated successfully!")
    print(f"   Word count: {result['word_count']}")
    print(f"   Status: {result['status']}")
    
    return result


async def test_full_workflow():
    """Test the complete workflow."""
    return await full_workflow_demo()


# Main entry point
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    
    print("\n🧪 Argos Content System - Team Test")
    print("-" * 40)
    print("1. Test Phase 1 only (Topic Discovery)")
    print("2. Test Phase 2 only (Article Generation)")
    print("3. Test Full Workflow (Phase 1 + Phase 2)")
    print("-" * 40)
    print("\nCost estimates:")
    print("   Phase 1: ~$0.02")
    print("   Phase 2: ~$0.15-0.20")
    print("   Full: ~$0.20-0.25")
    print("-" * 40)
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        asyncio.run(test_phase1_only())
    elif choice == "2":
        confirm = input("This will generate a full article (~$0.15-0.20). Proceed? (y/n): ").strip().lower()
        if confirm == 'y':
            asyncio.run(test_phase2_only())
        else:
            print("Cancelled.")
    elif choice == "3":
        confirm = input("This runs the full workflow (~$0.20-0.25). Proceed? (y/n): ").strip().lower()
        if confirm == 'y':
            asyncio.run(test_full_workflow())
        else:
            print("Cancelled.")
    else:
        print("Invalid choice.")