#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات جرأت یا حقیقت برای Robica
نسخه کامل با توکن واقعی
"""
from flask import Flask, request, jsonify
import requests
import random
app = Flask(__name__)


TOKEN = "GIIJJ0DWRJGREKPRNJJXNSGGJVJNGWMMZGUWKZZSKEBUCFKFVEUNOHKZIWVKCGTL"
API_URL = "https://botapi.rubika.ir/v3/"

print("🤖 ربات جرأت یا حقیقت شروع شد...")
import json
import random
import time
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse
from collections import defaultdict
import sqlite3
import os
import logging

# تنظیمات لاگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============ تنظیمات اصلی ============
class Config:
    # توکن ربات شما
    BOT_TOKEN = "GIIJJ0DWRJGREKPRNJJXNSGGJVJNGWMMZGUWKZZSKEBUCFKFVEUNOHKZIWVKCGTL"
    
    # آدرس API روبیکا
    API_URL = "https://botapi.rubika.ir/v3/"
    
    # تنظیمات سرور
    SERVER_PORT = 8080
    SERVER_HOST = "0.0.0.0"
    
    # زمان‌های انتظار (ثانیه)
    WAIT_FOR_ANSWER = 180  # 3 دقیقه برای پاسخ
    WAIT_FOR_DARE = 300    # 5 دقیقه برای انجام جرات
    CLEANUP_INTERVAL = 3600  # 1 ساعت برای پاک‌سازی
    
    # بانک سوالات حقیقت (100+ سوال)
    TRUTH_QUESTIONS = [
        "چه کسی توی این جمع از همه خوشگلتره؟",
        "یکی از فانتزی‌هات رو تعریف کن؟",
        "اگر دوست‌دخترت از دوست صمیمیت متنفر باشه، چکار می‌کنی؟",
        "تا به حال مواد مخدر مصرف کردی؟",
        "تا به حال کسی پیشنهاد دوستی تو رو رد کرده؟",
        "تا به حال از دوستِ دوست‌دخترت خوشت اومده؟",
        "مرد یا زن رویا‌های تو چه شکلیه؟",
        "جذابترین آدم توی این اتاق از نظر تو کیه؟",
        "به نظرت مخاطب خاص تو، کیس ازدواج هست؟",
        "تا حالا شده به همسرت دروغ بگی تا از نزدیک شدن بهش اجتناب کنی؟",
        "دوست داری چه چیزی در مورد مخاطب خاصت تغییر کنه؟",
        "چه کسی رو پنهانی دوست داری؟",
        "تا به حال به همسرت / مخاطب خاصت خیانت کردی؟",
        "اصلی‌ترین چیزی که توی جنس مقابل برای تو جذابه چیه؟",
        "معیارهات برای ورود به یک رابطه چی هستن؟",
        "در مورد اولین تجربه‌ی عاشقانه‌ ات بگو ؟",
        "یه قسمت خنده‌دار از اولین تجربه‌ی پرحرارت زندگیت رو تعریف کن؟",
        "بدترین ویژگی بغل دستیت چیه؟",
        "بدترین قرارت با یه پسر چطوری بوده؟",
        "تا به حال از دوست‌پسر یا دوست‌دختر دوستت خوشت اومده؟",
        "تا به حال شده پسری که دوستش داری بفهمه، و بهت جواب منفی بده؟",
        "برای اینکه جذاب به نظر برسی چه کار می‌کنی؟",
        "در حال حاضر از کی خوشت میاد؟",
        "اگر می‌تونستی یک چیز در بدنت رو تغییر بدی اون چی بود؟",
        "بدترین شوخی که با کسی داشته ای چه بوده است؟",
        "اگر نامرئی شوی اولین کاری که انجام می دهی چیست؟",
        "اگر مجبور باشی در یک جزیره به تنهایی با یک نفر زندگی کنی چه کسی را انتخاب می کنی؟",
        "احمقانه ترین حرفی که در لحظات عاشقانه به همسرت زده ای چه بوده است؟",
        "اسم کسی را بگو که وانمود می کنی دوستش داری اما در واقع چشم دیدنش را نداری؟",
        "سگ یا گرگ؟",
        "ب کی خیلی حسودیت میشه؟",
        "بنظرت غرور من چقدره؟",
        "حجاب یا بد حجاب یا متوسط؟",
        "اخرین باری ک گریه کردی؟",
        "اسم مامان بابات؟",
        "سیگار یا قیلیون؟",
        "میری بیرون چجور تیپی میزنی؟",
        "شات از گالریت؟",
        "تا حالا شپش گرفتی؟",
        "غرور یا عشق ابدی",
        "مو فر دوست داری یا صاف",
        "شش تیکه داری",
        "شش تیکه دوست داری",
        "نوشابه مشکی یا زرد",
        "دوغ یا نوشابه",
        "بنظرت میتونی مرگ پدر مادرت رو تحمل کنی",
        "دوست داری دنیا همیشه روز باشه یا شب",
        "تو بچگی دکتر بازی کردی",
        "اکثر درددلات با کدوم فردگپه؟",
        "ازچی جنس مخالف بدت میاد؟",
        "دوس داری ضربان قلبم بشی؟",
        "کیو دوس داری؟",
        "میخوای شغل آیندت چی باشه؟",
        "خجالت آور ترین کاری ک کردی چیه؟",
        "احساساتتو بگو",
        "بچه بودی چن بار گمشدی؟",
        "بهترین بلاگر از نظرت کیه؟",
        "یک شعر عاشقانه برام بخون.",
        "میوه مورد علاقت؟",
        "یک واقعیت آزار دهنده راجب خودت بگو؟",
        "بدترین دعوایی که کردی را تعریف کن.",
        "نزدیک ترین شخص به تو در خانواده ات کیست؟ پدر؟ مادر؟ یا خواهر و برادر؟",
        "بازی های خجالت آور در دوران بچگیت را بگو.",
        "خجالت آورترین خاطره کودکی ات چیست؟",
        "تو رفیقات ب نظرت کی از همه جذاب تره؟ چرا؟",
        "بد ترین سوتی ک دادی چی بوده؟",
        "قدت چنتاست؟",
        "پوستت چه رنگیه؟",
        "احساساتتو بگو",
        "چ غذای رو خیلی دوس داری",
        "تلخ شیرین ترش یا تند؟",
        "باحال ترین کاری ک کردی چی بوده؟",
        "اگ صب پاشی ببینی بقلتم چیکا میکنی؟",
        "همین الان ی عکس از خودت بده؟",
        "اگ قبل از ب دنیا اومدن میدونسی ک قرار این شخصیت و این زندگی رو داشه باشی باز انتخابش میکردی؟؟",
        "تا ب حال گم شدی؟",
        "یکی از آرزو هات ک خیلی دوس داری بش برسی بگو",
        "تا ب حال شده از دس مامان یا بابات کتک بخوری سر چی بوده؟",
        "شات از نتایج گوگلت",
        "چشای کیو تو گپ میبوسی و لبای کیو؟(دونفرمتفاوت)",
        "رو کسی کراش داری؟",
        "کدومش بدتره؟(موجودی شما کافی نمیباشد)_(اینترنت شما به اتمام رسید)",
        "شات از لیست پیوی هات",
        "شات از پیوی کسی ک زیاد باهاش میچتی و تو این گپه.",
        "روز شانست کدومه؟",
        "میوه مورد علاقت؟",
        "چیو ب ماها دروغ گفتی؟",
        "تا حالا شده بخاطر یکی از بچه های این گپ گریه کنی؟یا ناراحت شی بخاطرش؟",
        "زیرلباست چ رنگیه؟",
        "لجبازی؟",
        "تا چند سالگی تو کوچه بازی میکردی؟",
        "ب کسی علاقه داشته باشی ولی نتونی بگی.بش کم محلی میکنی یا بیشتر حسادت میکنی؟",
        "یکی از فحشایی ک زیاد استفادش میکنی چیه؟",
        "رنگ پتویی ک هرشب باهاش میخوابی؟",
        "دوتا از اهنگایی ک بیشتر تو حموم میخونی چیه؟"
    ]
    
    # بانک جرات‌ها (30+ جرات)
    DARE_TASKS = [
        "📱 برای ۵ دقیقه عکس پروفایل خودت رو به عکس یک حیوان تغییر بده",
        "🎤 یک آهنگ عاشقانه را با صدای بلند بخوان",
        "🤳 سلفی با حالت خنده‌دار بگیر و در گپ بفرست",
        "💬 آخرین پیام خودت در پیوی را در گپ نشان بده",
        "📞 به یکی از مخاطبینت زنگ بزن و بگو 'دوستت دارم'",
        "🎭 برای ۱۰ دقیقه نقش یک هنرپیشه را بازی کن",
        "📸 از سقف اتاقت عکس بگیر و بفرست",
        "🎵 نام ۵ آهنگ مورد علاقه‌ات را بگو",
        "👟 کفش‌هایت را بو کن و نظرت را بگو",
        "🤣 به مدت ۳۰ ثانیه بلند بخند بدون دلیل",
        "👻 برای یک نفر در گپ پیام بفرست و بگو 'دیدی چی گفتی؟'",
        "🍎 اگر میوه دارید، یک گاز بزرگ از آن بزنید و عکس بفرستید",
        "💃 حرکات رقص انجام بده و ویدیو بفرست",
        "📖 یک داستان کوتاه ۳ خطی درباره گپ بساز",
        "🎯 نام سه نفر از اعضای گپ را بگو که فکر می‌کنی باهوش‌ترین هستند",
        "🍽️ اگر غذا می‌خوری، عکس آن را بفرست",
        "🌙 آخرین رویایی که دیدی را تعریف کن",
        "👂 اگر گوشی دارید، از لاله گوش خود عکس بگیرید",
        "📅 برنامه فردای خودت را بگو",
        "🥚 اگر تخم مرغ دارید، روی آن نقاشی بکشید و عکس بفرستید",
        "📱 شماره خودت را به صورت برعکس در گپ بنویس",
        "🎭 حالت چهره یک حیوان را در بیار و عکس بگیر",
        "💬 به آخرین شخصی که با او چت کردی بگو 'دوستت دارم'",
        "📝 اسم ۳ تا از معایب خودت را بگو",
        "🕺 یک حرکت رقص جدید اختراع کن و اسم بگذار",
        "🎤 مثل یک گوینده اخبار برای ۱ دقیقه صحبت کن",
        "📸 از پنجره اتاقت عکس بگیر و بفرست",
        "🎵 آهنگ مورد علاقه‌ات را زمزمه کن و صدا ضبط کن",
        "🤪 یک جوک تعریف کن (حتی اگر خنده‌دار نباشد)",
        "👁️ به مدت ۱ دقیقه بدون پلک زدن به دوربین نگاه کن",
        "📱 آخرین عکسی که از گالریت حذف کردی چه بود؟",
        "💭 بزرگترین رازت رو بگو",
        "🤝 با نفر بغلی دست بده و عکس بگیر",
        "🎶 با صدای خودت یک تبلیغ بساز",
        "📞 به مامانت زنگ بزن و بگو دوستت دارم",
        "🎤 آهنگ تولدت رو بخون",
        "📸 از داخل یخچالت عکس بگیر",
        "🎭 نقش معلم رو بازی کن",
        "📝 یک داستان ۵ کلمه‌ای بساز",
        "🤔 سخت‌ترین تصمیم زندگیت رو بگو"
    ]

# ============ API ارتباط با روبیکا ============
class RubikaAPI:
    """کلاس برای ارتباط با Robica API"""
    
    @staticmethod
    def call_method(method, data=None):
        """فراخوانی متدهای Robica API"""
        url = f"{Config.API_URL}{Config.BOT_TOKEN}/{method}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/json'
            }
            
            if data:
                data_json = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(url, data=data_json, headers=headers, method='POST')
            else:
                req = urllib.request.Request(url, headers=headers, method='GET')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                logger.info(f"API Call: {method} -> {result.get('status', 'unknown')}")
                return result
                
        except urllib.error.HTTPError as e:
            logger.error(f"HTTP Error in {method}: {e.code} - {e.reason}")
            return {"status": "error", "message": f"HTTP {e.code}"}
        except urllib.error.URLError as e:
            logger.error(f"URL Error in {method}: {e.reason}")
            return {"status": "error", "message": "Connection failed"}
        except Exception as e:
            logger.error(f"Error in {method}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    @staticmethod
    def send_message(chat_id, text, reply_to=None, keyboard=None):
        """ارسال پیام به چت"""
        data = {
            "chat_id": chat_id,
            "text": text[:4096]  # محدودیت طول متن
        }
        
        if reply_to:
            data["reply_to"] = reply_to
        
        if keyboard:
            data["keyboard"] = keyboard
        
        result = RubikaAPI.call_method("sendMessage", data)
        
        if result and result.get("status") == "OK":
            logger.info(f"پیام ارسال شد به {chat_id}")
            return result.get("data", {}).get("message_id")
        else:
            logger.error(f"خطا در ارسال پیام به {chat_id}: {result}")
            return None
    
    @staticmethod
    def edit_message(chat_id, message_id, text, keyboard=None):
        """ویرایش پیام"""
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text[:4096]
        }
        
        if keyboard:
            data["keyboard"] = keyboard
        
        return RubikaAPI.call_method("editMessage", data)
    
    @staticmethod
    def delete_message(chat_id, message_id):
        """حذف پیام"""
        data = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        
        return RubikaAPI.call_method("deleteMessage", data)
    
    @staticmethod
    def get_chat_info(chat_id):
        """دریافت اطلاعات چت"""
        data = {"chat_id": chat_id}
        return RubikaAPI.call_method("getChat", data)
    
    @staticmethod
    def get_user_info(user_id):
        """دریافت اطلاعات کاربر"""
        data = {"user_id": user_id}
        result = RubikaAPI.call_method("getUser", data)
        
        if result and result.get("status") == "OK":
            user_data = result.get("data", {})
            return {
                "first_name": user_data.get("first_name", "کاربر"),
                "last_name": user_data.get("last_name", ""),
                "username": user_data.get("username", "")
            }
        return {"first_name": "کاربر", "last_name": "", "username": ""}
    
    @staticmethod
    def create_keyboard(buttons, rows=2):
        """ایجاد کیبورد"""
        keyboard = []
        row = []
        
        for i, button in enumerate(buttons):
            row.append({
                "id": f"btn_{i}",
                "text": button
            })
            
            if len(row) >= rows:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        return keyboard

# ============ مدیریت بازی ============
class GameManager:
    """مدیریت بازی‌های جرأت یا حقیقت"""
    
    def __init__(self):
        self.games = {}  # {chat_id: game_data}
        self.user_cache = {}  # کش اطلاعات کاربران
        self.db = Database()
        self.init_game_timers()
        logger.info("GameManager initialized")
    
    def init_game_timers(self):
        """شروع تایمرهای بازی"""
        # تایمر پاک‌سازی بازی‌های قدیمی
        cleanup_thread = threading.Thread(target=self.cleanup_loop, daemon=True)
        cleanup_thread.start()
        
        # تایمر بررسی زمان پاسخ‌ها
        check_timers_thread = threading.Thread(target=self.check_timers_loop, daemon=True)
        check_timers_thread.start()
    
    def cleanup_loop(self):
        """حلقه پاک‌سازی بازی‌های قدیمی"""
        while True:
            time.sleep(Config.CLEANUP_INTERVAL)
            self.cleanup_old_games()
    
    def check_timers_loop(self):
        """حلقه بررسی زمان‌سنج‌ها"""
        while True:
            time.sleep(60)  # هر 1 دقیقه چک کن
            self.check_timeouts()
    
    def get_user_name(self, user_id):
        """دریافت نام کاربر با کش"""
        if user_id in self.user_cache:
            return self.user_cache[user_id]
        
        user_info = RubikaAPI.get_user_info(user_id)
        name = user_info.get("first_name", "کاربر")
        self.user_cache[user_id] = name
        return name
    
    def create_game(self, chat_id, creator_id):
        """ایجاد بازی جدید"""
        if chat_id in self.games:
            game = self.games[chat_id]
            if not self.is_game_expired(game):
                return False, "🎮 یک بازی فعال در این گپ وجود دارد!\n\nبرای پیوستن:\n/join\n\nبرای دیدن اطلاعات:\n/players"
        
        creator_name = self.get_user_name(creator_id)
        
        game = {
            'chat_id': chat_id,
            'creator_id': creator_id,
            'creator_name': creator_name,
            'players': [{'id': creator_id, 'name': creator_name, 'score': 0}],
            'player_ids': [creator_id],
            'current_player_index': 0,
            'scores': {creator_name: 0},
            'used_questions': set(),
            'used_dares': set(),
            'started': False,
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'game_type': None,
            'current_task': None,
            'task_start_time': None,
            'waiting_for_response': False
        }
        
        self.games[chat_id] = game
        self.db.save_game(chat_id, game)
        
        logger.info(f"بازی جدید ایجاد شد در چت {chat_id} توسط {creator_name}")
        
        players_list = "\n".join([f"• {p['name']}" for p in game['players']])
        
        message = f"""
🎮 **بازی جرأت یا حقیقت ساخته شد!**

👤 سازنده: {creator_name}
👥 بازیکنان ({len(game['players'])} نفر):
{players_list}

📌 **دستورات:**
/join - عضویت در بازی
/startgame - شروع بازی (سازنده)
/players - نمایش بازیکنان
/help - راهنما

⏰ بازی تا ۲ ساعت بدون فعالیت فعال می‌ماند.
        """
        
        return True, message
    
    def join_game(self, chat_id, user_id):
        """عضویت در بازی"""
        if chat_id not in self.games:
            return False, "⚠️ هیچ بازی فعالی در این گپ وجود ندارد!\n\nبرای ایجاد بازی:\n/play"
        
        game = self.games[chat_id]
        
        if self.is_game_expired(game):
            del self.games[chat_id]
            return False, "⚠️ بازی منقضی شده!\n\nبرای ایجاد بازی جدید:\n/play"
        
        if game['started']:
            return False, "⚠️ بازی قبلاً شروع شده!\n\nبرای شروع بازی جدید صبر کنید تا این بازی تمام شود."
        
        if user_id in game['player_ids']:
            user_name = self.get_user_name(user_id)
            return False, f"⚠️ {user_name} شما قبلاً عضو بازی هستید!"
        
        user_name = self.get_user_name(user_id)
        
        # اضافه کردن بازیکن
        game['players'].append({'id': user_id, 'name': user_name, 'score': 0})
        game['player_ids'].append(user_id)
        game['scores'][user_name] = 0
        game['last_activity'] = datetime.now()
        
        self.db.save_game(chat_id, game)
        
        logger.info(f"{user_name} به بازی در چت {chat_id} پیوست")
        
        players_list = "\n".join([f"• {p['name']}" for p in game['players']])
        
        message = f"""
✅ **{user_name} به بازی پیوست!**

👥 بازیکنان ({len(game['players'])} نفر):
{players_list}

{"🎮 بازی شروع شده" if game['started'] else "⏳ در انتظار شروع توسط سازنده"}

📌 سازنده می‌تواند با دستور زیر بازی را شروع کند:
/startgame
        """
        
        return True, message
    
    def start_game(self, chat_id, user_id):
        """شروع بازی"""
        if chat_id not in self.games:
            return False, "⚠️ هیچ بازی فعالی وجود ندارد!"
        
        game = self.games[chat_id]
        
        if self.is_game_expired(game):
            del self.games[chat_id]
            return False, "⚠️ بازی منقضی شده!\n\nبرای ایجاد بازی جدید:\n/play"
        
        if game['creator_id'] != user_id:
            creator_name = self.get_user_name(game['creator_id'])
            return False, f"⚠️ فقط سازنده ({creator_name}) می‌تواند بازی را شروع کند!"
        
        if len(game['players']) < 2:
            return False, "⚠️ حداقل ۲ نفر برای شروع بازی نیاز است!\n\nاز دیگران بخواهید با /join عضو شوند."
        
        game['started'] = True
        game['last_activity'] = datetime.now()
        
        self.db.save_game(chat_id, game)
        
        logger.info(f"بازی شروع شد در چت {chat_id}")
        
        # انتخاب بازیکن اول
        first_player = game['players'][0]
        
        # ایجاد کیبورد
        keyboard = RubikaAPI.create_keyboard(["❓ حقیقت", "🎯 جرات", "📊 امتیازات", "👥 بازیکنان"])
        
        players_list = "\n".join([f"• {p['name']}" for p in game['players']])
        
        message = f"""
🎮 **بازی شروع شد!**

👥 **بازیکنان ({len(game['players'])} نفر):**
{players_list}

🎯 **نوبت:** {first_player['name']}

📌 **انتخاب کنید:**
❓ **حقیقت** - یک سوال صادقانه
🎯 **جرات** - یک کار جالب

⚡ **قوانین:**
1. باید صادقانه پاسخ دهید
2. جرات‌ها باید انجام شوند
3. می‌توانید با /skip رد کنید
4. با /scores امتیازات را ببینید

⏰ زمان پاسخ: ۳ دقیقه
⏰ زمان جرات: ۵ دقیقه
        """
        
        return True, message, keyboard
    
    def get_truth(self, chat_id, user_id):
        """دریافت سوال حقیقت"""
        if chat_id not in self.games:
            return False, "⚠️ هیچ بازی فعالی وجود ندارد!"
        
        game = self.games[chat_id]
        
        if self.is_game_expired(game):
            del self.games[chat_id]
            return False, "⚠️ بازی منقضی شده!"
        
        if not game['started']:
            return False, "⚠️ بازی هنوز شروع نشده!\n\nسازنده باید /startgame را بفرستد."
        
        current_player = game['players'][game['current_player_index'] % len(game['players'])]
        
        if current_player['id'] != user_id:
            return False, f"⚠️ نوبت شما نیست!\n\n🎯 نوبت: {current_player['name']}"
        
        if game['waiting_for_response']:
            return False, "⚠️ در حال انتظار برای پاسخ قبلی!\n\nلطفا اول به سوال/جرات قبلی پاسخ دهید."
        
        # انتخاب سوال تصادفی
        available = [q for q in Config.TRUTH_QUESTIONS if q not in game['used_questions']]
        
        if not available:
            game['used_questions'] = set()
            available = Config.TRUTH_QUESTIONS
        
        question = random.choice(available)
        game['used_questions'].add(question)
        game['game_type'] = 'truth'
        game['current_task'] = question
        game['task_start_time'] = datetime.now()
        game['waiting_for_response'] = True
        game['last_activity'] = datetime.now()
        
        self.db.save_game(chat_id, game)
        
        logger.info(f"سوال حقیقت برای {current_player['name']} در چت {chat_id}")
        
        # ایجاد کیبورد برای پاسخ
        keyboard = RubikaAPI.create_keyboard(["✅ پاسخ دادم", "⏭️ رد کن", "⏰ زمان"])
        
        message = f"""
❓ **سوال حقیقت برای {current_player['name']}:**

{question}

⏰ **زمان:** ۳ دقیقه
🏅 **امتیاز فعلی:** {current_player['score']}

📌 **پس از پاسخ:**
✅ **پاسخ دادم** - امتیاز بگیر
⏭️ **رد کن** - امتیاز از دست بده
        """
        
        return True, message, keyboard
    
    def get_dare(self, chat_id, user_id):
        """دریافت سوال جرات"""
        if chat_id not in self.games:
            return False, "⚠️ هیچ بازی فعالی وجود ندارد!"
        
        game = self.games[chat_id]
        
        if self.is_game_expired(game):
            del self.games[chat_id]
            return False, "⚠️ بازی منقضی شده!"
        
        if not game['started']:
            return False, "⚠️ بازی هنوز شروع نشده!"
        
        current_player = game['players'][game['current_player_index'] % len(game['players'])]
        
        if current_player['id'] != user_id:
            return False, f"⚠️ نوبت شما نیست!\n\n🎯 نوبت: {current_player['name']}"
        
        if game['waiting_for_response']:
            return False, "⚠️ در حال انتظار برای پاسخ قبلی!\n\nلطفا اول به سوال/جرات قبلی پاسخ دهید."
        
        # انتخاب جرات تصادفی
        available = [d for d in Config.DARE_TASKS if d not in game['used_dares']]
        
        if not available:
            game['used_dares'] = set()
            available = Config.DARE_TASKS
        
        dare = random.choice(available)
        game['used_dares'].add(dare)
        game['game_type'] = 'dare'
        game['current_task'] = dare
        game['task_start_time'] = datetime.now()
        game['waiting_for_response'] = True
        game['last_activity'] = datetime.now()
        
        self.db.save_game(chat_id, game)
        
        logger.info(f"جرات برای {current_player['name']} در چت {chat_id}")
        
        # ایجاد کیبورد
        keyboard = RubikaAPI.create_keyboard(["✅ انجام دادم", "⏭️ رد کن", "⏰ زمان"])
        
        message = f"""
🎯 **جرات برای {current_player['name']}:**

{dare}

⏰ **زمان:** ۵ دقیقه
🏅 **امتیاز فعلی:** {current_player['score']}

📌 **پس از انجام:**
✅ **انجام دادم** - امتیاز بگیر
⏭️ **رد کن** - امتیاز از دست بده
        """
        
        return True, message, keyboard
    
    def complete_task(self, chat_id, user_id):
        """تکمیل کار (پاسخ/انجام)"""
        if chat_id not in self.games:
            return False, "⚠️ هیچ بازی فعالی وجود ندارد!"
        
        game = self.games[chat_id]
        
        if not game['started']:
            return False, "⚠️ بازی هنوز شروع نشده!"
        
        if not game['waiting_for_response']:
            return False, "⚠️ هیچ سوال/جرات فعالی وجود ندارد!"
        
        current_player = game['players'][game['current_player_index'] % len(game['players'])]
        
        if current_player['id'] != user_id:
            return False, f"⚠️ این سوال/جرات برای شما نیست!\n\n🎯 برای: {current_player['name']}"
        
        # بررسی زمان
        if game['task_start_time']:
            elapsed = (datetime.now() - game['task_start_time']).seconds
            max_time = Config.WAIT_FOR_ANSWER if game['game_type'] == 'truth' else Config.WAIT_FOR_DARE
            
            if elapsed > max_time:
                game['waiting_for_response'] = False
                game['current_task'] = None
                game['task_start_time'] = None
                self.db.save_game(chat_id, game)
                return False, "⏰ زمان تمام شد!\n\nبه صورت خودکار رد شد."
        
        # افزایش امتیاز
        game['scores'][current_player['name']] += 1
        current_player['score'] += 1
        
        # رفتن به بازیکن بعدی
        game['current_player_index'] += 1
        next_player = game['players'][game['current_player_index'] % len(game['players'])]
        
        # ریست وضعیت
        game['current_task'] = None
        game['task_start_time'] = None
        game['waiting_for_response'] = False
        game['last_activity'] = datetime.now()
        
        self.db.save_game(chat_id, game)
        
        logger.info(f"{current_player['name']} کار را تکمیل کرد در چت {chat_id}")
        
        # ایجاد کیبورد جدید
        keyboard = RubikaAPI.create_keyboard(["❓ حقیقت", "🎯 جرات", "📊 امتیازات", "⏭️ نفر بعدی"])
        
        message = f"""
✅ **{current_player['name']} کار را تکمیل کرد!**

🏅 **امتیاز جدید:** {current_player['score']}

⏭️ **نوبت:** {next_player['name']}

📌 **انتخاب کنید:**
❓ **حقیقت** - سوال صادقانه
🎯 **جرات** - کار جالب
📊 **امتیازات** - جدول امتیازات
        """
        
        return True, message, keyboard
    
    def skip_task(self, chat_id, user_id):
        """رد کردن سوال/جرات"""
        if chat_id not in self.games:
            return False, "⚠️ هیچ بازی فعالی وجود ندارد!"
        
        game = self.games[chat_id]
        
        if not game['started']:
            return False, "⚠️ بازی هنوز شروع نشده!"
        
        if not game['waiting_for_response']:
            return False, "⚠️ هیچ سوال/جرات فعالی وجود ندارد!"
        
        current_player = game['players'][game['current_player_index'] % len(game['players'])]
        
        if current_player['id'] != user_id:
            return False, f"⚠️ این سوال/جرات برای شما نیست!\n\n🎯 برای: {current_player['name']}"
        
        # کاهش امتیاز (حداقل صفر)
        new_score = max(0, game['scores'][current_player['name']] - 1)
        game['scores'][current_player['name']] = new_score
        current_player['score'] = new_score
        
        # رفتن به بازیکن بعدی
        game['current_player_index'] += 1
        next_player = game['players'][game['current_player_index'] % len(game['players'])]
        
        # ریست وضعیت
        game['current_task'] = None
        game['task_start_time'] = None
        game['waiting_for_response'] = False
        game['last_activity'] = datetime.now()
        
        self.db.save_game(chat_id, game)
        
        logger.info(f"{current_player['name']} سوال را رد کرد در چت {chat_id}")
        
        # ایجاد کیبورد
        keyboard = RubikaAPI.create_keyboard(["❓ حقیقت", "🎯 جرات", "📊 امتیازات", "⏭️ نفر بعدی"])
        
        message = f"""
⏭️ **{current_player['name']} سوال را رد کرد!**

🏅 **امتیاز جدید:** {current_player['score']}

⏭️ **نوبت:** {next_player['name']}

📌 **انتخاب کنید:**
❓ **حقیقت** - سوال صادقانه
🎯 **جرات** - کار جالب
📊 **امتیازات** - جدول امتیازات
        """
        
        return True, message, keyboard
    
    def get_scores(self, chat_id):
        """دریافت جدول امتیازات"""
        if chat_id not in self.games:
            return False, "⚠️ هیچ بازی فعالی وجود ندارد!\n\nبرای شروع:\n/play"
        
        game = self.games[chat_id]
        
        if self.is_game_expired(game):
            del self.games[chat_id]
            return False, "⚠️ بازی منقضی شده!"
        
        # مرتب‌سازی بر اساس امتیاز
        sorted_scores = sorted(game['scores'].items(), key=lambda x: x[1], reverse=True)
        
        scoreboard = "🏆 **جدول امتیازات**\n\n"
        
        for i, (player, score) in enumerate(sorted_scores):
            if i == 0:
                medal = "🥇"
            elif i == 1:
                medal = "🥈"
            elif i == 2:
                medal = "🥉"
            else:
                medal = "🔸"
            
            # پیدا کردن بازیکن فعلی
            is_current = False
            if game['started']:
                current_idx = game['current_player_index'] % len(game['players'])
                current_player = game['players'][current_idx]
                if current_player['name'] == player:
                    is_current = True
            
            current_marker = "🎯 " if is_current else ""
            scoreboard += f"{medal} {current_marker}{player}: {score} امتیاز\n"
        
        if game['started']:
            current_idx = game['current_player_index'] % len(game['players'])
            current_player = game['players'][current_idx]
            scoreboard += f"\n🎮 **بازیکن فعلی:** {current_player['name']}"
        
        scoreboard += f"\n\n👥 **تعداد بازیکنان:** {len(game['players'])}"
        
        # ایجاد کیبورد
        keyboard = RubikaAPI.create_keyboard(["🎮 ادامه بازی", "👥 بازیکنان", "❌ پایان بازی"])
        
        return True, scoreboard, keyboard
    
    def get_players(self, chat_id):
        """دریافت لیست بازیکنان"""
        if chat_id not in self.games:
            return False, "⚠️ هیچ بازی فعالی وجود ندارد!\n\nبرای شروع:\n/play"
        
        game = self.games[chat_id]
        
        players_list = "\n".join([f"• {p['name']} ({p['score']} امتیاز)" for p in game['players']])
        
        message = f"""
👥 **بازیکنان** ({len(game['players'])} نفر)

{players_list}

{"🎮 بازی در حال انجام" if game['started'] else "⏳ در انتظار شروع"}
{"⏰ در حال پاسخگویی" if game['waiting_for_response'] else ""}
        """
        
        # ایجاد کیبورد
        keyboard = RubikaAPI.create_keyboard(["🎮 ادامه بازی", "📊 امتیازات", "❌ ترک بازی"])
        
        return True, message, keyboard
    
    def end_game(self, chat_id, user_id):
        """پایان بازی"""
        if chat_id not in self.games:
            return False, "⚠️ هیچ بازی فعالی وجود ندارد!"
        
        game = self.games[chat_id]
        
        if game['creator_id'] != user_id:
            creator_name = self.get_user_name(game['creator_id'])
            return False, f"⚠️ فقط سازنده ({creator_name}) می‌تواند بازی را پایان دهد!"
        
        # ذخیره نتایج نهایی
        sorted_scores = sorted(game['scores'].items(), key=lambda x: x[1], reverse=True)
        
        final_results = "🎮 **نتایج نازی بازی**\n\n"
        
        for i, (player, score) in enumerate(sorted_scores):
            if i == 0:
                medal = "👑 قهرمان"
            elif i == 1:
                medal = "🥈 نائب قهرمان"
            elif i == 2:
                medal = "🥉 مقام سوم"
            else:
                medal = "🎖️ شرکت کننده"
            
            final_results += f"{medal}: {player} - {score} امتیاز\n"
        
        final_results += f"\n👥 تعداد بازیکنان: {len(game['players'])}"
        final_results += f"\n⏱️ مدت بازی: {(datetime.now() - game['created_at']).seconds // 60} دقیقه"
        
        # حذف بازی
        del self.games[chat_id]
        self.db.delete_game(chat_id)
        
        logger.info(f"بازی در چت {chat_id} پایان یافت")
        
        # ایجاد کیبورد برای بازی جدید
        keyboard = RubikaAPI.create_keyboard(["🎮 بازی جدید", "📋 راهنما", "👋 خداحافظ"])
        
        message = f"""
{final_results}

✅ **بازی با موفقیت پایان یافت!**

برای شروع بازی جدید:
🎮 /play
        """
        
        return True, message, keyboard
    
    def leave_game(self, chat_id, user_id):
        """ترک بازی"""
        if chat_id not in self.games:
            return False, "⚠️ شما در هیچ بازی فعالی عضو نیستید!"
        
        game = self.games[chat_id]
        
        # پیدا کردن بازیکن
        player_index = -1
        player_name = ""
        
        for i, player in enumerate(game['players']):
            if player['id'] == user_id:
                player_index = i
                player_name = player['name']
                break
        
        if player_index == -1:
            return False, "⚠️ شما در این بازی عضو نیستید!"
        
        # اگر سازنده بازی را ترک کند
        if user_id == game['creator_id']:
            if len(game['players']) > 1:
                # سازنده جدید انتخاب شود
                new_creator_index = 1 if player_index == 0 else 0
                game['creator_id'] = game['players'][new_creator_index]['id']
                game['creator_name'] = game['players'][new_creator_index]['name']
            else:
                # اگر فقط یک نفر بود، بازی بسته شود
                del self.games[chat_id]
                self.db.delete_game(chat_id)
                return True, "✅ بازی بسته شد چون همه بازیکنان ترک کردند."
        
        # حذف بازیکن
        del game['players'][player_index]
        del game['player_ids'][player_index]
        
        # اگر بازی شروع شده بود و نوبت این بازیکن بود
        if game['started'] and game['current_player_index'] >= player_index:
            game['current_player_index'] -= 1
        
        # اگر بازیکنی باقی نماند
        if not game['players']:
            del self.games[chat_id]
            self.db.delete_game(chat_id)
            return True, "✅ بازی بسته شد چون همه بازیکنان ترک کردند."
        
        game['last_activity'] = datetime.now()
        self.db.save_game(chat_id, game)
        
        remaining_players = len(game['players'])
        
        return True, f"✅ {player_name} بازی را ترک کرد.\n\n👥 بازیکنان باقی‌مانده: {remaining_players} نفر"
    
    def is_game_expired(self, game):
        """بررسی منقضی شدن بازی"""
        elapsed = (datetime.now() - game['last_activity']).seconds
        return elapsed > 7200  # 2 ساعت
    
    def check_timeouts(self):
        """بررسی زمان‌سنج‌های بازی"""
        current_time = datetime.now()
        chats_to_notify = []
        
        for chat_id, game in self.games.items():
            if game['waiting_for_response'] and game['task_start_time']:
                elapsed = (current_time - game['task_start_time']).seconds
                
                if game['game_type'] == 'truth' and elapsed > Config.WAIT_FOR_ANSWER:
                    chats_to_notify.append((chat_id, 'truth'))
                elif game['game_type'] == 'dare' and elapsed > Config.WAIT_FOR_DARE:
                    chats_to_notify.append((chat_id, 'dare'))
        
        for chat_id, game_type in chats_to_notify:
            self.handle_timeout(chat_id, game_type)
    
    def handle_timeout(self, chat_id, game_type):
        """مدیریت زمان تمام شده"""
        if chat_id not in self.games:
            return
        
        game = self.games[chat_id]
        
        if not game['waiting_for_response']:
            return
        
        current_player = game['players'][game['current_player_index'] % len(game['players'])]
        
        # کاهش امتیاز برای تمام شدن زمان
        new_score = max(0, game['scores'][current_player['name']] - 1)
        game['scores'][current_player['name']] = new_score
        current_player['score'] = new_score
        
        # رفتن به بازیکن بعدی
        game['current_player_index'] += 1
        next_player = game['players'][game['current_player_index'] % len(game['players'])]
        
        # ریست وضعیت
        game['current_task'] = None
        game['task_start_time'] = None
        game['waiting_for_response'] = False
        game['last_activity'] = datetime.now()
        
        self.db.save_game(chat_id, game)
        
        # ارسال پیام اخطار
        timeout_msg = f"""
⏰ **زمان تمام شد!**

{current_player['name']} زمان پاسخ {f'سوال حقیقت' if game_type == 'truth' else 'انجام جرات'} را از دست داد.

🏅 **امتیاز جدید:** {current_player['score']}

⏭️ **نوبت:** {next_player['name']}

📌 **انتخاب کنید:**
❓ /truth - سوال حقیقت
🎯 /dare - سوال جرات
        """
        
        RubikaAPI.send_message(chat_id, timeout_msg)
        logger.info(f"زمان تمام شد برای {current_player['name']} در چت {chat_id}")
    
    def cleanup_old_games(self):
        """پاک‌سازی بازی‌های قدیمی"""
        current_time = datetime.now()
        chats_to_remove = []
        
        for chat_id, game in self.games.items():
            elapsed = (current_time - game['last_activity']).seconds
            if elapsed > 7200:  # 2 ساعت
                chats_to_remove.append(chat_id)
        
        for chat_id in chats_to_remove:
            del self.games[chat_id]
            self.db.delete_game(chat_id)
            logger.info(f"بازی قدیمی در چت {chat_id} پاک شد.")
            
            # ارسال پیام انقضا
            expire_msg = "⏰ **بازی به دلیل عدم فعالیت بسته شد.**\n\nبرای شروع بازی جدید:\n🎮 /play"
            RubikaAPI.send_message(chat_id, expire_msg)

# ============ دیتابیس ============
class Database:
    """مدیریت پایگاه داده SQLite"""
    
    def __init__(self):
        self.db_file = "truth_dare_games.db"
        self.init_database()
    
    def init_database(self):
        """ایجاد جداول دیتابیس"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # جدول بازی‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    chat_id TEXT PRIMARY KEY,
                    game_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول آمار کاربران
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_stats (
                    user_id TEXT,
                    chat_id TEXT,
                    username TEXT,
                    total_games INTEGER DEFAULT 0,
                    total_score INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    last_played TIMESTAMP,
                    PRIMARY KEY (user_id, chat_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("پایگاه داده راه‌اندازی شد.")
        except Exception as e:
            logger.error(f"خطا در راه‌اندازی دیتابیس: {e}")
    
    def save_game(self, chat_id, game_data):
        """ذخیره بازی در دیتابیس"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            game_json = json.dumps(game_data)
            
            cursor.execute('''
                INSERT OR REPLACE INTO games (chat_id, game_data, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (chat_id, game_json))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"خطا در ذخیره بازی: {e}")
            return False
    
    def load_game(self, chat_id):
        """بارگذاری بازی از دیتابیس"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT game_data FROM games WHERE chat_id = ?', (chat_id,))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return json.loads(result[0])
            return None
        except Exception as e:
            logger.error(f"خطا در بارگذاری بازی: {e}")
            return None
    
    def delete_game(self, chat_id):
        """حذف بازی از دیتابیس"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM games WHERE chat_id = ?', (chat_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"خطا در حذف بازی: {e}")
            return False

# ============ سرور وب‌هوک ============
class RobicaWebhookHandler(BaseHTTPRequestHandler):
    """Handler برای دریافت وب‌هوک از Robica"""
    
    game_manager = GameManager()
    
    def log_message(self, format, *args):
        """لاگ پیام‌های سرور"""
        logger.info(f"HTTP {format % args}")
    
    def do_GET(self):
        """درخواست GET برای چک کردن سلامت"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            status_html = """
            <!DOCTYPE html>
            <html dir="rtl">
            <head>
                <meta charset="UTF-8">
                <title>ربات جرأت یا حقیقت</title>
                <style>
                    body {
                        font-family: Tahoma, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        text-align: center;
                        padding: 50px;
                    }
                    .container {
                        background: rgba(255, 255, 255, 0.1);
                        backdrop-filter: blur(10px);
                        border-radius: 20px;
                        padding: 40px;
                        max-width: 800px;
                        margin: 0 auto;
                        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    }
                    h1 {
                        color: #FFD700;
                        margin-bottom: 30px;
                    }
                    .status {
                        background: rgba(255, 255, 255, 0.2);
                        border-radius: 15px;
                        padding: 20px;
                        margin: 20px 0;
                    }
                    .emoji {
                        font-size: 48px;
                        margin: 20px;
                    }
                    .command {
                        background: rgba(255, 255, 255, 0.15);
                        border-radius: 10px;
                        padding: 10px;
                        margin: 10px 0;
                        text-align: right;
                        font-family: monospace;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="emoji">🎮</div>
                    <h1>ربات جرأت یا حقیقت</h1>
                    
                    <div class="status">
                        <h2>✅ ربات فعال است!</h2>
                        <p>ربات آماده دریافت پیام‌ها از Robica می‌باشد.</p>
                        <p>🕐 زمان سرور: """ + datetime.now().strftime("%Y/%m/%d - %H:%M:%S") + """</p>
                        <p>🎯 بازی‌های فعال: """ + str(len(self.game_manager.games)) + """</p>
                    </div>
                    
                    <h3>🎮 دستورات اصلی:</h3>
                    <div class="command">/start یا /help - راهنمای بازی</div>
                    <div class="command">/play - ایجاد بازی جدید</div>
                    <div class="command">/join - عضویت در بازی</div>
                    <div class="command">/truth - سوال حقیقت</div>
                    <div class="command">/dare - سوال جرات</div>
                    <div class="command">/scores - جدول امتیازات</div>
                    
                    <p style="margin-top: 40px; font-size: 14px; opacity: 0.8;">
                        توسعه داده شده برای Robica | نسخه 2.0
                    </p>
                </div>
            </body>
            </html>
            """
            
            self.wfile.write(status_html.encode('utf-8'))
            
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status_data = {
                'status': 'online',
                'timestamp': datetime.now().isoformat(),
                'active_games': len(self.game_manager.games),
                'version': '2.0',
                'bot_name': 'Truth or Dare Bot'
            }
            
            self.wfile.write(json.dumps(status_data, indent=2, ensure_ascii=False).encode('utf-8'))
        
        else:
            self.send_error(404, "صفحه پیدا نشد")
    
    def do_POST(self):
        """دریافت وب‌هوک از Robica"""
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length == 0:
            self.send_error(400, "بدون داده")
            return
        
        post_data = self.rfile.read(content_length)
        
        try:
            # پارس کردن JSON دریافتی
            data = json.loads(post_data.decode('utf-8'))
            logger.info(f"📥 دریافت داده از Robica: {json.dumps(data, ensure_ascii=False)}")
            
            # پردازش Update
            response = self.process_update(data)
            
            # ارسال پاسخ
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ خطا در پارس JSON: {e}")
            self.send_error(400, "JSON نامعتبر")
        except Exception as e:
            logger.error(f"❌ خطا در پردازش: {e}")
            self.send_error(500, "خطای سرور")
    
    def process_update(self, data):
        """پردازش Update دریافتی از Robica"""
        try:
            # بررسی نوع Update
            if 'inline_message' in data:
                return self.process_inline_message(data['inline_message'])
            elif 'update' in data:
                return self.process_update_message(data['update'])
            else:
                logger.warning("⚠️ فرمت داده ناشناخته")
                return {'status': 'ignored', 'reason': 'unknown_format'}
                
        except Exception as e:
            logger.error(f"❌ خطا در process_update: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def process_inline_message(self, inline_msg):
        """پردازش inline message (کلیک روی دکمه)"""
        try:
            chat_id = inline_msg.get('chat_id')
            user_id = inline_msg.get('sender_id')
            text = inline_msg.get('text', '').strip()
            button_id = inline_msg.get('aux_data', {}).get('button_id')
            message_id = inline_msg.get('message_id')
            
            logger.info(f"📱 Inline: chat={chat_id}, user={user_id}, text='{text}', button={button_id}")
            
            # پردازش بر اساس متن دکمه
            if text == "❓ حقیقت":
                return self.handle_command(chat_id, user_id, "/truth")
            elif text == "🎯 جرات":
                return self.handle_command(chat_id, user_id, "/dare")
            elif text == "📊 امتیازات":
                return self.handle_command(chat_id, user_id, "/scores")
            elif text == "👥 بازیکنان":
                return self.handle_command(chat_id, user_id, "/players")
            elif text == "✅ پاسخ دادم":
                return self.handle_command(chat_id, user_id, "/done")
            elif text == "✅ انجام دادم":
                return self.handle_command(chat_id, user_id, "/done")
            elif text == "⏭️ رد کن":
                return self.handle_command(chat_id, user_id, "/skip")
            elif text == "🎮 ادامه بازی":
                return self.handle_command(chat_id, user_id, "/continue")
            elif text == "❌ پایان بازی":
                return self.handle_command(chat_id, user_id, "/end")
            elif text == "❌ ترک بازی":
                return self.handle_command(chat_id, user_id, "/leave")
            elif text == "🎮 بازی جدید":
                return self.handle_command(chat_id, user_id, "/play")
            elif text == "📋 راهنما":
                return self.handle_command(chat_id, user_id, "/help")
            elif text == "⏰ زمان":
                return self.handle_command(chat_id, user_id, "/time")
            elif text == "⏭️ نفر بعدی":
                return self.handle_command(chat_id, user_id, "/next")
            
            return {'status': 'processed', 'button': button_id}
            
        except Exception as e:
            logger.error(f"❌ خطا در process_inline_message: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def process_update_message(self, update_data):
        """پردازش update message (پیام جدید)"""
        try:
            chat_id = update_data.get('chat_id')
            new_message = update_data.get('new_message', {})
            user_id = new_message.get('sender_id')
            text = new_message.get('text', '').strip()
            message_id = new_message.get('message_id')
            
            logger.info(f"📨 Update: chat={chat_id}, user={user_id}, text='{text}'")
            
            # نادیده گرفتن پیام‌های خالی
            if not text:
                return {'status': 'ignored', 'reason': 'empty_message'}
            
            # پردازش دستور
            if text.startswith('/'):
                return self.handle_command(chat_id, user_id, text, message_id)
            else:
                # پاسخ به پیام‌های معمولی
                return self.handle_text_message(chat_id, user_id, text, message_id)
                
        except Exception as e:
            logger.error(f"❌ خطا در process_update_message: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def handle_command(self, chat_id, user_id, command, message_id=None):
        """پردازش دستورات"""
        try:
            command = command.strip().lower()
            logger.info(f"🎮 دستور: {command} از {user_id} در {chat_id}")
            
            # جداسازی دستور و آرگومان‌ها
            parts = command.split()
            cmd = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            response_text = ""
            keyboard = None
            
            # پردازش دستورات
            if cmd in ['/start', '/help']:
                response_text = self.get_help_message()
                keyboard = RubikaAPI.create_keyboard(["🎮 بازی جدید", "📋 راهنما", "ℹ️ اطلاعات"])
            
            elif cmd == '/play':
                success, message = self.game_manager.create_game(chat_id, user_id)
                response_text = message
            
            elif cmd == '/join':
                success, message = self.game_manager.join_game(chat_id, user_id)
                response_text = message
            
            elif cmd == '/startgame':
                success, message, keyboard = self.game_manager.start_game(chat_id, user_id)
                response_text = message
            
            elif cmd == '/truth':
                success, message, keyboard = self.game_manager.get_truth(chat_id, user_id)
                response_text = message
            
            elif cmd == '/dare':
                success, message, keyboard = self.game_manager.get_dare(chat_id, user_id)
                response_text = message
            
            elif cmd == '/done':
                success, message, keyboard = self.game_manager.complete_task(chat_id, user_id)
                response_text = message
            
            elif cmd == '/skip':
                success, message, keyboard = self.game_manager.skip_task(chat_id, user_id)
                response_text = message
            
            elif cmd == '/scores':
                success, message, keyboard = self.game_manager.get_scores(chat_id)
                response_text = message
            
            elif cmd == '/players':
                success, message, keyboard = self.game_manager.get_players(chat_id)
                response_text = message
            
            elif cmd == '/end':
                success, message, keyboard = self.game_manager.end_game(chat_id, user_id)
                response_text = message
            
            elif cmd == '/leave':
                success, message = self.game_manager.leave_game(chat_id, user_id)
                response_text = message
            
            elif cmd == '/time':
                response_text = self.get_time_message()
            
            elif cmd == '/next':
                # رفتن به بازیکن بعدی
                if chat_id in self.game_manager.games:
                    game = self.game_manager.games[chat_id]
                    if game['started']:
                        game['current_player_index'] += 1
                        next_player = game['players'][game['current_player_index'] % len(game['players'])]
                        response_text = f"⏭️ رفت به بازیکن بعدی!\n\n🎯 نوبت: {next_player['name']}"
                    else:
                        response_text = "⚠️ بازی هنوز شروع نشده!"
                else:
                    response_text = "⚠️ هیچ بازی فعالی وجود ندارد!"
            
            elif cmd == '/continue':
                # ادامه بازی
                if chat_id in self.game_manager.games:
                    game = self.game_manager.games[chat_id]
                    if game['started']:
                        current_player = game['players'][game['current_player_index'] % len(game['players'])]
                        response_text = f"🎮 ادامه بازی\n\n🎯 نوبت: {current_player['name']}\n🏅 امتیاز: {current_player['score']}"
                        keyboard = RubikaAPI.create_keyboard(["❓ حقیقت", "🎯 جرات", "📊 امتیازات"])
                    else:
                        response_text = "⚠️ بازی هنوز شروع نشده!\n\nسازنده باید /startgame را بفرستد."
                else:
                    response_text = "⚠️ هیچ بازی فعالی وجود ندارد!\n\nبرای شروع:\n/play"
            
            else:
                response_text = "⚠️ دستور ناشناخته!\n\nبرای راهنما:\n/help"
            
            # ارسال پاسخ
            if response_text:
                RubikaAPI.send_message(chat_id, response_text, reply_to=message_id, keyboard=keyboard)
            
            return {'status': 'processed', 'command': cmd}
            
        except Exception as e:
            logger.error(f"❌ خطا در handle_command: {e}")
            error_msg = "⚠️ خطا در پردازش دستور!\n\nلطفاً دوباره تلاش کنید."
            RubikaAPI.send_message(chat_id, error_msg, reply_to=message_id)
            return {'status': 'error', 'message': str(e)}
    
    def handle_text_message(self, chat_id, user_id, text, message_id):
        """پردازش پیام متنی معمولی"""
        try:
            # پاسخ به پیام‌های غیردستوری
            responses = [
                "🎮 برای شروع بازی 'جرأت یا حقیقت' دستور /play را بفرستید!",
                "🤔 به نظر می‌رسد می‌خواهید بازی کنید! دستور /help را بفرستید.",
                "🎯 بازی جالبی داریم! برای اطلاعات بیشتر /start را بفرستید.",
                "😊 سلام! برای بازی 'جرأت یا حقیقت' دستور /play را امتحان کنید."
            ]
            
            # اگر در حال بازی هستیم
            if chat_id in self.game_manager.games:
                game = self.game_manager.games[chat_id]
                if game['waiting_for_response']:
                    current_player = game['players'][game['current_player_index'] % len(game['players'])]
                    if current_player['id'] == user_id:
                        response = f"✅ {current_player['name']} پیام ارسال کرد!\n\nبرای ثبت پاسخ رسمی از دکمه‌ها استفاده کنید."
                        RubikaAPI.send_message(chat_id, response, reply_to=message_id)
                        return {'status': 'noted'}
            
            # پاسخ تصادفی
            response = random.choice(responses)
            RubikaAPI.send_message(chat_id, response, reply_to=message_id)
            
            return {'status': 'replied'}
            
        except Exception as e:
            logger.error(f"❌ خطا در handle_text_message: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_help_message(self):
        """پیام راهنما"""
        return """
🎮 **راهنمای بازی جرأت یا حقیقت**

📌 **دستورات اصلی:**
/play - ایجاد بازی جدید
/join - عضویت در بازی
/startgame - شروع بازی (سازنده)
/truth - سوال حقیقت
/dare - سوال جرات
/scores - جدول امتیازات
/players - لیست بازیکنان
/end - پایان بازی (سازنده)
/leave - ترک بازی

🎯 **نحوه بازی:**
1. با /play بازی را ایجاد کنید
2. دیگران با /join عضو شوند
3. سازنده با /startgame بازی را شروع کند
4. هر بازیکن به نوبت /truth یا /dare بفرستد
5. به سوال پاسخ دهید یا کار را انجام دهید
6. امتیازات با /scores قابل مشاهده است

⚡ **قوانین:**
• پاسخ‌ها باید صادقانه باشد
• جرات‌ها باید انجام شوند
• زمان پاسخ: ۳ دقیقه
• زمان جرات: ۵ دقیقه
• رد کردن سوال: -۱ امتیاز

⏰ **نکات:**
• بازی پس از ۲ ساعت عدم فعالیت بسته می‌شود
• حداقل ۲ نفر برای شروع نیاز است
• فقط سازنده می‌تواند بازی را پایان دهد

😊 **لذت ببرید و محترمانه بازی کنید!**
        """
    
    def get_time_message(self):
        """پیام زمان"""
        current_time = datetime.now()
        persian_time = current_time.strftime("%Y/%m/%d - %H:%M:%S")
        
        return f"""
⏰ **زمان سرور:**
{persian_time}

🕐 **مدت بازی‌های فعال:**
{len(self.game_manager.games)} بازی در حال اجرا

⚡ **ربات آماده خدمات‌رسانی است!**
        """

# ============ راه‌اندازی سرور ============
def start_webhook_server():
    """شروع سرور وب‌هوک"""
    try:
        server_address = (Config.SERVER_HOST, Config.SERVER_PORT)
        httpd = HTTPServer(server_address, RobicaWebhookHandler)
        
        logger.info(f"🚀 سرور وب‌هوک شروع شد: http://{Config.SERVER_HOST}:{Config.SERVER_PORT}")
        logger.info(f"🤖 ربات آماده دریافت پیام‌ها از Robica")
        logger.info(f"🔑 توکن ربات: {Config.BOT_TOKEN[:10]}...")
        
        print("\n" + "="*60)
        print("🎮 **ربات جرأت یا حقیقت برای Robica**")
        print("="*60)
        print(f"🔗 آدرس سرور: http://{Config.SERVER_HOST}:{Config.SERVER_PORT}")
        print(f"🤖 توکن ربات: {Config.BOT_TOKEN[:15]}...")
        print(f"🕐 زمان شروع: {datetime.now().strftime('%Y/%m/%d - %H:%M:%S')}")
        print("="*60)
        print("\n📱 برای تست ربات در Robica:")
        print("1. ربات را در @BotFather ساخته‌اید")
        print("2. این آدرس را به عنوان Webhook تنظیم کنید:")
        print(f"   http://YOUR_SERVER_IP:{Config.SERVER_PORT}")
        print("3. در Robica به ربات پیام بفرستید")
        print("\n⏳ در حال اجرا... (Ctrl+C برای خروج)")
        print("="*60)
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        logger.info("🛑 سرور متوقف شد (KeyboardInterrupt)")
        print("\n\n🛑 ربات متوقف شد!")
    except Exception as e:
        logger.error(f"❌ خطا در شروع سرور: {e}")
        print(f"\n❌ خطا: {e}")

# ============ اجرای برنامه ============
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎮 راه‌اندازی ربات جرأت یا حقیقت برای Robica")
    print("="*60)
    
    # بررسی توکن
    if Config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ خطا: لطفاً توکن ربات خود را در Config.BOT_TOKEN وارد کنید!")
        print("توکن شما: GIIJJ0DWRJGREKPRNJJXNSGGJVJNGWMMZGUWKZZSKEBUCFKFVEUNOHKZIWVKCGTL")
        exit(1)
    
    # شروع سرور
    start_webhook_server()
