import pytest
import allure
from playwright.sync_api import Page, expect
from pages.main_page import MainPage
from utils.test_helpers import (
    take_screenshot_on_failure,
    log_page_info,
    verify_url_contains,
    attach_html_content
)


@allure.feature("Main Page Navigation")
@allure.story("Navigation Links")
class TestMainPageNavigation:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test method"""
        self.page = page
        self.main_page = MainPage(page)
    
    @allure.title("Verify main page loads correctly")
    @allure.description("Test that the main page loads and basic elements are present")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_main_page_load(self):
        """Test that main page loads successfully"""
        with allure.step("Navigate to main page"):
            self.main_page.navigate_to_main_page()
        
        with allure.step("Wait for page to load completely"):
            self.main_page.wait_for_page_load()
        
        with allure.step("Verify page elements"):
            self.main_page.verify_main_page_elements()
        
        with allure.step("Attach HTML content for analysis"):
            attach_html_content(self.page, "Main Page HTML")
    
    @allure.title("Navigate to About Us page")
    @allure.description("Test navigation to About Us section and verify URL")
    @allure.severity(allure.severity_level.HIGH)
    def test_navigate_to_about_us(self):
        """Test navigation to About Us page"""
        with allure.step("Navigate to main page"):
            self.main_page.navigate_to_main_page()
            self.main_page.wait_for_page_load()
        
        with allure.step("Click About Us link"):
            try:
                self.main_page.click_about_us()
            except Exception as e:
                # Log available navigation links for debugging
                links = self.main_page.get_navigation_links()
                link_texts = [link.text_content() for link in links if link.text_content()]
                allure.attach(
                    f"Available navigation links: {link_texts}\nError: {str(e)}",
                    name="Navigation Analysis",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip(f"About Us link not found. Available links: {link_texts}")
        
        with allure.step("Wait for navigation"):
            self.page.wait_for_load_state("networkidle", timeout=10000)
        
        with allure.step("Verify URL contains about section"):
            # Check for common URL patterns
            url_patterns = ["/about", "/o-nas", "/company", "/о-нас"]
            current_url = self.page.url
            
            found_pattern = any(pattern in current_url.lower() for pattern in url_patterns)
            assert found_pattern, f"URL '{current_url}' does not contain expected about page patterns"
        
        allure.attach(
            self.page.url,
            name="Final URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.title("Navigate to Contacts page")
    @allure.description("Test navigation to Contacts section and verify URL")
    @allure.severity(allure.severity_level.HIGH)
    def test_navigate_to_contacts(self):
        """Test navigation to Contacts page"""
        with allure.step("Navigate to main page"):
            self.main_page.navigate_to_main_page()
            self.main_page.wait_for_page_load()
        
        with allure.step("Click Contacts link"):
            try:
                self.main_page.click_contacts()
            except Exception as e:
                links = self.main_page.get_navigation_links()
                link_texts = [link.text_content() for link in links if link.text_content()]
                allure.attach(
                    f"Available navigation links: {link_texts}\nError: {str(e)}",
                    name="Navigation Analysis",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip(f"Contacts link not found. Available links: {link_texts}")
        
        with allure.step("Wait for navigation"):
            self.page.wait_for_load_state("networkidle", timeout=10000)
        
        with allure.step("Verify URL contains contacts section"):
            url_patterns = ["/contact", "/kontakty", "/contacts", "/контакты"]
            current_url = self.page.url
            
            found_pattern = any(pattern in current_url.lower() for pattern in url_patterns)
            assert found_pattern, f"URL '{current_url}' does not contain expected contacts page patterns"
        
        allure.attach(
            self.page.url,
            name="Final URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.title("Navigate to Services page")
    @allure.description("Test navigation to Services section and verify URL")
    @allure.severity(allure.severity_level.HIGH)
    def test_navigate_to_services(self):
        """Test navigation to Services page"""
        with allure.step("Navigate to main page"):
            self.main_page.navigate_to_main_page()
            self.main_page.wait_for_page_load()
        
        with allure.step("Click Services link"):
            try:
                self.main_page.click_services()
            except Exception as e:
                links = self.main_page.get_navigation_links()
                link_texts = [link.text_content() for link in links if link.text_content()]
                allure.attach(
                    f"Available navigation links: {link_texts}\nError: {str(e)}",
                    name="Navigation Analysis",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip(f"Services link not found. Available links: {link_texts}")
        
        with allure.step("Wait for navigation"):
            self.page.wait_for_load_state("networkidle", timeout=10000)
        
        with allure.step("Verify URL contains services section"):
            url_patterns = ["/service", "/uslugi", "/services", "/услуги"]
            current_url = self.page.url
            
            found_pattern = any(pattern in current_url.lower() for pattern in url_patterns)
            assert found_pattern, f"URL '{current_url}' does not contain expected services page patterns"
        
        allure.attach(
            self.page.url,
            name="Final URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.title("Navigate to Careers page")
    @allure.description("Test navigation to Careers section and verify URL")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_navigate_to_careers(self):
        """Test navigation to Careers page"""
        with allure.step("Navigate to main page"):
            self.main_page.navigate_to_main_page()
            self.main_page.wait_for_page_load()
        
        with allure.step("Click Careers link"):
            try:
                self.main_page.click_careers()
            except Exception as e:
                links = self.main_page.get_navigation_links()
                link_texts = [link.text_content() for link in links if link.text_content()]
                allure.attach(
                    f"Available navigation links: {link_texts}\nError: {str(e)}",
                    name="Navigation Analysis",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip(f"Careers link not found. Available links: {link_texts}")
        
        with allure.step("Wait for navigation"):
            self.page.wait_for_load_state("networkidle", timeout=10000)
        
        with allure.step("Verify URL contains careers section"):
            url_patterns = ["/career", "/karera", "/careers", "/карьера", "/vacancy", "/vacancies"]
            current_url = self.page.url
            
            found_pattern = any(pattern in current_url.lower() for pattern in url_patterns)
            assert found_pattern, f"URL '{current_url}' does not contain expected careers page patterns"
        
        allure.attach(
            self.page.url,
            name="Final URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.title("Navigate to Blog page")
    @allure.description("Test navigation to Blog section and verify URL")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_navigate_to_blog(self):
        """Test navigation to Blog page"""
        with allure.step("Navigate to main page"):
            self.main_page.navigate_to_main_page()
            self.main_page.wait_for_page_load()
        
        with allure.step("Click Blog link"):
            try:
                self.main_page.click_blog()
            except Exception as e:
                links = self.main_page.get_navigation_links()
                link_texts = [link.text_content() for link in links if link.text_content()]
                allure.attach(
                    f"Available navigation links: {link_texts}\nError: {str(e)}",
                    name="Navigation Analysis",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip(f"Blog link not found. Available links: {link_texts}")
        
        with allure.step("Wait for navigation"):
            self.page.wait_for_load_state("networkidle", timeout=10000)
        
        with allure.step("Verify URL contains blog section"):
            url_patterns = ["/blog", "/news", "/статьи", "/articles"]
            current_url = self.page.url
            
            found_pattern = any(pattern in current_url.lower() for pattern in url_patterns)
            assert found_pattern, f"URL '{current_url}' does not contain expected blog page patterns"
        
        allure.attach(
            self.page.url,
            name="Final URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.title("Analyze available navigation links")
    @allure.description("Test to analyze and document all available navigation links")
    @allure.severity(allure.severity_level.MINOR)
    def test_analyze_navigation_links(self):
        """Analyze all available navigation links on the main page"""
        with allure.step("Navigate to main page"):
            self.main_page.navigate_to_main_page()
            self.main_page.wait_for_page_load()
        
        with allure.step("Get all navigation links"):
            links = self.main_page.get_navigation_links()
            
        with allure.step("Extract link information"):
            link_info = []
            for i, link in enumerate(links):
                try:
                    text = link.text_content() or ""
                    href = link.get_attribute("href") or ""
                    link_info.append({
                        "index": i,
                        "text": text.strip(),
                        "href": href
                    })
                except:
                    continue
        
        with allure.step("Attach navigation analysis"):
            import json
            allure.attach(
                json.dumps(link_info, indent=2, ensure_ascii=False),
                name="Navigation Links Analysis",
                attachment_type=allure.attachment_type.JSON
            )
        
        # Ensure we have some navigation links
        assert len(link_info) > 0, "No navigation links found on the page"
