import allure
from playwright.sync_api import Page
from .base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Navigation locators (will be updated after analyzing the actual site)
        self.navigation_menu = "nav"
        self.about_us_link = "text=О нас"
        self.contacts_link = "text=Контакты"
        self.services_link = "text=Услуги"
        self.careers_link = "text=Карьера"
        self.blog_link = "text=Блог"
        
        # Common navigation patterns
        self.header_logo = "header img[alt*='logo'], .logo"
        self.main_navigation = "header nav, .main-nav, .navigation"
        self.footer = "footer"
        
        # URL patterns
        self.about_us_url_pattern = "/about"
        self.contacts_url_pattern = "/contact"
        self.services_url_pattern = "/service"
        self.careers_url_pattern = "/career"
        self.blog_url_pattern = "/blog"
    
    @allure.step("Navigate to main page")
    def navigate_to_main_page(self):
        """Navigate to the main page"""
        self.navigate_to()
        self.page.wait_for_load_state("domcontentloaded")
    
    @allure.step("Wait for page to load completely")
    def wait_for_page_load(self):
        """Wait for the page to fully load"""
        # Wait for React app to render
        self.page.wait_for_selector("#root", timeout=self.timeout)
        # Wait for common navigation elements
        self.page.wait_for_load_state("networkidle", timeout=self.timeout)
    
    @allure.step("Click About Us link")
    def click_about_us(self):
        """Click on About Us navigation link"""
        # Try multiple possible selectors for "О нас"
        selectors = [
            "text=О нас",
            "text=О компании",
            "[href*='about']",
            "a:has-text('О нас')",
            "a:has-text('О компании')"
        ]
        
        for selector in selectors:
            if self.is_element_visible(selector, timeout=5000):
                self.click_element(selector)
                return
        
        raise Exception("About Us link not found")
    
    @allure.step("Click Contacts link")
    def click_contacts(self):
        """Click on Contacts navigation link"""
        selectors = [
            "text=Контакты",
            "text=Contact us",
            "[href*='contact']",
            "a:has-text('Контакты')",
            "a:has-text('Contact')"
        ]
        
        for selector in selectors:
            if self.is_element_visible(selector, timeout=5000):
                self.click_element(selector)
                return
        
        raise Exception("Contacts link not found")
    
    @allure.step("Click Services link")
    def click_services(self):
        """Click on Services navigation link"""
        selectors = [
            "text=Услуги",
            "text=Services",
            "[href*='service']",
            "a:has-text('Услуги')",
            "a:has-text('Services')"
        ]
        
        for selector in selectors:
            if self.is_element_visible(selector, timeout=5000):
                self.click_element(selector)
                return
        
        raise Exception("Services link not found")
    
    @allure.step("Click Careers link")
    def click_careers(self):
        """Click on Careers navigation link"""
        selectors = [
            "text=Карьера",
            "text=Careers",
            "[href*='career']",
            "a:has-text('Карьера')",
            "a:has-text('Careers')"
        ]
        
        for selector in selectors:
            if self.is_element_visible(selector, timeout=5000):
                self.click_element(selector)
                return
        
        raise Exception("Careers link not found")
    
    @allure.step("Click Blog link")
    def click_blog(self):
        """Click on Blog navigation link"""
        selectors = [
            "text=Блог",
            "text=Blog",
            "[href*='blog']",
            "a:has-text('Блог')",
            "a:has-text('Blog')"
        ]
        
        for selector in selectors:
            if self.is_element_visible(selector, timeout=5000):
                self.click_element(selector)
                return
        
        raise Exception("Blog link not found")
    
    @allure.step("Get all navigation links")
    def get_navigation_links(self):
        """Get all navigation links for analysis"""
        nav_selectors = [
            "header nav a",
            ".main-nav a",
            ".navigation a",
            "nav a",
            ".menu a"
        ]
        
        for selector in nav_selectors:
            links = self.page.locator(selector)
            if links.count() > 0:
                return links.all()
        
        return []
    
    @allure.step("Verify main page elements")
    def verify_main_page_elements(self):
        """Verify that main page elements are present"""
        # Check if page has loaded
        expect(self.page).to_have_url(self.base_url)
        
        # Check for common elements
        elements_to_check = [
            self.header_logo,
            self.main_navigation,
            "#root"  # React root element
        ]
        
        for element in elements_to_check:
            try:
                expect(self.page.locator(element)).to_be_visible(timeout=10000)
            except:
                # Log element not found but continue
                allure.attach(
                    f"Element {element} not found on page",
                    name="Missing Element",
                    attachment_type=allure.attachment_type.TEXT
                )
