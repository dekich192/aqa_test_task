import pytest
import os
from playwright.sync_api import Page, BrowserContext, Browser
from config.config import Config


@pytest.fixture(scope="function")
def page(page: Page):
    """Setup and teardown for each test"""
    # Set default timeout
    page.set_default_timeout(Config.PLAYWRIGHT_TIMEOUT)
    
    # Setup error handling
    def handle_error(error):
        print(f"Page error: {error}")
    
    page.on("pageerror", handle_error)
    
    yield page
    
    # Cleanup
    page.close()


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "java_script_enabled": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments"""
    return {
        **browser_type_launch_args,
        "headless": not Config.HEADED,
        "slow_mo": 100,  # Slow down for better visibility in headed mode
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to take screenshots on test failure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            page = item.funcargs.get("page")
            if page:
                if not os.path.exists("screenshots"):
                    os.makedirs("screenshots")
                
                screenshot_name = f"{item.name}_failure"
                screenshot_path = f"screenshots/{screenshot_name}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                
                # Attach to Allure report
                import allure
                allure.attach.file(
                    screenshot_path,
                    name=f"Failure Screenshot: {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")


@pytest.fixture(scope="session", autouse=True)
def setup_allure_environment():
    """Setup Allure environment properties"""
    if not os.path.exists("allure-results"):
        os.makedirs("allure-results")
    
    # Create environment properties file for Allure
    env_props = """Browser=Chromium
BaseURL={}
Headed={}
Timeout={}
Python Version=3.10+
""".format(Config.BASE_URL, Config.HEADED, Config.TIMEOUT)
    
    with open("allure-results/environment.properties", "w", encoding="utf-8") as f:
        f.write(env_props)
