#Jarvys_futures.py
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
import json
import webbrowser
import subprocess
import os

import sounddevice as sd
import pyttsx3
import ollama
from vosk import Model, KaldiRecognizer
from ddgs import DDGS


# ============================================================
# JARVYS SETTINGS
# ============================================================

VOSK_MODEL = "model"
OLLAMA_MODEL = "qwen3.5:0.8b"
SAMPLE_RATE = 16000


# ============================================================
# LOAD JARVYS
# ============================================================

print("==============================")
print("       JARVYS STARTING")
print("==============================")

print("Loading voice model...")

try:
    vosk_model = Model(VOSK_MODEL)
    print("Voice model loaded.")
except Exception as e:
    print("VOICE MODEL ERROR:", e)
    vosk_model = None

try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    print("Voice engine loaded.")
except Exception as e:
    print("TTS ERROR:", e)
    engine = None

print("JARVYS ready.")


# ============================================================
# VOICE OUTPUT
# ============================================================

def speak(text):

    print("JARVYS:", text)

    if engine is None:
        return

    try:
        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print("VOICE ERROR:", e)


# ============================================================
# VOICE INPUT
# ============================================================

def listen():

    if vosk_model is None:
        print("Voice model is not loaded.")
        return ""

    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):

        if status:
            print("MIC:", status)

        audio_queue.put(bytes(indata))

    recognizer = KaldiRecognizer(
        vosk_model,
        SAMPLE_RATE
    )

    print("🎤 Listening...")

    try:

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback
        ):

            while True:

                data = audio_queue.get()

                if recognizer.AcceptWaveform(data):

                    result = json.loads(
                        recognizer.Result()
                    )

                    text = result.get(
                        "text",
                        ""
                    ).strip()

                    if text:

                        print("YOU:", text)

                        return text

    except Exception as e:

        print("MIC ERROR:", e)

        return ""


# ============================================================
# WEB SEARCH
# ============================================================

def web_search(query):

    print("🌐 Searching:", query)

    try:

        results = DDGS().text(
            query,
            max_results=3
        )

        output = []

        for result in results:

            title = result.get(
                "title",
                ""
            )

            body = result.get(
                "body",
                ""
            )

            link = result.get(
                "href",
                ""
            )

            output.append(
                f"TITLE: {title}\n"
                f"INFO: {body}\n"
                f"LINK: {link}"
            )

        return "\n\n".join(output)

    except Exception as e:

        print("WEB ERROR:", e)

        return ""


# ============================================================
# DETECT WEB QUESTIONS
# ============================================================

def needs_web(text):

    words = [
        "latest",
        "today",
        "current",
        "news",
        "weather",
        "price",
        "recent",
        "now",
        "search",
        "internet",
        "who is",
        "what happened"
    ]

    text = text.lower()

    return any(
        word in text
        for word in words
    )


# ============================================================
# COMPUTER COMMANDS
# ============================================================

def handle_command(text):

    command = text.lower().strip()


    # ========================================================
    # CHROME
    # ========================================================

    if "open chrome" in command:

        chrome_paths = [

            r"C:\Program Files\Google\Chrome\Application\chrome.exe",

            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
            )
        ]

        for chrome_path in chrome_paths:

            if os.path.exists(chrome_path):

                try:

                    subprocess.Popen(
                        chrome_path
                    )

                    return "Opening Chrome."

                except Exception as e:

                    print(
                        "Chrome error:",
                        e
                    )

        try:

            subprocess.Popen(
                "chrome.exe"
            )

            return "Opening Chrome."

        except Exception:

            return (
                "Could not open Chrome. "
                "Chrome was not found."
            )


    # ========================================================
    # SPOTIFY
    # ========================================================

    if "open spotify" in command:

        try:

            # Try the Spotify application first
            subprocess.Popen(
                "spotify.exe"
            )

            return "Opening Spotify."

        except Exception:

            # If desktop application is unavailable,
            # open Spotify in browser
            webbrowser.open(
                "https://open.spotify.com"
            )

            return "Opening Spotify in your browser."


    # ========================================================
    # DOWNLOADS
    # ========================================================

    if "open downloads" in command:

        try:

            subprocess.Popen(
                [
                    "explorer.exe",
                    "shell:Downloads"
                ]
            )

            return "Opening Downloads."

        except Exception as e:

            return (
                f"Could not open Downloads: {e}"
            )


    # ========================================================
    # DESKTOP
    # ========================================================

    if "open desktop" in command:

        try:

            subprocess.Popen(
                [
                    "explorer.exe",
                    "shell:Desktop"
                ]
            )

            return "Opening Desktop."

        except Exception as e:

            return (
                f"Could not open Desktop: {e}"
            )


    # ========================================================
    # DOCUMENTS
    # ========================================================

    if "open documents" in command:

        try:

            subprocess.Popen(
                [
                    "explorer.exe",
                    "shell:Documents"
                ]
            )

            return "Opening Documents."

        except Exception as e:

            return (
                f"Could not open Documents: {e}"
            )


    # ========================================================
    # YOUTUBE
    # ========================================================

    if "open youtube" in command:

        try:

            webbrowser.open(
                "https://www.youtube.com"
            )

            return "Opening YouTube."

        except Exception as e:

            return (
                f"Could not open YouTube: {e}"
            )


    # ========================================================
    # GOOGLE
    # ========================================================

    if "open google" in command:

        try:

            webbrowser.open(
                "https://www.google.com"
            )

            return "Opening Google."

        except Exception as e:

            return (
                f"Could not open Google: {e}"
            )


    # ========================================================
    # GITHUB
    # ========================================================

    if "open github" in command:

        try:

            webbrowser.open(
                "https://github.com"
            )

            return "Opening GitHub."

        except Exception as e:

            return (
                f"Could not open GitHub: {e}"
            )


    # ========================================================
    # NOTEPAD
    # ========================================================

    if "open notepad" in command:

        try:

            subprocess.Popen(
                "notepad.exe"
            )

            return "Opening Notepad."

        except Exception as e:

            return (
                f"Could not open Notepad: {e}"
            )


    # ========================================================
    # CALCULATOR
    # ========================================================

    if "open calculator" in command:

        try:

            subprocess.Popen(
                "calc.exe"
            )

            return "Opening Calculator."

        except Exception as e:

            return (
                f"Could not open Calculator: {e}"
            )


    # ========================================================
    # FILE EXPLORER
    # ========================================================

    if "open file explorer" in command:

        try:

            subprocess.Popen(
                "explorer.exe"
            )

            return "Opening File Explorer."

        except Exception as e:

            return (
                f"Could not open File Explorer: {e}"
            )


    # ========================================================
    # COMMAND PROMPT
    # ========================================================

    if "open command prompt" in command:

        try:

            subprocess.Popen(
                "cmd.exe"
            )

            return "Opening Command Prompt."

        except Exception as e:

            return (
                f"Could not open Command Prompt: {e}"
            )


    # ========================================================
    # POWERSHELL
    # ========================================================

    if "open powershell" in command:

        try:

            subprocess.Popen(
                "powershell.exe"
            )

            return "Opening PowerShell."

        except Exception as e:

            return (
                f"Could not open PowerShell: {e}"
            )


        # ========================================================
    # VS CODE
    # ========================================================

    if (
        "open vs code" in command
        or "open visual studio code" in command
    ):

        vscode_paths = [

            os.path.expandvars(
                r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
            ),

            r"C:\Program Files\Microsoft VS Code\Code.exe",

            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
        ]

        for vscode_path in vscode_paths:

            if os.path.exists(vscode_path):

                try:

                    subprocess.Popen(
                        vscode_path
                    )

                    return "Opening Visual Studio Code."

                except Exception as e:

                    return (
                        f"Could not open VS Code: {e}"
                    )

        return (
            "I could not find Visual Studio Code "
            "on your computer."
        )

    # ========================================================
    # MORE WEBSITES
    # ========================================================

    if "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        return "Opening Instagram."

    if "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        return "Opening Facebook."

    if "open gmail" in command:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail."

    if "open reddit" in command:
        webbrowser.open("https://www.reddit.com")
        return "Opening Reddit."

    if "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp."

    if "open chatgpt" in command:
        webbrowser.open("https://chatgpt.com")
        return "Opening ChatGPT."
        # ========================================================
    # YOUTUBE SEARCH
    # ========================================================

    if "search youtube for" in command:

        query = command.split(
            "search youtube for",
            1
        )[1].strip()

        if query:

            search_url = (
                "https://www.youtube.com/results?search_query="
                + query.replace(" ", "+")
            )

            webbrowser.open(search_url)

            return f"Searching YouTube for {query}."

        return "What should I search for on YouTube?"
        # ========================================================
    # GOOGLE SEARCH
    # ========================================================

    if "search google for" in command:

        query = command.split(
            "search google for",
            1
        )[1].strip()

        if query:

            search_url = (
                "https://www.google.com/search?q="
                + query.replace(" ", "+")
            )

            webbrowser.open(search_url)

            return f"Searching Google for {query}."

        return "What should I search for on Google?"

    # ========================================================
    # WINDOWS CONTROLS
    # ========================================================

    if "lock computer" in command or "lock pc" in command:
        subprocess.Popen(
            ["rundll32.exe", "user32.dll,LockWorkStation"]
        )
        return "Locking the computer."

    if "open task manager" in command:
        subprocess.Popen("taskmgr.exe")
        return "Opening Task Manager."

    if "open settings" in command:
        subprocess.Popen("ms-settings:")
        return "Opening Windows Settings."
    # ========================================================
    # NO COMPUTER COMMAND FOUND
    # ========================================================

    return None


# ============================================================
# ASK LOCAL AI
# ============================================================

def ask_jarvys(user_text):

    # --------------------------------------------------------
    # FIRST: CHECK COMPUTER COMMANDS
    # --------------------------------------------------------

    command_result = handle_command(
        user_text
    )

    if command_result:

        return command_result


    # --------------------------------------------------------
    # SECOND: CHECK WHETHER WEB SEARCH IS NEEDED
    # --------------------------------------------------------

    if needs_web(user_text):

        web_data = web_search(
            user_text
        )

        if web_data:

            prompt = f"""
You are JARVYS.

The user asked:

{user_text}

Internet search results:

{web_data}

Use the search results to answer the user.

Do not invent information.

If the search results do not contain
the answer, say that you could not find
enough information.

Give a clear and concise answer.
"""

        else:

            prompt = user_text

    else:

        prompt = user_text


    # --------------------------------------------------------
    # THIRD: ASK LOCAL OLLAMA AI
    # --------------------------------------------------------

    print("🧠 Thinking...")

    try:

        response = ollama.chat(

            model=OLLAMA_MODEL,

            messages=[

                {
                    "role": "system",

                    "content": """
You are JARVYS,
a personal AI assistant.

Your name is JARVYS.

Answer naturally and clearly.

Be helpful.

Keep normal answers reasonably short.

Do not claim that you can control
the user's computer unless a command
has actually been executed by the program.
"""
                },

                {
                    "role": "user",

                    "content": prompt
                }

            ]
        )

        return response[
            "message"
        ][
            "content"
        ]


    except Exception as e:

        print(
            "OLLAMA ERROR:",
            e
        )

        return (
            "I could not connect to my local AI. "
            "Please make sure Ollama is running."
        )


# ============================================================
# GUI
# ============================================================

root = tk.Tk()

root.title(
    "J A R V Y S"
)

root.geometry(
    "1000x700"
)

root.configure(
    bg="#050505"
)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(

    root,

    text="J A R V Y S",

    font=(
        "Consolas",
        32,
        "bold"
    ),

    fg="#00ffff",

    bg="#050505"

)

title.pack(
    pady=15
)


# ============================================================
# SUBTITLE
# ============================================================

subtitle = tk.Label(

    root,

    text="PERSONAL AI ASSISTANT",

    font=(
        "Consolas",
        12
    ),

    fg="#777777",

    bg="#050505"

)

subtitle.pack()


# ============================================================
# STATUS
# ============================================================

status = tk.Label(

    root,

    text="● JARVYS ONLINE",

    font=(
        "Consolas",
        12,
        "bold"
    ),

    fg="#00ff88",

    bg="#050505"

)

status.pack(
    pady=10
)


# ============================================================
# CONVERSATION BOX
# ============================================================

conversation = scrolledtext.ScrolledText(

    root,

    width=100,

    height=25,

    font=(
        "Consolas",
        11
    ),

    bg="#080808",

    fg="#00ffff",

    insertbackground="#00ffff",

    relief="flat"

)

conversation.pack(

    padx=20,

    pady=10,

    fill="both",

    expand=True

)


# ============================================================
# GUI HELPER FUNCTIONS
# ============================================================

def add_message(
    sender,
    message
):

    conversation.insert(

        tk.END,

        f"\n{sender}: {message}\n"

    )

    conversation.see(
        tk.END
    )


def update_status(
    text,
    color
):

    status.config(

        text=text,

        fg=color

    )


# ============================================================
# TEXT INPUT
# ============================================================

entry = tk.Entry(

    root,

    font=(
        "Consolas",
        13
    ),

    bg="#111111",

    fg="#ffffff",

    insertbackground="#ffffff",

    relief="flat"

)

entry.pack(

    side="left",

    padx=(20, 5),

    pady=15,

    fill="x",

    expand=True

)


# ============================================================
# PROCESS COMMAND
# ============================================================

def process_command(command):

    # Add user's message safely
    root.after(
        0,
        lambda: add_message(
            "YOU",
            command
        )
    )

    root.after(
        0,
        lambda: update_status(
            "● JARVYS THINKING...",
            "#ffff00"
        )
    )

    # Ask JARVYS
    answer = ask_jarvys(
        command
    )

    # Display answer safely
    root.after(
        0,
        lambda: add_message(
            "JARVYS",
            answer
        )
    )

    # Change status safely
    root.after(
        0,
        lambda: update_status(
            "● JARVYS ONLINE",
            "#00ff88"
        )
    )

    # Speak in background
    threading.Thread(

        target=speak,

        args=(answer,),

        daemon=True

    ).start()


# ============================================================
# SEND COMMAND
# ============================================================

def send_command():

    command = entry.get().strip()

    if not command:

        return

    entry.delete(
        0,
        tk.END
    )

    threading.Thread(

        target=process_command,

        args=(command,),

        daemon=True

    ).start()


# ============================================================
# SEND BUTTON
# ============================================================

send_button = tk.Button(

    root,

    text="SEND",

    command=send_command,

    font=(
        "Consolas",
        11,
        "bold"
    ),

    bg="#111111",

    fg="#00ffff",

    activebackground="#222222",

    activeforeground="#ffffff",

    relief="flat",

    padx=20,

    pady=8

)

send_button.pack(

    side="right",

    padx=(5, 20),

    pady=15

)


# ============================================================
# VOICE BUTTON
# ============================================================

def wake_word_listener():

    if vosk_model is None:
        return

    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):

        if status:
            print("MIC:", status)

        audio_queue.put(bytes(indata))

    recognizer = KaldiRecognizer(
        vosk_model,
        SAMPLE_RATE
    )

    print("🎤 Wake-word mode started.")
    print("Say: Hey Jarvis")

    try:

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback
        ):

            while True:

                data = audio_queue.get()

                if recognizer.AcceptWaveform(data):

                    result = json.loads(
                        recognizer.Result()
                    )

                    text = result.get(
                        "text",
                        ""
                    ).lower().strip()

                    if text:
                        print("HEARD:", text)

                    if (
                        "hey jarvis" in text
                        or "hey jarvis" in text.replace(" ", "")
                    ):

                        root.after(
                            0,
                            lambda: update_status(
                                "● JARVYS ACTIVATED",
                                "#00ff88"
                            )
                        )

                        speak("Yes?")

                        command = listen()

                        if command:
                            process_command(command)

                        recognizer = KaldiRecognizer(
                            vosk_model,
                            SAMPLE_RATE
                        )

    except Exception as e:

        print(
            "WAKE WORD ERROR:",
            e
        )
def activate_voice():

    def voice_process():

        root.after(

            0,

            lambda: update_status(
                "● LISTENING...",
                "#00ffff"
            )

        )

        user_text = listen()

        if not user_text:

            root.after(

                0,

                lambda: update_status(
                    "● JARVYS ONLINE",
                    "#00ff88"
                )

            )

            return

        process_command(
            user_text
        )


    threading.Thread(

        target=voice_process,

        daemon=True

    ).start()


# ============================================================
# VOICE BUTTON
# ============================================================

voice_button = tk.Button(

    root,

    text="🎤 ACTIVATE JARVYS",

    command=activate_voice,

    font=(
        "Consolas",
        12,
        "bold"
    ),

    bg="#111111",

    fg="#00ffff",

    activebackground="#222222",

    activeforeground="#ffffff",

    relief="flat",

    padx=25,

    pady=10

)

voice_button.pack(

    pady=(0, 20)

)


# ============================================================
# START MESSAGE
# ============================================================

add_message(

    "JARVYS",

    "Systems online. How can I assist you?"

)


# ============================================================
# ENTER KEY
# ============================================================

entry.bind(

    "<Return>",

    lambda event: send_command()

)


# ============================================================
# START WAKE WORD MODE
# ============================================================

threading.Thread(
    target=wake_word_listener,
    daemon=True
).start()


# ============================================================
# START GUI
# ============================================================

root.mainloop()
