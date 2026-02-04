from flask import Flask, request, jsonify
import requests, random, os, json, time, threading

app = Flask(__name__)

TOKEN = "GIIJJ0DWRJGREKPRNJJXNSGGJVJNGWMMZGUWKZZSKEBUCFKFVEUNOHKZIWVKCGTL"
API = "https://botapi.rubika.ir/v3"
DATA_FILE = "data.json"
TURN_TIME = 60  # ثانیه

TRUTHS = [
    "بزرگ‌ترین رازت چیه؟",
    "آخرین دروغی که گفتی چی بود؟",
    "به کی تو این گروه علاقه داری؟"
]

DARES = [
    "۳ تا ایموجی پشت سر هم بفرست",
    "اسم ۲ نفر که دوستشون داری رو بگو",
    "۵ بار بگو من خیلی خفنم 😎"
]

def load():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

games = load()

def api(method, data):
    return requests.post(f"{API}/{TOKEN}/{method}", json=data).json()

def send(chat_id, text, keyboard=None):
    payload = {"chat_id": chat_id, "text": text}
    if keyboard:
        payload["inline_keyboard"] = keyboard
    api("sendMessage", payload)

def score_table(game):
    s = "🏆 امتیازها:\n"
    for p in game["players"].values():
        s += f"{p['name']} : {p['score']}\n"
    return s

def next_turn(chat_id):
    game = games.get(chat_id)
    if not game or not game["started"]:
        return
    game["turn"] += 1
    game["turn_time"] = time.time()
    save(games)
    uid = game["order"][game["turn"] % len(game["order"])]
    send(chat_id,
         f"نوبت {game['players'][uid]['name']}",
         [[{"text": "😇 حقیقت", "callback_data": "truth"},
           {"text": "🔥 جرأت", "callback_data": "dare"}]])

def timer_loop():
    while True:
        time.sleep(5)
        now = time.time()
        for chat_id, game in list(games.items()):
            if game.get("started") and now - game.get("turn_time", now) > TURN_TIME:
                next_turn(chat_id)

threading.Thread(target=timer_loop, daemon=True).start()

@app.route("/receiveUpdate", methods=["POST"])
def update():
    data = request.json
    upd = data.get("update") or data.get("inline_message")
    if not upd:
        return jsonify(ok=True)

    chat_id = upd["chat_id"]
    text = upd.get("text", "")
    user_id = upd.get("sender_id")
    name = upd.get("sender_name", "کاربر")
    cb = upd.get("callback_data")

    game = games.get(chat_id)

    if text == "/play":
        games[chat_id] = {
            "creator": user_id,
            "players": {},
            "order": [],
            "turn": 0,
            "started": False,
            "turn_time": time.time()
        }
        save(games)
        send(chat_id, "🎮 بازی ساخته شد",
             [[{"text": "➕ عضویت", "callback_data": "join"}],
              [{"text": "▶️ شروع بازی", "callback_data": "start"}]])

    elif cb == "join" and game and not game["started"]:
        if user_id not in game["players"]:
            game["players"][user_id] = {"name": name, "score": 0}
            game["order"].append(user_id)
            save(games)
            send(chat_id, f"✅ {name} وارد بازی شد")

    elif cb == "start" and game and user_id == game["creator"]:
        if len(game["order"]) < 2:
            send(chat_id, "❌ حداقل ۲ نفر")
        else:
            game["started"] = True
            game["turn_time"] = time.time()
            save(games)
            uid = game["order"][0]
            send(chat_id,
                 f"🚀 شروع شد\nنوبت {game['players'][uid]['name']}",
                 [[{"text": "😇 حقیقت", "callback_data": "truth"},
                   {"text": "🔥 جرأت", "callback_data": "dare"}]])

    elif cb in ["truth", "dare"] and game and game["started"]:
        uid = game["order"][game["turn"] % len(game["order"])]
        if user_id == uid:
            q = random.choice(TRUTHS if cb == "truth" else DARES)
            send(chat_id, q,
                 [[{"text": "✅ انجام شد", "callback_data": "done"},
                   {"text": "🚪 خروج", "callback_data": "leave"}]])

    elif cb == "done" and game:
        uid = game["order"][game["turn"] % len(game["order"])]
        if user_id == uid:
            game["players"][uid]["score"] += 1
            save(games)
            send(chat_id, score_table(game))
            next_turn(chat_id)

    elif cb == "leave" and game and user_id in game["players"]:
        game["players"].pop(user_id)
        game["order"].remove(user_id)
        save(games)
        send(chat_id, f"{name} از بازی خارج شد")

    elif text == "/end" and game and user_id == game["creator"]:
        games.pop(chat_id)
        save(games)
        send(chat_id, "🛑 بازی پایان یافت")

    return jsonify(ok=True)

@app.route("/")
def home():
    return "Rubika Ultimate Truth/Dare Bot Running"
