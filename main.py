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
ADMIN_PASSWORD = "priyanrkp098"  # changable.......


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
    {"jumbled": "KROWTEN", "answer": "NETWORK"},
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
sentence_puzzles += [

{
"question": "Why use antivirus?",
"words": ["antivirus", "protects", "device"],
"answer": "antivirus protects device"
},
{
"question": "Why avoid fake apps?",
"words": ["fake", "apps", "can", "steal", "data"],
"answer": "fake apps can steal data"
},
{
"question": "What is data privacy?",
"words": ["data", "privacy", "protects", "personal", "information"],
"answer": "data privacy protects personal information"
},
{
"question": "Why use VPN?",
"words": ["vpn", "hides", "your", "identity"],
"answer": "vpn hides your identity"
},
{
"question": "What is secure password?",
"words": ["secure", "password", "is", "hard", "to", "guess"],
"answer": "secure password is hard to guess"
},
{
"question": "Why check URL?",
"words": ["check", "url", "before", "login"],
"answer": "check url before login"
},
{
"question": "What is cyber crime?",
"words": ["cyber", "crime", "uses", "internet"],
"answer": "cyber crime uses internet"
},
{
"question": "Why use lock screen?",
"words": ["lock", "screen", "protects", "device"],
"answer": "lock screen protects device"
},
{
"question": "What is spyware?",
"words": ["spyware", "tracks", "user", "activity"],
"answer": "spyware tracks user activity"
},
{
"question": "Why avoid unknown emails?",
"words": ["unknown", "emails", "may", "be", "dangerous"],
"answer": "unknown emails may be dangerous"
},

{
"question": "What is ransomware?",
"words": ["ransomware", "locks", "files"],
"answer": "ransomware locks files"
},
{
"question": "Why update system?",
"words": ["system", "updates", "improve", "security"],
"answer": "system updates improve security"
},
{
"question": "What is OTP security?",
"words": ["otp", "protects", "login"],
"answer": "otp protects login"
},
{
"question": "Why avoid public computers?",
"words": ["public", "computers", "are", "not", "safe"],
"answer": "public computers are not safe"
},
{
"question": "What is data backup?",
"words": ["backup", "stores", "copy", "of", "data"],
"answer": "backup stores copy of data"
},
{
"question": "Why use strong PIN?",
"words": ["strong", "pin", "protects", "device"],
"answer": "strong pin protects device"
},
{
"question": "What is spam email?",
"words": ["spam", "email", "is", "unwanted"],
"answer": "spam email is unwanted"
},
{
"question": "Why check permissions?",
"words": ["check", "app", "permissions", "carefully"],
"answer": "check app permissions carefully"
},
{
"question": "What is firewall protection?",
"words": ["firewall", "blocks", "threats"],
"answer": "firewall blocks threats"
},
{
"question": "Why not click ads?",
"words": ["ads", "may", "contain", "malware"],
"answer": "ads may contain malware"
},

{
"question": "Arrange sentence:",
"words": ["use", "vpn", "secure", "connection"],
"answer": "use vpn secure connection"
},
{
"question": "Arrange sentence:",
"words": ["protect", "your", "personal", "data"],
"answer": "protect your personal data"
},
{
"question": "Arrange sentence:",
"words": ["never", "click", "unknown", "links"],
"answer": "never click unknown links"
},
{
"question": "Arrange sentence:",
"words": ["always", "update", "your", "apps"],
"answer": "always update your apps"
},
{
"question": "Arrange sentence:",
"words": ["use", "different", "passwords"],
"answer": "use different passwords"
},
{
"question": "Arrange sentence:",
"words": ["enable", "two", "factor", "authentication"],
"answer": "enable two factor authentication"
},
{
"question": "Arrange sentence:",
"words": ["check", "email", "sender", "carefully"],
"answer": "check email sender carefully"
},
{
"question": "Arrange sentence:",
"words": ["do", "not", "share", "otp"],
"answer": "do not share otp"
},
{
"question": "Arrange sentence:",
"words": ["keep", "software", "updated"],
"answer": "keep software updated"
},
{
"question": "Arrange sentence:",
"words": ["use", "secure", "wifi", "only"],
"answer": "use secure wifi only"
},

{
"question": "What is safe browsing?",
"words": ["safe", "browsing", "protects", "information"],
"answer": "safe browsing protects information"
},
{
"question": "Why logout accounts?",
"words": ["logout", "keeps", "account", "safe"],
"answer": "logout keeps account safe"
},
{
"question": "What is identity theft?",
"words": ["identity", "theft", "steals", "personal", "data"],
"answer": "identity theft steals personal data"
},
{
"question": "Why avoid pirated software?",
"words": ["pirated", "software", "contains", "viruses"],
"answer": "pirated software contains viruses"
},
{
"question": "What is secure login?",
"words": ["secure", "login", "protects", "accounts"],
"answer": "secure login protects accounts"
},
{
"question": "Why use encryption?",
"words": ["encryption", "keeps", "data", "safe"],
"answer": "encryption keeps data safe"
},
{
"question": "What is cyber safety?",
"words": ["cyber", "safety", "protects", "users"],
"answer": "cyber safety protects users"
},
{
"question": "Why avoid unknown downloads?",
"words": ["unknown", "downloads", "can", "harm", "device"],
"answer": "unknown downloads can harm device"
},
{
"question": "What is data security?",
"words": ["data", "security", "protects", "information"],
"answer": "data security protects information"
},
{
"question": "Why use password manager?",
"words": ["password", "manager", "stores", "passwords"],
"answer": "password manager stores passwords"
},

{
"question": "Arrange sentence:",
"words": ["avoid", "using", "public", "wifi"],
"answer": "avoid using public wifi"
},
{
"question": "Arrange sentence:",
"words": ["always", "verify", "before", "click"],
"answer": "always verify before click"
},
{
"question": "Arrange sentence:",
"words": ["protect", "device", "with", "password"],
"answer": "protect device with password"
},
{
"question": "Arrange sentence:",
"words": ["backup", "your", "important", "files"],
"answer": "backup your important files"
},
{
"question": "Arrange sentence:",
"words": ["do", "not", "trust", "unknown", "sources"],
"answer": "do not trust unknown sources"
},
{
"question": "Arrange sentence:",
"words": ["keep", "your", "data", "safe"],
"answer": "keep your data safe"
},
{
"question": "Arrange sentence:",
"words": ["enable", "security", "settings"],
"answer": "enable security settings"
},
{
"question": "Arrange sentence:",
"words": ["never", "reuse", "passwords"],
"answer": "never reuse passwords"
},
{
"question": "Arrange sentence:",
"words": ["check", "website", "security"],
"answer": "check website security"
},
{
"question": "Arrange sentence:",
"words": ["use", "antivirus", "software"],
"answer": "use antivirus software"
}    
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
"a": "Use secure sites"},
puzzle_levels.update({

    5: [
        {"q": "What is data breach?", 
         "options": ["Safe storage", "Unauthorized data access", "Backup", "Encryption"], 
         "a": "Unauthorized data access"},

        {"q": "What should you check before login?", 
         "options": ["Color", "URL", "Font", "Image"], 
         "a": "URL"},

        {"q": "Is saving password in browser safe?", 
         "options": ["Always safe", "Risky", "Best method", "Required"], 
         "a": "Risky"},

        {"q": "What is VPN used for?", 
         "options": ["Gaming", "Hide identity", "Faster speed", "Download"], 
         "a": "Hide identity"},

        {"q": "What is social engineering?", 
         "options": ["Coding", "Tricking people", "Networking", "Design"], 
         "a": "Tricking people"},
    ],

    6: [
        {"q": "What is brute force attack?", 
         "options": ["Guessing passwords", "Sending email", "Downloading file", "Using VPN"], 
         "a": "Guessing passwords"},

        {"q": "Why use different passwords?", 
         "options": ["Easy to remember", "Reduce risk", "Faster login", "No reason"], 
         "a": "Reduce risk"},

        {"q": "What is spyware?", 
         "options": ["Game", "Tracking software", "Browser", "Tool"], 
         "a": "Tracking software"},

        {"q": "What is secure website sign?", 
         "options": ["http", "https", "ftp", "file"], 
         "a": "https"},

        {"q": "What is identity theft?", 
         "options": ["Create account", "Steal personal info", "Delete data", "Backup"], 
         "a": "Steal personal info"},
    ],

    7: [
        {"q": "What is ransomware attack?", 
         "options": ["Delete files", "Lock files for money", "Speed up system", "Backup"], 
         "a": "Lock files for money"},

        {"q": "What should you do after data breach?", 
         "options": ["Ignore", "Change passwords", "Share info", "Delete apps"], 
         "a": "Change passwords"},

        {"q": "What is secure authentication?", 
         "options": ["Simple login", "Multi-layer login", "No password", "Fast login"], 
         "a": "Multi-layer login"},

        {"q": "Why disable Bluetooth?", 
         "options": ["Save battery", "Reduce hacking risk", "Increase speed", "Play music"], 
         "a": "Reduce hacking risk"},

        {"q": "What is phishing website sign?", 
         "options": ["Correct URL", "Wrong spelling URL", "Secure lock", "Fast loading"], 
         "a": "Wrong spelling URL"},
    ],

    8: [
        {"q": "What is zero-day vulnerability?", 
         "options": ["Old bug", "Unknown security flaw", "Patch update", "Firewall"], 
         "a": "Unknown security flaw"},

        {"q": "What is encryption used for?", 
         "options": ["Delete data", "Hide data", "Copy data", "Share data"], 
         "a": "Hide data"},

        {"q": "What is password manager?", 
         "options": ["Game", "Store passwords securely", "Delete passwords", "Hack tool"], 
         "a": "Store passwords securely"},

        {"q": "What is multi-factor authentication?", 
         "options": ["Single password", "Multiple verification steps", "No login", "Fast login"], 
         "a": "Multiple verification steps"},

        {"q": "What is secure network?", 
         "options": ["Open WiFi", "Protected connection", "Slow internet", "Public hotspot"], 
         "a": "Protected connection"},

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
{"q":"Click unknown USB devices?", "a":"no"},
quiz += [

{"q":"Should you lock your phone?", "a":"yes"},
{"q":"Is sharing passwords safe?", "a":"no"},
{"q":"Use official app stores?", "a":"yes"},
{"q":"Is email spoofing dangerous?", "a":"yes"},
{"q":"Trust unknown phone calls?", "a":"no"},
{"q":"Use screen lock pattern?", "a":"yes"},
{"q":"Install random APK files?", "a":"no"},
{"q":"Check website certificate?", "a":"yes"},
{"q":"Use different passwords?", "a":"yes"},
{"q":"Leave devices unattended?", "a":"no"},

{"q":"Enable auto updates?", "a":"yes"},
{"q":"Is identity theft real?", "a":"yes"},
{"q":"Share location publicly?", "a":"no"},
{"q":"Use secure websites only?", "a":"yes"},
{"q":"Ignore suspicious emails?", "a":"no"},
{"q":"Verify app developer?", "a":"yes"},
{"q":"Use simple passwords?", "a":"no"},
{"q":"Log out from shared devices?", "a":"yes"},
{"q":"Trust unknown QR codes?", "a":"no"},
{"q":"Use device encryption?", "a":"yes"},

{"q":"Backup important data?", "a":"yes"},
{"q":"Click shortened links blindly?", "a":"no"},
{"q":"Use antivirus on phone?", "a":"yes"},
{"q":"Is malware harmful?", "a":"yes"},
{"q":"Open spam emails?", "a":"no"},
{"q":"Use secure lock screen?", "a":"yes"},
{"q":"Accept all app permissions?", "a":"no"},
{"q":"Use OTP for login?", "a":"yes"},
{"q":"Ignore privacy settings?", "a":"no"},
{"q":"Use trusted networks?", "a":"yes"},

{"q":"Download cracked games?", "a":"no"},
{"q":"Is ransomware dangerous?", "a":"yes"},
{"q":"Use password hints?", "a":"no"},
{"q":"Check login history?", "a":"yes"},
{"q":"Use two-step verification?", "a":"yes"},
{"q":"Trust fake giveaways?", "a":"no"},
{"q":"Use secure cloud storage?", "a":"yes"},
{"q":"Share bank details online?", "a":"no"},
{"q":"Install updates immediately?", "a":"yes"},
{"q":"Use biometric authentication?", "a":"yes"},

{"q":"Open unknown links in SMS?", "a":"no"},
{"q":"Use firewall protection?", "a":"yes"},
{"q":"Save passwords in notes?", "a":"no"},
{"q":"Verify website domain?", "a":"yes"},
{"q":"Use public WiFi without VPN?", "a":"no"},
{"q":"Trust unknown downloads?", "a":"no"},
{"q":"Enable device tracking?", "a":"yes"},
{"q":"Share OTP with friends?", "a":"no"},
{"q":"Use strong security questions?", "a":"yes"},
{"q":"Disable security alerts?", "a":"no"},

{"q":"Use HTTPS websites?", "a":"yes"},
{"q":"Click suspicious popups?", "a":"no"},
{"q":"Install security patches?", "a":"yes"},
{"q":"Use password autofill blindly?", "a":"no"},
{"q":"Trust unknown software?", "a":"no"},
{"q":"Check app ratings before install?", "a":"yes"},
{"q":"Use private browsing mode?", "a":"yes"},
{"q":"Share personal photos publicly?", "a":"no"},
{"q":"Use secure email providers?", "a":"yes"},
{"q":"Ignore data breaches?", "a":"no"},

{"q":"Use anti-phishing tools?", "a":"yes"},
{"q":"Open unknown attachments?", "a":"no"},
{"q":"Use login notifications?", "a":"yes"},
{"q":"Save cards on all websites?", "a":"no"},
{"q":"Use multi-device sync securely?", "a":"yes"},
{"q":"Trust fake job offers?", "a":"no"},
{"q":"Use encrypted backups?", "a":"yes"},
{"q":"Disable antivirus?", "a":"no"},
{"q":"Verify payment requests?", "a":"yes"},
{"q":"Click ads blindly?", "a":"no"}    
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
    elif "my account hacked" in msg or "account hack" in msg:
        return """🚨 Account hacked?
         1️⃣ Change password immediately
         2️⃣ Enable 2FA
         3️⃣ Check login activity
         4️⃣ Report platform support
         ⚡ Act fast to recover!"""    

    elif "how are you" in msg:
        return "😊 I'm good! Ready to help you stay safe online."

    elif "money deducted" in msg or "upi fraud" in msg or "lost money" in msg:
       return """💸 Money lost in scam?
👉 Call 1930 immediately
👉 Report: cybercrime.gov.in
⏰ Report within 24 hrs for better recovery chance!"""

    elif "whatsapp hack" in msg or "whatsapp scam" in msg:
       return """📱 WhatsApp Safety:
🚫 Never share OTP
🚫 Don't click unknown links
✅ Enable 2-step verification"""

    elif "email fake" in msg or "fake email" in msg:
       return """📧 Fake Email Signs:
⚠️ Unknown sender
⚠️ Urgent message ("act now")
⚠️ Suspicious links
👉 Always verify sender!"""

    elif "free fire hack" in msg or "game hack" in msg or "free skins" in msg:
       return """🎮 Gaming Scam Alert:
🚫 No real hacks or free skins
🚫 Don't download mod apps
💡 These steal your account!"""

    elif "shopping scam" in msg or "fake website" in msg:
        return """🛒 Shopping Safety:
✅ Check reviews
✅ Use trusted sites
🚫 Avoid too-good-to-be-true deals"""

    elif "how to create password" in msg:
       return """🔐 Strong Password Tips:
✔️ Use 12+ characters
✔️ Mix letters, numbers, symbols
✔️ Avoid name/DOB"""

    
    elif "kyc" in msg:
        return """📄 KYC Scam Alert:
🚫 Bank never asks KYC via link
🚫 Don't share OTP or details
⚠️ Always visit official website"""

    elif "instagram hack" in msg or "social media hacked" in msg:
        return """📷 Social Media Safety:
🔒 Enable 2FA
🔑 Change password
👀 Remove unknown devices"""

    elif "is this safe" in msg or "safe or not" in msg:
        return """🤔 Not sure?
👉 Don't click unknown links
👉 Don't share personal info
💡 When in doubt = avoid!"""

    elif "job scam" in msg or "fake job" in msg:
        return """💼 Job Scam Alert:
🚫 No legit job asks money
🚫 Avoid random WhatsApp jobs
✅ Verify company first"""

    elif "card details" in msg or "credit card scam" in msg:
        return """💳 Card Safety:
🚫 Never share CVV/OTP
🔐 Use secure payment gateway
⚠️ Block card if suspicious"""

    elif "confused" in msg or "don't know" in msg:
        return "😅 No worries! Tell me your problem, I'll guide you step by step."
 
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
#--------leaderboard---------------


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

    cursor.execute("SELECT coins, level, xp FROM users WHERE name=%s", (session['user'],))
    data = cursor.fetchone()

    if data:
        coins, level, xp = data
    else:
        coins, level, xp = 200, 1, 0

    owned = session.get("owned_chars", ["🤖"])
    selected = session.get("selected_char", "🤖")

    characters = [
        {"emoji":"🤖","cost":0},
        {"emoji":"👨‍💻","cost":150},
        {"emoji":"🧠","cost":400},
        {"emoji":"👾","cost":500},
        {"emoji":"🛡️","cost":600}, 
        {"emoji":"🕵️‍♂️","cost":700},
        {"emoji":"⚡","cost":950},
        {"emoji":"😈","cost":1000},
        {"emoji":"💀","cost":1500},
        {"emoji":"🔥","cost":2000}
       
       ]

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
    
@app.route('/buy_char', methods=['POST'])
def buy_char():
    try:
        user = session.get("user")
        emoji = request.form.get("emoji")

        char_cost = {
            "👨‍💻":100, "🕵️‍♂️":1000, "👾":170,
            "😈":800, "💀":500, "🧠":80,
            "🛡️":570, "⚡":450, "🔥":900
        }

        cost = char_cost.get(emoji, 0)

        db = get_db()
        cursor = db.cursor(buffered=True)

        # 💰 coins
        cursor.execute("SELECT coins FROM users WHERE name=%s", (user,))
        coins = cursor.fetchone()[0]

        # 🎭 check already owned
        cursor.execute("SELECT emoji FROM user_chars WHERE user=%s", (user,))
        owned = [x[0] for x in cursor.fetchall()]

        if emoji in owned:
            return "⚠️ Already owned"

        if coins < cost:
            return "😢 Better luck next time"

        # 💰 deduct coins
        cursor.execute(
            "UPDATE users SET coins = coins - %s WHERE name=%s",
            (cost, user)
        )

        # 🎭 add character
        cursor.execute(
            "INSERT INTO user_chars (user, emoji) VALUES (%s, %s)",
            (user, emoji)
        )

        # 🟢 auto select
        cursor.execute(
            "UPDATE users SET selected_char=%s WHERE name=%s",
            (emoji, user)
        )

        db.commit()
        db.close()

        return "✅ Purchased Successfully!"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"
@app.route('/use_char/<emoji>')
def use_char(emoji):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
     "UPDATE users SET coins = coins - %s, selected_char=%s WHERE name=%s",
    (cost, emoji, session['user'])
)
   

    db.commit()
    db.close()

    return redirect('/profile')
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
@app.route('/password', methods=['GET', 'POST'])
def password():
    result = None

    if request.method == 'POST':

        import random
        import string

        length = int(request.form.get('length') or 8)

        chars = ""

        if request.form.get('upper'):
            chars += string.ascii_uppercase
        if request.form.get('lower'):
            chars += string.ascii_lowercase
        if request.form.get('digits'):
            chars += string.digits
        if request.form.get('symbols'):
            chars += "@#$%&*!?"

        # 🔥 FIX
        if chars == "":
            return render_template("result.html", result="❌ Please select at least one option")

        pwd = ''.join(random.choice(chars) for _ in range(length))

        if 'user' in session:
            execute_query(
                "UPDATE users SET password_used = password_used + 1 WHERE name=%s",
                (session['user'],)
            )

        return render_template("result.html", result=pwd)

    # GET request (page open hone par)
    return render_template("password.html")
# ---------------- WEBSITE CHECK ----------------
@app.route('/check', methods=['GET', 'POST'])
def check():
    import requests
    import re

    if request.method == 'GET':
        return render_template("check.html")

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

    domain = re.sub(r'https?://', '', url).split('/')[0].lower()

    bad_words = ["login", "verify", "bank", "free", "win"]

    for word in bad_words:
        if word in domain:
            score -= 10
            warnings.append(f"Suspicious word: {word}")

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

    if score >= 80:
        result = "✅ Safe Website"
    elif score >= 50:
        result = "⚠️ Moderate Risk"
    else:
        result = "❌ Dangerous Website"

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

    quiz_set = session.get('quiz_set')
    if not quiz_set:
        return redirect('/quiz')

    score = 0
    results = []

    # ---------------- CHECK ANSWERS ----------------
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

    username = session.get("user")

    # ---------------- UPDATE DATABASE ----------------
    if username:
        db = get_db()
        cursor = db.cursor()

        # 🔥 WIN + COINS + XP
        if score > 0:
            cursor.execute("""
                UPDATE users 
                SET puzzle_wins = puzzle_wins + 1,
                    coins = coins + (10 * %s),
                    xp = xp + (5 * %s)
                WHERE name = %s
            """, (score, score, username))

        # 🔥 QUIZ USAGE TRACK
        cursor.execute("""
            UPDATE users 
            SET quiz_used = quiz_used + 1
            WHERE name = %s
        """, (username,))

        # 🔥 LEVEL UPDATE
        cursor.execute("""
            UPDATE users 
            SET level = FLOOR(xp / 20) + 1
            WHERE name = %s
        """, (username,))

        db.commit()
        db.close()

    # ---------------- RETURN RESULT ----------------
    return render_template(
        "quiz_result.html",
        score=score,
        results=results
    )

#=------random puzzle ----------------
def get_random_puzzle():
    types = ["mcq", "word", "sentence"]
    mode = random.choice(types)

    if mode == "mcq":
        level = random.choice(list(puzzle_levels.keys()))
        q = random.choice(puzzle_levels[level])

    elif mode == "word":
        q = random.choice(word_puzzles)

    elif mode == "sentence":
        q = random.choice(sentence_puzzles)

    return mode, q

#------------tips------------
from flask import jsonify

@app.route('/get_tip')
def get_tip():
    return jsonify({
        "tips": random.sample(tips_list, min(3, len(tips_list)))
    })


@app.route('/check_email', methods=['GET', 'POST'])
def check_email():
    import re
    import requests

    if request.method == 'GET':
        return render_template("email.html")

    email_text = request.form.get('email', '')

    score = 100
    warnings = []

    bad_words = ["urgent", "win", "free", "verify", "bank", "password", "click", "offer"]

    for word in bad_words:
        if word in email_text.lower():
            score -= 10
            warnings.append(f"⚠️ Suspicious word: {word}")

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

    if email_text.isupper():
        score -= 10
        warnings.append("⚠️ All caps message (scam trick)")

    if email_text.count("!") > 3:
        score -= 10
        warnings.append("⚠️ Too many exclamation marks")

    if "@" not in email_text:
        score -= 5
        warnings.append("⚠️ Invalid email format")

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
@app.route('/scan_file', methods=['GET', 'POST'])
def scan_file():

    if request.method == 'GET':
        return render_template("scan_file.html")

    try:
        if 'file' not in request.files:
            return "❌ No file uploaded"

        file = request.files.get('file')

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

@app.route('/updates', methods=['GET'])
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

    import random

    # 🔁 RESET if coming from restart (game over)
    if session.get('puzzle_failed'):
        session['puzzle_failed'] = False

        # 💾 restart same game
        session['puzzle_index'] = 0
        session['puzzle_score'] = 0
        session['lives'] = 5
        return redirect('/game/puzzle/play')

    # 🔥 safe game counter
    session['game_count'] = session.get('game_count', 0) + 1
    game_count = session['game_count']

    # 🎯 level system
    if game_count <= 1:
        level = 1
    elif game_count <= 2:
        level = 2
    elif game_count <= 4:
        level = 3
    else:
        level = 4

    session['level'] = level

    # =========================
    # 🔥 MCQ QUESTIONS (existing)
    # =========================
    all_questions = []
    for k in puzzle_levels:
        all_questions.extend(puzzle_levels[k])

    # 🔥 dedup
    seen = set()
    unique_questions = []

    for q in all_questions:
        key = q.get('q', str(q))
        if key not in seen:
            seen.add(key)
            unique_questions.append(q)

    random.shuffle(unique_questions)

    # =========================
    # 🔥 WORD + SENTENCE ADD (NEW)
    # =========================
    word = word_puzzles[:]
    sentence = sentence_puzzles[:]

    random.shuffle(word)
    random.shuffle(sentence)

    # =========================
    # 🎯 LEVEL BASED MIX
    # =========================
    if level == 1:
        questions = unique_questions[:3] + word[:1] + sentence[:1]

    elif level == 2:
        questions = unique_questions[:4] + word[:2] + sentence[:1]

    elif level == 3:
        questions = unique_questions[:5] + word[:2] + sentence[:2]

    else:
        questions = unique_questions[:6] + word[:3] + sentence[:3]

    # 🔥 FINAL SHUFFLE (IMPORTANT)
    random.shuffle(questions)

    # 💾 session reset
    session['puzzle_game'] = questions
    session['puzzle_index'] = 0
    session['puzzle_score'] = 0
    session['lives'] = 5

    return redirect('/game/puzzle/play')
 #-------------puzzle win----------------   


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

@app.route('/select_char/<emoji>')
def select_char(emoji):
    session["selected_char"] = emoji
    return redirect('/profile')
#-------------leaderboard system-----------
@app.route('/leaderboard')
def leaderboard():
    db = get_db()
    cursor = db.cursor(buffered=True)

    cursor.execute("""
        SELECT 
            name,
            SUM(coins) AS coins,
            SUM(puzzle_wins) AS puzzle_wins,
            MAX(level) AS level
        FROM users
        GROUP BY name
        ORDER BY coins DESC, puzzle_wins DESC
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

@app.route('/add_coins', methods=['POST'])
def add_coins():
    coins = session.get("coins", 0)

    coins += 20   # 🎯 reward (change kar sakta hai)

    session["coins"] = coins

    # 🔥 DB update (important)
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE users SET coins=%s WHERE name=%s",
        (coins, session['user'])
    )

    db.commit()
    db.close()

    return "ok"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')

        if password != ADMIN_PASSWORD:
            return "❌ Wrong Password"

        title = request.form.get('title')
        content = request.form.get('content')

        file = request.files.get('file')

        filename = None
        if file and file.filename != "":
            filename = file.filename

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO updates (title, content, filename) VALUES (%s, %s, %s)",
            (title, content, filename)
        )

        db.commit()
        db.close()

        return "✅ Posted Successfully"

    return render_template("admin.html")
@app.route('/delete_update/<int:id>', methods=['GET', 'POST'])
def delete_update(id):

    # 🔐 Admin check
    if request.method == 'POST':
        password = request.form.get('password')

        if password != ADMIN_PASSWORD:
            return "❌ Not Allowed (Wrong Admin Password)"

        db = get_db()
        cursor = db.cursor()

        cursor.execute("DELETE FROM updates WHERE id=%s", (id,))

        db.commit()
        db.close()

        return "✅ Deleted Successfully"

    return render_template("delete_confirm.html", id=id)

#----------translate -----------------------
from deep_translator import GoogleTranslator

@app.route('/translate', methods=['GET', 'POST'])
def translate():

    result = ""

    if request.method == 'POST':
        text = request.form.get('text')
        lang = request.form.get('lang')

        if text:
            try:
                result = GoogleTranslator(source='auto', target=lang).translate(text)
            except:
                result = "❌ Translation failed"

    return render_template("translate.html", result=result)
   

  
# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
    
