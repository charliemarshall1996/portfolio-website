from .models import Message


def get_message(properties, context=None):
    metric = properties.get("metric")
    score = properties.get("score")

    if metric and score:
        band = (
            'low' if score <= 50 else
            'medium' if score < 100 else
            'high'
        )
        properties['score_band'] = band
    try:
        msg_obj = Message.objects.get(**properties)
        if context:
            return msg_obj.message.format(**context)
        return msg_obj.message
    except Message.DoesNotExist:
        return None


def get_score_bullet(score, metric, campaign):
    return get_message({"score": score, "metric": metric, "campaign": campaign},
                       {"score": score})


def parse_scores(scores):
    acc_score = scores["accessibility"] * 100
    bp_score = scores["best-practices"] * 100
    per_score = scores["performance"] * 100
    seo_score = scores["seo"] * 100
    return acc_score, bp_score, per_score, seo_score


def get_bullets_section(data, campaign):
    scores = data["scores"]
    acc_score, seo_score, per_score, bp_score = parse_scores(scores)
    acc_bullet = get_score_bullet(acc_score, "accessibility", campaign)
    bp_bullet = get_score_bullet(bp_score, "best-practices", campaign)
    per_bullet = get_score_bullet(per_score, "performance", campaign)
    seo_bullet = get_score_bullet(seo_score, "seo", campaign)

    bullets_section = f"""
            So I ran a quick check on your site:
            - Accessibility {acc_score}%: {acc_bullet}
            - Best Practices {bp_score}%: {bp_bullet}
            - Performance {per_score}%: {per_bullet}
            - SEO {seo_score}%: {seo_bullet}
            """
    html_bullets_section = f"""
            <p>So I ran a quick check on your site:</p>
            <ul>
            <li><b>Accessibility {acc_score}%:</b> {acc_bullet}</li>
            <li><b>Best Practices {bp_score}%:</b> {bp_bullet}</li>
            <li><b>Performance {per_score}%:</b> {per_bullet}</li>
            <li><b>SEO {seo_score}%:</b> {seo_bullet}</li>
            </ul>
            """

    return bullets_section, html_bullets_section


def get_email_message(data, first_name, url, location, campaign):
    greeting = get_message({"campaign": campaign, "part": "greeting"})
    intro = get_message({"campaign": campaign, "part": "intro"},
                        {"location": location})
    bullets_section, html_bullets_section = get_bullets_section(data, campaign)

    plain = f"""
            {greeting} {first_name},
            
            {intro}
            
            {bullets_section}          
            
            Here's the full breakdown if you're curious:
            {url}

            If you'd like a second opinion or want help tightening up performance and 
            accessibility, happy to dig in further — no strings attached.

            Best,
            Charlie Marshall
            https://www.charlie-marshall.dev
            07464 706 184
            """

    html = f"""
            <p>{greeting} {first_name},</p>
            <p>{intro}</p>
            <p>{html_bullets_section}</p>
            <p>Here's the full breakdown if you're curious:</p>
            <p><a href="{url}">{url}</a></p>
            <p>If you'd like a second opinion or want help tightening up performance and 
            accessibility, happy to dig in further — no strings attached.</p>
            <p>Best,<br>
            Charlie Marshall<br>
            <a href="https://www.charlie-marshall.dev">https://www.charlie-marshall.dev</a><br>
            07464 706 184</p>
            """

    return plain, html
