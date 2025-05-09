
from scrapers.models import SearchParameter
import re
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException, ElementNotInteractableException)
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

from crm.models import Contact, Website

# Load spaCy's English model for NER
nlp = spacy.load("en_core_web_sm")

# Load NLTK first names dataset
try:
    first_names = set(name.lower() for name in nltk.corpus.names.words('male.txt')) | set(
        name.lower() for name in nltk.corpus.names.words('female.txt'))
except LookupError:
    nltk.download('names')
    first_names = set(name.lower() for name in nltk.corpus.names.words('male.txt')) | set(
        name.lower() for name in nltk.corpus.names.words('female.txt'))


pattern = re.compile(
    r'\b(?:click|visit|open|link|go to|our)?\s*(?:the\s*)?(website|site|web\s*page)\b')

logger = logging.getLogger(__name__)
handler = logging.Handler()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(stdout))


def random_sleep(min_time=2.5, max_time=15):
    time.sleep(uniform(min_time, max_time))


class FreeindexScraper:
    options = uc.ChromeOptions()
    options.add_argument('--headless')  # Optional: headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    driver = uc.Chrome(options=options)

    def __init__(self):
        self.base_domain = "freeindex.co.uk"
        self.visited_domains = {self.base_domain}
        self.data = []

    def _load_all(self):
        logger.info("Loading full page...")
        load_more_btn = None
        try:
            load_more_btn = self.driver.find_element(By.ID, "load-more-btn")
        except (NoSuchElementException, ElementNotInteractableException):
            pass

        while load_more_btn:
            try:
                load_more_btn.click()
                load_more_btn = self.driver.find_element(
                    By.ID, "load-more-btn")
            except (NoSuchElementException, ElementNotInteractableException):
                break

    def _extract_redirect_url(self, page_source):
        match = re.search(
            r"<body>\s*(\{.*\})\s*</body>", page_source, re.DOTALL)
        if match:
            json_text = match.group(1)
            try:
                json_data = json.loads(json_text)
                actual_url = json_data.get("REDIRECT-URL")
                if actual_url:
                    logger.debug(
                        f"Extracted redirect URL: {actual_url}")
                    self.data.append(actual_url)
                    self.visited_domains.add(
                        actual_url.split("/")[2])
                else:
                    logger.debug(
                        "No REDIRECT-URL key found in parsed JSON.")
            except json.JSONDecodeError as e:
                logger.debug(f"JSON decode error: {e}")
        else:
            logger.debug(
                "Could not extract JSON from body tag.")

    def _retrieve_websites(self):
        logger.info("Retrieving websites from freeindex...")

        links = self.driver.find_elements(By.TAG_NAME, "a")
        logger.debug("FOUND %s LINKS.", len(links))

        clickable_links = []
        for l in links:
            if l.text:
                logger.debug("CHECKING LINK: %s", l.text)
                if pattern.search(l.text):
                    logger.debug("PATTERN MATCH: %s", l.text)
                    clickable_links.append(l)
                elif l.text.strip().lower() == "link website":
                    logger.debug("EXACT MATCH: %s", l.text)
                    clickable_links.append(l)
                else:
                    logger.debug("NO PATTERN MATCH: %s", l.text)

        logger.info("Found %s clickable links", len(clickable_links))

        for link in clickable_links:
            try:
                # Get the 'onclick' attribute
                onclick = link.get_attribute("onclick")

                if onclick:
                    # Extract the business ID and type using regex
                    match = re.search(
                        r"RecordClick\('(\d+)',\s*'(\w+)'\)", onclick)

                    if match:
                        business_id = match.group(1)
                        ctype = match.group(2)

                        # Construct the URL
                        url = f"https://www.freeindex.co.uk/record_click.asp?id={business_id}&ctype={ctype}"
                        logger.debug(f"Found URL: {url}")
                        random_sleep()
                        self.driver.get(url)
                        time.sleep(5)  # Allow the page to load

                        page_source = self.driver.page_source
                        logger.debug("PAGE SOURCE: %s", page_source)

                        self._extract_redirect_url(page_source)

                    else:
                        logger.debug("No match found in onclick attribute.")
                else:
                    logger.debug("No onclick attribute found.")

                random_sleep()
                # Switch back to the original window
                self.driver.back()

                try:
                    current = self.driver.current_url
                    domain = current.split("/")[2]
                    assert domain == self.base_domain
                except AssertionError:
                    logger.error("Domain: %s is not base domain.", domain)

            except Exception as e:
                logger.debug(f"Error processing link: {e}")

    def scrape(self, url):
        logger.info("Starting freeindex scrape...")
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        logger.info("Retrieved search url")
        self._load_all()
        self._retrieve_websites()
        logger.info("Retrieved data: %s", self.data)
        if self.driver:
            self.driver.quit()
        return self.data


def request_user_agent(url, ua):
    try:
        user_agent = ua.random
        headers = {'User-Agent': user_agent,
                   "Accept-Language": "en-GB,en;q=0.9",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Referer": "https://www.google.com/",
                   "Connection": "keep-alive"}
        logger.info("Using UA: %s...", user_agent[:60])
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            logger.info("was successful.")
            return response
        else:
            logger.info("Got status %s", response.status_code)
    except requests.exceptions.RequestException as e:
        logger.warning("Request error: %s", e)

# Extract email addresses from a page


def extract_emails(html):
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html)

# Validate names based on first name list from nltk


def validate_probable_names(text):
    name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2}\b'
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
    section_keywords = ['team', 'about', 'staff',
                        'people', 'founder', 'leadership']
    candidate_sections = []

    for tag in soup.find_all(['section', 'div', 'article']):
        id_class = ' '.join(
            [tag.get('id', ''), ' '.join(tag.get('class', []))]).lower()
        if any(keyword in id_class for keyword in section_keywords):
            candidate_sections.append(tag)

    if not candidate_sections:
        candidate_sections = soup.find_all(
            ['section', 'div'])  # fallback to all

    name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z]\.)?(?:\s+[A-Z][a-z]+){1,2}\b'
    possible_names = set()

    for section in candidate_sections:
        elements = section.find_all(['h1', 'h2', 'h3', 'p', 'span', 'a'])
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

    soup = BeautifulSoup(html.text, 'html.parser')
    emails = extract_emails(html.text)

    if emails:
        for email in emails:
            scraped_emails.add(email)
    logger.info(f"Emails found on {url}: {emails}")

    # Extract possible names
    possible_names = extract_probable_names(soup)
    logger.info(f"Possible names found on {url}: {possible_names}")

    # Extract probable names
    valid_names = valid_names.union(validate_probable_names(
        soup.get_text(separator=' ', strip=True)))
    logger.info(f"Valid names found on {url}: {valid_names}")

    # Get all links pointing to the same domain
    links_to_follow = []
    for link in soup.find_all('a', href=True):
        link_url = urljoin(url, link['href'])
        link_domain = urlparse(link_url).netloc
        if link_domain == domain and link_url not in scraped_urls:
            links_to_follow.append(link_url)

    # Recursively scrape linked pages
    for next_url in links_to_follow:
        more_names, scraped_urls, emails = scrape_site(
            next_url, ua, scraped_emails=scraped_emails, valid_names=valid_names, scraped_urls=scraped_urls)
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
                f"{first[0]}.{last[0]}"
            }

            for email in emails:
                local_part = email.split('@')[0].lower()
                print(local_part)
                if any(p in local_part for p in patterns):
                    print(f"Match found: Name = {name}, Email = {email}")
                    return first, last, email.lower()
    return None, None, None


def parse_urls(urls):
    for url in urls:
        first_name, last_name, email = parse_url(url)
        if first_name and email:
            contact, created = Contact.objects.get_or_create(first_name=first_name,
                                                             last_name=last_name, email=email)
            if created:
                logger.info("New Contact Created: %s",
                            f"{contact.first_name} {contact.last_name}")
                contact.save()

            website, created = Website.objects.get_or_create(
                url=url, contact=contact)
            if created:
                logger.info("New website created: %s", website.url)
                website.save()


def scrape_and_parse(location, term):
    scraper = FreeindexScraper()
    url = f"https://www.freeindex.co.uk/searchresults.htm?k={term}&l={location}"
    found_urls = scraper.scrape(url)
    parse_urls(found_urls)
    logger.info("Scrape complete!")


def test():
    contacts = list(Contact.objects.all())
    n_contacts = 0
    n_correct = 0
    for contact in contacts:
        print(f"TESTING: {contact.first_name}")
        n_contacts += 1
        email = contact.email
        first_name = contact.first_name

        website = Website.objects.filter(contact=contact).first()
        result_first_name, _, result_email = parse_url([website.url])

        if result_first_name == first_name.lower() and result_email == email.lower():
            n_correct += 1

    print(f"TEST ACCURACY: {n_correct / n_contacts}")


def run():
    is_test = input("Is this a test run? [Y/n]") or "Y"

    if is_test.lower() == "y":
        test()
    else:
        parameters = SearchParameter.objects.filter(
            live=True).order_by("last_run_freeindex").first()

        scrape_and_parse(parameters.location.name, parameters.term.term)
