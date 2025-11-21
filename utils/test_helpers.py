import os
import allure
import pytest
from playwright.sync_api import Page
from typing import Dict, List


def take_screenshot_on_failure(page: Page, test_name: str):
    """Take screenshot when test fails"""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    
    screenshot_path = f"screenshots/{test_name}_failure.png"
    page.screenshot(path=screenshot_path, full_page=True)
    
    allure.attach.file(
        screenshot_path,
        name=f"Screenshot: {test_name}",
        attachment_type=allure.attachment_type.PNG
    )


def log_page_info(page: Page, test_name: str):
    """Log page information for debugging"""
    page_info = {
        "url": page.url,
        "title": page.title(),
        "content": page.content()[:1000] + "..." if len(page.content()) > 1000 else page.content()
    }
    
    allure.attach(
        str(page_info),
        name=f"Page Info: {test_name}",
        attachment_type=allure.attachment_type.TEXT
    )


def wait_for_network_idle(page: Page, timeout: int = 30000):
    """Wait for network to be idle"""
    page.wait_for_load_state("networkidle", timeout=timeout)


def get_element_text_safe(page: Page, selector: str, timeout: int = 10000) -> str:
    """Safely get element text with timeout"""
    try:
        element = page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element.text_content(timeout=timeout)
    except:
        return ""


def verify_url_contains(page: Page, expected_pattern: str):
    """Verify URL contains expected pattern"""
    current_url = page.url
    assert expected_pattern in current_url, f"URL '{current_url}' does not contain '{expected_pattern}'"


def attach_html_content(page: Page, name: str = "Page HTML"):
    """Attach HTML content to Allure report"""
    allure.attach(
        page.content(),
        name=name,
        attachment_type=allure.attachment_type.HTML
    )
