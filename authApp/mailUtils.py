from django.template.loader import render_to_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader 



EMAIL_HOST='smtp4.eganet.go.tz'
PROTOCOL='https'
EMAIL_PORT=587
EMAIL_HOST_USER="noreply.mikutano@serikali.go.tz"
EMAIL_HOST_PASSWORD="dodom@s!mu32"
EMAIL_USE_SSL=False
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL="noreply.mikutano@serikali.go.tz"
DOMAIN='http://localhost:4200'
DB_DRIVER="sqlite"

class EmailNotifications:
    def send_email_notification(emailBody, html_template):
            EMAIL_HOST = EMAIL_HOST
            EMAIL_PASSWORD = EMAIL_HOST_PASSWORD
            EMAIL_USER = EMAIL_HOST_USER
            EMAIL_PORT = EMAIL_PORT
            DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
            
            html_content = render_to_string(html_template, {'data': emailBody})
            
            # Create a Jinja2 environment with the HTML template
            env = Environment(loader=FileSystemLoader(html_template))
            template = env.from_string(html_content)

            # Render the template with the provided context
            rendered_template = template.render({'data': emailBody})
        
            # Create a multipart message and set the headers
            msg = MIMEMultipart()
            msg['From'] = DEFAULT_FROM_EMAIL
            msg['To'] = emailBody['receiver_details']
            msg['Subject'] = emailBody['subject']

            # Attach the rendered HTML content as the email body
            msg.attach(MIMEText(rendered_template, 'html'))
            
            # Create a secure SSL/TLS connection to the SMTP server
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
            

            # Login to the email account
            server.login(EMAIL_USER, EMAIL_PASSWORD)

            # Send the email
            server.sendmail(DEFAULT_FROM_EMAIL, emailBody['receiver_details'], msg.as_string())

            # Disconnect from the server
            server.quit()

            return True

