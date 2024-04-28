# functions
def evaluate_letters(words, letters):
    global vowelcount
    abcs = []
    for letter in abc:
        abcs.append([letter, 0, 0, 0, 0])
    for word in words:
        for letter in letters:
            if letter in word:
                abcs[abc.index(letter)][1] += 1
                for i, l in enumerate(word):
                    if l == letter:
                        abcs[abc.index(letter)][2] += i
                        abcs[abc.index(letter)][3] += 1
                        abcs[abc.index(letter)][4] = int(
                            round(abcs[abc.index(letter)][2] / abcs[abc.index(letter)][3], 0))
    sortees = sorted(abcs, key=lambda x: x[1], reverse=True)
    for letter in sortees:
        letter[1] = round((letter[1] / len(words)) * 100, 3)
    if vowelcount <= 1:
        for letter in sortees:
            if letter[0] in vowels:
                letter[1] *= 2
    return sortees


def sort_words(words, letters):
    global sortedwords, currentrow
    stats = evaluate_letters(words, letters)
    stats2 = []
    for letter in stats:
        stats2.append(letter[0])
    valuedwords = []
    for word in words:
        total = 0
        used = []
        for i, letter in enumerate(word):
            if (letter not in used):
                if i == stats[stats2.index(letter)][4]:
                    if letter in vowels:
                        total += (stats[stats2.index(letter)][1] * 1.2)
                    else:
                        total += (stats[stats2.index(letter)][1] * 1.1)
                else:
                    total += stats[stats2.index(letter)][1]
                used.append(letter)
            if currentrow > 2:
                if word in answers:
                    total = total * 1.5
        valuedwords.append([word, total])
    sortedwords = []
    sortedwords = sorted(valuedwords, key=lambda x: x[1], reverse=True)
    return sortedwords


def eliminate_grays(words):
    pops = []
    for word in words:
        for letter in grays:
            if letter in word:
                pop = True
                if letter in greens1:
                    pop = False
                if letter in yellows1:
                    pop = False
                if (pop == True) and (word not in pops):
                    pops.append(word)
                    break
    for word in pops:
        words.pop(words.index(word))


def eliminate_greens(words):
    pops = []
    for word in words:
        for letter in greens:
            if word[letter[1]] != letter[0]:
                pops.append(word)
                break
    for word in pops:
        words.pop(words.index(word))


def eliminate_yellows(words):
    pops = []
    for word in words:
        for letter in yellows:
            if (letter[0] not in word) or (word[letter[1]] == letter[0]):
                pops.append(word)
                break
    for word in pops:
        words.pop(words.index(word))


def return_hint():
    global guess, pressing, typing, autoload
    pressing = True
    hintpen.clear()
    hintpen.write("Thinking...", font=('impact', 15, 'bold'), align='center')
    for letter in grays:
        if letter in remaining:
            remaining.pop(remaining.index(letter))
    eliminate_grays(available)
    eliminate_greens(available)
    eliminate_yellows(available)
    out = sort_words(available, remaining)
    pressing = False
    typing = True
    guess = []
    if autoload == True:
        for l in out[0][0]:
            keypress_letter(l)
    refresh_hints()
    hintpen.clear()


def move_arrows(row, space):
    verti.goto(-260, 200 - ((row - 1) * 70))
    if space < 0:
        space = 0
    hori.goto(-200 + ((space) * 70), 260)


def keypress_delete():
    global currentrow, guess, pressing, typing
    if (pressing == False) and (len(guess) > 0) and (typing == True):
        pressing = True
        place = len(guess)
        guess.pop(place - 1)
        display_letter(currentrow, place, 'delete')
        move_arrows(currentrow, len(guess) - 1)
        pressing = False


def keypress_letter(letter):
    global currentrow, guess, pressing, typing
    if (len(guess) < 5) and (pressing == False) and (typing == True):
        pressing = True
        guess.append(letter)
        display_letter(currentrow, len(guess), letter)
        move_arrows(currentrow, len(guess) - 1)
        pressing = False


def keypress_enter():
    global typing, pressing, currentrow, currentplace, color, vowelcount, guess
    if (typing == True) and (pressing == False) and (len(guess) == 5):
        typing = False
        cycle_letter_color()
        move_arrows(currentrow, currentplace)
    elif (typing == False) and (pressing == False):
        pressing = True
        if len(guess) == 5:
            if (color == 0) and (guess[currentplace] not in grays):
                grays.append(guess[currentplace])
            if (color == 1) and ([guess[currentplace], currentplace] not in yellows):
                yellows.append([guess[currentplace], currentplace])
                yellows1.append(guess[currentplace])
            if (color == -1) and ([guess[currentplace], currentplace] not in greens):
                greens.append([guess[currentplace], currentplace])
                greens1.append(guess[currentplace])
            if (guess[currentplace] not in foundletters) and (color != 0):
                foundletters.append(guess[currentplace])
                if letter in vowels:
                    vowelcount += 1
            color = -1
        if currentplace == 4:
            if len(greens) == 5:
                pressing = True
                return
            currentplace = 0
            currentrow += 1
            move_arrows(currentrow, currentplace)
            pressing = False
            guess = []
            return_hint()
            typing = True
        else:
            currentplace += 1
            move_arrows(currentrow, currentplace)
            pressing = False
            cycle_letter_color()


def toggle_autoload(x, y):
    global autoload, pressing
    if pressing == False:
        if autoload == True:
            autoload = False
            loadpen2.clear()
            loadpen2.write("AUTOLOAD: OFF", font=('impact', 20, 'bold'))
            pressing = False
            for i in range(5):
                keypress_delete()
        elif autoload == False:
            autoload = True
            loadpen2.clear()
            loadpen2.write("AUTOLOAD: ON", font=('impact', 20, 'bold'))
            for l in sortedwords[0][0]:
                keypress_letter(l)


def cycle_letter_color():
    global typing, pressing, color, currentrow, currentplace
    if (typing == False) and (pressing == False) and (len(guess) == 5):
        pressing = True
        color += 1
        if color == 2:
            color = -1
        change_color(currentrow, currentplace + 1, colors[color])
        display_letter(currentrow, currentplace + 1, guess[currentplace])
        pressing = False


def display_letter(row, place, letter):
    if letter == 'delete':
        pens[row - 1][place - 1].clear()
    else:
        pens[row - 1][place - 1].write(letter.upper(), font=('impact', 30, 'bold'), align='center')


def change_color(row, place, colour):
    turtles[row - 1][place - 1].color(colour)


def refresh_hints():
    pen.clear()
    y = 180
    x = 210
    total = 0
    pen.goto(x, y)
    r = len(sortedwords)
    if r > 10:
        r = 10
    for i in range(len(sortedwords)):
        total += sortedwords[i][1]
    average = total / len(sortedwords)
    onepercent = average / 100
    for i in range(r):
        if i == 0:
            pen.color('gold')
            pen.write(sortedwords[i][0].upper(), font=('impact', 30, 'bold'), align='center', move=True)
            pen.color('white')
            pen.setheading(90)
            pen.fd(10)
        else:
            pen.color('white')
            pen.write(sortedwords[i][0].upper(), font=('impact', 20, 'bold'), align='center', move=True)
        pen.setheading(0)
        pen.fd(10)
        pen.setheading(90)
        pen.fd(10)
        percent = (sortedwords[i][1] / onepercent) - 100
        if percent > 0:
            pen.color(0, 102, 0)
            modifier = '+'
        elif percent < 0:
            pen.color(102, 0, 0)
            modifier = '-'
            percent = abs(percent)
        elif percent == 0:
            pen.color(102, 102, 0)
            modifier = '+'
        percent = "(" + modifier + str(round(percent, 1)) + '%)'
        pen.write(percent, font=('impact', 8, 'bold'), align='left')
        y -= 30
        pen.goto(x, y)
    if r == 10:
        pen.goto(x, y + 12)
        pen.color('gray')
        pen.write("+" + str(len(sortedwords) - 10) + " more", font=('impact', 10, 'bold'), align='center')
    pen.color('white')


# -----definitions-----

# --variables--
vowelcount = 0
currentrow = 1
currentplace = 0
color = -1

green = 83, 141, 78
yellow = 181, 159, 59
gray = 58, 58, 60
white = 215, 218, 220
answerlist = 'NYTpossibleanswers.txt'
wordlist = 'NYTwords.txt'

typing = True
pressing = False
autoload = True

abc = list('abcdefghijklmnopqrstuvwxyz')
vowels = list('euioa')
remaining = list('abcdefghijklmnopqrstuvwxyz')
available = []
answers = []
grays = []
greens = []
greens1 = []
yellows = []
yellows1 = []
foundletters = []
colors = [gray, yellow, green]
turtles = [[], [], [], [], [], []]
pens = [[], [], [], [], [], []]
guess = []
abcs1 = list('qwertyuiopasdfghjklzxcvbnm')

with open(wordlist, 'r') as f:
    rawtext = f.readlines()
for word in rawtext:
    available.append(word.strip())

with open(answerlist, 'r') as f:
    rawtext = f.readlines()
for word in rawtext:
    answers.append(word.strip())

# --turtles--
import turtle

wn = turtle.Screen()
wn.colormode(255)
wn.bgcolor(18, 18, 19)
wn.tracer(False)

for i in range(6):
    for n in range(5):
        t = turtle.Turtle()
        turtles[i].append(t)
        t.penup()
        t.shape('square')
        t.shapesize(3)
        t.color(gray)
        t.fillcolor(18, 18, 19)
        t.goto(-200 + (n * 70), 200 - (i * 70))
        x = t.xcor() + 1
        y = t.ycor() - 30
        p = turtle.Turtle()
        p.penup()
        p.hideturtle()
        p.pencolor(white)
        p.goto(x, y)
        pens[i].append(p)

hori = turtle.Turtle()
hori.shape('triangle')
hori.penup()
hori.speed(0)
hori.goto(-200, 260)
hori.setheading(270)
hori.color('orange')

verti = turtle.Turtle()
verti.shape('triangle')
verti.penup()
verti.speed(0)
verti.goto(-260, 200)
verti.setheading(0)
verti.color('orange')

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.speed(0)
pen.color('white')

pen2 = turtle.Turtle()
pen2.hideturtle()
pen2.penup()
pen2.speed(0)
pen2.color('white')

hintpen = turtle.Turtle()
hintpen.penup()
hintpen.hideturtle()
hintpen.color('white')
hintpen.goto(-60, -260)

loadbutton = turtle.Turtle()
loadbutton.penup()
loadbutton.speed(0)
loadbutton.color('gray')
loadbutton.fillcolor(18, 18, 19)
loadbutton.shape('circle')
loadbutton.shapesize(1)
loadbutton.goto(-180, -215)

loadpen2 = turtle.Turtle()
loadpen2.penup()
loadpen2.speed(0)
loadpen2.color('white')
loadpen2.hideturtle()
loadpen2.goto(-160, -230)
loadpen2.write("AUTOLOAD: ON", font=('impact', 20, 'bold'))

pen2.goto(-60, 300)
pen2.write("WORDLE SOLVER", font=('impact', 50, 'bold'), align='center')

wn.tracer(True)

# -----calls-----

return_hint()

wn.listen()
for letter in abcs1:
    wn.onkeypress(lambda a=letter: keypress_letter(a), letter)
wn.onkeypress(keypress_delete, 'BackSpace')
wn.onkeypress(keypress_enter, 'Return')
wn.onkeypress(cycle_letter_color, 'space')
loadbutton.onclick(toggle_autoload)
wn.mainloop()
