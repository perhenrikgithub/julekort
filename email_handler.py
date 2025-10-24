import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()
gmail_user = os.getenv("GMAIL_USER")
app_password = os.getenv("GMAIL_APP_PASSWORD")
app_url = os.getenv("APP_URL")

class emailHandler():
    def __init__(self, gmail_user: str, app_password: str):
        self.gmail_user = gmail_user
        self.app_password = app_password

    def send_christmas_card(self, to_email: str, card_id: str, from_name: str):
        if "," in to_email:
            to_emails = [email.strip() for email in to_email.split(",")]
        else:
            to_emails = [to_email]

        for to_email in to_emails:
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(self.gmail_user, self.app_password)
                subject = f"[Julepost 2025] Du har mottatt et julekort fra {from_name}!"
                body = f"""
                        <table style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f6f4f2" width="100%" cellpadding="0" cellspacing="0" bgcolor="#f6f4f2">
                            <tr>
                                <td align="center">
                                    <table width="600" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="margin: 20px auto; max-width: 600px; border-collapse: collapse">
                                        <tr>
                                            <td align="center"><h1>🎄🎅✨</h1></td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 0 20px 10px 20px">
                                                <h2 style="margin: 0 0 10px; font-size: 24px; color: #141414">{from_name} har sendt deg et julekort!</h2>
                                                <p style="margin: 0 0 10px; font-size: 14px; line-height: 20px; color: #141414">Hei der, du har mottatt et digitalt julekort!</p>
                                                <a style="color: #141414; text-decoration: none" href="{app_url}/card/{card_id}"><h3 style="margin: 0 0 15px; font-size: 20px; padding: 0.5em; border: 1px solid #000; width: fit-content; border-radius: 5px; background-color: #f6f4f2">Du kan se julekortet her</h3></a>
                                                <p style="margin: 0 0 10px; font-size: 14px; line-height: 20px; color: #141414">Dette er ikke fishing, det er Per som har for mye fritid (<a href="https://github.com/perhenrikgithub/julekort" target="_blank" style="color: #000000; text-decoration: underline">GitHub</a>).</p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 10px 0"></td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                """
                msg = MIMEMultipart()
                msg["From"] = self.gmail_user
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "html"))
                server.sendmail(self.gmail_user, to_email, msg.as_string())
                server.quit()
                print("Email sent successfully!")
            except Exception as e:
                print(f"Error sending email: {e}")



if not gmail_user or not app_password:
    raise ValueError("GMAIL_USER and GMAIL_APP_PASSWORD must be set in the .env file")

christmas_card_email_handler = emailHandler(gmail_user, app_password)

if __name__ == "__main__":
    christmas_card_email_handler.send_christmas_card(
        to_email="perhenrikmv@gmail.com",
        card_id="e054a50f",
        from_name="Per Henrik"
    )