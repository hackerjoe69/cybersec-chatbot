import groq
import re
import random
from time import sleep
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class CyberSecurityChatbot:
    def __init__(self, api_key):
        self.client = groq.Client(api_key=api_key)
        self.conversation_history = []
        self.topics = {
            "password": {
                "name": "Password Security",
                "examples": [
                    "How to create strong passwords?",
                    "What is password hashing?",
                    "Why shouldn't I reuse passwords?"
                ]
            },
            "phishing": {
                "name": "Phishing Awareness",
                "examples": [
                    "How to spot a phishing email?",
                    "What are common phishing tactics?",
                    "What should I do if I clicked a phishing link?"
                ]
            },
            "malware": {
                "name": "Malware Protection",
                "examples": [
                    "How does malware spread?",
                    "What's the difference between viruses and worms?",
                    "How to protect against ransomware?"
                ]
            },
            "privacy": {
                "name": "Online Privacy",
                "examples": [
                    "How to browse anonymously?",
                    "What is VPN and do I need one?",
                    "How to protect my social media privacy?"
                ]
            }
        }
        
        # System message to guide the AI's behavior
        self.system_message = {
            "role": "system",
            "content": """You are CyberGuard, an advanced cybersecurity teaching assistant. Your role is to:
            1. Teach cybersecurity concepts in simple, engaging ways
            2. Provide interactive examples and scenarios
            3. Ask follow-up questions to check understanding
            4. Use analogies and real-world examples
            5. Never reveal sensitive or harmful information
            6. Correct misconceptions gently
            7. Adapt explanations to the user's knowledge level
            8. Use markdown formatting for code snippets and important points"""
        }
        
        self.conversation_history.append(self.system_message)
    
    def print_banner(self):
        banner = f"""
        {Fore.RED}╔════════════════════════════════════════════════╗
        {Fore.RED}║{Fore.YELLOW}       🛡️  {Fore.CYAN}CYBER SECURITY CHATBOT{Fore.YELLOW} 🛡️        {Fore.RED}║
        {Fore.RED}╚════════════════════════════════════════════════╝
        {Style.RESET_ALL}
        {Fore.GREEN}Learn about:{Style.RESET_ALL}
        • Password security
        • Phishing detection
        • Malware protection
        • Online privacy
        
        {Fore.YELLOW}Type 'quit' to exit{Style.RESET_ALL}
        """
        print(banner)
    
    def get_ai_response(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",  # Groq's fastest model
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=500
            )
            
            ai_reply = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_reply})
            return ai_reply
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def format_response(self, text):
        # Highlight important security terms
        security_terms = ["phishing", "malware", "ransomware", "VPN", "2FA", 
                         "encryption", "firewall", "password manager", "social engineering"]
        
        for term in security_terms:
            text = text.replace(term, f"{Fore.YELLOW}{term}{Style.RESET_ALL}")
        
        # Format code blocks if present
        text = re.sub(r'```(.*?)```', f'{Fore.BLUE}\\1{Style.RESET_ALL}', text, flags=re.DOTALL)
        
        return text
    
    def interactive_quiz(self, topic):
        """Generate an interactive quiz on the selected topic"""
        quiz_prompt = f"""
        Create a short interactive quiz (3 questions) about {topic}.
        Format each question with:
        1. The question text
        2. Multiple choice options (A-D)
        3. The correct answer
        4. A brief explanation
        
        Present one question at a time and wait for user response before continuing.
        """
        
        quiz = self.get_ai_response(quiz_prompt)
        print(f"\n{Fore.CYAN}🔐 {topic.upper()} QUIZ{Style.RESET_ALL}")
        
        # Split questions and present one at a time
        questions = quiz.split("\n\n")
        for i, question in enumerate(questions[:3]):  # Take first 3 questions
            print(f"\n{Fore.GREEN}Question {i+1}:{Style.RESET_ALL}")
            print(question)
            
            if i < 2:  # Don't pause after last question
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def run(self):
        self.print_banner()
        
        while True:
            try:
                # Show topic suggestions randomly
                if len(self.conversation_history) <= 1:  # Only system message
                    topic = random.choice(list(self.topics.keys()))
                    examples = self.topics[topic]["examples"]
                    print(f"\n{Fore.MAGENTA}Try asking about {self.topics[topic]['name']}:")
                    for ex in examples:
                        print(f" • {ex}")
                    print(Style.RESET_ALL)
                
                user_input = input(f"\n{Fore.BLUE}You:{Style.RESET_ALL} ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print(f"{Fore.RED}\nStay safe online! Goodbye!{Style.RESET_ALL}")
                    break
                
                # Check for quiz request
                if "quiz" in user_input.lower():
                    topic_match = re.search(r'quiz about (.*?)$', user_input.lower())
                    if topic_match:
                        topic = topic_match.group(1)
                        self.interactive_quiz(topic)
                    else:
                        topic = random.choice(list(self.topics.keys()))
                        self.interactive_quiz(self.topics[topic]["name"])
                    continue
                
                # Get AI response
                print(f"\n{Fore.GREEN}CyberGuard:{Style.RESET_ALL} ", end='', flush=True)
                
                response = self.get_ai_response(user_input)
                formatted_response = self.format_response(response)
                
                # Typewriter effect
                for char in formatted_response:
                    print(char, end='', flush=True)
                    sleep(0.02)
                print()
                
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}\nSession ended. Remember to practice good cyber hygiene!{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    # Replace with your actual Groq API key
    API_KEY = "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"
    
    if API_KEY.startswith("gsk-your"):
        print(f"{Fore.RED}ERROR: Please replace 'gsk-your-groq-api-key-here' with your actual Groq API key{Style.RESET_ALL}")
    else:
        chatbot = CyberSecurityChatbot(API_KEY)
        chatbot.run()