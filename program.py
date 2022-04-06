from random import randrange
from shutil import ExecError
import string
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, JoinEvent, FollowEvent, GiftEvent
import PySimpleGUI as pg
import asyncio



currWord = ""
encryptedWord = ""
client: TikTokLiveClient = TikTokLiveClient(unique_id="@kursosi4ka") #your id

pg.theme("DarkAmber")

layout = [
    [pg.Push("darkred")],
    [pg.Text(
        "Guess the word",
        key='-NAZVA-',
        text_color = "white",
        size=(50, 1),
        font=('Lucida',34),
        justification='center',)
    ],[pg.Push("darkred")],[pg.Push()],
    [pg.Text("Follow for more games!",font=('Lucida',20),text_color = "pink",size=(50, 2),justification='center' )],
    
    [pg.Text(
        "Current word:",
        font=('Lucida',27),
        text_color = "red",
        size=(50, 1)
        ,justification='center')
    ],
    [pg.Text
        (
            "а**вw*в",
            key = '-WORD-',
            font=('Lucida',60),
            text_color = "white",
            size=(50, 1),
            background_color=None,
            justification='center'
        )
    ],
    [pg.Text                                      
        (
            "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾",
            font=2,
            size=(50, 1),
            text_color = "white",
            justification='center'
        )
    ], [pg.Push()],
    [pg.Image
        (
            "try1.png",
            size = (70,70)
        ),
        pg.Image
        (
            "tenis.png",
            size = (70,70)
        ),
        pg.Image
        (
            "dinamil1.png",
            size = (70,70)
        ),
        pg.Image
        (
            "gg1.png",
            size = (70,70)
        ),
        pg.Image
        (
            "tik1.png",
            size = (70,70)
        ),
        pg.Text
        (
            "→1 hint",
            text_color = "white",
            font=('Lucida',15)
        )
    ],[pg.Push()],[pg.Push()],[pg.Push()],
    [pg.Text
        (
            "The last word was guessed by:\n@kursosi4ka",
            key = '-GB-',
            font=('Lucida',23),
            text_color = "DarkGoldenrod1",
            size=(50, 4),
            justification='center',
            auto_size_text= True
        )
    ],
    [pg.Text
        (
            "Hello, ЩІЩАЩ",
            key = '-Hello-',
            font=('Lucida',23),
            text_color = "white",
            size=(50, 2),
            justification='center',
            auto_size_text= True
        )
    ],
    [pg.Multiline
        (
            "Thanks for a gift, ЩІЩАЩ and me and u and wqrqw adaq",
            key = '-GIFTFOLLOW-',
            background_color = "firebrick4",
            no_scrollbar = True,
            font=('Lucida',23),
            text_color = "white",
            size=(50, 2),
            justification='center',
            auto_size_text= True
        )
    ],

    [pg.Push()],[pg.Push()],[pg.Push()],[pg.Push()],[pg.Push()],
    [pg.Push("darkred")]
]

window = pg.Window(' ', layout, size=(500, 800))

@client.on("comment")
async def on_comment(event: CommentEvent):
    global currWord
    global guessed
    print(f"{event.user.nickname} -> {event.comment}", flush=True)
    try:
        if event.comment == currWord:
            if not guessed:
                guessed = True
                window['-GB-'].update(f"The last word was guessed by:\n@{event.user.uniqueId}\n({currWord})")
                word = get_word()
                currWord = word
                encrypt(word)
                guessed = False
            else:
                return
    except Exception as i:
        print(i)
        

@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id, flush=True)
    word = get_word()
    encrypt(word)

@client.on("join")
async def on_join(event: JoinEvent):
    print(f"Hello, @{event.user.uniqueId}!")
    window['-Hello-'].update(f"Hello, @{event.user.uniqueId}!")

@client.on("follow")
async def on_follow(event: FollowEvent):
    print(f"Thanks for following, @{event.user.uniqueId}!")
    window['-GIFTFOLLOW-'].update(f"Thanks for following, @{event.user.uniqueId}!")

@client.on("gift")
async def on_gift(event: GiftEvent):
    global currWord
    global encryptedWord
    if event.gift.gift_type == 1 and event.gift.repeat_end == 1:
        print(f"{event.user.uniqueId} sent {event.gift.repeat_count}x \"{event.gift.extended_gift.name}\"")
        window['-GIFTFOLLOW-'].update(f"Thanks {event.user.uniqueId} for {event.gift.repeat_count}x \"{event.gift.extended_gift.name}\"")

    elif event.gift.gift_type != 1:
        print(f"{event.user.uniqueId} sent \"{event.gift.extended_gift.name}\"")
        window['-GIFTFOLLOW-'].update(f"Thanks {event.user.uniqueId} for \"{event.gift.extended_gift.name}\"")

    if encryptedWord.count("*") != 1:
        count = 0
        for c in encryptedWord:
            if c == '*':
                encryptedWord = encryptedWord[:count] + currWord[count] + encryptedWord[count+1:]
                break
            count += 1
        window['-WORD-'].update(encryptedWord)

        
async def winReadLoop():
    while(True):
        await asyncio.sleep(0.01)
        event, values = window.read(0)
        if event == "__TIMEOUT__":
            continue
        if event is None or event == 'Exit':
            return

def run(words):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(winReadLoop(), client.start()))

def encrypt(word: str):
    global currWord
    global encryptedWord
    stars = starsSet[randrange(0,len(starsSet)-1)]
    encryptedWord = ""
    count = 0
    for c in word:
        if count in stars:
            encryptedWord += "*"
        else:
            encryptedWord += c
        count += 1
    window['-WORD-'].update(encryptedWord)
    print(f"\n\n\n[CURRENT WORD]\n{word}\n[CURRENT WORD]\n\n\n")
    currWord = word

def get_word():
    return words[randrange(0,len(words)-1)]

guessed = False
connected = False
words = []
starsSet = [ #cringe
    [0,4,5],
    [6,1,2],
    [2,6,5],
    [3,5,4],
    [1,3,4],
    [6,3,4],
    [1,3,5],
    [1,3,6],
    [1,5,4],
    [2,5,4],
    [6,1,3],
    [0,3,2],
    [0,1,6],
    [0,2,3],
    [0,5,3],
    [0,5,3]
]
with open('words.txt') as f:
    line = f.read()
    lines = line.split("\n")
    for l in lines:
        words.append(l)
run(words)
