from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

class EmailService:
    @staticmethod
    def send_email(template_name, subject, recipient_list, context, from_email=None, reply_to_message_id=None):
        """
        Sends an email, optionally as a reply to a previous email.
        :param template_name: The name of the email template (without .html)
        :param subject: Email subject
        :param recipient_list: List of recipients
        :param context: Dictionary of variables for the template
        :param from_email: Sender email (optional, uses default if not provided)
        :param reply_to_message_id: Message-ID of the original email (if replying)
        """
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        html_content = render_to_string(f"entries/email_templates/{template_name}.html", context)

        email = EmailMultiAlternatives(
            subject=subject,
            body="This is an HTML email. Please enable HTML rendering.",
            from_email=from_email,
            to=recipient_list,
        )
        email.attach_alternative(html_content, "text/html")

        # If replying to an email, set email headers
        if reply_to_message_id:
            email.extra_headers = {
                "In-Reply-To": reply_to_message_id,
                "References": reply_to_message_id
            }

        email.send()
