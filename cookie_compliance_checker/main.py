import requests
import pandas as pd
import os
from scraper import (
    fetch_static_content,
    extract_cookie_banner,
    find_privacy_policy_link,
    extract_cookie_banner_dynamic
)
from analyzer import clean_text, compute_similarity

# List of websites to check
websites = [
    "https://www.bbc.com",
    "https://www.kaggle.com",
    "https://www.mozilla.org",
    "https://www.bripublish.com/bookwriting",
]

data = []

def scrape_website(url):
    """Fetch and analyze website's cookie banner and privacy policy."""
    # Fetch static HTML content
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text
    except requests.exceptions.RequestException as e:
        print(f"[Error fetching static] {url} - {e}")
        html = None

    # Try static banner extraction first
    banner = extract_cookie_banner(html) if html else "N/A"

    # Fallback to dynamic banner (using Selenium) if static extraction fails
    if banner == "N/A" and html is None:
        try:
            print(f"[Using Selenium] Extracting cookie banner from {url}")
            banner = extract_cookie_banner_dynamic(url, save_screenshot=True)
        except Exception as e:
            print(f"[Error with Selenium] {url} - {e}")
            banner = "N/A"

    # Find privacy policy URL
    policy_url = find_privacy_policy_link(html, url) if html else "N/A"

    # Try fetching policy text if URL exists
    if policy_url and policy_url != "N/A":
        policy_html = fetch_static_content(policy_url)
        policy_clean = clean_text(policy_html) if policy_html else ""
    else:
        policy_clean = ""

    # Clean the banner text
    banner_clean = clean_text(banner) if banner != "N/A" else ""

    # Compute similarity only if both banner and policy text are non-empty
    similarity = 0.0
    if banner_clean and policy_clean:
        similarity = compute_similarity(banner_clean, policy_clean)

    # Return the results
    return banner, policy_url, round(similarity, 3)


# Loop through websites
for url in websites:
    print(f"\nChecking {url}")
    banner, policy_url, similarity = scrape_website(url)

    # Append the results to the data list
    data.append({
        "Website": url,
        "CookieBanner": banner,
        "PrivacyPolicyURL": policy_url,
        "SimilarityScore": similarity
    })

# Save report to a CSV file
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(data)
df.to_csv("data/reports.csv", index=False)
print("\n✅ Report saved to data/reports.csv")
