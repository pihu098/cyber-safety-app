from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import random
import string
import re
from datetime import date, timedelta
import time
import requests
import mysql.connector
import os
os 
app = Flask(__name__)
app.secret_key = "secret123"

app.permanent_session_lifetime = timedelta(days=365)  # 1 YEAR LOGIN
print("🔥 App starting...")

@app.route('/')
def home_page():
    return render_template("index.html")

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 🔥 safe create
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ADMIN_PASSWORD = "priyanrkp098"  # changable.........

#-----------------------puzzle---------------
word_puzzles = [
    {"jumbled": "phsiihng", "answer": "phishing"},
    {"jumbled": "pwaorssd", "answer": "password"},
    {"jumbled": "HSIPINGH", "answer": "PHISHING"},
    {"jumbled": "RVIUS", "answer": "VIRUS"},
    {"jumbled": "HSIPINGH", "answer": "PHISHING"},
    {"jumbled": "LMAREWA", "answer": "MALWARE"},
    {"jumbled": "SPYAREWA", "answer": "SPYWARE"},
    {"jumbled": "RANSMOWARE", "answer": "RANSOMWARE"},
    {"jumbled": "VIRSU", "answer": "VIRUS"},
    {"jumbled": "OTPW", "answer": "OTP"},
    {"jumbled": "KCAHRE", "answer": "HACKER"},
    {"jumbled": "ERWALLIF", "answer": "FIREWALL"},
    {"jumbled": "SUSREVI", "answer": "VIRUSES"},
    {"jumbled": "DORWSSAP", "answer": "PASSWORD"},
    {"jumbled": "ETCNEPIONRCY", "answer": "ENCRYPTION"},
    {"jumbled": "ATAD", "answer": "DATA"},
    {"jumbled": "YTIRUCES", "answer": "SECURITY"},
    {"jumbled": "SSECCA", "answer": "ACCESS"},
    {"jumbled": "GNIGOL", "answer": "LOGGING"},
    {"jumbled": "PUKCAB", "answer": "BACKUP"},
    {"jumbled": "ETANIDUOTR", "answer": "ROUTINATED"},
    {"jumbled": "RESU", "answer": "USER"},
    {"jumbled": "TENRETNI", "answer": "INTERNET"},
    {"jumbled": "KROWTEN", "answer": "NETWORK"}
]


sentence_puzzles = [
{
"question": "What is malware?",
"words": ["malware", "is", "harmful", "software"],
"answer": "malware is harmful software"
},
{
"question": "What is phishing?",
"words": ["phishing", "is", "a", "fake", "message"],
"answer": "phishing is a fake message"
},
{
"question": "Why use strong passwords?",
"words": ["strong", "passwords", "protect", "accounts"],
"answer": "strong passwords protect accounts"
},
{
"question": "What is OTP?",
"words": ["otp", "is", "one", "time", "password"],
"answer": "otp is one time password"
},
{
"question": "Why avoid public WiFi?",
"words": ["public", "wifi", "is", "not", "secure"],
"answer": "public wifi is not secure"
},
{
"question": "What is a hacker?",
"words": ["hacker", "tries", "to", "access", "data"],
"answer": "hacker tries to access data"
},
{
"question": "Why update apps?",
"words": ["updates", "fix", "security", "issues"],
"answer": "updates fix security issues"
},
{
"question": "What is antivirus?",
"words": ["antivirus", "protects", "from", "viruses"],
"answer": "antivirus protects from viruses"
},
{
"question": "Why backup data?",
"words": ["backup", "keeps", "data", "safe"],
"answer": "backup keeps data safe"
},
{
"question": "What is encryption?",
"words": ["encryption", "protects", "data"],
"answer": "encryption protects data"
},
{
"question": "Why logout after use?",
"words": ["logout", "prevents", "unauthorized", "access"],
"answer": "logout prevents unauthorized access"
},
{
"question": "What is firewall?",
"words": ["firewall", "blocks", "unauthorized", "access"],
"answer": "firewall blocks unauthorized access"
},
{
"question": "Why avoid unknown links?",
"words": ["unknown", "links", "may", "be", "dangerous"],
"answer": "unknown links may be dangerous"
},
{
"question": "What is data theft?",
"words": ["data", "theft", "means", "stealing", "data"],
"answer": "data theft means stealing data"
},
{
"question": "Why use 2FA?",
"words": ["2fa", "adds", "extra", "security"],
"answer": "2fa adds extra security"
},
{
"question": "What is spam?",
"words": ["spam", "is", "unwanted", "messages"],
"answer": "spam is unwanted messages"
},
{
"question": "Why secure WiFi?",
"words": ["secure", "wifi", "protects", "network"],
"answer": "secure wifi protects network"
},
{
"question": "What is cyber attack?",
"words": ["cyber", "attack", "targets", "systems"],
"answer": "cyber attack targets systems"
},
{
"question": "Why not share password?",
"words": ["sharing", "passwords", "is", "unsafe"],
"answer": "sharing passwords is unsafe"
},
{
"question": "What is secure browsing?",
"words": ["secure", "browsing", "protects", "users"],
"answer": "secure browsing protects users"
},
{
        "question": "Arrange the sentence:",
        "words": ["data", "steal", "fake", "website", "to"],
        "answer": "fake website to steal data"
},

{
        "question": "Arrange the sentence:",
        "words": ["accounts", "protect", "to"],
        "answer": "to protect accounts"
},
{
        "question": "Arrange sentence:",
        "words": ["never", "password", "share", "your"],
        "answer": "never share your password"
},
{
        "question": "Arrange sentence:",
        "words": ["use", "strong", "always", "password"],
        "answer": "always use strong password"
},
{
        "question": "What is malware?",
        "words": ["malware", "is", "harmful", "software"],
        "answer": "malware is harmful software"
},
{
        "question": "What is phishing?",
        "words": ["phishing", "is", "fake", "message"],
        "answer": "phishing is fake message"
},
]
#-------puzzle game-----------------
puzzle_levels = {
    1: [
        {"q": "What should you do if you receive an unknown link?", 
         "options": ["Click it", "Ignore it", "Share it", "Download it"], 
         "a": "Ignore it"},

        {"q": "What is a strong password?", 
         "options": ["123456", "name123", "J@hn#91!", "abcd"], 
         "a": "J@hn#91!"},

        {"q": "What should you do with an OTP?", 
         "options": ["Share it", "Save it", "Never share it", "Post it online"], 
         "a": "Never share it"},
    ],

    2: [
        {"q": "Is public WiFi safe for banking?", 
         "options": ["Yes", "No", "Sometimes", "Depends"], 
         "a": "No"},

        {"q": "What does phishing mean?", 
         "options": ["Game", "Fake website to steal data", "App", "Virus"], 
         "a": "Fake website to steal data"},

        {"q": "What should you do with unknown email attachments?", 
         "options": ["Open them", "Delete them", "Save them", "Forward them"], 
         "a": "Delete them"},
    ],

    3: [
        {"q": "What is the purpose of 2FA (two-factor authentication)?", 
         "options": ["Increase security", "Increase speed", "Hack", "None"], 
         "a": "Increase security"},

        {"q": "What does HTTPS stand for?", 
         "options": ["Secure", "Fast", "Virus", "Hack"], 
         "a": "Secure"},

        {"q": "Is reusing passwords safe?", 
         "options": ["Safe", "Risky", "Best practice", "Normal"], 
         "a": "Risky"},
    ],

    4: [
{"q": "Is a 'free money' link safe?", 
"options": ["Real", "Fake", "Safe", "Trusted"], 
"a": "Fake"},

{"q": "What is the purpose of antivirus software?", 
"options": ["Hack systems", "Protect devices", "Slow down system", "Delete files"], 
"a": "Protect devices"},

{"q": "Should Bluetooth be always on?", 
"options": ["Always", "Only when needed", "Never", "Randomly"], 
"a": "Only when needed"},

{"q": "What should you do if you receive an unknown link?",
"options": ["Click it", "Ignore it", "Share it", "Download it"],
"a": "Ignore it"},

{"q": "What is phishing?",
"options": ["Safe email", "Fake message", "Strong password", "App update"],
"a": "Fake message"},

{"q": "What is malware?",
"options": ["Safe app", "Harmful software", "Game", "Browser"],
"a": "Harmful software"},

{"q": "What should you never share?",
"options": ["Name", "OTP", "Age", "City"],
"a": "OTP"},

{"q": "What does antivirus do?",
"options": ["Delete files", "Protect system", "Slow PC", "Open apps"],
"a": "Protect system"},

{"q": "What is a strong password?",
"options": ["1234", "password", "abc", "Mix of letters and symbols"],
"a": "Mix of letters and symbols"},

{"q": "Why use 2FA?",
"options": ["For fun", "Extra security", "Faster login", "Games"],
"a": "Extra security"},

{"q": "What is public WiFi risk?",
"options": ["Fast speed", "Free internet", "Data theft", "Strong signal"],
"a": "Data theft"},

{"q": "What is a hacker?",
"options": ["Gamer", "Security expert", "Unauthorized access person", "Teacher"],
"a": "Unauthorized access person"},

{"q": "Why update apps?",
"options": ["New bugs", "Security fix", "Slow device", "Delete data"],
"a": "Security fix"},

{"q": "What is OTP?",
"options": ["Password", "One-time code", "Username", "Email"],
"a": "One-time code"},

{"q": "What is spam?",
"options": ["Important mail", "Unwanted messages", "Games", "Photos"],
"a": "Unwanted messages"},

{"q": "Why logout?",
"options": ["Save time", "Prevent access", "Open apps", "Download"],
"a": "Prevent access"},

{"q": "What is encryption?",
"options": ["Delete data", "Protect data", "Send data", "Copy data"],
"a": "Protect data"},

{"q": "Why not click popups?",
"options": ["Safe", "Fun", "Risky", "Fast"],
"a": "Risky"},

{"q": "What is firewall?",
"options": ["Game", "Security system", "Browser", "File"],
"a": "Security system"},

{"q": "Why use backup?",
"options": ["Delete data", "Save data", "Slow system", "Hack"],
"a": "Save data"},

{"q": "What is cyber attack?",
"options": ["Game", "System attack", "Movie", "Song"],
"a": "System attack"},

{"q": "Why secure WiFi?",
"options": ["Speed", "Protection", "Games", "Fun"],
"a": "Protection"},

{"q": "What is safe browsing?",
"options": ["Click all links", "Use secure sites", "Download all", "Ignore warnings"],
"a": "Use secure sites"}

]
}
# ---------------- QUIZ ----------------
quiz = [
{"q":"What is phishing?", "a":"fake"},
{"q":"Should you share OTP?", "a":"no"},
{"q":"Strong password needed?", "a":"yes"},
{"q":"Is public WiFi safe?", "a":"no"},
{"q":"Is HTTPS secure?", "a":"yes"},
{"q":"Download unknown file?", "a":"no"},
{"q":"Use antivirus?", "a":"yes"},
{"q":"Click random links?", "a":"no"},
{"q":"Save password in browser?", "a":"no"},
{"q":"Update apps regularly?", "a":"yes"},

{"q":"Should you use 2FA?", "a":"yes"},
{"q":"Is 'free money' link safe?", "a":"no"},
{"q":"Check email sender?", "a":"yes"},
{"q":"Use same password everywhere?", "a":"no"},
{"q":"Is bank OTP shareable?", "a":"no"},
{"q":"Install apps from unknown sites?", "a":"no"},
{"q":"Is VPN useful?", "a":"yes"},
{"q":"Use public computer for banking?", "a":"no"},
{"q":"Enable firewall?", "a":"yes"},
{"q":"Click pop-up ads?", "a":"no"},

{"q":"Is antivirus important?", "a":"yes"},
{"q":"Use biometric lock?", "a":"yes"},
{"q":"Is long password better?", "a":"yes"},
{"q":"Use pirated software?", "a":"no"},
{"q":"Check URL spelling?", "a":"yes"},
{"q":"Trust unknown email attachments?", "a":"no"},
{"q":"Use cloud backup?", "a":"yes"},
{"q":"Disable Bluetooth when not needed?", "a":"yes"},
{"q":"Save passwords in plain text?", "a":"no"},
{"q":"Use strong PIN?", "a":"yes"},
{"q":"Share personal info online?", "a":"no"},
{"q":"Check app permissions?", "a":"yes"},
{"q":"Is public WiFi safe for payment?", "a":"no"},
{"q":"Use secure payment gateway?", "a":"yes"},
{"q":"Ignore software updates?", "a":"no"},
{"q":"Use encrypted messaging apps?", "a":"yes"},
{"q":"Trust urgent messages?", "a":"no"},
{"q":"Check login alerts?", "a":"yes"},
{"q":"Use password manager?", "a":"yes"},
{"q":"Click unknown USB devices?", "a":"no"}
]

# ---------------- DATABASE ---------------

def get_db():
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306)),
        autocommit=True
    )
    db.ping(reconnect=True)
    return db

def execute_query(query, params=(), fetch=False):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(query, params)

    if fetch:
        data = cursor.fetchall()
        db.close()
        return data

    db.commit()
    db.close()

def init_db():
    try:
        db = get_db()
        cursor = db.cursor()

        # ================= USERS TABLE =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),

            coins INT DEFAULT 0,
            xp INT DEFAULT 0,
            level INT DEFAULT 1,
            streak INT DEFAULT 0,
            logins INT DEFAULT 0,

            password_used INT DEFAULT 0,
            website_used INT DEFAULT 0,
            quiz_used INT DEFAULT 0,
            puzzle_wins INT DEFAULT 0,

            last_play_date DATE
        )
        """)

        # ================= UPDATES TABLE =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS updates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            content TEXT,
            filename VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ================= POSTS TABLE =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user VARCHAR(100),
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ================= PUZZLE PROGRESS TABLE (NEW 🔥) =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS puzzle_progress (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user VARCHAR(100),
            level INT DEFAULT 1,
            games_played INT DEFAULT 0,
            best_score INT DEFAULT 0,
            last_play DATE
        )
        """)

        

        db.commit()
        db.close()

        print("✅ ALL TABLES READY (users + updates + posts + puzzle_progress)")

    except mysql.connector.Error as err:
        print("❌ DB ERROR:", err)

    except Exception as e:
        print("❌ GENERAL ERROR:", e)

# 🔥 DEBUG (optional)
print("HOST =", os.getenv("DB_HOST"))
print("USER =", os.getenv("DB_USER"))
print("DB =", os.getenv("DB_NAME"))


init_db()


    
# ---------------- CYBER TIPS ----------------
tips_list = [
"Use strong passwords 🔐","Never share OTP 🚫","Check HTTPS before login 🌐",
"Avoid public WiFi for banking 📶","Enable 2FA 🔒","Don’t click unknown links ⚠️",
"Update apps regularly 🔄","Use antivirus 🛡️","Don’t download from unknown sites ❌",
"Keep backup 💾","Never reuse passwords 🔁","Use password manager 🔑",
"Verify email sender 📧","Logout after use 🔓","Use official apps ✔️",
"Avoid pirated software 🚫","Don’t trust free offers 🎁","Secure your WiFi 🔐",
"Use VPN on public network 🌍","Check URL spelling carefully 🔍",
"Don't save passwords in browser ⚠️","Turn on firewall 🔥",
"Be aware of phishing emails 🎣","Check app permissions 📱",
"Use biometric lock 🔒","Keep OS updated 🖥️","Use strong PIN 🔢",
"Avoid unknown USB devices 💾","Don't share personal info 🧠",
"Check website certificate 📜","Use encrypted messaging 🔐",
"Disable auto-connect WiFi 📶","Monitor account activity 👀",
"Use spam filters 📩","Don't click pop-ups 🚫",
"Use secure payment methods 💳","Check domain carefully 🌐",
"Don't trust urgent messages ⏳","Use cloud backup ☁️",
"Secure social media 🔒","Turn off Bluetooth when not needed 📡",
"Use trusted antivirus 🛡️","Never share passwords 🚫",
"Check file extensions 📁","Beware of fake apps 📱",
"Keep private data safe 🔐","Use multi-device security 📊",
"Check login alerts 🚨","Educate yourself on cyber safety 📘",
"Stay alert online always 👁️","🚨 If cyber fraud happens report at cybercrime.gov.in",
"📞 Call 1930 immediately in case of fraud",
"⚠️ Never trust unknown job offers",
"💳 Never share card details online",
"📧 Check email spelling carefully",
"🔗 Fake links look real — double check URL",
"📱 Don't install unknown apps",
" DO NOT CLICK RANDOM MESSAGES....",    
"🔒 Always lock your device when not in use",
"🧾 Regularly check bank statements for unknown activity",
"📵 Disable app permissions you don't need",
"🧑‍💻 Use different passwords for different accounts",
"🛑 Avoid saving passwords on shared devices",
"📡 Turn off WiFi & Bluetooth when not needed",
"🔍 check Google unknown websites before trusting them",
"🧠 Don't panic in urgent messages — think first",
"📦 Beware of fake delivery/scam messages",
"🎮 Don't trust free game hacks or cheats",
"💼 Verify job offers before applying",
"📧 Don't open attachments from unknown senders",
"🔑 Enable recovery email & phone for accounts",
"📲 Keep screen lock enabled (PIN/Pattern/Biometric)",
"⚙️ Review security settings regularly",
"📊 Check login history of your accounts",
"🚫 Avoid clicking shortened links (bit.ly etc.)",
"🌐 Use official websites only (avoid clones)",
"🛡️ Install apps only from Play Store/App Store",
"📁 Scan USB drives before opening files",
"📢 Do't overshare personal info on social media",
"🧠 Stay updated with latest cyber scams",
"🧠 Think before clicking anything online"
]
#------------question bank--------------
quiz_levels = {
    1: [
        {"q": "What is phishing?", "options": ["Fake website", "Game", "App", "Virus"], "a": "Fake website"},
        {"q": "Strong password should have?", "options": ["12345", "Name", "Symbols + numbers", "Only letters"], "a": "Symbols + numbers"},
    ],
    2: [
        {"q": "Should you share OTP?", "options": ["Yes", "No", "Sometimes", "Maybe"], "a": "No"},
        {"q": "Public WiFi is safe for banking?", "options": ["Yes", "No", "Always", "Depends"], "a": "No"},
    ],
}

# ---------------- AI RESPONSE ----------------
def ai_response(msg):
    msg = msg.lower()

    if "fraud" in msg or "scam" in msg:
        return """🚨 If you are victim of cyber fraud:
👉 Report: https://cybercrime.gov.in
📞 Call: 1930
Stay calm & act fast!"""

    elif "hlo" in msg or "hello" in msg:
        return "👋 Hello buddy! If you have any cyber safety queries, ask me."

    elif "otp" in msg:
        return "🚫 Never share OTP!"

    elif "phishing" in msg:
        return "🎣 Phishing is fake message to steal data"

    elif "how are you" in msg:
        return "😊 I'm good! Ready to help you stay safe online."

    elif "virus" in msg:
        return "🛡️ Use antivirus and avoid unknown downloads"

    elif "safe" in msg:
        return "🔐 Use HTTPS and strong passwords"

    elif "link" in msg:
        return "⚠️ Suspicious link ho sakta hai"

    elif "password" in msg:
        return "💪 Use strong password with symbols"

    elif "hi" in msg or "brother" in msg:
        return "Hlo brother/sister, do you have any question about cyber safety?"

    elif "hack" in msg or "hacked" in msg:
        return "⚠️ Stay safe! Avoid suspicious links and enable 2FA."

    elif "wifi" in msg:
        return "📶 Avoid public WiFi for sensitive activities like banking."

    elif "bank" in msg or "payment" in msg:
        return "💳 Use secure websites (HTTPS) and never share bank details."

    elif "cyber" in msg:
        return "🌐 Cyber safety means protecting your data and privacy online."

    # ---------------- HELPLINE SYSTEM (SMART ADDON) ----------------

    elif any(word in msg for word in ["women", "woman", "lady", "girl", "mahila", "harassment", "abuse"]):
        return "👩 Women Helpline: 📞 1091"

    elif any(word in msg for word in ["child", "kid", "bacha", "minor", "children"]):
        return "🧒 Child Helpline: 📞 1098"

    elif any(word in msg for word in ["police", "theft", "crime", "attack", "danger"]):
        return "🚓 Police Helpline: 📞 100"

    elif any(word in msg for word in ["ambulance", "medical", "hospital", "injury"]):
        return "🚑 Ambulance: 📞 102 / 108"

    elif any(word in msg for word in ["fire", "aag", "blast"]):
        return "🔥 Fire Emergency: 📞 101"

    elif any(word in msg for word in ["help", "helpline", "emergency", "number"]):
        return """📞 Important Helplines:

👩 Women: 1091  
🧒 Child: 1098  
🚓 Police: 100  
🚑 Ambulance: 102 / 108  
🔥 Fire: 101  
💻 Cyber Crime: 1930"""

    # ---------------- NORMAL FLOW ----------------

    elif "yes" in msg:
        return "Okay! Feel free to ask anything."

    elif "have a question" in msg:
        return "Sure! Ask me anything about cyber safety."

    elif "no" in msg:
        return "🙂 No problem! Ask something else."

    elif "thanks" in msg or "thank you" in msg:
        return "😊 You're welcome! Stay safe online."

    else:
        return "🤖 I can help with cyber safety, scams, passwords, suspicious links and helplines!"

def init_user():
    if 'coins' not in session:
        session['coins'] = 200
    if 'owned_chars' not in session:
        session['owned_chars'] = ["🤖"]
    if 'xp' not in session:
        session['xp'] = 0
    if 'level' not in session:
        session['level'] = 1


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    init_user()   # 👈 yaha lagana hai

    return render_template("dashboard.html",
        name=session['user'],
        level=session['level'],
        coins=session['coins'],
        streak=session['streak']
    )
# ---------------- LOGIN --------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    # 🔥 already logged in → skip login page
    if 'user' in session:
        return redirect('/welcome')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if not user:
            db.close()
            return render_template("result.html",
                                   result="❌ User not found",
                                   extra="Please signup first")

        if check_password_hash(user[3], password):

            # 🔥 update login count
            cursor.execute(
                "UPDATE users SET logins = COALESCE(logins,0) + 1 WHERE email=%s",
                (email,)
            )
            db.commit()

            # 🔥 SESSION (MAIN PART)
            
            session['user'] = user[1]     # name
            session['email'] = user[2]
            session.permanent = True
            db.close()
            return redirect('/home')

        else:
            db.close()
            return render_template("result.html",
                                   result="❌ Wrong Password",
                                   extra="Try again")

    return render_template("index.html")

@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect('/')
    return render_template("welcome.html", name=session['user'])

#---------------auto login check---------------
@app.route('/')
def index():
    # 🔥 auto-login if session exists
    if 'user' in session:
        return redirect('/home')
    return render_template("index.html")

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing = cursor.fetchone()

        if existing:
            db.close()
            return render_template("result.html",
                                   result="❌ Email already exists",
                                   extra="Try another email")

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )

        db.commit()
        db.close()

        # 🔥 AUTO LOGIN AFTER SIGNUP
        session.permanent = True
        session['user'] = name
        session['email'] = email

        return redirect('/home')

    return render_template("signup.html")
# ---------------- HOME ----------------
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')

    db = get_db()  # 🔥 fresh connection
    cursor = db.cursor(buffered=True)

    # 🔹 total users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # 🔹 total logins
    cursor.execute("SELECT SUM(logins) FROM users")
    total_logins = cursor.fetchone()[0] or 0

    # 🔹 user stats
    cursor.execute(
        "SELECT password_used, website_used, quiz_used, coins, level, xp, streak FROM users WHERE name=%s",
        (session['user'],)
    )
    data = cursor.fetchone()

    if data:
        password_used, website_used, quiz_used, coins, level, xp, streak = data
    else:
        password_used = website_used = quiz_used = 0
        coins = level = xp = streak = 0

    db.close()  # 🔥 important

    return render_template(
        "home.html",
        name=session['user'],
        message="✅ Welcome to Cyber Safety Platform",
        quiz_used=quiz_used,
        password_used=password_used,
        coins=coins,
        level=level,
        xp=xp,
        website_used=website_used,
        streak=streak
    )

    return redirect('/')

#-----------profile page--------------
#-----------profile page--------------
@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/')

    db = get_db()
    cursor = db.cursor(buffered=True)

    # 🔹 user ka latest data DB se lao
    cursor.execute("SELECT coins, level, xp FROM users WHERE name=%s", (session['user'],))
    data = cursor.fetchone()

    if data:
        coins, level, xp = data
    else:
        coins, level, xp = 200, 1, 0

    # 🔹 session sync
    session["coins"] = coins
    session["level"] = level
    session["xp"] = xp

    # 🔹 owned characters
    owned = session.get("owned_chars", ["🤖"])
    selected = session.get("selected_char", "🤖")

    characters = [
        {"emoji":"🤖","cost":0},
        {"emoji":"👨‍💻","cost":50},
        {"emoji":"🕵️‍♂️","cost":70},
        {"emoji":"👾","cost":100},
        {"emoji":"😈","cost":120},
        {"emoji":"💀","cost":150},
        {"emoji":"🧠","cost":80},
        {"emoji":"🛡️","cost":60},
        {"emoji":"⚡","cost":40},
        {"emoji":"🔥","cost":90}
    ]

    db.close()

    return render_template(
        "profile.html",
        name=session['user'],
        level=level,
        coins=coins,
        xp=xp,
        owned=owned,
        selected=selected,
        characters=characters
    )
   # 🔥 COMMON FUNCTION
def handle_buy(emoji, cost=None):
    coins = session.get("coins", 200)
    owned = session.get("owned_chars", ["🤖"])

    char_cost = {
        "👨‍💻":50, "🕵️‍♂️":70, "👾":100,
        "😈":120, "💀":150, "🧠":80,
        "🛡️":60, "⚡":40, "🔥":90
    }

    if cost is None:
        cost = char_cost.get(emoji, 0)

    if emoji not in owned and coins >= cost:
        coins -= cost
        owned.append(emoji)

        session["coins"] = coins
        session["owned_chars"] = owned
        session["selected_char"] = emoji

    return True

@app.route('/buy_char', methods=['POST'])
def buy_char():
    emoji = request.form.get("emoji")
    cost = int(request.form.get("cost"))

    handle_buy(emoji, cost)
    return "ok"

@app.route('/buy_char/<emoji>')
def buy_char_link(emoji):
    handle_buy(emoji)
    return redirect('/profile')
# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ----------------- COMMUNITY SYSTEM -----------------
@app.route('/community', methods=['GET', 'POST'])
def community():
    if 'user' not in session:
        return redirect('/')

    db=get_db()
    cursor = db.cursor(buffered=True)
    
    # POST = jab user kuch likh ke bhejega
    if request.method == 'POST':
        content = request.form.get('content')

        if content:
            cursor.execute(
                "INSERT INTO posts(user, content) VALUES(%s,%s)",
                (session['user'], content)
            )
            db.commit()

    # sab posts fetch karo
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()

    db.close()
    return render_template("community.html", posts=posts)

# ---------------- CHATBOT ----------------
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.form.get('message', "")
    return ai_response(user_msg)

# ---------------- PASSWORD GENERATOR ----------------
@app.route('/password', methods=['POST'])
def password():

    import random
    import string

    length = int(request.form.get('length', 8))
    chars = ""

    if 'upper' in request.form:
        chars += string.ascii_uppercase
    if 'lower' in request.form:
        chars += string.ascii_lowercase
    if 'digits' in request.form:
        chars += string.digits
    if 'symbols' in request.form:
        chars += "@#$%&*!?"

    pwd = ''.join(random.choice(chars) for _ in range(length))

    if 'user' in session:
        execute_query(
            "UPDATE users SET password_used = password_used + 1 WHERE name=%s",
            (session['user'],)
        )

    return render_template("result.html", result=pwd)
# ---------------- WEBSITE CHECK ----------------

@app.route('/check', methods=['POST'])
def check():
    import requests
    import re

    url = request.form.get('url', '').strip()

    score = 100
    warnings = []

    if not url:
        return "❌ No URL provided"

    # 🔥 FIX URL
    if not url.startswith("http"):
        url = "http://" + url

    # 🌐 WEBSITE CHECK
    try:
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            score -= 20
            warnings.append("Website not responding properly")

        if not url.startswith("https"):
            score -= 20
            warnings.append("No HTTPS (Not Secure)")

    except requests.exceptions.RequestException:
        score -= 50
        warnings.append("Website not reachable")

    # 🔍 extract domain only (IMPORTANT FIX)
    domain = re.sub(r'https?://', '', url).split('/')[0].lower()

    bad_words = ["login", "verify", "bank", "free", "win"]

    for word in bad_words:
        if word in domain:
            score -= 10
            warnings.append(f"Suspicious word: {word}")

    # ⚠️ URL checks
    if len(url) > 50:
        score -= 10
        warnings.append("Too long URL")

    if "-" in domain:
        score -= 5
        warnings.append("Hyphen suspicious")

    if "@" in url:
        score -= 20
        warnings.append("@ symbol found")

    if domain.count('.') > 3:
        score -= 10
        warnings.append("Too many subdomains")

    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    if re.search(ip_pattern, domain):
        score -= 25
        warnings.append("IP address used")

    # 🎯 FINAL RESULT
    if score >= 80:
        result = "✅ Safe Website"
    elif score >= 50:
        result = "⚠️ Moderate Risk"
    else:
        result = "❌ Dangerous Website"

    # 📊 SAFE DB UPDATE
    try:
        if 'user' in session:
            db = get_db()
            cursor = db.cursor()

            cursor.execute(
                "UPDATE users SET website_used = website_used + 1 WHERE name=%s",
                (session['user'],)
            )

            db.commit()
            db.close()

    except Exception as e:
        print("DB Error:", e)

    return render_template(
        "result.html",
        result=f"{result} (Score: {score}/100)",
        extra=" | ".join(warnings)
    )
      
# ---------------- QUIZ ----------------
@app.route('/quiz')
def quiz_page():

    selected = random.sample(quiz, 5)
    session['quiz_set'] = selected
    

    return render_template("quiz.html", quiz=selected)

#-------------------quiz submit --------------
@app.route('/quiz_submit', methods=['POST'])
def quiz_submit():

    # 🔥 safety check
    quiz_set = session.get('quiz_set')
    if not quiz_set:
        return redirect('/quiz')

    score = 0
    results = []

    for i, q in enumerate(quiz_set):

        user_ans = (request.form.get(f"q{i}") or "").strip().lower()
        correct_ans = q['a'].strip().lower()

        if user_ans == correct_ans:
            score += 1
            status = "✅ Correct"
        else:
            status = "❌ Wrong"

        results.append({
            "question": q['q'],
            "your": user_ans,
            "correct": correct_ans,
            "status": status
        })

    # 🔥 update DB only if user logged in
    if 'user' in session:
        execute_query(
            "UPDATE users SET quiz_used = quiz_used + 1 WHERE name=%s",
            (session['user'],)
        )

    # 🔥 optional: coins/xp reward system
    if 'user' in session:
        execute_query(
            "UPDATE users SET coins = coins + %s, xp = xp + %s WHERE name=%s",
            (score * 2, score, session['user'])
        )

    return render_template(
        "quiz_result.html",
        score=score,
        results=results
    )
#------profile----------------

#------------tips------------
from flask import jsonify

@app.route('/get_tip')
def get_tip():
    return jsonify({
        "tips": random.sample(tips_list, min(3, len(tips_list)))
    })


@app.route('/check_email', methods=['POST'])
def check_email():
    email_text = request.form['email']

    score = 100
    warnings = []

    # 🔍 1. Suspicious words
    bad_words = ["urgent", "win", "free", "verify", "bank", "password", "click", "offer"]

    for word in bad_words:
        if word in email_text.lower():
            score -= 10
            warnings.append(f"⚠️ Suspicious word: {word}")

    # 🔗 2. Extract links from email
    links = re.findall(r'(https?://\S+)', email_text)

    for link in links:
        warnings.append(f"🔗 Link found: {link}")

        try:
            res = requests.get(link, timeout=5)

            if res.status_code != 200:
                score -= 15
                warnings.append("⚠️ Link not responding")

            if not link.startswith("https"):
                score -= 15
                warnings.append("⚠️ Link is not secure (HTTP)")

        except:
            score -= 25
            warnings.append("❌ Link unreachable")

    # 🔥 3. ALL CAPS detection
    if email_text.isupper():
        score -= 10
        warnings.append("⚠️ All caps message (scam trick)")

    # ❗ 4. Too many exclamation marks
    if email_text.count("!") > 3:
        score -= 10
        warnings.append("⚠️ Too many exclamation marks")

    # 📧 5. Basic email format check
    if "@" not in email_text:
        score -= 5
        warnings.append("⚠️ Invalid email format")

    # 🎯 FINAL RESULT
    if score >= 80:
        result = "✅ Safe Email"
    elif score >= 50:
        result = "⚠️ Suspicious Email"
    else:
        result = "❌ Phishing Email"

    return render_template(
        "result.html",
        result=f"{result} (Score: {score}/100)",
        extra=" | ".join(warnings)
    )
#--------file scan ----------------------
@app.route('/scan_file', methods=['POST'])
def scan_file():

    try:
        if 'file' not in request.files:
            return "❌ No file uploaded"

        file = request.files['file']

        if file.filename == '':
            return "❌ No selected file"

        content = file.read().decode(errors='ignore').lower()

        score = 100
        warnings = []

        bad_words = ["virus", "hack", "crack", "password", "keylogger"]

        for word in bad_words:
            if word in content:
                score -= 15
                warnings.append(f"⚠️ Suspicious: {word}")

        if file.filename.endswith(".exe"):
            score -= 20
            warnings.append("⚠️ Executable file")

        if len(content.strip()) == 0:
            score -= 30
            warnings.append("⚠️ Empty or unreadable file")

        if score >= 80:
            result = "✅ Safe File"
            level = "Low Risk 🟢"
        elif score >= 50:
            result = "⚠️ Suspicious File"
            level = "Medium Risk 🟡"
        else:
            result = "❌ Dangerous File"
            level = "High Risk 🔴"

        return render_template(
            "result.html",
            result=f"{result} ({level})",
            extra=" | ".join(warnings)
        )

    except Exception as e:
        print("File Scan Error:", e)
        return "❌ File scan failed"
        
@app.route('/admin', methods=['GET', 'POST'])        
def admin():
    if request.method == 'POST':
        try:
            password = request.form.get('password')
            if password != ADMIN_PASSWORD:
                return "❌ Wrong Password"

            title = request.form.get('title')
            content = request.form.get('content')

            file = request.files.get('file')
            filename = None

            # 📁 FILE UPLOAD
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

            # 🔥 DB CONNECT (IMPORTANT)
            db = get_db()
            cursor = db.cursor(buffered=True)

            cursor.execute(
                "INSERT INTO updates (title, content, filename) VALUES (%s, %s, %s)",
                (title, content, filename)
            )

            db.commit()

            cursor.close()
            db.close()

            return "✅ Update Posted Successfully"

        except Exception as e:
            return f"❌ ERROR: {str(e)}"

    return render_template("admin.html")

@app.route('/delete_update/<int:id>')
def delete_update(id):
    if 'user' not in session:
        return redirect('/')

    try:
        db = get_db()
        cursor = db.cursor(buffered=True)

        # file naam nikaal
        cursor.execute("SELECT filename FROM updates WHERE id=%s", (id,))
        data = cursor.fetchone()

        if data and data[0]:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], data[0])
            if os.path.exists(filepath):
                os.remove(filepath)

        # DB se delete
        cursor.execute("DELETE FROM updates WHERE id=%s", (id,))
        db.commit()

        cursor.close()
        db.close()

        return redirect('/updates')

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@app.route('/updates')
def updates():
    db = get_db()
    cursor = db.cursor(buffered=True)

    cursor.execute("SELECT * FROM updates ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("updates.html", updates=data)

#----------------puzzle game-----------------
@app.route('/game/puzzle')
def puzzle_game():
    if 'user' not in session:
        return redirect('/')
    return render_template("puzzle_game.html")
#----------start puzzle---------
@app.route('/game/puzzle/start')
def puzzle_start():
    if 'user' not in session:
        return redirect('/')

    # 🔁 RESET if coming from restart (game over)
    if session.get('puzzle_failed'):
        session['puzzle_failed'] = False
        questions = session.get('puzzle_game', [])

        # 💾 restart same game
        session['puzzle_index'] = 0
        session['puzzle_score'] = 0
        session['lives'] = 5

        return redirect('/game/puzzle/play')

    # 🔥 safe game counter
    session['game_count'] = session.get('game_count', 0) + 1
    game_count = session['game_count']

    # 🎯 level system (smooth progression)
    if game_count <= 1:
        level = 1
    elif game_count <= 2:
        level = 2
    elif game_count <= 4:
        level = 3
    else:
        level = 4

    session['level'] = level

    # 🔥 collect all questions safely
    all_questions = []
    for k in puzzle_levels:
        all_questions.extend(puzzle_levels[k])

    # 🔥 safe dedup
    seen = set()
    unique_questions = []

    for q in all_questions:
        key = q.get('q', str(q))
        if key not in seen:
            seen.add(key)
            unique_questions.append(q)

    random.shuffle(unique_questions)

    # 🎯 level based question count
    if level == 1:
        questions = unique_questions[:5]
    elif level == 2:
        questions = unique_questions[:7]
    elif level == 3:
        questions = unique_questions[:9]
    else:
        questions = unique_questions[:12]

    # 💾 session reset
    session['puzzle_game'] = questions
    session['puzzle_index'] = 0
    session['puzzle_score'] = 0
    session['lives'] = 5

    return redirect('/game/puzzle/play')
 #-------------puzzle win----------------   
@app.route('/game/puzzle_win', methods=['POST'])
def puzzle_win():
    if 'user' not in session:
        return {"status": "error"}

    db = get_db()  # 🔥 add this
    cursor = db.cursor(buffered=True)

    cursor.execute("""
        UPDATE users 
        SET coins = coins + 10,
            puzzle_wins = puzzle_wins + 1
        WHERE name=%s
    """, (session['user'],))

    db.commit()
    db.close()  # 🔥 important

    return {"status": "win", "coins": 10}

#----------load character ------------
@app.route('/characters')
def characters():
    if 'user' not in session:
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM characters")
    chars = cursor.fetchall()

    cursor.execute("SELECT coins, character_id FROM users WHERE name=%s", (session['user'],))
    user = cursor.fetchone()

    return render_template("characters.html", chars=chars, user=user)


#--------------------buy character---------------
@app.route('/select_character/<int:cid>')
def select_character(cid):
    if 'user' not in session:
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    # get character price
    cursor.execute("SELECT price FROM characters WHERE id=%s", (cid,))
    char = cursor.fetchone()

    if not char:
        return redirect('/characters')

    price = char[0]

    # get user coins
    cursor.execute("SELECT coins FROM users WHERE name=%s", (session['user'],))
    user = cursor.fetchone()
    coins = user[0]

    if coins >= price:
        cursor.execute("""
            UPDATE users 
            SET coins = coins - %s, character_id=%s
            WHERE name=%s
        """, (price, cid, session['user']))
        db.commit()
    else:
        return "❌ Not enough coins"

    db.close()
    return redirect('/characters')
    
#-------------leaderboard system-----------
@app.route('/leaderboard')
def leaderboard():
    db = get_db()
    cursor = db.cursor(buffered=True)

    cursor.execute("""
        SELECT 
            name,
            MAX(coins) AS coins,
            MAX(puzzle_wins) AS puzzle_wins
        FROM users
        GROUP BY name
        ORDER BY coins DESC
    """)

    data = cursor.fetchall()
    current_user = session.get("user")

    db.close()

    return render_template(
        "leaderboard.html",
        users=data,
        current_user=current_user
    )
# 🔥 PUZZLE PLAY
@app.route('/game/puzzle/play')
def puzzle_play():

    game = session.get('puzzle_game')
    i = session.get('puzzle_index', 0)
    lives = session.get('lives', 5)

    if not game:
        return redirect('/game/puzzle/start')

    if i >= len(game):
        return redirect('/game/puzzle/result')

    if lives <= 0:
        return redirect('/game/puzzle/result')

    q = game[i]

    # 🔥 auto detect type (SMART SYSTEM)
    if "options" in q:
        mode = "mcq"

    elif "words" in q:
        mode = "word"

        words = q["words"][:]
        random.shuffle(words)
        q["words"] = words

    else:
        mode = "sentence"

    return render_template(
        "puzzle_game.html",
        q=q,
        mode=mode,
        index=i + 1,
        total=len(game),
        lives=lives
    )

# 🔥 PUZZLE CHECK
# -------------------------------
@app.route('/game/puzzle/check', methods=['POST'])
def puzzle_check():

    game = session.get('puzzle_game')
    i = session.get('puzzle_index', 0)
    score = session.get('puzzle_score', 0)
    lives = session.get('lives', 5)

    answer = request.form.get("answer", "").strip().lower()

    if not game or i >= len(game):
        return redirect('/game/puzzle/result')

    q = game[i]

    # 🔥 UNIVERSAL ANSWER KEY FIX
    correct = q.get('a') or q.get('answer', '')

    if answer == correct.strip().lower():
        score += 5
    else:
        lives -= 1

    session['puzzle_score'] = score
    session['lives'] = lives
    session['puzzle_index'] = i + 1

    if lives <= 0:
        session['puzzle_failed'] = True
        return redirect('/game/puzzle/result')

    return redirect('/game/puzzle/play')
#--------game result----------------
@app.route('/game/puzzle/result')
def puzzle_result():

    from datetime import date, timedelta

    if 'user' not in session:
        return redirect('/')

    user = session['user']

    # 💀 CHECK IF GAME FAILED
    failed = session.get('puzzle_failed', False)

    # =========================
    # 💀 LOSS CASE (NO REWARD)
    # =========================
    if failed:
        session['puzzle_failed'] = False

        return render_template(
            "result.html",
            result="💀 Game Over!",
            extra="❌ You lost all lives",
            restart=True
        )

    # =========================
    # ✅ WIN CASE (REWARDS)
    # =========================
    score = session.get('puzzle_score', 0)

    coins_gain = score
    xp_gain = score

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT level, xp, streak, last_play_date FROM users WHERE name=%s",
        (user,)
    )
    data = cursor.fetchone()

    level = data[0] if data else 1
    xp = data[1] if data else 0
    streak = data[2] if data else 0
    last_date = data[3] if data else None

    today = date.today()

    if last_date and not isinstance(last_date, date):
        last_date = date.fromisoformat(str(last_date))

    # 🔥 streak logic
    if last_date is None:
        streak = 1
    elif last_date == today:
        pass
    elif last_date == today - timedelta(days=1):
        streak += 1
    else:
        streak = 1

    # 🔥 XP system
    xp += xp_gain
    if xp >= 10:
        level += 1
        xp = 0

    # 💰 bonus coins
    if streak % 7 == 0:
        coins_gain += 20

    cursor.execute("""
        UPDATE users 
        SET coins = coins + %s,
            level = %s,
            xp = %s,
            streak = %s,
            last_play_date = %s
        WHERE name=%s
    """, (coins_gain, level, xp, streak, today, user))

    db.commit()
    db.close()

    # 🔥 fun messages
    if streak == 1:
        msg = "🔥 Fresh start!"
    elif streak < 5:
        msg = "💪 Keep pushing!"
    elif streak < 10:
        msg = "🚀 Fire mode!"
    else:
        msg = "👑 Legend unlocked!"

    return render_template(
        "result.html",
        result="🎯 Puzzle Completed!",
        extra=f"🪙 +{coins_gain} Coins | ⭐ XP Updated | 🔥 Streak: {streak} | {msg} | 📊 Level: {level}",
        restart=False
    )
# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
    
