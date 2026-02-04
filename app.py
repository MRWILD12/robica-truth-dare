#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, json, random, time, os

TOKEN = "GIIJJ0DWRJGREKPRNJJXNSGGJVJNGWMMZGUWKZZSKEBUCFKFVEUNOHKZIWVKCGTL"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

START_ID_FILE = "start_id.txt"
DATA_FILE = "data.json"

# بارگذاری start_id
if os.path.exists(START_ID_FILE):
    with open(START_ID_FILE, "r") as f:
        start_id = f.read().strip()
else:
    start_id = None

# ذخیره start_id
def save_start_id(sid):
    with open(START_ID_FILE, "w") as f:
        f.write(str(sid))

# ذخیره داده‌ها
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        games = json.load(f)
else:
    games = {}

def save_games():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)

# بانک سوال و جرات ساده
TRUTH_QUESTIONS = ["چه کسی خوشگلتره؟", "تا حالا دروغ گفتی؟"]
DARE_TASKS = ["یک آهنگ بخون", "یک عکس بامزه بفرست"]

# ارسال پیام
def send_message(chat_id, text):
    try:
        requests.post(API_URL + "sendMessage", json={"chat_id": chat_id, "text": text[:2000]}, timeout=10)
    except:
        pass

# دریافت پیام‌ها
def get_updates(start_id=None):
    data = {"start_id": start_id} if start_id else {}
    try:
        r = requests.post(API_URL + "getUpdates", json=data, timeout=15)
        return r.json()
    except:
        return None

# حلقه اصلی
while True:
    updates = get_updates(start_id)
    if updates and updates.get("ok"):
        for msg in updates.get("updates", []):
            inline = msg.get("inline_message") or {}
            chat_id = inline.get("chat_id")
            text = inline.get("text", "").strip()
            update_id = msg.get("update_id")

            if not chat_id or not text:
                continue

            # پاسخ ساده
            if text.lower() in ["/start", "سلام"]:
                send_message(chat_id, "سلام! ربات جرأت یا حقیقت آماده است. برای شروع /play بده.")
            elif text.lower() == "/play":
                choice = random.choice(TRUTH_QUESTIONS + DARE_TASKS)
                send_message(chat_id, f"🎲 انتخاب ربات: {choice}")

            start_id = update_id
            save_start_id(start_id)
    time.sleep(2)
