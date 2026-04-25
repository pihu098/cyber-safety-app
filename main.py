from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import random
import string
import re
import mysql.connector
import time
import requests
import os

app = Flask(__name__)
app.secret_key = "secret123"
print("🔥 App starting...")

# 🔥 ADD THIS
@app.route('/')
def home_page():
    return render_template("index.html")

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 🔥 safe create
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ADMIN_PASSWORD = "admin123"  # changable.........

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

# ---------------- DATABASE ----------------
import mysql.connector
import os

db = None
cursor = None

try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

    cursor = db.cursor(buffered=True)
    print("✅ Database Connected")

    # 🔥 TABLE AUTO CREATE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        email VARCHAR(100),
        password VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
    )
    """)

    db.commit()

    print("✅ Users table ready")

except mysql.connector.Error as err:
    print("❌ Database Error:", err)
    db = None
    cursor = None

except Exception as e:
    print("❌ General Error:", e)
    db = None
    cursor = None

# 🔥 DEBUG
print("HOST =", os.getenv("DB_HOST"))
print("USER =", os.getenv("DB_USER"))
print("DB =", os.getenv("DB_NAME"))
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
"🔒 Always lock your device when not in use",
"🧾 Regularly check bank statements for unknown activity",
"📵 Disable app permissions you don't need",
"🧑‍💻 Use different passwords for different accounts",
"🛑 Avoid saving passwords on shared devices",
"📡 Turn off WiFi & Bluetooth when not needed",
"🔍 Google unknown websites before trusting them",
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
👉 Report here: https://cybercrime.gov.in
👉 Call: 1930 (India Helpline)
Stay calm & act fast!"""

    elif "hlo" in msg or "hello" in msg:
        return "👋 Hello! buddy,how are you?,.If you have any queries about cyber safety, tell me. I'll try my best to help you."
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
        return "Hlo brother/sister do you have any question about cyber safety? "
    elif "hack" in msg or "hacked" in msg:
        return "⚠️ Stay safe! Avoid suspicious links and enable 2FA."
    elif "wifi" in msg:
        return "📶 Avoid public WiFi for sensitive activities like banking."

    elif "bank" in msg or "payment" in msg:
        return "💳 Use secure websites (HTTPS) and never share bank details."
    elif "cyber" in msg:
        return "🌐 Cyber safety means protecting your data and privacy online."
    elif "yes" in msg:
        return "okay Feel free to ask anything — I’ll try my best to assist you."
    elif "have a question" in msg:
        return "Sure! You can ask me about cyber safety topics like suspicious links, passwords, and more."
    elif "no" in msg:
        return "🙂 No problem! Ask me something else about cyber safety."

    elif "thanks" in msg or "thank you" in msg:
        return "😊 You're welcome! Stay safe online."
    else:
        return "🤖 I can help with cyber safety topics like passwords, phishing, hacking, suspicious links, and more!🌐"

# ---------------- LOGIN --------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):

            # 🔥 safe update
            try:
                cursor.execute("UPDATE users SET logins = logins + 1 WHERE email=%s", (email,))
                db.commit()
            except:
                pass  # ignore if column issue

            session['user'] = user[1]
            return redirect('/home')

        else:
            return render_template("result.html",
                                   result="❌ Invalid Login",
                                   extra="Try again")

    return render_template("index.html")

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template("result.html",
                                   result="❌ Email already exists",
                                   extra="Try another email")

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )
        db.commit()

        return render_template("result.html",
                               result="✅ Signup Successful",
                               extra="Now login")

    # 🔥 IMPORTANT (GET request ke liye)
    return render_template("signup.html")
# ---------------- HOME ----------------

@app.route('/home')
def home():
    if 'user' in session:
         
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(logins) FROM users")
        total_logins = cursor.fetchone()[0] or 0

        cursor.execute("SELECT password_used, website_used, quiz_used FROM users WHERE name=%s", (session['user'],))
        data = cursor.fetchone()

        password_used = data[0]
        website_used = data[1]
        quiz_used = data[2]

        cursor.execute("SELECT coins, level, xp FROM users WHERE name=%s", (session['user'],))
        data2 = cursor.fetchone()

        cursor.execute("SELECT streak FROM users WHERE name=%s", (session['user'],))
        streak = cursor.fetchone()[0]

        coins = data2[0]
        level = data2[1]
        xp = data2[2]
 

        return render_template("home.html",
                               name=session['user'],
                               message="✅ Welcome to Cyber Safety Platform",
                               total_users=total_users,
                               total_logins=total_logins,
                               quiz_used=quiz_used,
                               password_used=password_used,
                               coins=coins,
                               level=level,
                               xp=xp,
                               website_used=website_used,
                               streak=streak)
    return redirect('/')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# ----------------- COMMUNITY SYSTEM -----------------
@app.route('/community', methods=['GET', 'POST'])
def community():
    if 'user' not in session:
        return redirect('/')

    # POST = jab user kuch likh ke bhejega
    if request.method == 'POST':
        content = request.form.get('content')

        if content:
            cursor.execute(
                "INSERT INTO posts(username, content) VALUES(%s,%s)",
                (session['user'], content)
            )
            db.commit()

    # sab posts fetch karo
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()

    return render_template("community.html", posts=posts)

# ---------------- CHATBOT ----------------
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.form.get('message', "")
    return ai_response(user_msg)

# ---------------- PASSWORD GENERATOR ----------------
@app.route('/password', methods=['POST'])
def password():
    length = int(request.form.get('length', 8))
    chars = ""

    if 'upper' in request.form:
        chars += string.ascii_uppercase
    if 'lower' in request.form:
        chars += string.ascii_lowercase
    if 'digits' in request.form:
        chars += string.digits
    if 'symbols' in request.form:
        chars += string.punctuation

    if chars == "":
        return render_template("result.html",
                               result="❌ Select options",
                               extra="")

    pwd = ''.join(random.choice(chars) for _ in range(length))
   
    cursor.execute("UPDATE users SET password_used = password_used + 1 WHERE name=%s", (session['user'],))
    db.commit()
    return render_template("result.html",
                           result=f"Password: {pwd}",
                           extra="🔐 Strong password generated")

# ---------------- WEBSITE CHECK ----------------

@app.route('/check', methods=['POST'])
def check():
    url = request.form['url']

    score = 100
    warnings = []

    # 🔥 fix URL (http add if missing)
    if not url.startswith("http"):
        url = "http://" + url

    # 🌐 TRY TO CONNECT WEBSITE
    try:
        res = requests.get(url, timeout=5)

        # status check
        if res.status_code != 200:
            score -= 20
            warnings.append("Website not responding properly")

        # HTTPS check
        if not url.startswith("https"):
            score -= 20
            warnings.append("No HTTPS (Not Secure)")

    except:
        score -= 50
        warnings.append("Website not reachable")

    # 🔍 OLD LOGIC (KEEP THIS)
    bad_words = ["login", "verify", "bank", "free", "win"]
    for word in bad_words:
        if word in url.lower():
            score -= 10
            warnings.append(f"Suspicious word: {word}")

    if len(url) > 50:
        score -= 10
        warnings.append("Too long URL")

    if "-" in url:
        score -= 5
        warnings.append("Hyphen suspicious")

    if "@" in url:
        score -= 20
        warnings.append("@ symbol found")

    if url.count('.') > 3:
        score -= 10
        warnings.append("Too many subdomains")

    import re
    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    if re.search(ip_pattern, url):
        score -= 25
        warnings.append("IP address used")

    # 🎯 FINAL RESULT
    if score >= 80:
        result = "✅ Safe Website"
    elif score >= 50:
        result = "⚠️ Moderate Risk"
    else:
        result = "❌ Dangerous Website"

    # 📊 usage count
    if 'user' in session:
        cursor.execute(
            "UPDATE users SET website_used = website_used + 1 WHERE name=%s",
            (session['user'],)
        )
        db.commit()

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
    score = 0
    quiz_set = session.get('quiz_set', [])

    results = []

    for i in range(len(quiz_set)):
        user_ans = request.form.get(f"q{i}")
        correct_ans = quiz_set[i]['a']

        if user_ans and user_ans.lower() == correct_ans:
            score += 1
            status = "✅ Correct"
        else:
            status = "❌ Wrong"
       

        results.append({
            "question": quiz_set[i]['q'],
            "your": user_ans,
            "correct": correct_ans,
            "status": status
        })

    cursor.execute("UPDATE users SET quiz_used = quiz_used + 1 WHERE name=%s", (session['user'],))
    db.commit()
    return render_template("quiz_result.html",
                           score=score,
                           results=results)

# ---------------- TIP ----------------
@app.route('/get_tip')
def get_tip():
     return {"tips":random.sample(tips_list, min(3, len(tips_list)))}


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

@app.route('/scan_file', methods=['POST'])
def scan_file():

    file = request.files['file']   # ✅ ADD THIS LINE

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



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        password = request.form.get('password')
        if password != ADMIN_PASSWORD:
            return "❌ Wrong Password"

        title = request.form.get('title')
        content = request.form.get('content')

        file = request.files.get('file')
        filename = None   # 🔥 default

        # 📁 FILE UPLOAD
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

        # 📝 ALWAYS SAVE (IMPORTANT 🔥)
        cursor.execute(
            "INSERT INTO updates (title, content, filename) VALUES (%s, %s, %s)",
            (title, content, filename)
        )
        db.commit()

        return "✅ Update Posted Successfully"

    return render_template("admin.html")

@app.route('/delete_update/<int:id>')
def delete_update(id):
    if 'user' not in session:
        return redirect('/')

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

    return redirect('/updates')

@app.route('/updates')
def updates():
    cursor.execute("SELECT * FROM updates ORDER BY id DESC")
    data = cursor.fetchall()
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

    # 🔥 user ka level (default = 1)
    level = session.get('level', 1)

    # 🔥 questions fetch (level wise)
    questions = puzzle_levels.get(level, puzzle_levels[1])

    # 🔀 random shuffle
    random.shuffle(questions)

    # 🎯 session me save
    session['puzzle_game'] = questions
    session['puzzle_index'] = 0
    session['puzzle_score'] = 0
    session['lives'] = 5 
    # 🚀 start game
    return redirect('/game/puzzle/play')

#---------submit result game-----------
@app.route('/game/puzzle_win', methods=['POST'])
def puzzle_win():
    if 'user' not in session:
        return redirect('/')

    cursor.execute("""
        UPDATE users 
        SET coins = coins + 10,
            puzzle_wins = puzzle_wins + 1
        WHERE name=%s
    """, (session['user'],))

    db.commit()

    return {"status": "win", "coins": 10}

#-------------leaderboard system-----------
@app.route('/leaderboard')
def leaderboard():
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

    if lives <= 0:
        return redirect('/game/puzzle/result')

    # 🔥 FIXED MODE LOGIC
    if i < 3:
        q = game[i]
        mode = "mcq"

    elif i < 5:
        idx = i - 3
        if idx < len(word_puzzles):
            q = word_puzzles[idx]
            mode = "word"
        else:
            return redirect('/game/puzzle/result')

    elif i < 7:
        idx = i - 5
        if idx < len(sentence_puzzles):
            q = sentence_puzzles[idx]

        mode = random.choice(["sentence", "sentence_click"])

        if "words" in q and isinstance(q["words"], list):
            words = q["words"][:]
            random.shuffle(words)
            q["words"] = words
    else:
        return redirect('/game/puzzle/result')
        


    print("INDEX:", i)
    print("MODE:", mode)
    print("QUESTION:", q)

    return render_template(
        "puzzle_game.html",
        q=q,
        mode=mode,
        index=i + 1,
        total=7,
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

    # 🧠 MCQ
    if i < 3:
        correct = game[i]['a'].strip().lower()   # ⚠️ ensure 'a' exists
        if answer == correct:
            score += 2
        else:
            lives -= 1

    # 🧩 WORD
    elif i < 5:
        correct = word_puzzles[i - 3]['answer'].strip().lower()
        if answer == correct:
            score += 3
        else:
            lives -= 1

    # 🧠 SENTENCE
    elif i < 7:
        correct = sentence_puzzles[i - 5]['answer'].strip().lower()
        if answer == correct:
            score += 5
        else:
            lives -= 1

    # 🔥 UPDATE SESSION
    session['puzzle_score'] = score
    session['lives'] = lives
    session['puzzle_index'] = i + 1

    # 💀 GAME OVER
    if lives <= 0:
        return redirect('/game/puzzle/result')

    return redirect('/game/puzzle/play')
#--------game result----------------
@app.route('/game/puzzle/result')
def puzzle_result():

    score = session.get('puzzle_score', 0)
    user = session['user']

    coins = score
    xp_gain = score

    # fetch user stats
    cursor.execute("SELECT level, xp FROM users WHERE name=%s", (user,))
    data = cursor.fetchone()

    level = data[0] or 1
    xp = data[1] or 0

    xp += xp_gain

    # 🔥 DATE
    from datetime import date, timedelta
    today = date.today()

    # 🔥 streak fetch
    cursor.execute("SELECT streak, last_play_date FROM users WHERE name=%s", (user,))
    data2 = cursor.fetchone()

    if data2:
        streak = data2[0] or 0
        last_date = data2[1]
    else:
        streak = 0
        last_date = None

    # convert if string
    if last_date and not isinstance(last_date, date):
        last_date = date.fromisoformat(str(last_date))

    # 🔥 STREAK LOGIC
    if last_date is None:
        streak = 1

    elif last_date == today:
        pass

    elif last_date == today - timedelta(days=1):
        streak += 1

    else:
        streak = 1

    # 🔥 BONUS (NOW SAFE)
    if streak > 0 and streak % 7 == 0:
        coins += 20

    # 🔥 LEVEL SYSTEM
    if xp >= 10:
        level += 1
        xp = 0

    # update DB
    cursor.execute("""
        UPDATE users 
        SET coins = coins + %s,
            level = %s,
            xp = %s,
            streak = %s,
            last_play_date = %s
        WHERE name=%s
    """, (coins, level, xp, streak, today, user))

    db.commit()

    # 🔥 MESSAGE
    if streak == 1:
        msg = "🔥 Great start!"
    elif streak < 5:
        msg = "💪 Keep going!"
    elif streak < 10:
        msg = "🚀 You're on fire!"
    else:
        msg = "👑 Legend streak!"

    return render_template(
        "result.html",
        result="🎯 Puzzle Completed!",
        extra=f"🪙 +{coins} Coins | ⭐ XP Updated | 🔥 Streak: {streak} | {msg} | 📊 Level: {level}"
    )

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
    
