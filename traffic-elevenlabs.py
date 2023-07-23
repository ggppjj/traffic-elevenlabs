#python-dotenv
from dotenv import dotenv_values, set_key as set_dotenv_key
#elevenlabs
#also requires ffmpeg installed
from elevenlabs import generate as generate_elevenlabs_api_voice, play as play_elevenlabs_api_voice, set_api_key as set_elevenlabs_api_key

from os.path import isfile
from pathlib import Path
from platform import system
from subprocess import run
from feedparser import parse

def touch(path):
    Path(path).touch()
    
def open_file(filename):
    if system() == "Windows":
        run(['notepad.exe', filename])
    elif system() == "Darwin":
        run(['open', '-t', filename])
    elif system() == "Linux":
        run(['gedit', filename])

def play_traffic_entry(entry):
    title: str = entry.title
    title = title.replace(" | ", " - ").replace("(","").replace(")","").replace("A1", "Eigh one-").replace("A30", "Eigh thirty ") + "."
    print(title)
    category: str = entry.category
    print(category)
    for tag in entry.tags:
        if "No Delay" in tag.term:
            title = title + " But don't worry, there's no delay."
    play_elevenlabs_api_voice(
        generate_elevenlabs_api_voice(
            text=title, 
            voice="Josh", 
            model="eleven_monolingual_v1"
            )
        )

TrafficFeed = parse("http://m.highwaysengland.co.uk/feeds/rss/UnplannedEvents.xml")

if isfile("./APIKey.env"):
    env_values = dotenv_values("./APIKey.env")
else:
    touch("./APIKey.env")
    set_dotenv_key("./APIKey.env", "APIKey", "")
    try:
        open_file("./APIKey.env")
    except:
        print("Elevenlabs API Key not loaded!")
    env_values = dotenv_values("./APIKey.env")
    
if "APIKey" in env_values and env_values["APIKey"] != "":
    set_elevenlabs_api_key(env_values["APIKey"])
    print("Elevenlabs API Key Loaded!")

audio = generate_elevenlabs_api_voice(
    text = "This is the channel for the " + TrafficFeed.feed.title + ".",
    voice = "Josh",
    model = "eleven_monolingual_v1"
)
play_elevenlabs_api_voice(audio)

for entry in TrafficFeed.entries:
    play_traffic_entry(entry)

if len(TrafficFeed.entries) == 0:
    audio = generate_elevenlabs_api_voice(
        text = "There are currently no reported incidents.",
        voice = "Josh",
        model = "eleven_monolingual_v1"
    )
    play_elevenlabs_api_voice(audio)

audio = generate_elevenlabs_api_voice(
        text = "That is all.",
        voice = "Josh",
        model = "eleven_monolingual_v1"
        )
play_elevenlabs_api_voice(audio)