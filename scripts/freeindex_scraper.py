import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sys import stdout
import logging
from random import uniform
import time
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import nltk
import spacy
from urllib.parse import urlparse, urljoin


EXCLUDED_HREFS = [
    "https://twitter.com",
    "https://www.instagram.com",
    "https://www.youtube.com",
    "https://www.facebook.com",
    "/private/",
    "/",
    "/sitemap",
    "#",
    "/login",
    "/signup",
    "/categories",
    "/getquotes",
    "javascript",
]

# Load spaCy's English model for NER
nlp = spacy.load("en_core_web_sm")

# Load NLTK first names dataset
try:
    first_names = set(
        name.lower() for name in nltk.corpus.names.words("male.txt")
    ) | set(name.lower() for name in nltk.corpus.names.words("female.txt"))
except LookupError:
    nltk.download("names")
    first_names = set(
        name.lower() for name in nltk.corpus.names.words("male.txt")
    ) | set(name.lower() for name in nltk.corpus.names.words("female.txt"))


pattern = re.compile(
    r"\b(?:click|visit|open|link|go to|our)?\s*(?:the\s*)?(website|site|web\s*page)\b"
)

logger = logging.getLogger(__name__)
handler = logging.Handler()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(stdout))


def random_sleep(min_time=2.5, max_time=15):
    time.sleep(uniform(min_time, max_time))


def request_user_agent(url, ua):
    try:
        user_agent = ua.chrome
        headers = {
            "User-Agent": user_agent,
            "Accept-Language": "en-GB,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }
        logger.info("Using UA: %s...", user_agent[:60])
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            logger.info("was successful.")
            return response
        else:
            logger.info("Got status %s", response.status_code)
    except requests.exceptions.RequestException as e:
        logger.warning("Request error: %s", e)


class FreeindexScraper:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Optional: headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    def __init__(self):
        self.base_domain = "freeindex.co.uk"
        self.visited_domains = {self.base_domain}
        self.data = []

    def _handle_consent_dialog(self):
        try:
            dialog = self.driver.find_element(By.CLASS_NAME, "fc-dialog-overlay")
            if dialog:
                # Wait for the consent button to be clickable
                consent_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "fc-button"))
                )

                # Scroll and click via JavaScript to avoid overlays
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", consent_button
                )
                self.driver.execute_script("arguments[0].click();", consent_button)
        except NoSuchElementException:
            logger.info("No dialog box found.")

    def _load_more(self):
        logger.info("Loading full page...")
        load_more_btn = None
        wait = WebDriverWait(self.driver, 5)
        try:
            load_more_btn = self.driver.find_element(By.ID, "load-more-btn")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                load_more_btn,
            )
            load_more_btn = wait.until(EC.element_to_be_clickable(load_more_btn))
            load_more_btn.click()
            return True
        except (NoSuchElementException, ElementNotInteractableException):
            logger.info("No results beyond initial results.")
            return False

    def _extract_redirect_url(self, page_source):
        match = re.search(r"<body>\s*(\{.*\})\s*</body>", page_source, re.DOTALL)
        if match:
            json_text = match.group(1)
            try:
                json_data = json.loads(json_text)
                actual_url = json_data.get("REDIRECT-URL")
                if actual_url:
                    logger.debug(f"Extracted redirect URL: {actual_url}")
                    self.data.append(actual_url)
                    self.visited_domains.add(actual_url.split("/")[2])
                else:
                    logger.debug("No REDIRECT-URL key found in parsed JSON.")
            except json.JSONDecodeError as e:
                logger.debug(f"JSON decode error: {e}")
        else:
            logger.debug("Could not extract JSON from body tag.")

    def _retrieve_profile_links(self):
        logger.info("Retrieving websites from freeindex...")

        profile_links = set()
        listing_names = self.driver.find_elements(By.CLASS_NAME, "listing_name")
        logger.debug("FOUND %s LISTING NAMES.", len(listing_names))
        for listing_name in listing_names:
            profile_link = listing_name.find_element(By.TAG_NAME, "a")
            profile_link = profile_link.get_attribute("href")
            profile_links.add(profile_link)
            logger.debug("PROFILE LINK: %s", profile_link)
        return profile_links

    def _parse_profile_html(self, html):
        soup = BeautifulSoup(html)
        profile_links = soup.find_all("a")
        for link in profile_links:
            href = link.get("href")
            if href:
                logger.debug("HREF: %s", href)
                if not any([href.startswith(e) for e in EXCLUDED_HREFS]):
                    return href

    def _scrape_profiles(self, profile_links):
        websites = set()
        ua = UserAgent()
        for link in profile_links:
            response = request_user_agent(link, ua)

            if response.status_code == 200:
                website = self._parse_profile_html(response.text)
                if website:
                    websites.add(website)
            else:
                logger.warning("RESPONSE INVALID: %s", response.status_code)

        self.data = websites

    def scrape(self, url):
        logger.info("Starting freeindex scrape for URL: %s...", url)
        profile_links = set()
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        self._handle_consent_dialog()
        if url == self.driver.current_url:
            logger.debug("Requested URL matches driver URL.")
        logger.info("Retrieved search url")

        more_links = True
        while more_links:
            profile_links = profile_links.union(self._retrieve_profile_links())
            more_links = self._load_more()
        self._scrape_profiles(profile_links)
        logger.info("Retrieved data: %s", self.data)
        if self.driver:
            self.driver.quit()
        return self.data


# Extract email addresses from a page


def extract_emails(html):
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html)


# Validate names based on first name list from nltk


def validate_probable_names(text):
    name_pattern = r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2}\b"
    regex_matches = re.findall(name_pattern, text)

    valid_names = set()
    for name in regex_matches:
        parts = name.split()
        # First and last name
        if len(parts) == 2 and parts[0].lower() in first_names:
            logger.info(f"{parts[0]} in first_names")
            valid_names.add(name)

    return valid_names


# Extract probable names from certain sections of the page


def extract_probable_names(soup):
    section_keywords = ["team", "about", "staff", "people", "founder", "leadership"]
    candidate_sections = []

    for tag in soup.find_all(["section", "div", "article"]):
        id_class = " ".join([tag.get("id", ""), " ".join(tag.get("class", []))]).lower()
        if any(keyword in id_class for keyword in section_keywords):
            candidate_sections.append(tag)

    if not candidate_sections:
        candidate_sections = soup.find_all(["section", "div"])  # fallback to all

    name_pattern = r"\b[A-Z][a-z]+(?:\s+[A-Z]\.)?(?:\s+[A-Z][a-z]+){1,2}\b"
    possible_names = set()

    for section in candidate_sections:
        elements = section.find_all(["h1", "h2", "h3", "p", "span", "a"])
        for el in elements:
            text = el.get_text(strip=True)
            if 5 < len(text) <= 40:
                matches = re.findall(name_pattern, text)
                for match in matches:
                    possible_names.add(match)

    return possible_names


# Function to follow links and scrape pages until all pages in the same domain are explored


def scrape_site(url, ua, scraped_emails=None, valid_names=None, scraped_urls=None):
    if not valid_names:
        valid_names = set()

    if scraped_emails is None:
        scraped_emails = set()

    if scraped_urls is None:
        scraped_urls = set()

    # Extract domain from URL
    domain = urlparse(url).netloc
    if url in scraped_urls:
        return valid_names, scraped_urls, scraped_emails

    scraped_urls.add(url)

    # Request page content
    html = request_user_agent(url, ua)
    if html is None:
        return valid_names, scraped_urls, scraped_emails

    soup = BeautifulSoup(html.text, "html.parser")
    emails = extract_emails(html.text)

    if emails:
        for email in emails:
            scraped_emails.add(email)
    logger.info(f"Emails found on {url}: {emails}")

    # Extract possible names
    possible_names = extract_probable_names(soup)
    logger.info(f"Possible names found on {url}: {possible_names}")

    # Extract probable names
    valid_names = valid_names.union(
        validate_probable_names(soup.get_text(separator=" ", strip=True))
    )
    logger.info(f"Valid names found on {url}: {valid_names}")

    # Get all links pointing to the same domain
    links_to_follow = []
    for link in soup.find_all("a", href=True):
        link_url = urljoin(url, link["href"])
        link_domain = urlparse(link_url).netloc
        if link_domain == domain and link_url not in scraped_urls:
            links_to_follow.append(link_url)

    # Recursively scrape linked pages
    for next_url in links_to_follow:
        more_names, scraped_urls, emails = scrape_site(
            next_url,
            ua,
            scraped_emails=scraped_emails,
            valid_names=valid_names,
            scraped_urls=scraped_urls,
        )
        possible_names.update(more_names)

    return valid_names, scraped_urls, emails


def parse_url(url):
    ua = UserAgent()

    valid_names, scraped_urls, emails = scrape_site(url, ua)
    logger.info(f"Final valid names: {valid_names}")
    # Assuming you want to output the names found
    if valid_names:
        for name in valid_names:
            parts = name.split()
            if len(parts) != 2:
                continue  # skip malformed names
            first, last = parts
            first = first.lower()
            last = last.lower()

            patterns = {
                first,
                last,
                f"{first}{last}",
                f"{first}.{last}",
                f"{first}_{last}",
                f"{first}-{last}",
                f"{first[0]}{last}",
                f"{first}{last[0]}",
                f"{first[0]}.{last}",
                f"{first}.{last[0]}",
                f"{first[0]}.{last[0]}",
            }

            for email in emails:
                local_part = email.split("@")[0].lower()
                print(local_part)
                if any(p in local_part for p in patterns):
                    print(f"Match found: Name = {name}, Email = {email}")
                    return first, last, email.lower()
    return None, None, None


def parse_urls(urls):
    contacts = []
    for url in urls:
        first_name, last_name, email = parse_url(url)
        if first_name and email:
            contacts.append(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "url": url,
                }
            )

    return contacts


def scrape_and_parse(location, term):
    logger.debug("SEARCHING FOR %s IN %s", term, location)
    scraper = FreeindexScraper()
    url = f"https://www.freeindex.co.uk/searchresults.htm?k={term}&l={location}"
    logger.debug("SEARCHING URL: %s", url)
    found_urls = scraper.scrape(url)
    return parse_urls(found_urls)


def run():
    while True:
        data = requests.get(
            "https://www.charlie-marshall.dev/scrapers/api/get-oldest-searchparameter/"
        )
        data = data.json()
        contacts = scrape_and_parse(data["term"], data["location"])

        data["contacts"] = contacts

        response = requests.post(
            "https://www.charlie-marshall.dev/crm/api/add-contacts/", json=data
        )

        logger.info("POST REQUEST STATUS: %s", response.status_code)
        random_sleep()
