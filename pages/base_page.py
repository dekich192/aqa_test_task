import pytest
from playwright.sync_api import Page, expect
from config.config import Config


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = Config.BASE_URL
        self.timeout = Config.PLAYWRIGHT_TIMEOUT
    
    def navigate_to(self, url: str = None):
        """Navigate to a specific URL"""
        target_url = url if url else self.base_url
        self.page.goto(target_url, timeout=self.timeout)
        self.page.wait_for_load_state("networkidle", timeout=self.timeout)
    
    def wait_for_element(self, locator, timeout: int = None):
        """Wait for element to be visible"""
        timeout = timeout or self.timeout
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)
    
    def click_element(self, locator, timeout: int = None):
        """Click on element with wait"""
        timeout = timeout or self.timeout
        self.wait_for_element(locator, timeout)
        self.page.locator(locator).click(timeout=timeout)
    
    def get_text(self, locator, timeout: int = None):
        """Get text from element"""
        timeout = timeout or self.timeout
        self.wait_for_element(locator, timeout)
        return self.page.locator(locator).text_content(timeout=timeout)
    
    def is_element_visible(self, locator, timeout: int = None):
        """Check if element is visible"""
        timeout = timeout or self.timeout
        try:
            self.page.locator(locator).wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False
    
    def verify_url(self, expected_url: str):
        """Verify current URL matches expected"""
        current_url = self.page.url
        assert expected_url in current_url, f"Expected URL '{expected_url}' not found in '{current_url}'"
    
    def take_screenshot(self, name: str):
        """Take screenshot for debugging"""
        self.page.screenshot(path=f"screenshots/{name}.png")
