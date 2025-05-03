import re
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# Fetch page content using requests for static content
def fetch_static_content(url):
    """Fetch page content using requests."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[Error fetching static] {url} - {e}")
        return None


# Extract likely cookie banner text from static HTML
def extract_cookie_banner(html):
    """Extract likely cookie banner text from static HTML."""
    if not html:
        return "N/A"

    soup = BeautifulSoup(html, "html.parser")
    keywords = ['cookie', 'consent', 'privacy', 'gdpr', 'data']
    banner_texts = []

    # Search by class or id for potential cookie banners
    for tag in soup.find_all(["div", "section", "footer", "span", "p"]):
        attrs = ' '.join(str(tag.get(attr, "")).lower() for attr in ["class", "id"])
        if any(kw in attrs for kw in keywords):
            text = tag.get_text(strip=True)
            if 30 < len(text) < 1000:
                banner_texts.append(text)

    # Fallback: plain keyword text search
    if not banner_texts:
        for tag in soup.find_all(text=True):
            if any(kw in tag.lower() for kw in keywords):
                clean_text = tag.strip()
                if 30 < len(clean_text) < 1000:
                    banner_texts.append(clean_text)

    return " ".join(banner_texts) if banner_texts else "N/A"


# Use Selenium to render dynamic content and extract cookie banner
def extract_cookie_banner_dynamic(url, save_screenshot=False):
    """Use Selenium to render dynamic content and extract cookie banner."""
    # Selenium options setup
    options = Options()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    # Install and configure ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load

        # Scroll to bottom to load all dynamic content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load

        if save_screenshot:
            driver.save_screenshot("debug_screenshot.png")

        # Fetch page source after dynamic content is loaded
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Try clicking any consent buttons if available
        buttons = driver.find_elements(By.XPATH, "//button | //a")
        for btn in buttons:
            try:
                btn_text = btn.text.lower()
                if any(x in btn_text for x in ['accept', 'agree', 'consent']):
                    print(f"Clicking button: {btn.text}")
                    btn.click()
                    time.sleep(1)
                    break
            except Exception:
                continue

        # Extract the cookie banner after clicking the consent button
        return extract_cookie_banner(driver.page_source)
    except Exception as e:
        print(f"[Error fetching dynamic content] {url} - {e}")
        return "N/A"
    finally:
        driver.quit()


# Enhanced Privacy Policy link extraction
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_privacy_policy_link(html, base_url):
    """Improved method to find the privacy policy URL from static or dynamic content."""
    
    if not html:
        return "N/A"

    soup = BeautifulSoup(html, "html.parser")
    candidate_links = []

    # Define keywords related to privacy policy
    keywords = ["privacy", "privacy policy", "data protection", "gdpr", "your privacy", "/privacy", "terms"]

    # 1. Search for links in anchor tags (<a>) with privacy-related keywords in href or text
    for a_tag in soup.find_all("a", href=True):
        text = (a_tag.text or "").strip().lower()
        href = a_tag["href"].strip().lower()

        # Combine text and href for matching
        combined = text + " " + href

        # Check if any keywords are in the combined text or href
        if any(kw in combined for kw in keywords):
            full_url = urljoin(base_url, a_tag["href"])  # Absolute URL in case it's relative
            candidate_links.append((text, full_url))

    # 2. If no link found, search for privacy-related terms in meta tags (sometimes defined in meta data)
    if not candidate_links:
        for meta_tag in soup.find_all("meta", attrs={"name": True, "content": True}):
            content = meta_tag.get("content", "").lower()
            if any(kw in content for kw in keywords):
                # If meta tag has privacy-related content, add it as a candidate
                candidate_links.append(("privacy-related meta tag", content))
    
    # 3. Fallback to footer or other sections (e.g., check div with "footer" class)
    if not candidate_links:
        footer = soup.find("footer")
        if footer:
            for a_tag in footer.find_all("a", href=True):
                text = (a_tag.text or "").strip().lower()
                href = a_tag["href"].strip().lower()
                combined = text + " " + href
                if any(kw in combined for kw in keywords):
                    full_url = urljoin(base_url, a_tag["href"])
                    candidate_links.append((text, full_url))

    # 4. If still no link found, we can check common "privacy" page links, e.g., /privacy or /terms
    if not candidate_links:
        possible_urls = [
            urljoin(base_url, "/privacy"),
            urljoin(base_url, "/terms"),
            urljoin(base_url, "/terms-and-conditions")
        ]
        candidate_links.extend([(url, url) for url in possible_urls])

    # If candidate links exist, return the first privacy-related URL found
    if candidate_links:
        return candidate_links[0][1]

    return "N/A"

# Wrapper to handle both static and dynamic content
def get_privacy_policy(url):
    """Fetch the privacy policy link, handling static and dynamic content."""
    # Try static content first
    html = fetch_static_content(url)
    privacy_policy = find_privacy_policy_link(html, url) if html else "N/A"

    # If static content doesn't have it, try dynamic content
    if privacy_policy == "N/A":
        print(f"[Using Selenium] Trying dynamic content for {url}")
        privacy_policy = extract_cookie_banner_dynamic(url)

    return privacy_policy


