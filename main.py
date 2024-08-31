import smtplib
from email.mime.text import MIMEText
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

# Define the schedule directly in the script
schedule_data = {
    "schedule": [
        {"week": 1, "day": "Mo", "cook": "Ash", "dish": "Cauliflower Stir-Fry"},
        {"week": 1, "day": "Tu", "cook": "Bangaru", "dish": "Spinach Dal"},
        {"week": 1, "day": "We", "cook": "Ash", "dish": "Cabbage Sabzi"},
        {"week": 1, "day": "Th", "cook": "Bangaru", "dish": "Lemon Dal"},
        {"week": 1, "day": "Fr", "cook": "Sam", "dish": "Carrot and Beans Stir-Fry"},
        {"week": 1, "day": "Sa", "cook": "Sam", "dish": "Aloo Fry"},
        {"week": 2, "day": "Mo", "cook": "Ash", "dish": "Ladies Finger Stir-Fry"},
        {"week": 2, "day": "Tu", "cook": "Bangaru", "dish": "Tomato Dal"},
        {"week": 2, "day": "We", "cook": "Ash", "dish": "Dondakaya Stir-Fry"},
        {"week": 2, "day": "Th", "cook": "Bangaru", "dish": "Beetroot Fry"},
        {"week": 2, "day": "Fr", "cook": "Sam", "dish": "Methi Dal"},
        {"week": 2, "day": "Sa", "cook": "Sam", "dish": "Paneer Stir-Fry"}
    ]
}

# Email settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# Email recipients based on cook
EMAIL_RECIPIENTS = {
    'Bangaru': 'sreeram.bangaroo@gmail.com',
    'Ash': 'ashwithamary123@gmail.com',
    'Sam': 'ynsameer@gmail.com'
}

def send_email(recipient_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_email}")

def send_reminder():
    today = datetime.date.today()
    start_date = datetime.date(2024, 9, 2)  # Replace with your actual start date
    days_passed = (today - start_date).days
    current_week = (days_passed // 7) % 2 + 1  # 1 for Week 1, 2 for Week 2
    weekday = today.strftime('%a')[:2]  # Get short form of the day ('Mo', 'Tu', etc.)

    if weekday == 'Su':
        # Special case for Sunday: send an email to everyone
        for cook in EMAIL_RECIPIENTS.keys():
            recipient_email = EMAIL_RECIPIENTS.get(cook)
            if recipient_email:
                subject = "Sunday Cooking Reminder"
                body = f"Reminder: {cook}, today is a rest day or special task!"
                send_email(recipient_email, subject, body)
    else:
        # Regular schedule for other days
        for record in schedule_data['schedule']:
            if record['week'] == current_week and record['day'] == weekday:
                cook = record['cook']
                dish = record['dish']
                recipient_email = EMAIL_RECIPIENTS.get(cook)
                if recipient_email:
                    subject = "Cooking Reminder"
                    body = f"Reminder: {cook}, today you are cooking {dish}."
                    send_email(recipient_email, subject, body)

    
    # today = datetime.date.today()
    # start_date = datetime.date(2024, 9, 2)  # Replace with your actual start date
    # days_passed = (today - start_date).days
    # current_week = (days_passed // 7) % 2 + 1  # 1 for Week 1, 2 for Week 2
    # weekday = today.strftime('%a')[:2]  # Get short form of the day ('Mo', 'Tu', etc.)

    # for record in schedule_data['schedule']:
    #     if record['week'] == current_week and record['day'] == weekday:
    #         cook = record['cook']
    #         dish = record['dish']
    #         recipient_email = EMAIL_RECIPIENTS.get(cook)
    #         if recipient_email:
    #             subject = "Cooking Reminder"
    #             body = f"Reminder: {cook}, today you are cooking {dish}."
    #             send_email(recipient_email, subject, body)

# Run the reminder function
send_reminder()
