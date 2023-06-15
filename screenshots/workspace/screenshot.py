import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
# Import the ScreenshotManager class from another module
from screenshot_manager import ScreenshotManager

# Create an instance of ScreenshotManager
screenshot_manager = ScreenshotManager()


class Screenshot:
    def __init__(self, screenshot_url: str, image_bytes: bytes, width: int, height: int):
        self.url = screenshot_url
        self.image = image_bytes
        self.width = width
        self.height = height


class Screenshotter:
    def __init__(self):
        self.driver = self._create_driver()

    def take_screenshot(self, screenshot_url: str) -> Screenshot:
        self.driver.get(screenshot_url)
        self._click_hamburger_menu()
        self._scroll_to_bottom()
        self.driver.get_screenshot_as_png()
        width = self.driver.execute_script('return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);')
        height = self.driver.execute_script('return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);')

        return Screenshot(url, image, width, height)

    def _create_driver(self) -> WebDriver:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--start-maximized')
        options.add_argument('--window-size=1440,900')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--disable-web-security')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')

        driver = webdriver.Chrome(options=options)
        return driver

    def _remove_overlays(self) -> None:
        overlays = self.driver.find_elements_by_css_selector('[class*="modal"], [class*="overlay"], [class*="popup"], [class*="dialog"], [class*="lightbox"], [class*="tooltip"], [class*="banner"], [class*="notification"], [class*="cookie"], [class*="privacy"], [class*="gdpr"], [class*="consent"], [class*="agegate"], [class*="interstitial"], [class*="curtain"]')
        for overlay in overlays:
            self.driver.execute_script("arguments[0].style.display='none';", overlay)

    def _remove_fixed_elements(self) -> None:
        elements = self.driver.find_elements_by_css_selector('[style*="position: fixed"]')
        for element in elements:
            self.driver.execute_script("arguments[0].style.position='static';", element)

    def _remove_trays(self) -> None:
        trays = self.driver.find_elements_by_css_selector('[class*="tray"], [class*="preview"]')
        for tray in trays:
            self.driver.execute_script("arguments[0].remove();", tray)

    def _remove_iframes(self) -> None:
        iframes = self.driver.find_elements_by_tag_name('iframe')
        for iframe in iframes:
            self.driver.execute_script("arguments[0].style.outline='2px solid black';", iframe)

    def _wait_for_animations(self) -> None:
        self.driver.execute_script('''
            const elements = document.querySelectorAll('*');
            for (const element of elements) {
                const computedStyle = getComputedStyle(element);
                const animationDuration = computedStyle.animationDuration;
                const transitionDuration = computedStyle.transitionDuration;
                const totalDuration = Math.max(parseFloat(animationDuration), parseFloat(transitionDuration));
                if (totalDuration > 0) {
                    element.style.animationDuration = '0s';
                    element.style.transitionDuration = '0s';
                }
            }
        ''')

    def _click_expand_buttons(self) -> None:
        buttons = self.driver.find_elements_by_css_selector('[class*="expand"], [class*="toggle"], [class*="show-more"], [class*="load-more"]')
        for button in buttons:
            self.driver.execute_script("arguments[0].click();", button)

    def _click_hamburger_menu(self) -> None:
        hamburger_menu = self.driver.find_element_by_css_selector('[class*="hamburger"], [class*="menu-button"], [class*="nav-toggle"]')
        if hamburger_menu:
            self.driver.execute_script("arguments[0].click();", hamburger_menu)
            menu_item = self.driver.find_element_by_xpath('//li[1]')  # Replace with correct XPath for hovering over the first menu item
            action_chains = ActionChains(self.driver)
            action_chains.move_to_element(menu_item).perform()

    def _scroll_to_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# Create an instance of ScreenshotManager
screenshot_manager = ScreenshotManager()

# Example usage
url = "https://www.example.com"
screenshot = screenshot_manager.take_screenshot(url)

# Save the screenshot as an image file
image = Image.open(io.BytesIO(screenshot.image))
image.save("screenshot.png")
