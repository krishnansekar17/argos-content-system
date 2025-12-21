"""
Argos Products Tool
Provides access to the Argos Fragrance product database
for article recommendations and product integration
"""

import json
import os


# Load products database
def load_products():
    """Load the Argos products from JSON file."""
    # Get the path relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    json_path = os.path.join(parent_dir, "data", "argos_products.json")
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"products": [], "brand": {}}


def get_all_products() -> str:
    """
    Get all Argos fragrance products.
    
    Returns:
        Formatted string with all products
    """
    data = load_products()
    products = data.get("products", [])
    
    output = f"## Argos Fragrances - Complete Product Catalog\n"
    output += f"Total Products: {len(products)}\n\n"
    
    for p in products:
        # Skip accessories
        if "Accessories" in p.get("collection", ""):
            continue
            
        output += f"### {p.get('short_name', 'Unknown')}\n"
        output += f"- Collection: {p.get('collection', 'N/A')}\n"
        output += f"- Style: {p.get('style', 'N/A')}\n"
        output += f"- Best For: {p.get('best_for', 'N/A')}\n"
        output += f"- URL: {p.get('website_url', 'N/A')}\n\n"
    
    return output


def get_products_by_style(style_keywords: str) -> str:
    """
    Find Argos products matching a style description.
    
    Args:
        style_keywords: Keywords like "warm", "spicy", "romantic", "fresh"
    
    Returns:
        Formatted string with matching products
    """
    data = load_products()
    products = data.get("products", [])
    keywords = style_keywords.lower().split()
    
    matches = []
    for p in products:
        # Skip accessories
        if "Accessories" in p.get("collection", ""):
            continue
            
        style = p.get("style", "").lower()
        best_for = p.get("best_for", "").lower()
        description = p.get("description", "").lower()
        
        # Check if any keyword matches
        score = 0
        for kw in keywords:
            if kw in style:
                score += 3
            if kw in best_for:
                score += 2
            if kw in description:
                score += 1
        
        if score > 0:
            matches.append((score, p))
    
    # Sort by score descending
    matches.sort(key=lambda x: x[0], reverse=True)
    
    if not matches:
        return f"No products found matching: {style_keywords}"
    
    output = f"## Argos Products Matching: {style_keywords}\n\n"
    for score, p in matches[:5]:  # Top 5 matches
        output += f"### {p.get('short_name', 'Unknown')}\n"
        output += f"- Style: {p.get('style', 'N/A')}\n"
        output += f"- Notes: Top: {p.get('notes', {}).get('top', 'N/A')}\n"
        output += f"- Best For: {p.get('best_for', 'N/A')}\n"
        output += f"- URL: {p.get('website_url', 'N/A')}\n\n"
    
    return output


def get_products_by_season(season: str) -> str:
    """
    Find Argos products suitable for a specific season.
    
    Args:
        season: "winter", "summer", "spring", "fall", or "all"
    
    Returns:
        Formatted string with seasonal product recommendations
    """
    data = load_products()
    products = data.get("products", [])
    season_lower = season.lower()
    
    # Season keyword mapping
    season_map = {
        "winter": ["winter", "fall", "cold", "evening", "cozy", "warm", "spicy"],
        "summer": ["summer", "spring", "fresh", "light", "daytime", "aquatic"],
        "spring": ["spring", "floral", "fresh", "light", "daytime"],
        "fall": ["fall", "autumn", "warm", "spicy", "evening", "woody"],
    }
    
    keywords = season_map.get(season_lower, [])
    if not keywords:
        keywords = [season_lower]
    
    matches = []
    for p in products:
        if "Accessories" in p.get("collection", ""):
            continue
            
        best_for = p.get("best_for", "").lower()
        style = p.get("style", "").lower()
        
        score = 0
        for kw in keywords:
            if kw in best_for:
                score += 2
            if kw in style:
                score += 1
        
        if score > 0:
            matches.append((score, p))
    
    matches.sort(key=lambda x: x[0], reverse=True)
    
    if not matches:
        return f"No products found for season: {season}"
    
    output = f"## Argos Products for {season.title()}\n\n"
    for score, p in matches[:5]:
        output += f"### {p.get('short_name', 'Unknown')}\n"
        output += f"- Style: {p.get('style', 'N/A')}\n"
        output += f"- Best For: {p.get('best_for', 'N/A')}\n"
        output += f"- URL: {p.get('website_url', 'N/A')}\n\n"
    
    return output


def get_products_for_occasion(occasion: str) -> str:
    """
    Find Argos products for a specific occasion.
    
    Args:
        occasion: "date night", "formal", "office", "casual", "wedding"
    
    Returns:
        Formatted string with occasion-based recommendations
    """
    data = load_products()
    products = data.get("products", [])
    occasion_lower = occasion.lower()
    
    # Occasion keyword mapping
    occasion_map = {
        "date night": ["romantic", "evening", "sensual", "intimate", "seductive"],
        "formal": ["formal", "elegant", "sophisticated", "evening", "special events"],
        "office": ["daily", "clean", "refined", "daytime", "subtle"],
        "casual": ["daily", "relaxed", "fresh", "versatile", "everyday"],
        "wedding": ["elegant", "romantic", "special", "celebrations", "formal"],
        "gift": ["luxurious", "opulent", "special", "elegant", "signature"],
    }
    
    keywords = occasion_map.get(occasion_lower, [occasion_lower])
    
    matches = []
    for p in products:
        if "Accessories" in p.get("collection", ""):
            continue
            
        best_for = p.get("best_for", "").lower()
        style = p.get("style", "").lower()
        description = p.get("description", "").lower()
        
        score = 0
        for kw in keywords:
            if kw in best_for:
                score += 3
            if kw in style:
                score += 2
            if kw in description:
                score += 1
        
        if score > 0:
            matches.append((score, p))
    
    matches.sort(key=lambda x: x[0], reverse=True)
    
    if not matches:
        return f"No products found for occasion: {occasion}"
    
    output = f"## Argos Products for {occasion.title()}\n\n"
    for score, p in matches[:4]:
        output += f"### {p.get('short_name', 'Unknown')}\n"
        output += f"- Collection: {p.get('collection', 'N/A')}\n"
        output += f"- Style: {p.get('style', 'N/A')}\n"
        output += f"- Notes:\n"
        notes = p.get('notes', {})
        output += f"  - Top: {notes.get('top', 'N/A')}\n"
        output += f"  - Heart: {notes.get('middle', 'N/A')}\n"
        output += f"  - Base: {notes.get('base', 'N/A')}\n"
        output += f"- Price: {p.get('size_price', 'N/A')}\n"
        output += f"- URL: {p.get('website_url', 'N/A')}\n\n"
    
    return output


def get_product_details(product_name: str) -> str:
    """
    Get detailed information about a specific Argos product.
    
    Args:
        product_name: Full or partial name of the product
    
    Returns:
        Detailed product information
    """
    data = load_products()
    products = data.get("products", [])
    search_name = product_name.lower()
    
    for p in products:
        short_name = p.get("short_name", "").lower()
        full_name = p.get("fragrance_name", "").lower()
        
        if search_name in short_name or search_name in full_name:
            notes = p.get('notes', {})
            
            output = f"## {p.get('fragrance_name', 'Unknown')}\n\n"
            output += f"**Collection:** {p.get('collection', 'N/A')}\n\n"
            output += f"**Style:** {p.get('style', 'N/A')}\n\n"
            output += f"**Fragrance Notes:**\n"
            output += f"- Top Notes: {notes.get('top', 'N/A')}\n"
            output += f"- Heart Notes: {notes.get('middle', 'N/A')}\n"
            output += f"- Base Notes: {notes.get('base', 'N/A')}\n\n"
            output += f"**Best For:** {p.get('best_for', 'N/A')}\n\n"
            output += f"**Price:** {p.get('size_price', 'N/A')}\n\n"
            output += f"**Description:**\n{p.get('description', 'N/A')[:500]}...\n\n"
            output += f"**URL:** {p.get('website_url', 'N/A')}\n"
            output += f"**Hashtags:** {p.get('hashtags', 'N/A')}\n"
            
            return output
    
    return f"Product not found: {product_name}"


def get_brand_info() -> str:
    """
    Get Argos Fragrances brand information.
    
    Returns:
        Brand information string
    """
    data = load_products()
    brand = data.get("brand", {})
    
    output = "## About Argos Fragrances\n\n"
    output += f"**Name:** {brand.get('name', 'Argos Fragrances')}\n"
    output += f"**Origin:** {brand.get('origin', 'USA')}\n"
    output += f"**Theme:** {brand.get('theme', 'Greek and Roman Mythology')}\n"
    output += f"**Tagline:** {brand.get('tagline', 'Luxury niche perfumes')}\n"
    output += f"**Website:** {brand.get('website', 'https://argosfragrances.com')}\n"
    output += f"**Shipping:** {brand.get('shipping', 'Global shipping available')}\n"
    
    return output


# Test when run directly
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING ARGOS PRODUCTS TOOL")
    print("=" * 60)
    
    # Test 1: Brand info
    print("\n📌 Test 1: Brand Info")
    print("-" * 40)
    print(get_brand_info())
    
    # Test 2: Products by style
    print("\n📌 Test 2: Products by Style (warm spicy)")
    print("-" * 40)
    print(get_products_by_style("warm spicy"))
    
    # Test 3: Products by season
    print("\n📌 Test 3: Products for Winter")
    print("-" * 40)
    print(get_products_by_season("winter"))
    
    # Test 4: Products for occasion
    print("\n📌 Test 4: Products for Date Night")
    print("-" * 40)
    print(get_products_for_occasion("date night"))
    
    print("\n" + "=" * 60)
    print("✅ Argos Products Tool Ready!")
    print("=" * 60)