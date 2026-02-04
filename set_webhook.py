import requests

# توکن ربات تو
TOKEN = "GIIJJ0DWRJGREKPRNJJXNSGGJVJNGWMMZGUWKZZSKEBUCFKFVEUNOHKZIWVKCGTL"
API_URL = "https://botapi.rubika.ir/v3/"

# آدرس سرور تو
SERVER_URL = "https://robica-truth-dare.onrender.com"

def set_webhooks():
    """تنظیم Webhook ها در روبیکا"""
    
    # ۱. برای receiveUpdate
    data1 = {
        "endpoint_url": f"{SERVER_URL}/receiveUpdate",
        "type": "receiveUpdate"
    }
    
    url1 = f"{API_URL}{TOKEN}/updateBotEndpoint"
    response1 = requests.post(url1, json=data1)
    print(f"Webhook 1 (receiveUpdate): {response1.status_code}")
    print(response1.json())
    
    # ۲. برای receiveInlineMessage
    data2 = {
        "endpoint_url": f"{SERVER_URL}/receiveInlineMessage",
        "type": "receiveInlineMessage"
    }
    
    url2 = f"{API_URL}{TOKEN}/updateBotEndpoint"
    response2 = requests.post(url2, json=data2)
    print(f"Webhook 2 (receiveInlineMessage): {response2.status_code}")
    print(response2.json())

if __name__ == "__main__":
    print("تنظیم Webhook ها...")
    set_webhooks()
