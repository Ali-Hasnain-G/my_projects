import nltk
from nltk.chat.util import Chat, reflections

# Define pairs of patterns and responses
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how can I help you today?",]
    ],
    [
        r"what is your name?",
        ["My name is ChatBot and I'm here to assist you.",]
    ],
    [
        r"how are you ?",
        ["I'm doing good\nHow about You ?",]
    ],
    [
        r"sorry (.*)",
        ["It's alright", "It's OK, never mind",]
    ],
    [
        r"(.*) thank you (.*)",
        ["You're welcome", "You're welcome :)",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ],
    [
        r"quit",
        ["Bye, take care. See you soon :) ", "It was nice talking to you. Goodbye!"]
    ],
]

# Create a ChatBot instance
def chatbot():
    print("Hi, I'm ChatBot! How can I assist you today?")
    chatbot = Chat(pairs, reflections)
    chatbot.converse()

if __name__ == "__main__":
    nltk.download('punkt')
    chatbot()
