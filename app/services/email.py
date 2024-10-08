from type_def.configs import SMTP
import smtplib
from email.mime.text import MIMEText


def send_email(subject, email, body, smtp_config: SMTP):
    html_message = MIMEText(body, "html")
    html_message["Subject"] = subject
    html_message["From"] = smtp_config.sender_email
    html_message["To"] = email

    print(smtp_config)

    # Login to sender's gmail account, and send the message
    if smtp_config.ssl:
        with smtplib.SMTP_SSL(smtp_config.host, smtp_config.port) as server:
            # server.connect(host=smtp_config.host, port=smtp_config.port)
            # server.starttls()
            server.login(smtp_config.sender_email, smtp_config.sender_password)
            server.sendmail(smtp_config.sender_email, email, html_message.as_string())
    else:
        with smtplib.SMTP(smtp_config.host, smtp_config.port) as server:
            # server.connect(smtp_config.host, smtp_config.port)
            server.login(smtp_config.sender_email, smtp_config.sender_password)
            server.sendmail(
                smtp_config.sender_email,
                smtp_config.recipient_email,
                html_message.as_string(),
            )
