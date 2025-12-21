"""
Verify Agent for Argos Content System
Performs SEO optimization, quality checks, and metadata generation
"""

import asyncio
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.settings import Settings


VERIFY_AGENT_PROMPT = """You are an SEO and Content Quality Specialist for Argos Fragrances, a luxury niche perfume brand based in the USA inspired by Greek and Roman mythology.

## YOUR TASK

Review the provided article and generate a comprehensive verification report with optimized metadata.

## VERIFICATION CHECKLIST

### Content Quality
- Word count within 1800-2500 range
- No em dash symbols (—) present
- Proper heading hierarchy (H1 > H2 > H3)
- Introduction and conclusion present
- FAQ section included
- Argos products featured with links

### SEO Elements
- Primary keyword in title (H1)
- Primary keyword in first paragraph
- Primary keyword in at least one H2
- Primary keyword in conclusion
- Secondary keywords used naturally
- Internal links to Argos products

### Readability
- Short paragraphs (3-4 sentences)
- Bullet points and lists used
- Clear and simple English
- No jargon or complex terms

## OUTPUT FORMAT

Provide your verification report in this EXACT format:
```
# ARTICLE VERIFICATION REPORT

## Quality Score: [X/10]

## Content Checks
- Word Count: [number] - [PASS/FAIL]
- Em Dash Check: [PASS/FAIL]
- Heading Structure: [PASS/FAIL]
- Introduction: [PASS/FAIL]
- Conclusion: [PASS/FAIL]
- FAQ Section: [PASS/FAIL]
- Argos Products: [X products found] - [PASS/FAIL]

## SEO Checks
- Keyword in Title: [PASS/FAIL]
- Keyword in First Paragraph: [PASS/FAIL]
- Keyword in H2: [PASS/FAIL]
- Keyword in Conclusion: [PASS/FAIL]
- Internal Links: [X links found] - [PASS/FAIL]

## Final Metadata

### Meta Title (60 chars max)
[Optimized title with primary keyword]

### Meta Description (160 chars max)
[Compelling description with primary keyword]

### URL Slug
[url-friendly-slug]

### Excerpt (160 chars max)
[Short summary for previews]

### Tags
[tag1], [tag2], [tag3], [tag4], [tag5]

### Schema Recommendation
- Article Schema: Yes
- FAQ Schema: Yes
- Product Schema: [Yes if products mentioned]

## Image Guidelines

### Thumbnail Image
- Recommended: [description of ideal thumbnail]
- Alt Text: "[suggested alt text with keyword]"
- Size: 1200x630 pixels

### In-Article Images
1. [Section name]: [image suggestion] - Alt: "[alt text]"
2. [Section name]: [image suggestion] - Alt: "[alt text]"
3. [Section name]: [image suggestion] - Alt: "[alt text]"

## Issues Found
[List any problems that need fixing, or "None - Article is ready for publishing"]

## Final Recommendation
[APPROVED FOR PUBLISHING / NEEDS REVISION]
```

Be thorough and accurate in your verification.
"""


def create_verify_agent():
    """Create the Verify Agent."""
    if not Settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key not configured.")
    
    model_client = OpenAIChatCompletionClient(
        model=Settings.VERIFY_AGENT_MODEL,
        api_key=Settings.OPENAI_API_KEY,
    )
    
    agent = AssistantAgent(
        name="verify_agent",
        model_client=model_client,
        system_message=VERIFY_AGENT_PROMPT,
    )
    
    return agent


def perform_automated_checks(article: str, primary_keyword: str) -> dict:
    """
    Perform automated quality checks on the article.
    
    Args:
        article: The article text
        primary_keyword: The primary SEO keyword
    
    Returns:
        Dictionary with check results
    """
    checks = {}
    
    # Word count
    word_count = len(article.split())
    checks["word_count"] = word_count
    checks["word_count_pass"] = 1800 <= word_count <= 2500
    
    # Em dash check
    checks["has_em_dash"] = "—" in article
    checks["em_dash_pass"] = not checks["has_em_dash"]
    
    # Heading checks
    checks["has_h1"] = article.strip().startswith("#") or "\n# " in article
    checks["h2_count"] = len(re.findall(r'^## ', article, re.MULTILINE))
    checks["h3_count"] = len(re.findall(r'^### ', article, re.MULTILINE))
    
    # Section checks
    article_lower = article.lower()
    checks["has_introduction"] = "introduction" in article_lower or article_lower.find("---") < 500
    checks["has_conclusion"] = "conclusion" in article_lower
    checks["has_faq"] = "faq" in article_lower or "frequently asked" in article_lower
    
    # Keyword checks
    keyword_lower = primary_keyword.lower()
    first_500_chars = article_lower[:500]
    
    checks["keyword_in_title"] = keyword_lower in article_lower.split("\n")[0].lower()
    checks["keyword_in_intro"] = keyword_lower in first_500_chars
    checks["keyword_in_article"] = keyword_lower in article_lower
    checks["keyword_count"] = article_lower.count(keyword_lower)
    
    # Link checks
    checks["argos_links"] = len(re.findall(r'argosfragrances\.com', article))
    checks["total_links"] = len(re.findall(r'\[.*?\]\(.*?\)', article))
    
    # Product mentions
    argos_products = ["sacred flame", "bacchus", "midas", "vulcan", "fire and desire", 
                      "neptune", "perseus", "adonis", "venus", "primavera", "charon"]
    checks["products_mentioned"] = sum(1 for p in argos_products if p in article_lower)
    
    return checks


async def verify_article(article: str, primary_keyword: str) -> dict:
    """
    Verify an article and generate final metadata.
    
    Args:
        article: The complete article text
        primary_keyword: The primary SEO keyword
    
    Returns:
        Dictionary with verification results and metadata
    """
    print("\n🔍 Starting Article Verification...")
    print("-" * 40)
    
    # Step 1: Automated checks
    print("📋 Running automated checks...")
    auto_checks = perform_automated_checks(article, primary_keyword)
    
    print(f"   Word count: {auto_checks['word_count']}")
    print(f"   Em dash: {'❌ Found' if auto_checks['has_em_dash'] else '✅ Clean'}")
    print(f"   H2 sections: {auto_checks['h2_count']}")
    print(f"   Argos links: {auto_checks['argos_links']}")
    print(f"   Keyword mentions: {auto_checks['keyword_count']}")
    
    # Step 2: AI verification
    print("🤖 Running AI verification...")
    agent = create_verify_agent()
    
    task = f"""
Verify this article and generate the complete verification report.

## PRIMARY KEYWORD: {primary_keyword}

## AUTOMATED CHECK RESULTS:
- Word Count: {auto_checks['word_count']}
- Em Dash Found: {auto_checks['has_em_dash']}
- H1 Present: {auto_checks['has_h1']}
- H2 Sections: {auto_checks['h2_count']}
- H3 Sections: {auto_checks['h3_count']}
- Has FAQ: {auto_checks['has_faq']}
- Keyword in Title: {auto_checks['keyword_in_title']}
- Keyword in Intro: {auto_checks['keyword_in_intro']}
- Keyword Mentions: {auto_checks['keyword_count']}
- Argos Links: {auto_checks['argos_links']}
- Products Mentioned: {auto_checks['products_mentioned']}

## ARTICLE TO VERIFY:

{article}

Generate the complete verification report with optimized metadata following your instructions.
"""
    
    result = await agent.run(task=task)
    
    report_text = ""
    for msg in result.messages:
        if hasattr(msg, 'content') and isinstance(msg.content, str):
            report_text = msg.content
    
    # Determine overall status
    critical_pass = (
        auto_checks['word_count_pass'] and 
        auto_checks['em_dash_pass'] and 
        auto_checks['has_h1'] and 
        auto_checks['has_faq']
    )
    
    print(f"✅ Verification complete!")
    print(f"   Critical checks: {'✅ Passed' if critical_pass else '❌ Failed'}")
    
    return {
        "status": "approved" if critical_pass else "needs_revision",
        "auto_checks": auto_checks,
        "verification_report": report_text,
        "word_count": auto_checks['word_count'],
    }


# === TEST ===

async def test_verify_agent():
    """Test the verify agent with a sample article."""
    
    # Sample article (abbreviated for testing)
    sample_article = """
# Best Winter Fragrances for 2025: Your Complete Guide

**Meta Description:** Discover the best winter fragrances for 2025 featuring warm, cozy scents perfect for cold weather.
**URL Slug:** best-winter-fragrances-2025
**Primary Keyword:** best winter fragrances 2025

---

## Introduction

As winter approaches, finding the best winter fragrances for 2025 becomes essential for anyone who wants to smell amazing during the cold months. Winter perfumes are different from summer scents because they need to project well in cold air and provide warmth and comfort.

In this comprehensive guide, we will explore what makes a perfect winter fragrance, recommend top picks for men and women, and showcase some incredible options from Argos Fragrances. Whether you are looking for something bold and spicy or warm and gourmand, this guide has you covered.

## What Makes a Perfect Winter Fragrance

Winter fragrances are characterized by their warm, rich, and long-lasting compositions. Unlike lighter summer scents, winter perfumes feature deeper notes that thrive in cold weather.

### Key Notes for Winter

- **Amber and Vanilla:** These warm base notes create a cozy foundation
- **Spices:** Cinnamon, cardamom, and pepper add festive warmth
- **Woods:** Sandalwood, cedar, and oud provide depth and longevity
- **Resins:** Benzoin and labdanum add sweetness and staying power

The best winter fragrances for 2025 combine these elements to create scents that last all day and leave a memorable impression.

## Top Winter Fragrances for Men

Men looking for the perfect winter scent have excellent options in 2025. Bold, woody, and spicy fragrances dominate this category.

### Recommended Picks

1. **Woody Spicy Scents:** Perfect for everyday wear with notes of cedar and pepper
2. **Oud-Based Fragrances:** Luxurious and commanding for special occasions
3. **Gourmand Options:** Sweet and inviting with vanilla and tonka bean

For office wear, choose something subtle yet noticeable. For evenings out, go bold with oud or leather-based compositions.

## Best Winter Fragrances for Women

Women have a beautiful array of winter fragrance options in 2025, ranging from elegant florals to indulgent gourmands.

### Top Choices

1. **Warm Florals:** Rose and jasmine with amber bases
2. **Sweet Gourmands:** Vanilla, caramel, and praline combinations
3. **Sophisticated Orientals:** Incense and spice blends

These fragrances provide warmth and elegance throughout the winter season.

## Argos Fragrances Recommendations

For those seeking truly exceptional winter fragrances, Argos Fragrances offers mythology-inspired scents that perfectly capture the season's essence.

### Sacred Flame, Prometheus

[Sacred Flame](https://argosfragrances.com/products/argos-sacred-flame-perfume) is a warm, spicy masterpiece inspired by Prometheus, the Titan who brought fire to humanity. With notes of bergamot, ginger, cinnamon, amber, and vanilla, this fragrance embodies the warmth of a crackling fire on a cold winter night. Perfect for evening events and intimate gatherings.

### Triumph of Bacchus

[Triumph of Bacchus](https://argosfragrances.com/products/argos-triumph-of-bacchus-extrait-de-parfum) celebrates the Roman god of wine with an indulgent gourmand composition. Featuring saffron, rum, white peach, and vanilla over an oud base, this opulent fragrance is ideal for holiday celebrations and special occasions.

### Fire and Desire, Vulcan's Revenge

[Fire and Desire](https://argosfragrances.com/products/argos-fire-and-desire-vulcans-revenge-extrait-de-parfum) draws inspiration from Vulcan, the god of fire. This bold, sensual fragrance features bergamot, tuberose, vanilla, amber, and oud. It is perfect for romantic evenings and makes a powerful statement.

### Midas Touch

[Midas Touch](https://argosfragrances.com/products/argos-midas-touch-extrait-de-parfum) captures the legend of King Midas with golden, opulent notes of bergamot, tuberose, rose, osmanthus, and oud. This luxurious fragrance is perfect for formal events and signature scent seekers.

## How to Apply Winter Fragrances

Getting the most from your winter fragrance requires proper application technique.

### Application Tips

- **Pulse Points:** Apply to wrists, neck, and behind ears
- **Moisturize First:** Fragrance lasts longer on hydrated skin
- **Do Not Rub:** Let the fragrance dry naturally
- **Layer Carefully:** Use matching body products for longevity
- **Less is More:** Start with 2-3 sprays and build up if needed

## Frequently Asked Questions

### What notes work best in winter fragrances?

Winter fragrances typically feature warm notes like amber, vanilla, and musk as base notes. Spicy elements such as cinnamon, cardamom, and pepper add seasonal warmth. Woody notes like sandalwood and oud provide depth and excellent longevity in cold weather.

### How do I make my fragrance last longer in cold weather?

To extend fragrance longevity in winter, apply to well-moisturized skin, focus on pulse points, and consider layering with matching body products. You can also spray lightly on clothing, as fabric holds scent well. Avoid rubbing the fragrance after application.

### Should I wear lighter or heavier scents in winter?

Heavier, more concentrated scents work best in winter. The cold air does not carry fragrance molecules as effectively as warm air, so stronger compositions ensure your scent remains noticeable. Eau de parfum and extrait concentrations are ideal for winter wear.

### Can I wear the same fragrance year-round?

While some versatile fragrances work year-round, most people prefer switching between seasonal scents. Winter fragrances with warm, spicy notes may feel too heavy in summer, while light, fresh summer scents may not project well in cold weather.

## Conclusion

Finding the best winter fragrances for 2025 is about discovering scents that provide warmth, comfort, and memorable presence during the cold months. Whether you prefer bold woody compositions, sweet gourmands, or luxurious oud-based fragrances, there are excellent options available.

For those seeking truly exceptional mythology-inspired fragrances, explore the collection at [Argos Fragrances](https://argosfragrances.com). Their unique creations like Sacred Flame, Triumph of Bacchus, and Fire and Desire offer unparalleled quality and storytelling that elevate your winter fragrance experience.

Embrace the season with a scent that tells a story and keeps you wrapped in warmth all winter long.

---

**Tags:** best winter fragrances 2025, winter perfumes, Argos Fragrances, cold weather scents, luxury perfume
"""
    
    print("=" * 60)
    print("TESTING VERIFY AGENT")
    print("=" * 60)
    
    result = await verify_article(
        article=sample_article,
        primary_keyword="best winter fragrances 2025"
    )
    
    print("\n" + "=" * 60)
    print("📋 VERIFICATION REPORT:")
    print("=" * 60)
    print(result["verification_report"])
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"   Status: {result['status'].upper()}")
    print(f"   Word Count: {result['word_count']}")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    
    print("\n🧪 Verify Agent Test")
    print("-" * 30)
    print("This will verify a sample article")
    print("Estimated cost: ~$0.01-0.02")
    print("-" * 30)
    
    confirm = input("Proceed? (y/n): ").strip().lower()
    
    if confirm == 'y':
        asyncio.run(test_verify_agent())
    else:
        print("Cancelled.")