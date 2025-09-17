import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
from email.mime.base import MIMEBase
from email import encoders
import ssl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email_with_attachments(to_email, subject, html_content, attachments=None):
    """
    Send an email with HTML content and attachments
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        html_content (str): Email body in HTML format
        attachments (list): List of tuples (file_path, filename)
    """
    try:
        # Email configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        if not all([sender_email, sender_password]):
            raise ValueError("Email credentials not found in environment variables")
        
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = formataddr(('YouTube Comment Analyzer', sender_email))
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach HTML content
        msg.attach(MIMEText(html_content, 'html'))
        
        # Attach files
        if attachments:
            for file_path, filename in attachments:
                try:
                    with open(file_path, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    # Encode file in ASCII characters to send by email
                    encoders.encode_base64(part)
                    
                    # Add header as key/value pair to attachment part
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {filename}',
                    )
                    
                    # Add attachment to message
                    msg.attach(part)
                except Exception as e:
                    print(f"Error attaching {filename}: {str(e)}")
                    continue
        
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
