
import logging

from django.apps import apps
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from website.models import Analysis

Contact = apps.get_model('crm', 'Contact')

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Analysis)
def create_website_for_contact(sender, instance, created, **kwargs):

    if created:
        print("New analysis created.")
        contact = Contact.objects.get(pk=instance.website.contact_id)
        email = contact.email
        if email:
            print("New analysis created. Sending email to %s...", email)
            date = instance.created_at.date()
            first_name = contact.first_name

            data = instance.data

            scores = data['scores']

            accessibility = scores['accessibility'] * 100
            seo = scores['seo'] * 100
            performance = scores['performance'] * 100
            best_practices = scores['best_practices'] * 100

            accessibility_text = f"<h2>👨‍🦽‍➡️ Accessibility: {accessibility}%</h2>\n"
            seo_text = f"<h2>🔎 Search Engine Optimization: {accessibility}%</h2>\n"
            performance_text = f"<h2>⚙️ Performance: {performance}%</h2>\n"
            best_practices_text = f"<h2>⚒️ Best Practices: {best_practices}%</h2>\n"

            if accessibility >= 90:
                accessibility_text += f"""
                <p>You scored {accessibility}% for accessibility. This means that 
                people with auditory, visual and motor impairments are able to 
                access and interact with your website affectively!</p>
                """
            else:
                accessibility_text += f"""
                <p>You scored {accessibility}% for accessibility. This means that 
                people with auditory, visual and motor impairments are unlikely to 
                be able to access and interact with your website affectively. 
                By making small changes, you can easily rectify this.</p>
                """
            if seo >= 90:
                seo_text += f"""
                <p>You scored {seo}% for Search Engine Optimization (SEO). This indicates your site is 
                well-optimized to be found by search engines, improving visibility and reach.</p>
                """
            else:
                seo_text += f"""
                <p>You scored {seo}% for Search Engine Optimization (SEO). This means your website 
                may not be ranking well in search results, reducing its discoverability. Improving 
                basic SEO practices like metadata, links, and mobile-friendliness can help a lot.</p>
                """

            if performance >= 90:
                performance_text += f"""
                <p>You scored {performance}% for performance. Your site loads quickly and responds 
                efficiently, which improves user experience and retention.</p>
                """
            else:
                performance_text += f"""
                <p>You scored {performance}% for performance. This means your website may be slow 
                to load or respond, which can frustrate users. Optimize images, reduce JavaScript, 
                and leverage caching to improve speed.</p>
                """

            if best_practices >= 90:
                best_practices_text += f"""
                <p>You scored {best_practices}% for best practices. Your website follows 
                modern web development standards and avoids common errors, which helps 
                ensure security and maintainability.</p>
                """
            else:
                best_practices_text += f"""
                <p>You scored {best_practices}% for best practices. This indicates some 
                outdated or unsafe code patterns may be present. Following up-to-date 
                coding guidelines and addressing flagged issues will improve your site's 
                quality and security.</p>
                """

            body_html = f"""
            <p>Hey {first_name},</p>
            
            <p>I took 10-15 minutes to run a free health check on your website. 
            Ensuring your website is up-to-scratch is incredibly important for 
            attracting, keeping and ultimately converting visitors to your site into 
            paying customers.</p>
            
            <h1><strong>📋 Website Health Check:</strong> {instance.website.url}</h1>\n
            
            <strong>Date:</strong> {date}\n
            
            {accessibility_text}
            
            {performance_text}
            
            {best_practices_text}
            
            {seo_text}            
            
            <p>If you're interested in finding out more actions we can take to improve the 
            performance of your website, and increase your conversion rate, I have 
            created a free full report with actionable insights you can take to improve 
            your site. Let me know, and I'll send this across.</p>
            
            Thank you very much,
            Charlie Marshall
            https://www.charlie-marshall.dev
            """
            try:
                send_mail(subject="I Audited Your Website.", message=body_html, from_email="charlie@charlie-marshall.dev",
                          recipient_list=[email], html_message=body_html)
            except Exception as e:
                print("ERROR SENDING EMAIL: %s", e)
