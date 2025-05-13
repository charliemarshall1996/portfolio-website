
from jinja2 import Template
import os

VERTICAL_KEYWORDS = {
    "local_services": [
        "plumber", "electrician", "builder", "handyman", "landscaper", "roofer",
        "locksmith", "painter", "cleaner", "boiler repair", "carpenter", "gutter cleaning",
        "drainage", "heating engineer"
    ],
    "therapist": [
        "counsellor", "therapist", "psychotherapist", "coach", "life coach", "cbt",
        "mental health", "trauma therapy", "relationship counsellor", "grief support",
        "hypnotherapy", "wellness coach"
    ],
    "agency": [
        "marketing agency", "web design", "seo agency", "creative studio", "branding agency",
        "ppc", "content marketing", "social media agency", "digital agency", "design consultancy"
    ]
}


def get_vertical_from_term(search_term):
    search_term = search_term.lower()
    for vertical, keywords in VERTICAL_KEYWORDS.items():
        if any(keyword in search_term for keyword in keywords):
            return vertical
    return "other"


def get_email_message(data, first_name, url, date, search_term):
    scores = data['scores']

    accessibility_score = scores['accessibility'] * 100
    seo_score = scores['seo'] * 100
    performance_score = scores['performance'] * 100
    best_practices_score = scores['best-practices'] * 100

    accessibility_text_string = ""
    seo_text_string = ""
    performance_text_string = ""
    best_practices_text_string = ""

    if accessibility_score >= 90:
        accessibility_text_string = f"""
                You scored {accessibility_score}% for accessibility. This means that 
                people with auditory, visual and motor impairments are able to 
                access and interact with your website affectively!
                """
    else:
        accessibility_text_string = f"""
                You scored {accessibility_score}% for accessibility. This means that 
                people with auditory, visual and motor impairments are unlikely to 
                be able to access and interact with your website affectively. 
                By making small changes, you can easily rectify this.
                """
    if seo_score >= 90:
        seo_text_string = f"""
                You scored {seo_score}% for Search Engine Optimization (SEO). This indicates your site is 
                well-optimized to be found by search engines, improving visibility and reach.
                """
    else:
        seo_text_string = f"""
                You scored {seo_score}% for Search Engine Optimization (SEO). This means your website 
                may not be ranking well in search results, reducing its discoverability. Improving 
                basic SEO practices like metadata, links, and mobile-friendliness can help a lot.
                """

    if performance_score >= 90:
        performance_text_string = f"""
                You scored {performance_score}% for performance. Your site loads quickly and responds 
                efficiently, which improves user experience and retention.
                """
    else:
        performance_text_string = f"""
                You scored {performance_score}% for performance. This means your website may be slow 
                to load or respond, which can frustrate users. Optimize images, reduce JavaScript, 
                and leverage caching to improve speed.
                """

    if best_practices_score >= 90:
        best_practices_text_string = f"""
                You scored {best_practices_score}% for best practices. Your website follows 
                modern web development standards and avoids common errors, which helps 
                ensure security and maintainability.
                """
    else:
        best_practices_text_string = f"""
                You scored {best_practices_score}% for best practices. This indicates some 
                outdated or unsafe code patterns may be present. Following up-to-date 
                coding guidelines and addressing flagged issues will improve your site's 
                quality and security.
                """

    vertical = get_vertical_from_term(search_term)
    if vertical == "local_services":
        context_line = (
            "For local businesses like yours, a fast, accessible website can directly increase the number of enquiries you receive."
        )
    elif vertical == "therapist":
        context_line = (
            "For therapy and wellness professionals, a trustworthy, fast-loading website helps build confidence with potential clients."
        )
    elif vertical == "agency":
        context_line = (
            "For marketing/design agencies, having your own site reflect modern best practices boosts credibility with your clients."
        )
    else:
        context_line = ""
    body_plain = f"""
            Hey {first_name},
            
            I took 10-15 minutes to run a free health check on your website. 
            {context_line}
            
            📋 Website Health Check: {url}\n
            
            Date: {date}\n
            
            {accessibility_text_string}
            
            {performance_text_string}
            
            {best_practices_text_string}
            
            {seo_text_string}            
            
            If you're interested in finding out more actions we can take to improve the 
            performance of your website, and increase your conversion rate, I have 
            created a free full report with actionable insights you can take to improve 
            your site. Let me know, and I'll send this across.
            
            Thank you very much,
            Charlie Marshall
            https://www.charlie-marshall.dev
            """
    html_template = os.path.abspath(
        "./website/templates/website/mjml/marketing_email.html")
    with open(html_template, "r") as template:
        html_template = Template(template.read())
        html_body = html_template.render(
            first_name=first_name,
            url=url,
            accessibility=accessibility_score,
            accessibility_text=accessibility_text_string,
            performance=performance_score,
            performance_text=performance_text_string,
            best_practices=best_practices_score,
            best_practices_text=best_practices_text_string,
            seo=seo_score,
            seo_text=seo_text_string,
            context_line=context_line
        )
    return body_plain, html_body
