"""
Argos Content System - Settings Configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Model Selection
    RESEARCH_AGENT_MODEL: str = os.getenv("RESEARCH_AGENT_MODEL", "gpt-4o-mini")
    CONTENT_AGENT_MODEL: str = os.getenv("CONTENT_AGENT_MODEL", "gpt-4o")
    VERIFY_AGENT_MODEL: str = os.getenv("VERIFY_AGENT_MODEL", "gpt-4o-mini")
    
    # Application Settings
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    PRODUCTS_FILE: str = os.path.join(DATA_DIR, "argos_products.json")
    
    @classmethod
    def validate(cls) -> bool:
        """Check if API keys are configured."""
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            print("❌ ERROR: No API key found!")
            print("   Please add your OPENAI_API_KEY in the .env file")
            return False
        print("✅ API Key found!")
        return True
    
    @classmethod
    def show_config(cls):
        """Display current configuration."""
        print("=" * 50)
        print("ARGOS CONTENT SYSTEM - CONFIGURATION")
        print("=" * 50)
        
        # Show API status (not the actual key)
        if cls.OPENAI_API_KEY:
            print(f"OpenAI API Key: ✅ Configured")
        else:
            print(f"OpenAI API Key: ❌ Not set")
            
        if cls.ANTHROPIC_API_KEY:
            print(f"Claude API Key: ✅ Configured")
        else:
            print(f"Claude API Key: ❌ Not set")
        
        print("-" * 50)
        print(f"Research Model: {cls.RESEARCH_AGENT_MODEL}")
        print(f"Content Model: {cls.CONTENT_AGENT_MODEL}")
        print(f"Verify Model: {cls.VERIFY_AGENT_MODEL}")
        print("=" * 50)


# Run when file is executed directly
if __name__ == "__main__":
    Settings.show_config()
    Settings.validate()