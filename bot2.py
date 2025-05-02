import re
import random
from time import sleep
from colorama import Fore, Style, init
import tkinter as tk
from tkinter import scrolledtext, messagebox
from flask import Flask, request, render_template_string
import threading

# Initialize colorama
init(autoreset=True)

class CyberSecurityChatbot:
    def __init__(self):
        self.knowledge_base = {
            "password": {
                "name": "Password Security",
                "description": "Creating and managing strong credentials to protect your accounts",
                "examples": [
                    "How to create a strong password: Use 12+ characters with upper/lower case, numbers, and symbols like 'Tr0ub4dour&3'",
                    "Password managers: Tools like Bitwarden or KeePass can generate/store complex passwords securely",
                    "Multi-factor authentication: Adds extra security beyond passwords (SMS codes, authenticator apps)",
                    "Password rotation: Change passwords every 3-6 months, especially for sensitive accounts",
                    "Avoid common patterns: Don't use sequential numbers (123) or keyboard walks (qwerty)"
                ],
                "quiz": [
                    {
                        "question": "Which is the strongest password?",
                        "options": [
                            "A) password123",
                            "B) Summer2023!",
                            "C) C0mpl3x!P@ssw0rd",
                            "D) 12345678"
                        ],
                        "answer": "C",
                        "explanation": "Option C combines length, complexity, and unpredictability - the hallmarks of a strong password."
                    }
                ]
            },
            "phishing": {
                "name": "Phishing Awareness",
                "description": "Identifying and avoiding fraudulent attempts to steal sensitive information",
                "examples": [
                    "Email red flags: Generic greetings ('Dear Customer'), urgent threats ('Account closing!'), mismatched sender addresses",
                    "Fake login pages: Always check URLs - 'amaz0n-login.com' vs 'amazon.com'",
                    "CEO fraud: Emails pretending to be from executives requesting urgent wire transfers",
                    "Smishing: Phishing via SMS/text messages with malicious links",
                    "Vishing: Phone call scams pretending to be tech support or banks"
                ],
                "quiz": [
                    {
                        "question": "You get an email from 'support@paypa1.com' asking you to verify your account. What should you do?",
                        "options": [
                            "A) Click the link and login",
                            "B) Forward to your IT department",
                            "C) Reply with your credentials",
                            "D) Ignore and delete it"
                        ],
                        "answer": "D",
                        "explanation": "The misspelled domain (paypa1 instead of paypal) is a clear phishing sign. Never engage with suspicious emails."
                    }
                ]
            },
            "malware": {
                "name": "Malware Protection",
                "description": "Defending against malicious software threats",
                "examples": [
                    "Ransomware: Encrypts files until payment is made (e.g., WannaCry attack)",
                    "Trojans: Malware disguised as legitimate software (fake Adobe Flash updates)",
                    "Keyloggers: Record keystrokes to steal passwords and data",
                    "Botnets: Networks of infected devices used for DDoS attacks",
                    "Protection methods: Regular backups, endpoint protection, software updates"
                ],
                "quiz": [
                    {
                        "question": "What's the first thing you should do if you suspect malware infection?",
                        "options": [
                            "A) Continue working normally",
                            "B) Disconnect from the network",
                            "C) Run multiple antivirus scans simultaneously",
                            "D) Reboot the computer repeatedly"
                        ],
                        "answer": "B",
                        "explanation": "Disconnecting prevents malware from spreading to other devices while you seek professional help."
                    }
                ]
            },
            "privacy": {
                "name": "Online Privacy",
                "description": "Protecting your personal information in digital spaces",
                "examples": [
                    "Social media settings: Limit post visibility, disable location tagging, review app permissions",
                    "Browser privacy: Use Firefox with uBlock Origin, enable Do Not Track, clear cookies regularly",
                    "VPN benefits: Encrypts internet traffic, hides IP address, bypasses geo-restrictions",
                    "Data minimization: Only provide necessary information when signing up for services",
                    "Metadata risks: Even without content, your digital footprint reveals patterns and habits"
                ],
                "quiz": [
                    {
                        "question": "Which practice best protects your privacy on public WiFi?",
                        "options": [
                            "A) Using HTTP websites",
                            "B) Connecting to any open network",
                            "C) Enabling a VPN",
                            "D) Disabling your firewall"
                        ],
                        "answer": "C",
                        "explanation": "VPNs encrypt all traffic, preventing eavesdropping on public networks where others could monitor your activity."
                    }
                ]
            }
        }
        
        self.general_responses = [
            "Remember: Cybersecurity is a shared responsibility - your actions affect everyone.",
            "Did you know? 90% of cyber attacks start with phishing emails.",
            "Pro tip: Always verify requests for sensitive actions, even if they appear to come from known contacts."
        ]
    
    def get_banner_text(self):
        return f"""
        ╔════════════════════════════════════════════════╗
        ║       🛡️  CYBER SECURITY CHATBOT 🛡️        ║
        ╚════════════════════════════════════════════════╝
        
        Available Topics:
        
        1. Password Security (type 'password')
        - Creating strong credentials
        - Password managers
        - Multi-factor authentication
        Example: "How long should my password be?"
        
        2. Phishing Detection (type 'phishing')
        - Email/SMS scams
        - Fake websites
        - Social engineering
        Example: "How can I spot a fake login page?"
        
        3. Malware Protection (type 'malware')
        - Viruses & ransomware
        - Protection methods
        - Incident response
        Example: "What should I do if I downloaded malware?"
        
        4. Online Privacy (type 'privacy')
        - Social media settings
        - VPNs & encryption
        - Data minimization
        Example: "Is public WiFi safe for banking?"
        
        Type:
        - 'quiz' for an interactive test
        - 'examples' for more scenario samples
        - 'quit' to exit
        """
    
    def show_topic_details(self, topic):
        if topic in self.knowledge_base:
            details = self.knowledge_base[topic]
            response = f"\n=== {details['name']} ===\n"
            response += f"{details['description']}\n"
            response += f"\nKey Examples:\n"
            for i, example in enumerate(details['examples'], 1):
                response += f"{i}. {example}\n"
            response += f"\nTry asking about:\n"
            response += f"- {random.choice(details['examples'])}\n"
            response += f"- How to protect against {topic} threats\n"
            response += f"- Common {topic} mistakes to avoid\n"
            return response
        else:
            return "Topic not found. Try 'password', 'phishing', 'malware', or 'privacy'"

    def process_query(self, query):
        topic = self.detect_topic(query)
        
        if topic:
            response = self.get_topic_response(topic, query)
        else:
            response = random.choice(self.general_responses)
        
        return response
    
    def detect_topic(self, text):
        text = text.lower()
        for topic in self.knowledge_base:
            if topic in text:
                return topic
        return None
    
    def get_topic_response(self, topic, query):
        examples = self.knowledge_base[topic]['examples']
        
        if "how" in query.lower():
            return f"{examples[0]}\n\n{examples[1]}"
        elif "why" in query.lower():
            return f"{examples[-1]}\n\nPro Tip: {random.choice(examples)}"
        else:
            return random.choice(examples)
    
    def start_quiz(self, topic):
        quiz = self.knowledge_base[topic]['quiz'][0]
        quiz_text = f"\n🔐 {self.knowledge_base[topic]['name'].upper()} QUIZ\n"
        quiz_text += f"\n{quiz['question']}\n"
        for option in quiz['options']:
            quiz_text += f"  {option}\n"
        return quiz_text, quiz['answer'], quiz['explanation']

# GUI Implementation
class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        self.bot = CyberSecurityChatbot()
        self.current_quiz = None
        
        master.title("Cyber Security Chatbot")
        master.geometry("800x600")
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled')
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(master)
        input_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.user_input = tk.Entry(input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)
        
        send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT)
        
        # Display banner
        self.display_message(self.bot.get_banner_text(), is_bot=True)
    
    def send_message(self, event=None):
        user_input = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)
        
        if not user_input:
            return
        
        self.display_message(user_input, is_bot=False)
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            self.display_message("Stay safe online! Goodbye!", is_bot=True)
            self.master.after(2000, self.master.destroy)
            return
        
        if user_input.lower() == 'examples':
            topic = random.choice(list(self.bot.knowledge_base.keys()))
            response = self.bot.show_topic_details(topic)
            self.display_message(response, is_bot=True)
            return
        
        if user_input.lower() == 'quiz':
            topic = random.choice(list(self.bot.knowledge_base.keys()))
            quiz_text, correct_answer, explanation = self.bot.start_quiz(topic)
            self.display_message(quiz_text, is_bot=True)
            self.current_quiz = (correct_answer, explanation)
            return
        
        if self.current_quiz:
            answer = user_input.upper()
            if answer in ['A', 'B', 'C', 'D']:
                correct_answer, explanation = self.current_quiz
                if answer == correct_answer:
                    response = f"✅ Correct!\n{explanation}"
                else:
                    response = f"❌ Incorrect.\nThe right answer is {correct_answer}. {explanation}"
                self.display_message(response, is_bot=True)
                self.current_quiz = None
            else:
                self.display_message("Please enter A, B, C, or D", is_bot=True)
            return
        
        if user_input.lower() in self.bot.knowledge_base:
            response = self.bot.show_topic_details(user_input.lower())
            self.display_message(response, is_bot=True)
            return
        
        response = self.bot.process_query(user_input)
        self.display_message(response, is_bot=True)
    
    def display_message(self, message, is_bot=False):
        self.chat_display.config(state='normal')
        if is_bot:
            self.chat_display.insert(tk.END, "\nCyberGuard: ", 'bot')
            self.chat_display.insert(tk.END, f"{message}\n")
        else:
            self.chat_display.insert(tk.END, "\nYou: ", 'user')
            self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
        # Configure tags for colors
        self.chat_display.tag_config('bot', foreground='green')
        self.chat_display.tag_config('user', foreground='blue')

# Web Implementation
app = Flask(__name__)
bot = CyberSecurityChatbot()
current_quiz = None

@app.route("/", methods=["GET", "POST"])
def home():
    global current_quiz
    
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        
        if not user_input:
            return render_template()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            return render_template("Stay safe online! Goodbye!")
        
        if user_input.lower() == 'examples':
            topic = random.choice(list(bot.knowledge_base.keys()))
            return render_template(bot.show_topic_details(topic))
        
        if user_input.lower() == 'quiz':
            topic = random.choice(list(bot.knowledge_base.keys()))
            quiz_text, correct_answer, explanation = bot.start_quiz(topic)
            current_quiz = (correct_answer, explanation)
            return render_template(quiz_text)
        
        if current_quiz:
            answer = user_input.upper()
            if answer in ['A', 'B', 'C', 'D']:
                correct_answer, explanation = current_quiz
                if answer == correct_answer:
                    response = f"✅ Correct!<br>{explanation}"
                else:
                    response = f"❌ Incorrect.<br>The right answer is {correct_answer}. {explanation}"
                current_quiz = None
                return render_template(response)
            else:
                return render_template("Please enter A, B, C, or D")
        
        if user_input.lower() in bot.knowledge_base:
            return render_template(bot.show_topic_details(user_input.lower()))
        
        return render_template(bot.process_query(user_input))
    
    return render_template(bot.get_banner_text())

def render_template(message=None):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyber Security Chatbot</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .chat-container { border: 1px solid #ddd; border-radius: 5px; padding: 10px; height: 500px; overflow-y: auto; margin-bottom: 10px; }
            .bot { color: green; font-weight: bold; }
            .user { color: blue; font-weight: bold; }
            input[type="text"] { width: 70%; padding: 8px; }
            input[type="submit"] { padding: 8px 15px; }
            .banner { white-space: pre-wrap; font-family: monospace; }
        </style>
    </head>
    <body>
        <h1>Cyber Security Chatbot</h1>
        <div class="chat-container" id="chat">
            <div class="banner">{{ banner }}</div>
            {% if message %}
            <div class="bot">CyberGuard: {{ message | safe }}</div>
            {% endif %}
        </div>
        <form method="POST">
            <input type="text" name="user_input" placeholder="Type your message here..." autofocus>
            <input type="submit" value="Send">
        </form>
        <script>
            window.onload = function() {
                document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, banner=bot.get_banner_text(), message=message)

def run_gui():
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()

def run_web():
    app.run(port=5000)

if __name__ == "__main__":
    print("Choose how to run the chatbot:")
    print("1. GUI (Tkinter window)")
    print("2. Web (Flask server)")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        run_gui()
    elif choice == "2":
        print("Starting web server at http://localhost:5000")
        run_web()
    else:
        print("Invalid choice. Running GUI by default.")
        run_gui()