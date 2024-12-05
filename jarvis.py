import openai
import webbrowser
import requests
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import tkinter as tk

print(f"welcome to adrian programs".capitalize())
# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Use female voice (change index for male)

# Set OpenAI API key (your provided key)
openai.api_key = ""

# Weather API setup
WEATHER_API_KEY = ""  # Your OpenWeatherMap API key
CITY = ""  # Your city name

def speak(text):
    """Speak the provided text."""
    engine.say(text)
    engine.runAndWait()

def recognize_voice():
    """Recognize voice command from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return "I couldn't connect to the speech recognition service."
        except Exception as e:
            return str(e)

def get_weather():
    """Fetch the current weather using OpenWeatherMap API."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("main"):
            temp = response["main"]["temp"]
            description = response["weather"][0]["description"]
            return f"The current temperature in {CITY} is {temp}°C with {description}."
        else:
            return "I couldn't fetch the weather information right now."
    except Exception as e:
        return "An error occurred while fetching the weather."

def greet_user():
    """Greet the user based on the time of day."""
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good morning, boss!"
    elif 12 <= current_hour < 18:
        return "Good afternoon, boss!"
    else:
        return "Good evening, boss!"

def chat_with_gpt(prompt):
    """
    Send a prompt to OpenAI's GPT-3.5 and get the response.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are JARVIS, an intelligent AI assistant. Be concise and helpful."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return "I couldn't fetch a response from the AI service."

def jarvis_main(gui_label):
    """
    Main loop for JARVIS.
    """
    gui_label.config(text="Waking up JARVIS...", fg="cyan")
    speak("JARVIS is online.")
    greeting = greet_user()
    speak(greeting)
    weather_info = get_weather()
    speak(weather_info)
    speak("What are today's plans?")
    
    while True:
        gui_label.config(text="Listening for your command...", fg="cyan")
        command = recognize_voice()
        if command:
            gui_label.config(text=f"Command: {command}", fg="cyan")
            if 'open youtube' in command:
                webbrowser.open('https://www.youtube.com')
                speak("Opening YouTube")
            elif 'search for' in command or 'on google' in command:
                search_query = command.replace("search for", "").replace("on google", "").strip()
                webbrowser.open(f'https://www.google.com/search?q={search_query}')
                speak(f"Searching Google for {search_query}")
            elif 'chat mode' in command:
                speak("Entering chat mode. Ask me anything.")
                while True:
                    gui_label.config(text="Chat mode active. Speak your query.", fg="cyan")
                    chat_query = recognize_voice()
                    if chat_query and 'exit chat' in chat_query:
                        speak("Exiting chat mode.")
                        break
                    elif chat_query:
                        gpt_response = chat_with_gpt(chat_query)
                        gui_label.config(text=gpt_response, fg="green")
                        speak(gpt_response)
            elif 'close app' in command:
                speak("Which application would you like to close?")
                # Implement app-closing logic here
            elif 'sleep jarvis' in command:
                speak("Goodbye, boss. Shutting down.")
                gui_label.config(text="JARVIS is shutting down...", fg="red")
                break
            else:
                gpt_response = chat_with_gpt(command)
                gui_label.config(text=gpt_response, fg="green")
                speak(gpt_response)
        else:
            gui_label.config(text="No command detected.", fg="red")
            speak("I didn't understand that. Please say it again.")

def gui():
    """
    GUI for JARVIS.
    """
    root = tk.Tk()
    root.title("JARVIS AI Assistant")
    root.geometry("600x400")
    root.configure(bg="black")

    label = tk.Label(root, text="JARVIS is offline", fg="white", bg="black", font=("Helvetica", 16))
    label.pack(pady=20)

    start_button = tk.Button(root, text="Wake Up JARVIS", command=lambda: jarvis_main(label), font=("Helvetica", 14), bg="green", fg="white")
    start_button.pack(pady=10)

    quit_button = tk.Button(root, text="Close JARVIS", command=root.quit, font=("Helvetica", 14), bg="red", fg="white")
    quit_button.pack(pady=10)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    gui()
