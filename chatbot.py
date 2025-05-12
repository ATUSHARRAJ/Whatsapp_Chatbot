from openai import OpenAI
from PIL import Image
import pyautogui
import time
import requests
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


client = OpenAI(
    api_key="###########################"
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Function to open WhatsApp
def open_whatsapp(contact_name):
    pyautogui.hotkey('win', 's')  # Open the search bar (Windows)
    time.sleep(1)
    pyautogui.write('WhatsApp')  # Search for WhatsApp
    pyautogui.press('enter')  # Press Enter to open WhatsApp
    time.sleep(4) 
    pyautogui.click(x=178, y=183)  # Adjust with your coordinates
    pyautogui.write(contact_name)  # Type the contact name  # Open the chat
    time.sleep(4)
    pyautogui.click(x=232, y=282) # Wait for WhatsApp to open

# Function to send a message to a specific contact
#get message

def capture_whatsapp_message(x, y, width, height):
    # Take screenshot of the specified region
    time.sleep(2)
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot_path = "screenshot.png"
    
    # Save the screenshot
    screenshot.save(screenshot_path)

    # Perform OCR to extract text
    text = pytesseract.image_to_string(screenshot)
    print("Extracted Text:")
    print(text)
    time.sleep(2)
    os.remove(screenshot_path)

    return text
def send_message(message): 
    pyautogui.click(x=995, y=978)  
    pyautogui.write(message) 
    time.sleep(2) 
    pyautogui.press('enter')  
#genai 

avaiable_tools = {
    "open_whatsapp": {
        "fn": open_whatsapp,
        "description": "This function opens the WhatsApp application on the system."
    },
    "send_message": {
        "fn": send_message,
        "description": "This function sends a message to a specific contact on WhatsApp."
    }
}
systemPrompt = """You are an AI assistant named Tushar. You should always respond in a friendly, brief, and to-the-point manner, focusing only on the required response.
And you  use hinglish language. 
Use your commom sense also not just my examples. First see the input and find what could be possible output then give
the proper output according to you but the output must be in hinglish language and words must match with my tone of ouput.

Always make conversation in a friendly way.

I am giving you  some examples how should be your output.
Follow the examples to undestand my tone of output.

Examples are : 
input: Good Morning
output: Good morning

input: Kkrh
output: kuch nhii?

input: Ohoo jao jaao
output: dekhte hai jaynge ya nhii?

input: aur batao?
output: aur sab mast.
input: hii
output: hlw
And also i am giving some words that make you easy to understand how your output must look like, use this type of patterns for your output. 
example words are:
Kkrh , aur batao , ja rhe hai.

"""
messages=[
            {"role": "system", "content": systemPrompt},

        ]
def get_ai_response(user_query):
    messages.append(
        {"role": "user", "content": user_query}
    )
    print("User Query:", user_query)
    response = client.chat.completions.create(
        model="gemini-2.5-flash-preview-04-17",
        reasoning_effort="low",
        messages=messages
        
    )
    return response.choices[0].message.content
response = client.chat.completions.create(
    model="gemini-2.5-flash-preview-04-17",
    reasoning_effort="low",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)

if __name__ == "__main__":
    # Open WhatsApp
    open_whatsapp("Ayushi")
    
    # Get AI response
    while True:
     user_query = capture_whatsapp_message(500, 816, 500, 100)
     if user_query.strip()[:-4]:
       print(user_query)
       ai_response = get_ai_response(user_query)
       messages.append(
           {"role": "assistant", "content": ai_response}
       )
       send_message( ai_response)
       user_query = ""
       continue
     else:
         print("No message detected. Please try again.")
         time.sleep(4)
         continue

