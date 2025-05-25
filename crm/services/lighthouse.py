import logging
from django.conf import settings

import pandas as pd
import requests
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
KEY = settings.GOOGLE_API_KEY
site = "https://www.art.yale.edu/"
params = f"?url={site}&key={KEY}&category=1&category=2&category=3&category=4&category=5"
url = ENDPOINT + params

audit_descriptions = {
    "performance": {
        "Failed": {
            "first-contentful-paint": "Make sure the first visible content loads quickly (preferably under 1.8s). Optimize CSS and reduce render-blocking resources.",
            "largest-contentful-paint": "Ensure the main content loads by 2.5s or faster. Optimize image sizes and server performance.",
            "speed-index": "Reduce the time it takes for visible content to appear on the screen by optimizing loading order and reducing JavaScript.",
            "time-to-interactive": "Aim for an interactive time under 5s. Minimize JavaScript and defer non-essential scripts.",
            "total-blocking-time": "Ensure minimal time where the main thread is blocked. Split large JavaScript bundles and optimize event handlers.",
            "cumulative-layout-shift": "Avoid layout shifts by specifying size attributes for images and using proper font loading strategies.",
            "reduced-javascript-execution-time": "Minimize and defer unused JavaScript to improve performance.",
            "lazy-loading-images": "Lazy load images to avoid unnecessary resource loading during the initial page load.",
            "server-response-time": "Optimize server response time by using caching, CDNs, or server-side optimizations.",
            "minimize-main-thread-work": "Break up large tasks into smaller, non-blocking chunks to improve responsiveness.",
        },
        "Passed": {
            "first-contentful-paint": "First contentful paint happens in under 1.8s, optimized CSS and render-blocking resources are minimized.",
            "largest-contentful-paint": "Main content loads in under 2.5s, with optimized image sizes and fast server response.",
            "speed-index": "Visible content appears quickly by optimizing resource loading and reducing JavaScript.",
            "time-to-interactive": "Interactive time is under 5s due to minimized and deferred JavaScript.",
            "total-blocking-time": "Main thread is mostly unblocked, large tasks are split for optimal performance.",
            "cumulative-layout-shift": "Layout shifts are minimized by using proper image sizes and font loading strategies.",
            "reduced-javascript-execution-time": "JavaScript execution time is minimized by deferring non-essential scripts.",
            "lazy-loading-images": "Images are lazy-loaded to avoid unnecessary initial load.",
            "server-response-time": "Server response time is optimized with caching, CDNs, or server-side improvements.",
            "minimize-main-thread-work": "Main thread work is minimized by breaking tasks into smaller, non-blocking chunks.",
        },
    },
    "accessibility": {
        "Failed": {
            "color-contrast": "Ensure sufficient color contrast between text and background for readability.",
            "document-title": "Ensure the page has a unique, descriptive title for accessibility and SEO.",
            "alt-text-for-images": "Add meaningful alt text to images to improve screen reader experience.",
            "form-labels": "Ensure all form inputs have clear, associated labels to enhance screen reader navigation.",
            "keyboard-navigation": "Ensure the website is fully navigable with a keyboard (no reliance on mouse).",
            "focus-visibility": "Ensure that interactive elements have visible focus styles for accessibility.",
            "semantic-html": "Use proper semantic HTML elements (like `<header>`, `<footer>`, `<nav>`, `<article>`) for better screen reader interpretation.",
            "error-identification": "Provide clear error messages for form validation to assist users with disabilities.",
            "landmark-roles": "Use landmark roles to define page structure, making it easier for screen reader users to navigate.",
            "accessible-names-for-interactive-elements": "Ensure buttons and links have clear, descriptive accessible names.",
        },
        "Passed": {
            "color-contrast": "Sufficient color contrast is maintained between text and background for readability.",
            "document-title": "Each page has a unique, descriptive title for better accessibility and SEO.",
            "alt-text-for-images": "All images have meaningful and descriptive alt text.",
            "form-labels": "Form inputs have clear and accessible labels, improving navigation.",
            "keyboard-navigation": "The website is fully navigable via keyboard alone.",
            "focus-visibility": "Interactive elements have visible focus styles for better accessibility.",
            "semantic-html": "Proper semantic HTML elements are used for better screen reader support.",
            "error-identification": "Clear and accessible error messages are provided for form validation.",
            "landmark-roles": "Landmark roles are used to define the page structure for better screen reader navigation.",
            "accessible-names-for-interactive-elements": "Buttons and links have clear, descriptive accessible names.",
        },
    },
    "best-practices": {
        "Failed": {
            "https-usage": "Ensure your site is fully served over HTTPS to protect user data.",
            "no-deprecated-apis": "Avoid using deprecated or obsolete APIs in your JavaScript code (like document.write).",
            "avoid-security-risks": "Ensure your site does not expose any potential security risks (e.g., mixed content).",
            "avoid-vulnerable-libraries": "Use up-to-date libraries and frameworks to avoid known vulnerabilities.",
            "disable-auto-play-for-media": "Disable auto-play for audio/video to improve user experience and reduce data usage.",
            "cross-origin-resource-sharing": "Ensure proper CORS configurations are in place for external API requests.",
            "preload-key-requests": "Preload critical resources to speed up page rendering.",
            "avoid-large-javascript-bundles": "Use smaller JavaScript bundles to improve performance and reduce load times.",
            "avoid-memory-leaks": "Make sure to clean up event listeners, intervals, and other references that can cause memory leaks.",
            "service-worker-setup": "Implement a service worker for offline capabilities and better caching.",
        },
        "Passed": {
            "https-usage": "The website is fully served over HTTPS, ensuring secure connections.",
            "no-deprecated-apis": "No deprecated or obsolete APIs are used in JavaScript.",
            "avoid-security-risks": "No security risks are found in the site (e.g., no mixed content).",
            "avoid-vulnerable-libraries": "Libraries and frameworks are up-to-date with no known vulnerabilities.",
            "disable-auto-play-for-media": "Audio and video elements are not set to auto-play.",
            "cross-origin-resource-sharing": "CORS is properly configured for external API requests.",
            "preload-key-requests": "Critical resources are preloaded to speed up page rendering.",
            "avoid-large-javascript-bundles": "JavaScript bundles are kept small for faster loading times.",
            "avoid-memory-leaks": "Event listeners, intervals, and other references are cleaned up to avoid memory leaks.",
            "service-worker-setup": "Service workers are properly implemented for offline capabilities and caching.",
        },
    },
    "seo": {
        "Failed": {
            "meta-description": "Ensure each page has a descriptive meta description for better SEO and social sharing.",
            "title-tag-length": "Ensure the title tag is between 50-60 characters for optimal SEO.",
            "structured-data": "Use structured data (like JSON-LD) to improve search engine understanding of your page content.",
            "image-alt-text": "Add descriptive alt text to all images to improve both accessibility and SEO.",
            "canonical-urls": "Use canonical tags to prevent duplicate content issues.",
            "http-status-codes": "Ensure that pages return appropriate status codes (e.g., 404 for not found).",
            "text-to-html-ratio": "Aim for a reasonable amount of content (text) compared to HTML to ensure quality SEO.",
            "avoid-broken-links": "Fix any broken links (404 errors) that might impact user experience and SEO.",
            "mobile-friendly-design": "Ensure your website is mobile-friendly to improve SEO rankings and user experience.",
            "xml-sitemap": "Make sure you have an XML sitemap that is properly configured for search engines to crawl.",
        },
        "Passed": {
            "meta-description": "Each page has a clear, descriptive meta description.",
            "title-tag-length": "Title tags are between 50-60 characters for optimal SEO.",
            "structured-data": "Structured data (JSON-LD) is used to enhance search engine understanding.",
            "image-alt-text": "All images have descriptive alt text for better SEO and accessibility.",
            "canonical-urls": "Canonical tags are used to prevent duplicate content issues.",
            "http-status-codes": "Appropriate HTTP status codes (e.g., 404 for errors) are in place.",
            "text-to-html-ratio": "The site maintains a healthy text-to-HTML ratio for quality SEO.",
            "avoid-broken-links": "No broken links or 404 errors are present.",
            "mobile-friendly-design": "The site is mobile-friendly and optimized for mobile devices.",
            "xml-sitemap": "An XML sitemap is present and properly configured for search engine crawling.",
        },
    },
}


def clean_description_regex(description):
    if isinstance(description, str):
        description = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", description)
        description = re.sub(r"\[Learn more[^\]]*\]", "", description)
        description = re.sub(r"\bLearn[^.]*\.", "", description)
        description = re.sub(r'\.\.\.', '', description)
        return description.strip()


def get_tier(score):
    if score >= 0.9:
        return "Pass"
    elif score >= 0.5:
        return "Needs Work"
    else:
        return "Fail"


class LighthouseAnalysisClient:
    def __init__(self):
        self.endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        self.key = settings.GOOGLE_API_KEY

        self.data = {
            "scores": {},
            "insights": {"passed": [], "failed": []},
            "sections": [],
        }

    def run(self, site):
        params = self._build_params(site)
        url = self._build_url(params)
        response = self._request_api(url)
        if response:
            df = self._parse_lighthouse_data(response)
            df = self._transform(df)
            self._parse_df_to_dict(df)
            return self.data

    def _build_params(self, site):
        return f"?url={site}&key={self.key}&category=1&category=2&category=3&category=4&category=5"

    def _build_url(self, params):
        return self.endpoint + params

    def _request_api(self, url):
        response = requests.get(url)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            logger.error("Failed to decode JSON response")
            return None

    def _parse_category_scores(self, categories):
        for k, v in categories.items():
            self.data["scores"][k] = v["score"]

    def _parse_audit_refs(self, categories):
        audit_refs = []
        for k, v in categories.items():
            category_audit_refs = v["auditRefs"]
            for category_audit_ref in category_audit_refs:
                category_audit_ref["category"] = k
                audit_refs.append(category_audit_ref)
        return audit_refs

    def _parse_audits(self, lighthouse_result):
        audits = []
        for k, v in lighthouse_result["audits"].items():
            v["name"] = k
            audits.append(v)
        return audits

    def _merge_audits_and_audit_refs(self, audits, audit_refs):
        audits_df = pd.DataFrame(audits)
        audit_refs_df = pd.DataFrame(audit_refs)
        return audits_df.merge(audit_refs_df, on=["id"], how="outer")

    def _parse_lighthouse_data(self, response):
        lighthouse_result = response["lighthouseResult"]
        categories = lighthouse_result["categories"]

        self._parse_category_scores(categories)
        audit_refs = self._parse_audit_refs(categories)
        audits = self._parse_audits(lighthouse_result)
        print(f"AUDIT REFS COLUMNS: {audit_refs}")

        df = self._merge_audits_and_audit_refs(audits, audit_refs)
        return df.mask(df["scoreDisplayMode"] == "manual")

    def _transform(self, df):
        df = df.mask(df["scoreDisplayMode"] == "notApplicable")
        df.dropna(axis=0, subset=["scoreDisplayMode"], inplace=True)

        df["description"] = df.description.apply(clean_description_regex)
        df.dropna(subset=["description", "score"], inplace=True)

        df["tier"] = df.score.apply(get_tier)
        df["impact"] = df["weight"].fillna(0).astype(float)
        return df

    def _parse_df_to_dict(self, df):
        df["passed"] = df["tier"].str.lower() == "pass"
        df["needs_work"] = df["tier"].isnull()
        df["failed"] = df["tier"].str.lower() == "fail"
        df["impact"] = df["weight"].fillna(0).astype(float)
        for category, group in df.groupby("category"):
            descriptions = audit_descriptions[category]
            audits = []

            passed = failed = needs_work = 0
            for _, row in group.iterrows():
                audit = {
                    "title": row["title"],
                    "description": row["description"],
                    "passed": bool(row["passed"]),
                    "impact": f"{row['impact']:.1f}"
                    if pd.notnull(row["impact"])
                    else "0.0",
                }
                audits.append(audit)

                print(row["id"], row["tier"])
                if row["tier"] == "Pass":
                    print(row["id"], "PASSED. CHECKING DESC....")
                    passed_descriptions = descriptions.get("Passed")
                    if passed_descriptions:
                        insight = passed_descriptions.get(row["id"])
                        if insight:
                            self.data["insights"]["passed"].append(insight)
                    passed += 1
                elif row["tier"] == "Fail":
                    print(row["id"], "FAILED. CHECKING DESC....")
                    failed_descriptions = descriptions.get("Failed")
                    if failed_descriptions:
                        insight = failed_descriptions.get(row["id"])
                        if insight:
                            self.data["insights"]["failed"].append(insight)
                    failed += 1
                elif row["tier"] == "Needs Work":
                    print(row["id"], "NEEDS WORK. CHECKING DESC....")
                    failed_descriptions = descriptions.get("Failed")
                    if failed_descriptions:
                        insight = failed_descriptions.get(row["id"])
                        if insight:
                            self.data["insights"]["failed"].append(insight)
                    needs_work += 1

            # Build dynamic summary
            if failed == 0 and needs_work == 0:
                summary = "All checks passed. Great job!"
            else:
                parts = []
                if failed:
                    parts.append(f"{failed} failed")
                if needs_work:
                    parts.append(f"{needs_work} need work")
                summary = f"{', '.join(parts)} in this section."

            section = {
                "name": category.capitalize(),
                "intro": f"This section covers {category.lower()} audits.",
                "overview": {
                    "passed": passed,
                    "failed": failed,
                    "needs_work": needs_work,
                },
                "audits": audits,
                "summary": summary,
            }

            self.data["sections"].append(section)
