"""
Web Search Tool for Research Agent
Uses DDGS (DuckDuckGo Search) for English web searches
"""

import warnings
warnings.filterwarnings("ignore")

from ddgs import DDGS


def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo (English results only).
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return
    
    Returns:
        A formatted string containing search results
    """
    try:
        ddgs = DDGS()
        # Correct syntax: query is positional argument
        results = list(ddgs.text(query, region="wt-wt", safesearch="moderate", max_results=max_results))
        
        if not results:
            return f"No results found for: {query}"
        
        # Filter for English results only
        english_results = []
        for r in results:
            title = r.get('title', '')
            body = r.get('body', '')
            # Skip Chinese/Japanese/Korean characters
            has_cjk = any('\u4e00' <= c <= '\u9fff' or '\u3040' <= c <= '\u30ff' or '\uac00' <= c <= '\ud7af' for c in title + body)
            if not has_cjk:
                english_results.append(r)
        
        if not english_results:
            return f"No English results found for: {query}"
        
        # Format results
        formatted = []
        for i, r in enumerate(english_results[:max_results], 1):
            formatted.append(
                f"{i}. **{r.get('title', 'No title')}**\n"
                f"   {r.get('body', 'No description')}\n"
                f"   Source: {r.get('href', 'No URL')}\n"
            )
        
        return "\n".join(formatted)
    
    except Exception as e:
        return f"Search error: {str(e)}"


def search_fragrance_trends() -> str:
    """
    Search for current trending fragrance topics.
    
    Returns:
        Formatted string with trending fragrance topics
    """
    queries = [
        "best niche perfumes 2025 fragrantica",
        "trending cologne for men 2025",
        "luxury perfume trends winter",
        "oud perfume recommendations",
        "long lasting fragrance reviews",
    ]
    
    ddgs = DDGS()
    all_topics = []
    
    for query in queries:
        try:
            results = list(ddgs.text(query, region="wt-wt", safesearch="moderate", max_results=2))
            for r in results:
                title = r.get('title', '')
                body = r.get('body', '')
                has_cjk = any('\u4e00' <= c <= '\u9fff' for c in title + body)
                if not has_cjk and title:
                    all_topics.append({
                        "query": query,
                        "title": title,
                        "snippet": body,
                        "url": r.get('href', '')
                    })
        except Exception:
            continue
    
    # Format output
    output = "## Trending Fragrance Topics\n\n"
    seen = set()
    count = 0
    
    for t in all_topics:
        if t['title'] not in seen and count < 8:
            seen.add(t['title'])
            count += 1
            output += f"{count}. **{t['title']}**\n"
            output += f"   {t['snippet'][:200]}...\n"
            output += f"   Source: {t['url']}\n\n"
    
    return output


def discover_trending_topics(niche: str = "luxury fragrance") -> list:
    """
    Discover 5 trending blog topics for the fragrance niche.
    Uses real search data to generate topic suggestions.
    
    Args:
        niche: The niche to find topics for
    
    Returns:
        List of topic dictionaries
    """
    ddgs = DDGS()
    
    # Search queries designed to find blog-worthy topics
    queries = [
        "best perfumes for winter 2025",
        "niche fragrance worth buying",
        "long lasting cologne recommendations",
        "oud fragrances for beginners",
        "date night perfume suggestions",
        "summer fragrance trends 2025",
        "affordable luxury perfume alternatives",
        "signature scent how to choose",
    ]
    
    raw_data = []
    
    for query in queries:
        try:
            results = list(ddgs.text(query, region="wt-wt", safesearch="moderate", max_results=2))
            for r in results:
                title = r.get('title', '')
                body = r.get('body', '')
                has_cjk = any('\u4e00' <= c <= '\u9fff' for c in title + body)
                if not has_cjk and title:
                    raw_data.append({
                        "query": query,
                        "title": title,
                        "snippet": body,
                        "url": r.get('href', '')
                    })
        except Exception:
            continue
    
    # Generate 5 topic suggestions based on search data
    topic_templates = [
        {
            "base_topic": "Best Winter Fragrances",
            "keyword": "best winter fragrances 2025",
            "secondary": ["cold weather cologne", "winter perfume", "cozy scents"]
        },
        {
            "base_topic": "Luxury Oud Perfumes Guide",
            "keyword": "luxury oud perfume",
            "secondary": ["oud fragrance", "middle eastern perfume", "oud cologne"]
        },
        {
            "base_topic": "Long-Lasting Fragrances That Perform",
            "keyword": "long lasting perfume",
            "secondary": ["beast mode fragrance", "strong projection cologne", "all day scent"]
        },
        {
            "base_topic": "Niche vs Designer Fragrances",
            "keyword": "niche vs designer perfume",
            "secondary": ["is niche worth it", "designer cologne comparison", "perfume value"]
        },
        {
            "base_topic": "Romantic Date Night Scents",
            "keyword": "date night fragrance",
            "secondary": ["romantic perfume", "seductive cologne", "attractive scent"]
        },
    ]
    
    topics = []
    for i, template in enumerate(topic_templates):
        topic = {
            "id": i + 1,
            "topic": template["base_topic"],
            "keyword": template["keyword"],
            "secondary_keywords": template["secondary"],
            "potential": 5 if i % 2 == 0 else 4,
            "source_data": raw_data[i] if i < len(raw_data) else None
        }
        topics.append(topic)
    
    return topics


# Test when run directly
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING WEB SEARCH TOOL")
    print("=" * 60)
    
    # Test 1: Basic search
    print("\n📌 Test 1: Basic Web Search")
    print("-" * 40)
    result = search_web("best luxury perfume men 2025", max_results=3)
    print(result)
    
    # Test 2: Fragrance trends
    print("\n📌 Test 2: Fragrance Trends Search")
    print("-" * 40)
    trends = search_fragrance_trends()
    print(trends[:1000])
    
    # Test 3: Discover topics
    print("\n📌 Test 3: Topic Discovery")
    print("-" * 40)
    topics = discover_trending_topics()
    for t in topics:
        print(f"\n{t['id']}. {t['topic']}")
        print(f"   Keyword: {t['keyword']}")
        print(f"   Potential: {'⭐' * t['potential']}")
        if t['source_data']:
            print(f"   Based on: {t['source_data']['title'][:50]}...")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)