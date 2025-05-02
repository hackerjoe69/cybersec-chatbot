import re
import random
from time import sleep
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class CyberSecurityChatbot:
    def __init__(self):
        self.knowledge_base = {
            "password": {
                "name": "Password Security",
                "responses": [
                    "Strong passwords should be at least 12 characters long with a mix of letters, numbers, and symbols.",
                    "Never reuse passwords across different accounts - use a password manager like Bitwarden or KeePass.",
                    "Enable two-factor authentication (2FA) whenever possible for extra security."
                ],
                "quiz": [
                    {
                        "question": "What's the minimum recommended length for a strong password?",
                        "options": ["A) 6 characters", "B) 8 characters", "C) 12 characters", "D) 16 characters"],
                        "answer": "C",
                        "explanation": "12 characters is the current minimum recommendation by cybersecurity experts."
                    }
                ]
            },
            "phishing": {
                "name": "Phishing Awareness",
                "responses": [
                    "Phishing emails often create urgency ('Your account will be closed!') to trick you.",
                    "Check sender addresses carefully - 'support@amaz0n.com' is fake (notice the zero).",
                    "Never click links in unexpected emails - go directly to the official website instead."
                ],
                "quiz": [
                    {
                        "question": "Which of these is a red flag in an email?",
                        "options": [
                            "A) Generic greeting like 'Dear Customer'",
                            "B) Urgent call to action",
                            "C) Suspicious sender address",
                            "D) All of the above"
                        ],
                        "answer": "D",
                        "explanation": "All these are common signs of phishing attempts."
                    }
                ]
            },
            "malware": {
                "name": "Malware Protection",
                "responses": [
                    "Only download software from official sources like vendor websites or app stores.",
                    "Keep your operating system and antivirus software updated regularly.",
                    "Be cautious with USB drives from unknown sources - they can contain malware."
                ],
                "quiz": [
                    {
                        "question": "What's the best defense against ransomware?",
                        "options": [
                            "A) Paying the ransom",
                            "B) Regular backups",
                            "C) Disabling antivirus",
                            "D) Using the same password everywhere"
                        ],
                        "answer": "B",
                        "explanation": "Regular, offline backups are your best protection against ransomware."
                    }
                ]
            },
            "privacy": {
                "name": "Online Privacy",
                "responses": [
                    "Use a VPN when on public WiFi to encrypt your internet traffic.",
                    "Review privacy settings on social media every few months.",
                    "Consider using privacy-focused browsers like Firefox with uBlock Origin."
                ],
                "quiz": [
                    {
                        "question": "What does a VPN help protect?",
                        "options": [
                            "A) Your internet browsing history",
                            "B) Your physical location",
                            "C) Your data on public WiFi",
                            "D) All of the above"
                        ],
                        "answer": "D",
                        "explanation": "VPNs help protect all these aspects of your privacy."
                    }
                ]
            }
        }
        
        self.general_responses = [
            "Cybersecurity is about protecting systems, networks, and data from digital attacks.",
            "Good security habits are like brushing your teeth - do them regularly!",
            "Remember: If something seems too good to be true online, it probably is."
        ]
    
    def print_banner(self):
        banner = f"""
        {Fore.RED}╔════════════════════════════════════════════════╗
        {Fore.RED}║{Fore.YELLOW}       🛡️  {Fore.CYAN}CYBER SECURITY CHATBOT{Fore.YELLOW} 🛡️        {Fore.RED}║
        {Fore.RED}╚════════════════════════════════════════════════╝
        {Style.RESET_ALL}
        {Fore.GREEN}Learn about:{Style.RESET_ALL}
        • Password security (type 'password')
        • Phishing detection (type 'phishing')
        • Malware protection (type 'malware')
        • Online privacy (type 'privacy')
        
        {Fore.YELLOW}Type 'quiz' for a quick test or 'quit' to exit{Style.RESET_ALL}
        """
        print(banner)
    
    def get_response(self, user_input):
        user_input = user_input.lower()
        
        # Check for specific topics
        for topic in self.knowledge_base:
            if topic in user_input:
                return random.choice(self.knowledge_base[topic]["responses"])
        
        # Check for quiz request
        if "quiz" in user_input:
            topic = self.detect_topic(user_input)
            if topic:
                return self.generate_quiz(topic)
            else:
                topic = random.choice(list(self.knowledge_base.keys()))
                return self.generate_quiz(topic)
        
        # Default response
        return random.choice(self.general_responses)
    
    def detect_topic(self, text):
        text = text.lower()
        for topic in self.knowledge_base:
            if topic in text:
                return topic
        return None
    
    def generate_quiz(self, topic):
        quiz_data = random.choice(self.knowledge_base[topic]["quiz"])
        quiz_str = f"\n{Fore.CYAN}🔐 {self.knowledge_base[topic]['name'].upper()} QUIZ{Style.RESET_ALL}\n"
        quiz_str += f"\n{quiz_data['question']}\n"
        for option in quiz_data["options"]:
            quiz_str += f"  {option}\n"
        
        quiz_str += f"\n{Fore.YELLOW}Think you know the answer? Type A, B, C, or D.{Style.RESET_ALL}"
        return quiz_str
    
    def check_quiz_answer(self, topic, answer):
        quiz_data = self.knowledge_base[topic]["quiz"][0]  # Get first quiz question
        if answer.upper() == quiz_data["answer"]:
            return f"{Fore.GREEN}Correct!{Style.RESET_ALL} {quiz_data['explanation']}"
        else:
            return f"{Fore.RED}Not quite.{Style.RESET_ALL} The correct answer is {quiz_data['answer']}. {quiz_data['explanation']}"
    
    def run(self):
        self.print_banner()
        current_quiz_topic = None
        
        while True:
            try:
                user_input = input(f"\n{Fore.BLUE}You:{Style.RESET_ALL} ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print(f"{Fore.RED}\nStay safe online! Goodbye!{Style.RESET_ALL}")
                    break
                
                # Check if we're expecting a quiz answer
                if current_quiz_topic:
                    response = self.check_quiz_answer(current_quiz_topic, user_input)
                    current_quiz_topic = None
                else:
                    if user_input.lower() == 'quiz':
                        topic = self.detect_topic(' '.join(self.conversation_history[-3:])) if self.conversation_history else None
                        if not topic:
                            topic = random.choice(list(self.knowledge_base.keys()))
                        response = self.generate_quiz(topic)
                        current_quiz_topic = topic
                    else:
                        response = self.get_response(user_input)
                
                # Print response with typewriter effect
                print(f"\n{Fore.GREEN}CyberGuard:{Style.RESET_ALL} ", end='', flush=True)
                for char in response:
                    print(char, end='', flush=True)
                    sleep(0.02)
                print()
                
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}\nSession ended. Remember to practice good cyber hygiene!{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    chatbot = CyberSecurityChatbot()
    chatbot.run()