import os
import requests
import jinja2

from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN_NAME")
template_loader = jinja2.FileSystemLoader("templates")
template_ev = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    return template_ev.get_template(template_filename).render(**context)


def send_simple_message(to, subject, body, html):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"Mohd Nasir Jamal <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html,
        },
    )


def send_user_registration_email(email, username):
    return send_simple_message(
        to=email,
        subject="Sign up Success.",
        body=f"Hi {username},\n\nWelcome to our app.",
        html=render_template("email/action.html", username=username),
    )
