import os
import pymysql
from crewai.tools import tool
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class MarketTools:
    @tool("query_starrocks")
    def query_starrocks(query: str):
        """
        Executes a SQL query on StarRocks to analyze live Crypto and FX data.
        Use this to check for price movements, averages, or volatility.
        """
        connection = pymysql.connect(
            host=os.getenv('STARROCKS_HOST'),
            port=9030,
            user=os.getenv('STARROCKS_USER'),
            password=os.getenv('STARROCKS_PASSWORD'),
            database=os.getenv('STARROCKS_DB'),
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            connection.close()

    @tool("send_whatsapp_msg")
    def send_whatsapp_msg(alert_text: str):
        """
        Sends a high-priority alert to the user's WhatsApp when a
        significant market event is detected.
        """
        client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        message = client.messages.create(
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            body=f"🚀 DATA LOUNGE ALERT: {alert_text}",
            to=os.getenv('MY_PHONE_NUMBER')
        )
        return f"WhatsApp Sent. SID: {message.sid}"
