#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات جرأت یا حقیقت برای Robica
نسخه ساده و کامل
"""

from flask import Flask, request, jsonify
import requests
import random
import json
from datetime import datetime

# ============ تنظیمات ============
app = Flask(__name__)

# توکن ربات شما
TOKEN = "GIIJJ0DWRJGREKPRNJJXNSGGJVJNGWMMZGUWKZZSKEBUCFKFVEUNOHKZIWVKCGTL"
API_URL = "https://botapi.rubika.ir/v3/"

print("=" * 60)
print("🤖 ربات جرأت یا حقیقت برای Robica")
print(f"🔑 توکن: {TOKEN[:15]}...")
print("=" * 60)

# ذخیره بازی‌ها
games = {}

# ============ بانک سوالات ============
TRUTH_QUESTIONS = [
    "چه کسی توی این جمع از همه خوشگلتره؟",
    "تا حالا مواد مخدر مصرف کردی؟",
    "به کی از گپ علاقه داری؟",
    "بدترین دروغی که گفتي چيه؟",
    "آخرین باری که گریه کردی کی بود؟",
    "کسی هستی که پنهانی دوستش داری؟",
    "اگر ۱ میلیارد تومان داشته باشی چی می‌خری؟",
    "بدترین کاری که کردی چیه؟",
    "تا حالا دزدی کردی؟",
    "زیباترین خاطره‌ات چیه؟",
    "آیا تا حالا کسی رو گول زدی؟",
    "راز بزرگی که هیچکس نمی‌دونه چیه؟",
    "اگر می‌تونستی نامرئی بشی چی کار می‌کردی؟",
    "بدترین عادتت چیه؟",
    "آیا تا حالا تقلب کردی؟",
    "چه چیزی رو بیشتر از همه پشیمونی؟",
    "آیا تا حالا کتک کاری کردی؟",
    "ترسناک‌ترین کاری که کردی چیه؟",
    "آیا تا حالا سیگار کشیدی؟",
    "چیزی هست که از والدینت پنهون کردی؟"
]

DARE_TASKS = [
    "برای ۵ دقیقه عکس پروفایلت رو به عکس حیوان تغییر بده",
    "یک آهنگ عاشقانه بلند بخون",
    "آخرین پیام پیویت رو در گپ بفرست",
    "به یکی از مخاطبینت زنگ بزن و بگو 'دوستت دارم'",
    "سلفی با حالت خنده‌دار بگیر",
    "برای ۱ دقیقه مثل بچه گریه کن",
    "آهنگ تولدت رو بخون",
    "به مامانت زنگ بزن و بگو دوستت دارم",
    "با صدای کارتون صحبت کن",
    "مثل یک گوینده اخبار صحبت کن",
    "یک داستان دروغ تعریف کن",
    "برقص و ویدیو بفرست",
    "اسم ۳ نفر از گپ رو بگو که فکر می‌کنی باهوشن",
    "از پنجره‌ات عکس بگیر و بفرست",
    "یک شعر بخون",
    "حالت چهره گربه رو در بیار",
    "۱۰ بار بگو 'من گوسفندم'",
    "یک حرکت رقص اختراع کن",
    "مثل دکتر صحبت کن",
    "آخرین عکس گالریت رو نشون بده"
]

# ============ توابع کمکی ============
def call_rubika_api(method, data):
    """فراخوانی API روبیکا"""
    url = f"{API_URL}{TOKEN}/{method}"
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ خطا در API: {e}")
        return None

def send_message(chat_id, text, reply_to=None):
    """ارسال پیام به روبیکا"""
    data = {
        "chat_id": chat_id,
        "text": text[:2000]
    }
    if reply_to:
        data["reply_to"] = reply_to
    
    result = call_rubika_api("sendMessage", data)
    if result and result.get("status") == "OK":
        print(f"✅ پیام به {chat_id} ارسال شد")
        return True
    else:
        print(f"❌ خطا در ارسال: {result}")
        return False

# ============ وب‌هوک‌ها ============
@app.route('/receiveUpdate', methods=['POST', 'GET'])
def handle_receive_update():
    """دریافت پیام‌های معمولی"""
    print(f"\n📥 دریافت در /receiveUpdate - Method: {request.method}")
    
    if request.method == 'GET':
        return jsonify({
            "status": "active",
            "endpoint": "receiveUpdate",
            "message": "برای دریافت پیام‌های معمولی از POST استفاده کنید"
        })
    
    try:
        data = request.json
        print(f"📦 داده دریافتی:\n{json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
        
        if 'inline_message' in data:
            msg = data['inline_message']
            chat_id = msg.get('chat_id')
            user_id = msg.get('sender_id')
            text = msg.get('text', '').strip()
            message_id = msg.get('message_id')
            
            print(f"👤 کاربر: {user_id}")
            print(f"💬 متن: '{text}'")
            print(f"🗨️ چت: {chat_id}")
            
            # ============ پردازش دستورات ============
            if text in ["/start", "/help", "شروع", "راهنما"]:
                welcome_msg = """
🎮 **ربات جرأت یا حقیقت**

سلام! به بازی جذاب «جرأت یا حقیقت» خوش آمدید!

📌 **دستورات اصلی:**
/play - ساخت بازی جدید
/truth - سوال حقیقت بگیر
/dare - جرات بگیر
/players - بازیکنان رو ببین
/scores - امتیازات رو ببین
/end - بازی رو تموم کن

🎯 **نحوه بازی:**
1. با /play بازی بساز
2. با /truth سوال حقیقت بگیر
3. با /dare جرات بگیر
4. صادقانه جواب بده یا جرات رو انجام بده

⚡ **قوانین:**
• باید راست بگی
• جرات‌ها رو باید انجام بدی
• می‌تونی با /skip رد کنی

😊 **لذت ببر!**
                """
                send_message(chat_id, welcome_msg, reply_to=message_id)
                
            elif text in ["/play", "بازی", "شروع بازی"]:
                if chat_id not in games:
                    games[chat_id] = {
                        'creator': user_id,
                        'players': [user_id],
                        'player_names': {user_id: "بازیکن ۱"},
                        'scores': {user_id: 0},
                        'current_turn': 0,
                        'started': False,
                        'questions_used': [],
                        'dares_used': [],
                        'created_at': datetime.now()
                    }
                    send_message(chat_id, 
                        "🎮 **بازی جدید ساخته شد!**\n\n"
                        "👤 سازنده: شما\n"
                        "👥 بازیکنان: ۱ نفر\n\n"
                        "به دیگران بگو با دستور /join عضو بشن.\n"
                        "بعدش با /startgame بازی رو شروع کن.",
                        reply_to=message_id)
                else:
                    send_message(chat_id, 
                        "⚠️ **یه بازی فعال داریم!**\n\n"
                        "برای عضویت:\n/join\n\n"
                        "برای شروع:\n/startgame\n\n"
                        "برای دیدن بازیکنان:\n/players",
                        reply_to=message_id)
                        
            elif text in ["/join", "عضو شو"]:
                if chat_id in games:
                    game = games[chat_id]
                    if user_id not in game['players']:
                        game['players'].append(user_id)
                        player_num = len(game['players'])
                        game['player_names'][user_id] = f"بازیکن {player_num}"
                        game['scores'][user_id] = 0
                        
                        send_message(chat_id,
                            f"✅ **عضویت موفق!**\n\n"
                            f"👤 بازیکن جدید اضافه شد\n"
                            f"👥 تعداد بازیکنان: {player_num} نفر\n\n"
                            f"{'🎮 بازی شروع شده' if game['started'] else '⏳ منتظر شروع توسط سازنده'}",
                            reply_to=message_id)
                    else:
                        send_message(chat_id, "⚠️ تو قبلاً عضو بازی هستی!", reply_to=message_id)
                else:
                    send_message(chat_id, 
                        "⚠️ **هیچ بازی فعالی نیست!**\n\n"
                        "برای ساخت بازی جدید:\n/play",
                        reply_to=message_id)
                        
            elif text in ["/startgame", "شروع کن"]:
                if chat_id in games:
                    game = games[chat_id]
                    if game['creator'] == user_id:
                        if len(game['players']) >= 2:
                            game['started'] = True
                            current_player = game['players'][0]
                            
                            send_message(chat_id,
                                f"🎉 **بازی شروع شد!**\n\n"
                                f"👥 بازیکنان: {len(game['players'])} نفر\n"
                                f"🎯 نوبت: {game['player_names'][current_player]}\n\n"
                                f"📌 **حالا می‌تونی انتخاب کنی:**\n"
                                f"• /truth - سوال حقیقت بگیر\n"
                                f"• /dare - جرات بگیر\n\n"
                                f"⏰ زمان پاسخ: ۳ دقیقه",
                                reply_to=message_id)
                        else:
                            send_message(chat_id,
                                "⚠️ **حداقل ۲ بازیکن نیازه!**\n\n"
                                "از بقیه بخواه با /join عضو بشن.",
                                reply_to=message_id)
                    else:
                        send_message(chat_id,
                            f"⚠️ **فقط سازنده می‌تونه بازی رو شروع کنه!**\n\n"
                            f"سازنده: {game['player_names'][game['creator']]}",
                            reply_to=message_id)
                else:
                    send_message(chat_id, "⚠️ هیچ بازی فعالی نیست!", reply_to=message_id)
                    
            elif text in ["/truth", "حقیقت", "سوال"]:
                if chat_id in games:
                    game = games[chat_id]
                    if game['started']:
                        current_player_id = game['players'][game['current_turn'] % len(game['players'])]
                        
                        if user_id == current_player_id:
                            # انتخاب سوال جدید
                            available = [q for q in TRUTH_QUESTIONS if q not in game['questions_used']]
                            if not available:
                                game['questions_used'] = []
                                available = TRUTH_QUESTIONS
                            
                            question = random.choice(available)
                            game['questions_used'].append(question)
                            
                            send_message(chat_id,
                                f"❓ **سوال حقیقت**\n\n"
                                f"👤 برای: {game['player_names'][user_id]}\n"
                                f"🏅 امتیاز: {game['scores'][user_id]}\n\n"
                                f"📝 **سوال:**\n{question}\n\n"
                                f"⏰ **۳ دقیقه وقت داری جواب بدی**\n\n"
                                f"✅ بعد از جواب:\n/done - ثبت کن\n"
                                f"⏭️ اگر نمی‌خواهی جواب بدی:\n/skip - رد کن",
                                reply_to=message_id)
                        else:
                            current_player_name = game['player_names'][current_player_id]
                            send_message(chat_id,
                                f"⚠️ **نوبت تو نیست!**\n\n"
                                f"🎯 نوبت: {current_player_name}\n"
                                f"⏳ صبر کن...",
                                reply_to=message_id)
                    else:
                        send_message(chat_id,
                            "⚠️ **بازی هنوز شروع نشده!**\n\n"
                            "سازنده باید با /startgame بازی رو شروع کنه.",
                            reply_to=message_id)
                else:
                    send_message(chat_id, "⚠️ هیچ بازی فعالی نیست!", reply_to=message_id)
                    
            elif text in ["/dare", "جرات", "چالش"]:
                if chat_id in games:
                    game = games[chat_id]
                    if game['started']:
                        current_player_id = game['players'][game['current_turn'] % len(game['players'])]
                        
                        if user_id == current_player_id:
                            # انتخاب جرات جدید
                            available = [d for d in DARE_TASKS if d not in game['dares_used']]
                            if not available:
                                game['dares_used'] = []
                                available = DARE_TASKS
                            
                            dare = random.choice(available)
                            game['dares_used'].append(dare)
                            
                            send_message(chat_id,
                                f"🎯 **جرات**\n\n"
                                f"👤 برای: {game['player_names'][user_id]}\n"
                                f"🏅 امتیاز: {game['scores'][user_id]}\n\n"
                                f"📝 **کار:**\n{dare}\n\n"
                                f"⏰ **۵ دقیقه وقت داری انجامش بدی**\n\n"
                                f"✅ بعد از انجام:\n/done - ثبت کن\n"
                                f"⏭️ اگر نمی‌خواهی انجام بدی:\n/skip - رد کن",
                                reply_to=message_id)
                        else:
                            current_player_name = game['player_names'][current_player_id]
                            send_message(chat_id,
                                f"⚠️ **نوبت تو نیست!**\n\n"
                                f"🎯 نوبت: {current_player_name}",
                                reply_to=message_id)
                    else:
                        send_message(chat_id, "⚠️ بازی هنوز شروع نشده!", reply_to=message_id)
                else:
                    send_message(chat_id, "⚠️ هیچ بازی فعالی نیست!", reply_to=message_id)
                    
            elif text in ["/players", "بازیکنان", "لیست"]:
                if chat_id in games:
                    game = games[chat_id]
                    players_list = ""
                    for i, player_id in enumerate(game['players']):
                        players_list += f"{i+1}. {game['player_names'][player_id]} - {game['scores'][player_id]} امتیاز\n"
                    
                    send_message(chat_id,
                        f"👥 **لیست بازیکنان**\n\n"
                        f"{players_list}\n"
                        f"🎮 وضعیت: {'شروع شده' if game['started'] else 'در انتظار'}\n"
                        f"🎯 نوبت: {game['player_names'][game['players'][game['current_turn'] % len(game['players'])]] if game['started'] else 'هنوز شروع نشده'}",
                        reply_to=message_id)
                else:
                    send_message(chat_id, "⚠️ هیچ بازی فعالی نیست!", reply_to=message_id)
                    
            elif text in ["/scores", "امتیازات", "نمره"]:
                if chat_id in games:
                    game = games[chat_id]
                    scores_list = ""
                    sorted_scores = sorted(game['scores'].items(), key=lambda x: x[1], reverse=True)
                    
                    for i, (player_id, score) in enumerate(sorted_scores):
                        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🔸"
                        scores_list += f"{medal} {game['player_names'][player_id]}: {score} امتیاز\n"
                    
                    send_message(chat_id,
                        f"🏆 **جدول امتیازات**\n\n"
                        f"{scores_list}\n"
                        f"👥 تعداد بازیکنان: {len(game['players'])}",
                        reply_to=message_id)
                else:
                    send_message(chat_id, "⚠️ هیچ بازی فعالی نیست!", reply_to=message_id)
                    
            elif text in ["/done", "انجام دادم", "جواب دادم"]:
                if chat_id in games:
                    game = games[chat_id]
                    if game['started']:
                        current_player_id = game['players'][game['current_turn'] % len(game['players'])]
                        
                        if user_id == current_player_id:
                            # افزایش امتیاز
                            game['scores'][user_id] += 1
                            game['current_turn'] += 1
                            
                            next_player_id = game['players'][game['current_turn'] % len(game['players'])]
                            
                            send_message(chat_id,
                                f"✅ **عالی! کارت رو انجام دادی**\n\n"
                                f"👤 بازیکن: {game['player_names'][user_id]}\n"
                                f"🎖️ امتیاز جدید: {game['scores'][user_id]}\n\n"
                                f"⏭️ **نوبت بعدی:**\n"
                                f"{game['player_names'][next_player_id]}\n\n"
                                f"📌 می‌تونه انتخاب کنه:\n"
                                f"/truth - سوال حقیقت\n"
                                f"/dare - سوال جرات",
                                reply_to=message_id)
                        else:
                            current_name = game['player_names'][current_player_id]
                            send_message(chat_id, f"⚠️ نوبت {current_name} است!", reply_to=message_id)
                    else:
                        send_message(chat_id, "⚠️ بازی شروع نشده!", reply_to=message_id)
                else:
                    send_message(chat_id, "⚠️ هیچ بازی فعالی نیست!", reply_to=message_id)
                    
            elif text in ["/skip", "رد کن", "نمی‌خواهم"]:
                if chat_id in games:
                    game = games[chat_id]
                    if game['started']:
                        current_player_id = game['players'][game['current_turn'] % len(game['players'])]
                        
                        if user_id == current_player_id:
                            # کاهش امتیاز (حداقل صفر)
                            game['scores'][user_id] = max(0, game['scores'][user_id] - 1)
                            game['current_turn'] += 1
                            
                            next_player_id = game['players'][game['current_turn'] % len(game['players'])]
                            
                            send_message(chat_id,
                                f"⏭️ **سوال رو رد کردی**\n\n"
                                f"👤 بازیکن: {game['player_names'][user_id]}\n"
                                f"🎖️ امتیاز جدید: {game['scores'][user_id]}\n\n"
                                f"⏭️ **نوبت بعدی:**\n"
                                f"{game['player_names'][next_player_id]}\n\n"
                                f"📌 می‌تونه انتخاب کنه:\n"
                                f"/truth - سوال حقیقت\n"
                                f"/dare - سوال جرات",
                                reply_to=message_id)
                        else:
                            current_name = game['player_names'][current_player_id]
                            send_message(chat_id, f"⚠️ نوبت {current_name} است!", reply_to=message_id)
                    else:
                        send_message(chat_id, "⚠️ بازی شروع نشده!", reply_to=message_id)
                else:
                    send_message(chat_id, "⚠️ هیچ بازی فعالی نیست!", reply_to=message_id)
                    
            elif text in ["/end", "تموم کن", "پایان"]:
                if chat_id in games:
                    game = games[chat_id]
                    if game['creator'] == user_id:
                        # نمایش نتایج
                        results = "🏆 **نتایج نهایی بازی**\n\n"
                        sorted_players = sorted(game['scores'].items(), key=lambda x: x[1], reverse=True)
                        
                        for i, (player_id, score) in enumerate(sorted_players):
                            if i == 0:
                                medal = "🥇 قهرمان"
                            elif i == 1:
                                medal = "🥈 نائب قهرمان"
                            elif i == 2:
                                medal = "🥉 مقام سوم"
                            else:
                                medal = "🎖️ شرکت کننده"
                            
                            results += f"{medal}: {game['player_names'][player_id]} - {score} امتیاز\n"
                        
                        results += f"\n👥 تعداد بازیکنان: {len(game['players'])}"
                        
                        send_message(chat_id, results, reply_to=message_id)
                        
                        # حذف بازی
                        del games[chat_id]
                        print(f"🗑️ بازی در چت {chat_id} پایان یافت")
                    else:
                        send_message(chat_id,
                            f"⚠️ **فقط سازنده می‌تونه بازی رو تموم کنه!**\n\n"
                            f"سازنده: {game['player_names'][game['creator']]}",
                            reply_to=message_id)
                else:
                    send_message(chat_id, "⚠️ هیچ بازی فعالی نیست!", reply_to=message_id)
            
            else:
                # پاسخ به پیام‌های دیگر
                if text and text.startswith('/'):
                    send_message(chat_id, 
                        f"دستور '{text}' رو دریافت کردم!\n"
                        f"برای شروع بازی /play رو بفرست.\n"
                        f"برای راهنما /help رو بفرست.",
                        reply_to=message_id)
                elif text:
                    responses = [
                        "برای بازی از دستورات استفاده کن! /help",
                        "می‌خواهی بازی کنی؟ /play",
                        "جرأت یا حقیقت؟ انتخاب کن! /play",
                        "دستورات بازی: /start"
                    ]
                    response = random.choice(responses)
                    send_message(chat_id, response, reply_to=message_id)
        
        return jsonify({"status": "ok", "message": "پیام پردازش شد"})
        
    except Exception as e:
        print(f"❌ خطا در پردازش: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/receiveInlineMessage', methods=['POST', 'GET'])
def handle_receive_inline_message():
    """دریافت کلیک روی دکمه‌های شیشه‌ای"""
    print(f"\n📱 دریافت در /receiveInlineMessage - Method: {request.method}")
    
    if request.method == 'GET':
        return jsonify({
            "status": "active",
            "endpoint": "receiveInlineMessage",
            "message": "برای دریافت کلیک روی دکمه‌ها از POST استفاده کنید"
        })
    
    try:
        data = request.json
        print(f"📱 داده دکمه: {data}")
        
        if 'update' in data:
            update = data['update']
            chat_id = update.get('chat_id')
            new_message = update.get('new_message', {})
            text = new_message.get('text', '').strip()
            button_id = new_message.get('aux_data', {}).get('button_id')
            
            print(f"🔘 دکمه: '{text}' | ID: {button_id}")
            
            if text == "شروع بازی":
                send_message(chat_id, "برای شروع بازی دستور /play رو بفرست.")
            elif text == "سوال حقیقت":
                send_message(chat_id, "برای سوال حقیقت دستور /truth رو بفرست.")
            elif text == "سوال جرات":
                send_message(chat_id, "برای سوال جرات دستور /dare رو بفرست.")
            elif text == "امتیازات":
                send_message(chat_id, "برای دیدن امتیازات دستور /scores رو بفرست.")
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        print(f"❌ خطا در پردازش دکمه: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============ صفحه اصلی و وضعیت ============
@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>ربات جرأت یا حقیقت</title>
        <style>
            body { 
                font-family: Tahoma, Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 30px; 
                text-align: center; 
                margin: 0;
                min-height: 100vh;
            }
            .container { 
                background: rgba(255,255,255,0.1); 
                backdrop-filter: blur(10px); 
                border-radius: 20px; 
                padding: 40px; 
                max-width: 800px; 
                margin: 0 auto; 
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                border: 1px solid rgba(255,255,255,0.2);
            }
            h1 { 
                color: #FFD700; 
                margin-bottom: 25px;
                font-size: 2.5em;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .status { 
                background: rgba(0,255,0,0.2); 
                border-radius: 15px; 
                padding: 20px; 
                margin: 25px 0; 
                border: 1px solid rgba(0,255,0,0.3);
            }
            .command { 
                background: rgba(255,255,255,0.15); 
                border-radius: 10px; 
                padding: 12px 15px; 
                margin: 10px 0; 
                text-align: right; 
                font-family: 'Courier New', monospace;
                font-size: 16px;
                border: 1px solid rgba(255,255,255,0.1);
                transition: all 0.3s;
            }
            .command:hover {
                background: rgba(255,255,255,0.25);
                transform: translateX(-5px);
            }
            .emoji {
                font-size: 60px;
                margin: 20px 0;
                display: block;
            }
            .game-stats {
                background: rgba(255,215,0,0.15);
                border-radius: 10px;
                padding: 15px;
                margin: 20px 0;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="emoji">🎮</span>
            <h1>🤖 ربات جرأت یا حقیقت</h1>
            
            <div class="status">
                <h2>✅ ربات فعال و آماده است!</h2>
                <p>ربات آماده دریافت پیام از Robica می‌باشد</p>
                <div class="game-stats">
                    <p>🎯 بازی‌های فعال: """ + str(len(games)) + """</p>
                    <p>🕐 زمان سرور: """ + datetime.now().strftime("%Y/%m/%d - %H:%M:%S") + """</p>
                </div>
            </div>
            
            <h3>🎮 دستورات اصلی ربات:</h3>
            <div class="command">/start یا /help - راهنمای بازی</div>
            <div class="command">/play - ساخت بازی جدید</div>
            <div class="command">/join - عضویت در بازی</div>
            <div class="command">/truth - دریافت سوال حقیقت</div>
            <div class="command">/dare - دریافت سوال جرات</div>
            <div class="command">/players - نمایش بازیکنان</div>
            <div class="command">/scores - نمایش امتیازات</div>
            <div class="command">/end - پایان بازی</div>
            
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
                <p style="font-size: 14px; opacity: 0.8;">
                    🌐 آدرس‌های Webhook:<br>
                    • <code>/receiveUpdate</code> - برای پیام‌ها<br>
                    • <code>/receiveInlineMessage</code> - برای دکمه‌ها
                </p>
                <p style="font-size: 14px; opacity: 0.8; margin-top: 20px;">
                    توسعه داده شده برای Robica | نسخه 3.0
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/status')
def status():
    return jsonify({
        "status": "online",
        "active_games": len(games),
        "endpoints": {
            "receiveUpdate": "active",
            "receiveInlineMessage": "active"
        },
        "version": "3.0",
        "timestamp": datetime.now().isoformat()
    })

# ============ اجرای برنامه ============
if __name__ == '__main__':
    print("\n🌐 Webhook های فعال:")
    print("• /receiveUpdate - برای دریافت پیام‌های معمولی")
    print("• /receiveInlineMessage - برای دریافت کلیک روی دکمه‌ها")
    print("\n🚀 ربات آماده دریافت پیام از Robica...")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=10000, debug=False)
