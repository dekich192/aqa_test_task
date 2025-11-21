import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://www.effective-mobile.ru")
    BROWSER = os.getenv("BROWSER", "chromium")
    HEADED = os.getenv("HEADED", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    
    # Playwright settings
    PLAYWRIGHT_TIMEOUT = TIMEOUT
    NAVIGATION_TIMEOUT = TIMEOUT
    
    # Test settings
    RETRY_COUNT = 2
    SCREENSHOT_ON_FAILURE = True
