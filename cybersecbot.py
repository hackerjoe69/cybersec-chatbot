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
    
    def print_banner(self):
        banner = f"""
        {Fore.RED}╔════════════════════════════════════════════════╗
        {Fore.RED}║{Fore.YELLOW}       🛡️  {Fore.CYAN}CYBER SECURITY CHATBOT{Fore.YELLOW} 🛡️        {Fore.RED}║
        {Fore.RED}╚════════════════════════════════════════════════╝
        {Style.RESET_ALL}
        {Fore.GREEN}Available Topics:{Style.RESET_ALL}
        
        {Fore.YELLOW}1. Password Security{Style.RESET_ALL} (type 'password')
        - Creating strong credentials
        - Password managers
        - Multi-factor authentication
        Example: "How long should my password be?"
        
        {Fore.YELLOW}2. Phishing Detection{Style.RESET_ALL} (type 'phishing')
        - Email/SMS scams
        - Fake websites
        - Social engineering
        Example: "How can I spot a fake login page?"
        
        {Fore.YELLOW}3. Malware Protection{Style.RESET_ALL} (type 'malware')
        - Viruses & ransomware
        - Protection methods
        - Incident response
        Example: "What should I do if I downloaded malware?"
        
        {Fore.YELLOW}4. Online Privacy{Style.RESET_ALL} (type 'privacy')
        - Social media settings
        - VPNs & encryption
        - Data minimization
        Example: "Is public WiFi safe for banking?"
        
        {Fore.YELLOW}Type:{Style.RESET_ALL}
        - 'quiz' for an interactive test
        - 'examples' for more scenario samples
        - 'quit' to exit
        """
        print(banner)
    
    def show_topic_details(self, topic):
        if topic in self.knowledge_base:
            details = self.knowledge_base[topic]
            print(f"\n{Fore.CYAN}=== {details['name']} ==={Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{details['description']}{Style.RESET_ALL}")
            print(f"\n{Fore.GREEN}Key Examples:{Style.RESET_ALL}")
            for i, example in enumerate(details['examples'], 1):
                print(f"{i}. {example}")
            print(f"\n{Fore.MAGENTA}Try asking about:{Style.RESET_ALL}")
            print(f"- {random.choice(details['examples'])}")
            print(f"- How to protect against {topic} threats")
            print(f"- Common {topic} mistakes to avoid")
        else:
            print(f"{Fore.RED}Topic not found. Try 'password', 'phishing', 'malware', or 'privacy'{Style.RESET_ALL}")

    def run(self):
        self.print_banner()
        current_quiz_topic = None
        
        while True:
            try:
                user_input = input(f"\n{Fore.BLUE}You:{Style.RESET_ALL} ").strip().lower()
                
                if user_input in ['exit', 'quit', 'bye']:
                    print(f"{Fore.RED}\nStay safe online! Goodbye!{Style.RESET_ALL}")
                    break
                
                # Handle special commands
                if user_input == 'examples':
                    topic = random.choice(list(self.knowledge_base.keys()))
                    self.show_topic_details(topic)
                    continue
                
                if user_input == 'quiz':
                    topic = random.choice(list(self.knowledge_base.keys()))
                    self.start_quiz(topic)
                    continue
                
                # Show topic details if user enters a topic name
                if user_input in self.knowledge_base:
                    self.show_topic_details(user_input)
                    continue
                
                # Process other queries
                self.process_query(user_input)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}\nSession ended. Remember to practice good cyber hygiene!{Style.RESET_ALL}")
                break
    
    def process_query(self, query):
        topic = self.detect_topic(query)
        
        if topic:
            response = self.get_topic_response(topic, query)
        else:
            response = random.choice(self.general_responses)
        
        self.type_response(response)
    
    def detect_topic(self, text):
        text = text.lower()
        for topic in self.knowledge_base:
            if topic in text:
                return topic
        return None
    
    def get_topic_response(self, topic, query):
        examples = self.knowledge_base[topic]['examples']
        
        # Check for specific question patterns
        if "how" in query:
            return f"{examples[0]}\n\n{examples[1]}"
        elif "why" in query:
            return f"{examples[-1]}\n\n{Fore.YELLOW}Pro Tip:{Style.RESET_ALL} {random.choice(examples)}"
        else:
            return random.choice(examples)
    
    def start_quiz(self, topic):
        quiz = self.knowledge_base[topic]['quiz'][0]
        print(f"\n{Fore.CYAN}🔐 {self.knowledge_base[topic]['name'].upper()} QUIZ{Style.RESET_ALL}")
        print(f"\n{quiz['question']}")
        for option in quiz['options']:
            print(f"  {option}")
        
        while True:
            answer = input("\nYour answer (A/B/C/D): ").upper()
            if answer in ['A', 'B', 'C', 'D']:
                if answer == quiz['answer']:
                    print(f"{Fore.GREEN}✅ Correct!{Style.RESET_ALL} {quiz['explanation']}")
                else:
                    print(f"{Fore.RED}❌ Incorrect.{Style.RESET_ALL} The right answer is {quiz['answer']}. {quiz['explanation']}")
                break
            else:
                print(f"{Fore.YELLOW}Please enter A, B, C, or D{Style.RESET_ALL}")
    
    def type_response(self, text):
        print(f"\n{Fore.GREEN}CyberGuard:{Style.RESET_ALL} ", end='', flush=True)
        for char in text:
            print(char, end='', flush=True)
            sleep(0.02)
        print()

if __name__ == "__main__":
    chatbot = CyberSecurityChatbot()
    chatbot.run()