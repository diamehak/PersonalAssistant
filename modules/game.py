from random import randint
import playsound
from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
import speech_recognition as sr
import pyttsx3
import time
from pynput.keyboard import Key, Controller

def closeWindow():
    keyboard = Controller()
    keyboard.press(Key.alt_l)
    keyboard.press(Key.f4)
    keyboard.release(Key.f4)
    keyboard.release(Key.alt_l)

try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # male voice
    engine.setProperty('volume', 1)
except Exception as e:
    print(e)

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def record():
    global userchat
    userchat['text'] = "Listening..."
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(f"\nUser said: {said}")
        except Exception as e:
            print(e)
            speak("I think it is an invalid move...")
            return "None"
    return said.lower()

moves = ['rock', 'paper', 'scissor']

class RockPaperScissor:
    def __init__(self):
        self.playerScore = 0
        self.botScore = 0
        self.total_moves = 0
        self.intro()

    def intro(self):
        speak("Welcome to the Rock Paper Scissor Game. To STOP the match, say STOP or Cancel. Let's Play.")

    def nextMove(self, move):
        global userchat, botchat, totalLabel, botMoveLBL
        userchat['text'] = move.upper()
        botMove = randint(0, 2)
        playerMove = moves.index(move)
        botchat['text'] = moves[botMove].upper()
        self.total_moves += 1

        # Score calculation
        if botMove == playerMove:
            self.botScore += 1
            self.playerScore += 1
        elif (botMove == 0 and playerMove == 2) or (botMove == 1 and playerMove == 0) or (botMove == 2 and playerMove == 1):
            self.botScore += 1
        else:
            self.playerScore += 1
        
        totalLabel['text'] = f"{self.botScore}   |   {self.playerScore}"
        if botMove == 0: botMoveLBL['image'] = rockImg
        if botMove == 1: botMoveLBL['image'] = paperImg
        if botMove == 2: botMoveLBL['image'] = scissorImg
        speak('I choose: ' + str(moves[botMove]))

    def whoWon(self):
        result = ""
        if self.playerScore == self.botScore:
            result = "The match is a draw!\n"
        elif self.playerScore > self.botScore:
            result = "You won the match, Sir! Well done!\n"
        else:
            result = "You lost the match, Sir! Haha!\n"

        for el in root.winfo_children():
            el.destroy()
        if 'won' in result:
            Label(root, image=winImg).pack(pady=30)
        elif 'lose' in result:
            Label(root, image=loseImg).pack(pady=30)
        else:
            Label(root, image=drawImg).pack(pady=30)

        result += f"You have won {self.playerScore}/{self.total_moves} matches."
        Label(root, text='Score', font=('Arial Bold', 50), fg='#FE8A28', bg='white').pack()
        Label(root, text=f"{self.playerScore} / {self.total_moves}", font=('Arial Bold', 40), fg='#292D3E', bg='white').pack()
        speak(result)
        time.sleep(1)
        closeWindow()

# Global variables
rockImg, paperImg, scissorImg, userchat, botchat, totalLabel, botMoveLBL, userMoveLBL, winImg, loseImg, drawImg = (None,) * 11

def playRock():
    rp = RockPaperScissor()
    while True:
        move = record()
        if isContain(move, ["don't", "cancel", "stop"]):
            rp.whoWon()
            break
        elif move in moves:
            if 'rock' in move:
                userMoveLBL['image'] = rockImg
                rp.nextMove('rock')
            elif 'paper' in move:
                userMoveLBL['image'] = paperImg
                rp.nextMove('paper')
            elif 'scissor' in move:
                userMoveLBL['image'] = scissorImg
                rp.nextMove('scissor')

def rockPaperScissorWindow():
    global root, rockImg, paperImg, scissorImg, userchat, botchat, totalLabel, botMoveLBL, userMoveLBL, winImg, loseImg, drawImg
    root = Tk()
    root.title('Rock Paper Scissor')
    w_width, w_height = 400, 650
    s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    root.geometry(f'{w_width}x{w_height}+{int(x)}+{int(y - 30)}')  # center location of the screen
    root.configure(bg='white')

    rockImg = ImageTk.PhotoImage(Image.open('assets/rps/1.jpg'))
    paperImg = ImageTk.PhotoImage(Image.open('assets/rps/2.jpg'))
    scissorImg = ImageTk.PhotoImage(Image.open('assets/rps/3.jpg'))
    grayImg = ImageTk.PhotoImage(Image.open('assets/rps/grayQuestion.png'))
    orangeImg = ImageTk.PhotoImage(Image.open('assets/rps/orangeQuestion.jpg'))
    winImg = ImageTk.PhotoImage(Image.open('assets/rps/win.jpg'))
    loseImg = ImageTk.PhotoImage(Image.open('assets/rps/lose.jpg'))
    drawImg = ImageTk.PhotoImage(Image.open('assets/rps/draw.jpg'))

    Label(root, text='Total Score', font=('Arial Bold', 20), fg='#FE8A28', bg='white').pack()
    totalLabel = Label(root, text='0   |   0', font=('Arial Bold', 15), fg='#1F1F1F', bg='white')
    totalLabel.pack()

    # Bottom image
    img = ImageTk.PhotoImage(Image.open('assets/rps/rockPaperScissor.jpg'))
    downLbl = Label(root, image=img)
    downLbl.pack(side=BOTTOM)

    # User response
    userchat = Label(root, text='Listening...', bg='#FE8A28', fg='white', font=('Arial Bold', 13))
    userchat.place(x=300, y=120)
    userMoveLBL = Label(root, image=orangeImg)
    userMoveLBL.place(x=260, y=150)

    # Bot response
    botchat = Label(root, text='Waiting...', bg='#EAEAEA', fg='#494949', font=('Arial Bold', 13))
    botchat.place(x=12, y=120)
    botMoveLBL = Label(root, image=grayImg)
    botMoveLBL.place(x=12, y=150)

    Thread(target=playRock).start()
    root.iconbitmap("assets/images/game.ico")
    root.mainloop()

def isContain(text, lst):
    return any(word in text for word in lst)

def play(gameName):
    speak('')
    if isContain(gameName, ['dice', 'die']):
        playsound.playsound('assets/audios/dice.mp3')
        result = "You got " + str(randint(1, 6))
        return result

    elif isContain(gameName, ['coin']):
        playsound.playsound('assets/audios/coin.mp3')
        p = randint(-10, 10)
        if p > 0:
            return "You got Head"
        else:
            return "You got Tail"

    elif isContain(gameName, ['rock', 'paper', 'scissor', 'first']):
        rockPaperScissorWindow()
        return

    else:
        print("Game Not Available")

def showGames():
    return "1. Rock Paper Scissor\n2. Online Games"

# Start the game when running the script
if __name__ == "__main__":
    play("rock paper scissor")
