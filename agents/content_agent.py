"""
Content Generation Agent - ENHANCED
Features:
- 2500+ words minimum
- H2 headings based on AI search queries
- Topic-specific content structures
- Meta Title different from H1 (60 chars)
- AI Engine optimized content
- EXACT Argos product names
"""

import asyncio
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.settings import Settings


# === EXACT PRODUCT DATABASE ===
ARGOS_PRODUCTS = {
    "winter": [
        ("Sacred Flame", "https://argosfragrances.com/products/argos-sacred-flame-perfume", "Bergamot, Ginger, Cinnamon, Amber, Sandalwood", "Warm spicy blend perfect for cold weather"),
        ("Triumph of Bacchus", "https://argosfragrances.com/products/argos-triumph-of-bacchus-extrait-de-parfum", "Saffron, Rum, Oud, Vanilla, White Peach", "Rich gourmand for celebrations"),
        ("Fire and Desire Vulcan's Revenge", "https://argosfragrances.com/products/argos-fire-and-desire-vulcans-revenge-extrait-de-parfum", "Bergamot, Tuberose, Vanilla, Amber, Oud", "Bold sensual warmth"),
        ("Midas Touch", "https://argosfragrances.com/products/argos-midas-touch-extrait-de-parfum", "Bergamot, Rose, Osmanthus, Oud, Patchouli", "Opulent luxury")
    ],
    "romantic": [
        ("Bacio Immortale", "https://argosfragrances.com/products/argos-bacio-immortale-perfume", "Rose, Oud, Vanilla, Musk", "The immortal kiss for romantic evenings"),
        ("Adonis Awakens", "https://argosfragrances.com/products/argos-adonis-awakens-perfume", "Bergamot, Lavender, Cedar, Amber", "Fresh romantic scent"),
        ("Cupid's Arrow", "https://argosfragrances.com/products/argos-cupids-arrow-perfume", "Fruity, Floral, Musky", "Playful romance"),
        ("Fire and Desire Vulcan's Revenge", "https://argosfragrances.com/products/argos-fire-and-desire-vulcans-revenge-extrait-de-parfum", "Bergamot, Tuberose, Vanilla, Amber, Oud", "Passionate intensity")
    ],
    "oud": [
        ("Midas Touch", "https://argosfragrances.com/products/argos-midas-touch-extrait-de-parfum", "Bergamot, Rose, Osmanthus, Oud, Patchouli", "Ultimate luxury oud"),
        ("Triumph of Bacchus", "https://argosfragrances.com/products/argos-triumph-of-bacchus-extrait-de-parfum", "Saffron, Rum, Oud, Vanilla", "Rich celebratory oud"),
        ("Bacio Immortale", "https://argosfragrances.com/products/argos-bacio-immortale-perfume", "Rose, Oud, Vanilla, Musk", "Romantic oud"),
        ("Fire and Desire Vulcan's Revenge", "https://argosfragrances.com/products/argos-fire-and-desire-vulcans-revenge-extrait-de-parfum", "Tuberose, Vanilla, Amber, Oud", "Bold oud expression")
    ],
    "summer": [
        ("Danae Shower of Gold", "https://argosfragrances.com/products/argos-danae-shower-of-gold-extrait-de-parfum", "Citrus, Floral, White Musk", "Light refreshing summer scent"),
        ("Adonis Awakens", "https://argosfragrances.com/products/argos-adonis-awakens-perfume", "Bergamot, Lavender, Cedar", "Fresh versatile fragrance"),
        ("Cupid's Arrow", "https://argosfragrances.com/products/argos-cupids-arrow-perfume", "Fruity, Floral, Musky", "Playful daytime scent"),
        ("Pour Homme", "https://argosfragrances.com/products/argos-pour-homme-extrait-de-parfum", "Woody, Aromatic", "Clean masculine freshness")
    ],
    "longevity": [
        ("Midas Touch", "https://argosfragrances.com/products/argos-midas-touch-extrait-de-parfum", "Rose, Oud, Patchouli", "12+ hours longevity"),
        ("Triumph of Bacchus", "https://argosfragrances.com/products/argos-triumph-of-bacchus-extrait-de-parfum", "Saffron, Rum, Oud, Vanilla", "All-day projection"),
        ("Fire and Desire Vulcan's Revenge", "https://argosfragrances.com/products/argos-fire-and-desire-vulcans-revenge-extrait-de-parfum", "Vanilla, Amber, Oud", "Beast mode longevity"),
        ("Sacred Flame", "https://argosfragrances.com/products/argos-sacred-flame-perfume", "Cinnamon, Amber, Sandalwood", "Lasting warm presence")
    ],
    "default": [
        ("Sacred Flame", "https://argosfragrances.com/products/argos-sacred-flame-perfume", "Bergamot, Ginger, Cinnamon, Amber", "Versatile signature scent"),
        ("Midas Touch", "https://argosfragrances.com/products/argos-midas-touch-extrait-de-parfum", "Rose, Oud, Patchouli", "Luxurious statement"),
        ("Bacio Immortale", "https://argosfragrances.com/products/argos-bacio-immortale-perfume", "Rose, Oud, Vanilla, Musk", "Elegant romantic"),
        ("Triumph of Bacchus", "https://argosfragrances.com/products/argos-triumph-of-bacchus-extrait-de-parfum", "Saffron, Rum, Oud, Vanilla", "Rich celebratory")
    ]
}


def get_topic_category(topic_title: str) -> str:
    """Determine topic category for content structure."""
    topic_lower = topic_title.lower()
    
    if any(w in topic_lower for w in ["winter", "cold", "fall", "autumn", "cozy"]):
        return "winter"
    elif any(w in topic_lower for w in ["date", "romantic", "romance", "love", "valentine"]):
        return "romantic"
    elif any(w in topic_lower for w in ["oud", "woody", "oriental", "niche", "luxury"]):
        return "oud"
    elif any(w in topic_lower for w in ["summer", "fresh", "spring", "light", "daytime"]):
        return "summer"
    elif any(w in topic_lower for w in ["lasting", "longevity", "projection", "strong"]):
        return "longevity"
    else:
        return "default"


def get_content_structure(topic_title: str, keyword: str) -> dict:
    """Get topic-specific content structure with AI search query H2s."""
    category = get_topic_category(topic_title)
    
    # Generate search-query style H2 headings (like ChatGPT uses)
    structures = {
        "winter": {
            "type": "Seasonal Guide",
            "h2_sections": [
                f"What Makes a Great Winter Fragrance in 2025",
                f"Best {keyword.title()} for Cold Weather",
                f"Top Warm and Spicy Perfumes for Winter Season",
                f"How to Choose Winter Fragrances That Last All Day",
                f"Cozy Fragrances Perfect for Indoor Winter Occasions",
                f"Best Winter Perfumes for Men and Women 2025",
                f"Luxury Niche Winter Fragrances Worth Trying",
                f"Our Top Winter Fragrance Recommendations from Argos"
            ],
            "intro_hook": "cold weather fragrance selection",
            "products": ARGOS_PRODUCTS["winter"]
        },
        "romantic": {
            "type": "Occasion Guide",
            "h2_sections": [
                f"What Makes a Fragrance Romantic and Seductive",
                f"Best {keyword.title()} for Date Night",
                f"Top Romantic Perfumes That Will Get You Compliments",
                f"How to Choose the Perfect Date Night Fragrance",
                f"Seductive Fragrances for Special Romantic Occasions",
                f"Best Romantic Perfumes for Him and Her",
                f"Luxury Niche Fragrances for Romance",
                f"Our Romantic Fragrance Picks from Argos Collection"
            ],
            "intro_hook": "romantic fragrance selection",
            "products": ARGOS_PRODUCTS["romantic"]
        },
        "oud": {
            "type": "Ingredient Guide",
            "h2_sections": [
                f"What is Oud and Why is It So Valuable",
                f"Best {keyword.title()} for Oud Lovers",
                f"Top Luxury Oud Perfumes Worth the Investment",
                f"How to Wear Oud Fragrances Properly",
                f"Oud Fragrances for Beginners vs Connoisseurs",
                f"Best Oud Perfumes for Different Occasions",
                f"Niche vs Designer Oud Fragrances Comparison",
                f"Premium Oud Fragrances from Argos Collection"
            ],
            "intro_hook": "luxury oud fragrance world",
            "products": ARGOS_PRODUCTS["oud"]
        },
        "summer": {
            "type": "Seasonal Guide",
            "h2_sections": [
                f"What Makes a Great Summer Fragrance",
                f"Best {keyword.title()} for Hot Weather",
                f"Top Fresh and Light Perfumes for Summer",
                f"How to Make Your Summer Fragrance Last Longer",
                f"Best Daytime Fragrances for Work and Casual",
                f"Summer Perfumes for Beach and Vacation",
                f"Light Luxury Fragrances for Warm Weather",
                f"Our Summer Fragrance Recommendations from Argos"
            ],
            "intro_hook": "summer fragrance essentials",
            "products": ARGOS_PRODUCTS["summer"]
        },
        "longevity": {
            "type": "Performance Guide",
            "h2_sections": [
                f"What Makes a Fragrance Long Lasting",
                f"Best {keyword.title()} That Last 12+ Hours",
                f"Top Perfumes with Beast Mode Projection",
                f"How to Make Any Fragrance Last Longer",
                f"Extrait vs EDP vs EDT Longevity Comparison",
                f"Best Long Lasting Perfumes for All Budgets",
                f"Skin Chemistry and Fragrance Longevity Tips",
                f"Our Longest Lasting Fragrances from Argos"
            ],
            "intro_hook": "long-lasting fragrance performance",
            "products": ARGOS_PRODUCTS["longevity"]
        },
        "default": {
            "type": "Comprehensive Guide",
            "h2_sections": [
                f"Understanding {keyword.title()} in Modern Perfumery",
                f"Best {keyword.title()} for Different Occasions",
                f"Top Rated Fragrances in This Category",
                f"How to Choose the Right Fragrance for You",
                f"Expert Tips for Fragrance Selection",
                f"Best Options for Men and Women",
                f"Luxury vs Budget Options Compared",
                f"Our Curated Recommendations from Argos"
            ],
            "intro_hook": "fragrance discovery journey",
            "products": ARGOS_PRODUCTS["default"]
        }
    }
    
    return structures.get(category, structures["default"])


CONTENT_SYSTEM_PROMPT = """You are an Expert SEO Content Writer for Argos Fragrances luxury perfume brand.

## YOUR MISSION
Create 2500+ word articles optimized for AI search engines (ChatGPT, Perplexity, Google AI).

## CRITICAL RULES

### Product Names - USE EXACTLY AS PROVIDED:
- Sacred Flame (NOT "Sacred Flame, Prometheus")
- Triumph of Bacchus (NOT "Triumph of Bacchus, Bacchus Extrait")
- Fire and Desire Vulcan's Revenge (NOT "Fire and Desire, Vulcan")
- Midas Touch (NOT "Midas Touch, King Midas")
- Bacio Immortale (NOT "Bacio Immortale, Immortal Kiss")
- Adonis Awakens
- Danae Shower of Gold
- Cupid's Arrow
- Pour Homme
- Homme Sauvage

### Writing Rules:
1. NO em dash (—) - use hyphen (-) or comma instead
2. Write in engaging, magazine-quality prose
3. Each H2 section: 250-350 words minimum
4. Include specific details, not generic fluff
5. Use the EXACT product names with markdown links
6. Meta Title MUST be different from H1 (use full 60 characters)

### AI Engine Optimization:
- H2 headings should be natural search queries people type
- Include question-style subheadings (H3) that AI engines answer
- Use specific facts, numbers, and details AI can cite
- Structure content so AI can extract clear answers
"""


def create_content_agent():
    """Create the Content Generation Agent."""
    if not Settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key not configured.")
    
    model_client = OpenAIChatCompletionClient(
        model=Settings.CONTENT_AGENT_MODEL,
        api_key=Settings.OPENAI_API_KEY,
    )
    
    return AssistantAgent(
        name="content_agent",
        model_client=model_client,
        system_message=CONTENT_SYSTEM_PROMPT,
    )


async def generate_article_in_parts(research_brief: str) -> dict:
    """Generate 2500+ word article with search-query H2 headings."""
    print("\n✍️ Starting Enhanced Article Generation...")
    print("-" * 50)
    
    agent = create_content_agent()
    
    # Extract topic info
    topic_title = ""
    primary_keyword = ""
    for line in research_brief.split("\n"):
        line_stripped = line.strip()
        if "Title:" in line_stripped:
            topic_title = line_stripped.split(":", 1)[-1].strip()
        elif "Topic:" in line_stripped and not topic_title:
            topic_title = line_stripped.split(":", 1)[-1].strip()
        elif "Primary Keyword:" in line_stripped:
            primary_keyword = line_stripped.split(":", 1)[-1].strip()
    
    if not topic_title:
        topic_title = "Luxury Fragrance Guide"
    if not primary_keyword:
        primary_keyword = "luxury fragrance"
    
    # Get topic-specific structure
    structure = get_content_structure(topic_title, primary_keyword)
    
    print(f"   Topic: {topic_title}")
    print(f"   Keyword: {primary_keyword}")
    print(f"   Content Type: {structure['type']}")
    print(f"   H2 Sections: {len(structure['h2_sections'])}")
    
    # Build product recommendations section
    products = structure["products"]
    products_text = "\n".join([
        f"- [{name}]({url}) - Notes: {notes}. {desc}"
        for name, url, notes, desc in products
    ])
    
    # Part 1: Meta, Intro, First 4 H2 sections
    task_part1 = f"""
Write the FIRST HALF of a comprehensive article about: "{topic_title}"
Primary keyword: "{primary_keyword}"

## REQUIRED META (at the very top):
**Meta Title:** [Write 55-60 character title DIFFERENT from H1, include brand. Example: "Best Winter Perfumes 2025 - Expert Guide | Argos Fragrances"]
**Meta Description:** [Write exactly 150-155 characters about {topic_title}]
**URL Slug:** {primary_keyword.lower().replace(' ', '-')}

---

# {topic_title}

## Introduction (250+ words)
Hook readers about {structure['intro_hook']}. Explain why this topic matters in 2025. 
Preview what they'll learn. Mention Argos Fragrances naturally.

Now write these 4 detailed H2 sections (300+ words each):

## {structure['h2_sections'][0]}
[Comprehensive content with specific details, not generic. Include H3 subheadings.]

## {structure['h2_sections'][1]}
[Include specific recommendations, comparisons, expert insights. Add H3s.]

## {structure['h2_sections'][2]}
[Detailed guide content with actionable advice. Add H3 subheadings.]

## {structure['h2_sections'][3]}
[In-depth exploration with specific examples. Add H3s.]

RULES:
- NO em dash (—) - use hyphen (-) instead
- Each H2 section must be 300+ words
- Include H3 subheadings within each H2
- Write specific, detailed content - not generic filler
- Total for Part 1: 1400+ words

START WRITING NOW:
"""
    
    print("🤖 Generating Part 1 (Intro + 4 H2 sections)...")
    result1 = await agent.run(task=task_part1)
    
    part1_text = ""
    for msg in result1.messages:
        if hasattr(msg, 'content') and isinstance(msg.content, str):
            part1_text = msg.content
    
    # Part 2: Remaining H2s, Products, FAQ, Conclusion
    task_part2 = f"""
Continue the article about "{topic_title}" with PRIMARY KEYWORD "{primary_keyword}".

Write these remaining sections:

## {structure['h2_sections'][4]}
[300+ words with specific details and H3 subheadings]

## {structure['h2_sections'][5]}
[300+ words with comparisons and recommendations]

## {structure['h2_sections'][6]}
[300+ words with expert insights]

## {structure['h2_sections'][7]} - Argos Fragrances Recommendations
Feature these EXACT products (use exact names, include links):
{products_text}

Write 100+ words for EACH product:
- Describe why it fits {topic_title}
- Mention key notes
- Suggest when to wear it
- Include the markdown link

## Frequently Asked Questions About {primary_keyword.title()}

### What is the best {primary_keyword} for beginners?
[50+ word answer]

### How long does a quality {primary_keyword.split()[0]} fragrance last?
[50+ word answer]

### Is it worth investing in niche fragrances?
[50+ word answer]

### How should I apply fragrance for best results?
[50+ word answer]

### Where can I buy authentic luxury fragrances?
[50+ word answer mentioning Argos Fragrances]

## Conclusion (200+ words)
Summarize key points about {topic_title}.
Recommend exploring Argos Fragrances collection.
Call-to-action to visit argosfragrances.com.

**Tags:** {primary_keyword}, luxury fragrance, Argos Fragrances, niche perfume, fragrance guide, perfume recommendations

CRITICAL:
- NO em dash (—) - use hyphen (-) only
- Use EXACT product names as provided
- Total Part 2: 1200+ words minimum
- Combined article must exceed 2500 words

WRITE NOW:
"""
    
    print("🤖 Generating Part 2 (4 H2s + Products + FAQ + Conclusion)...")
    result2 = await agent.run(task=task_part2)
    
    part2_text = ""
    for msg in result2.messages:
        if hasattr(msg, 'content') and isinstance(msg.content, str):
            part2_text = msg.content
    
    # Combine and clean
    full_article = part1_text + "\n\n" + part2_text
    
    # Clean em dashes
    full_article = full_article.replace("—", "-").replace("–", "-")
    
    # Fix any product name hallucinations
    fixes = [
        ("Sacred Flame, Prometheus", "Sacred Flame"),
        ("Sacred Flame Prometheus", "Sacred Flame"),
        ("Triumph of Bacchus, Bacchus", "Triumph of Bacchus"),
        ("Triumph of Bacchus Bacchus", "Triumph of Bacchus"),
        ("Triumph of Bacchus Extrait de Parfum", "Triumph of Bacchus"),
        ("Fire and Desire, Vulcan's Revenge, Vulcan", "Fire and Desire Vulcan's Revenge"),
        ("Fire and Desire, Vulcan", "Fire and Desire Vulcan's Revenge"),
        ("Fire and Desire Vulcan", "Fire and Desire Vulcan's Revenge"),
        ("Vulcan's Revenge, Vulcan", "Fire and Desire Vulcan's Revenge"),
        ("Midas Touch, King Midas", "Midas Touch"),
        ("Midas Touch King Midas", "Midas Touch"),
        ("Bacio Immortale, The Immortal", "Bacio Immortale"),
        ("Bacio Immortale, Immortal Kiss", "Bacio Immortale"),
        ("Danae, Shower of Gold", "Danae Shower of Gold"),
    ]
    
    for wrong, correct in fixes:
        full_article = full_article.replace(wrong, correct)
    
    word_count = len(full_article.split())
    
    print(f"\n✅ Article Generated!")
    print(f"   Topic: {topic_title}")
    print(f"   Word Count: {word_count}")
    print(f"   H2 Sections: 8+")
    print(f"   Target Met: {'✓ Yes' if word_count >= 2400 else '✗ No (may need review)'}")
    
    return {
        "status": "success" if word_count >= 2400 else "review",
        "article": full_article,
        "word_count": word_count,
        "has_em_dash": "—" in full_article,
        "structure": structure["type"],
        "h2_count": len(structure["h2_sections"])
    }


# Backwards compatibility
async def generate_article(research_brief: str) -> dict:
    return await generate_article_in_parts(research_brief)


if __name__ == "__main__":
    print("=" * 60)
    print("ENHANCED CONTENT AGENT")
    print("=" * 60)
    print("\nFeatures:")
    print("- 2500+ word articles")
    print("- 8+ H2 sections based on search queries")
    print("- Topic-specific content structures")
    print("- Meta Title different from H1")
    print("- EXACT Argos product names")
    print("- AI Engine optimized")
    print("\nTopic Categories:")
    print("- Winter/Cold Weather")
    print("- Romantic/Date Night")
    print("- Oud/Luxury/Niche")
    print("- Summer/Fresh/Light")
    print("- Longevity/Performance")
    print("=" * 60)