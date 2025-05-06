import re
import random
from difflib import get_close_matches

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Ensure NLTK resources are available, quiet downloads
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class EnhancedChatbot:
    def __init__(self):
        self.faqs = {
            "return policy": [
                "Our return policy allows returns within 30 days of purchase. Please visit our returns page for more details: /returns/",
                ["return policy", "returns", "refund", "money back", "send back", "return item"]
            ],
            "track order": [
                "You can track your order by visiting the 'Order History' section in your account dashboard after login:",
                ["track order", "where is my order", "order status", "package location", "delivery status",
                 "shipping status"]
            ],
            "payment methods": [
                "We accept all major credit cards (Visa, Mastercard, American Express), eSewa, Khalti and cash on delivery.",
                ["payment", "pay", "credit card", "debit card", "cash on delivery", "esewa", "khalti"]
            ],
            "shipping time": [
                "Shipping typically takes 2-5 business days for domestic orders. International shipping may take 7-14 business days depending on your location.",
                ["shipping time", "delivery time", "how long shipping", "when will arrive", "delivery duration"]
            ],
            "international shipping": [
                "Yes, we offer international shipping to most countries. Shipping times and costs vary by destination. Check our shipping calculator at checkout for exact rates.",
                ["international shipping", "ship overseas", "global delivery", "worldwide shipping",
                 "ship to another country"]
            ],
            "create account": [
                "You can create an account by clicking on the 'Sign Up' link in the top-right corner of our homepage or by visiting: /accounts/register/",
                ["create account", "sign up", "register", "join", "new account"]
            ],
            "customer support": [
                "You can contact our customer support team via phone at +977-1234567890 or email at support@example.com. Our live chat is also available Monday-Friday, 9AM-5PM.",
                ["customer support", "help", "contact", "assistance", "service", "speak to someone", "talk to agent"]
            ],
            "privacy policy": [
                "You can view our privacy policy here: /privacy-policy/",
                ["privacy policy", "data usage", "information policy", "personal data"]
            ],
            "payment security": [
                "Yes, we use industry-standard SSL encryption to ensure your payment details are secure. We are also PCI DSS compliant.",
                ["payment secure", "card security", "secure checkout", "safe payment", "data encryption"]
            ],
            "place order": [
                "To place an order, add the desired items to your cart, then proceed to checkout. You can review your order before finalizing the purchase.",
                ["place order", "buy", "purchase", "checkout", "order item", "make purchase"]
            ],
            "password reset": [
                "You can reset your password here: /accounts/password_reset/",
                ["reset password", "forgot password", "change password", "password recovery", "can't login"]
            ],
            "account access": [
                "You can access your account details here: /accounts/profile/",
                ["my account", "account details", "profile", "personal information", "account settings"]
            ],
            "business hours": [
                "Our customer service is available Monday through Friday, 9AM to 6PM. Our physical stores are open daily from 10AM to 8PM.",
                ["business hours", "opening hours", "store hours", "when open", "operation hours"]
            ],
            "product warranty": [
                "Most of our products come with a standard 1-year warranty. Extended warranties are available for select items.",
                ["warranty", "guarantee", "product protection", "coverage", "repair policy"]
            ], "phone number": [
                "+977 9866413343", ["phone number", "call", "contact"]
            ]
        }
        self.greetings = {
            "hello": ["Hi there! How can I help you today?", "Hello! What can I assist you with?",
                      "Greetings! How may I help you?"],
            "bye": ["Goodbye! Feel free to chat again if you have more questions.",
                    "Have a great day! Come back anytime.", "Bye! Thanks for chatting with us."]
        }
        self.conversation_context = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = word_tokenize(text)
        filtered_tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]

        return " ".join(filtered_tokens)

    def get_best_match(self, user_query, options, threshold=0.6):
        """Find the best matching option for the user query"""
        preprocessed_query = self.preprocess_text(user_query)

        best_match = None
        best_ratio = 0

        for option in options:
            match = get_close_matches(preprocessed_query, [option], n=1, cutoff=threshold)
            if match and len(match) > 0:
                ratio = 1.0  # Exact match found
                if ratio > best_ratio:
                    best_match = option
            else:
                query_tokens = set(preprocessed_query.split())
                option_tokens = set(self.preprocess_text(option).split())
                common_tokens = query_tokens.intersection(option_tokens)

                if common_tokens:
                    ratio = len(common_tokens) / max(len(query_tokens), len(option_tokens))
                    if ratio > best_ratio and ratio >= threshold:
                        best_ratio = ratio
                        best_match = option

        return best_match

    def check_for_keywords(self, user_message):
        """Check if any keywords from FAQ matches appear in the message"""
        for _, (response, keywords) in self.faqs.items():
            for keyword in keywords:
                if keyword in user_message:
                    return response
        return None

    def get_order_status(self, user_message):
        # Try to extract order ID using regex
        order_id_match = re.search(r'(?:order|id)[:\s]*#?([a-zA-Z0-9-]+)', user_message, re.IGNORECASE)

        if order_id_match:
            order_id = order_id_match.group(1).strip()
            return f"Thank you. I've found your order #{order_id}. Your order is currently being processed and will be shipped within 24 hours. You'll receive a tracking number via email once shipped."
        elif "order status" in user_message or "where is my order" in user_message or "track" in user_message:
            self.conversation_context = "awaiting_order_id"
            return "I'd be happy to help you track your order. Could you please provide your order ID? It should be in your confirmation email or account dashboard."
        return None

    def process_message(self, user_message):
        user_message = user_message.lower().strip()
        if self.conversation_context == "awaiting_order_id":
            self.conversation_context = None
            if re.search(r'[a-zA-Z0-9-]{4,}', user_message):
                order_id = re.search(r'[a-zA-Z0-9-]{4,}', user_message).group(0)
                return f"Thank you. I've found your order #{order_id}. Your order is currently being processed and will be shipped within 24 hours. You'll receive a tracking number via email once shipped."
            return "I couldn't identify an order ID in your message. Please make sure to include your complete order ID. Alternatively, you can check your order status by logging into your account at /orders/history/"

        for greeting_type, responses in self.greetings.items():
            if greeting_type in user_message or self.get_best_match(user_message, [greeting_type], threshold=0.7):
                return random.choice(responses)

        keyword_response = self.check_for_keywords(user_message)
        if keyword_response:
            return keyword_response

        order_status_response = self.get_order_status(user_message)
        if order_status_response:
            return order_status_response

        for faq_key, (response, keywords) in self.faqs.items():
            match = self.get_best_match(user_message, keywords, threshold=0.5)
            if match:
                return response

        return "I'm not sure I understand your question. For further assistance, please call our customer support team at +977-1234567890. " \
               "You might also find answers to common questions about our return policy, shipping, payment methods, or order tracking. "


def process_message(user_message):
    if not hasattr(process_message, '_chatbot_instance'):
        process_message._chatbot_instance = EnhancedChatbot()
    return process_message._chatbot_instance.process_message(user_message)