"""
Här är all logik och funktion.
"""

import math
import time


# Variabler för att spåra resultat
wrong_count = 0
total_words = 0
Elapsed_minutes = 0
wpn = 0
nwpnn = 0


def calculate_word_precision(correct_text, user_text):
    """
    Beräkna noggrannhet för ord i användarens inmatning jämfört med korrekt text.
    """
    global wrong_count
    global total_words

    correct_words = correct_text.split()
    user_words = user_text.split()

    correct_count = 0
    wrong_count = 0

    for correct_word, user_word in zip(correct_words, user_words):
        if correct_word == user_word:
            correct_count += 1
        else:
            wrong_count += 1

    total_words = max(len(correct_words), len(user_words))
    word_precision = correct_count / total_words

    return word_precision


def calculate_letter_precision(correct_text, user_text):
    """
    Beräkna noggrannhet för enskilda bokstäver i användarens inmatning jämfört med korrekt text.
    """

    # tar bort alla tecken som inte är alfanumeriska
    correct_letters = list(correct_text.strip())
    user_letters = list(user_text.strip())

    correct_count = 0

    for correct_letter, user_letter in zip(correct_letters, user_letters):
        if correct_letter == user_letter:
            correct_count += 1

    total_letters = max(len(correct_letters), len(user_letters))
    letter_precision = correct_count / total_letters

    return letter_precision


def fel_tecken(correct_text, user_text):
    """
    Identifiera och räkna felaktiga tecken i användarens inmatning jämfört med korrekt text.
    """
    fel_letters = {}
    correct_text = ''.join(filter(str.isalnum, correct_text))
    user_text = ''.join(filter(str.isalnum, user_text))

    if not user_text:
        letter_counts = {}
        for char in correct_text:
            if char in letter_counts:
                letter_counts[char] += 1
            else:
                letter_counts[char] = 1

        return [(char, count) for char, count in letter_counts.items()]

    for correct_char in correct_text:
        if correct_char not in user_text:
            if correct_char not in fel_letters:
                fel_letters[correct_char] = 1
            else:
                fel_letters[correct_char] += 1

    return [(char, count) for char, count in fel_letters.items()]


def round_elapsed_time(elapsed_time):
    """
    Avrunda förlupen tid från sekunder till minuter enligt specifik logik.
    """
    elapsed_minutes = elapsed_time / 60

    if elapsed_minutes < 1:
        elapsed_minutes = 1  # Avrunda upp till en minut om det är mindre än en minut
    elif elapsed_minutes % 1 >= 0.5:
        elapsed_minutes = math.ceil(elapsed_minutes)
    else:
        elapsed_minutes = math.floor(elapsed_minutes)

    return elapsed_minutes


def calculate_wpn():
    """
    Beräkna och returnera Bruttoord Per Minut (Gwpn) baserat på globala variabler.
    """
    global wpn
    wpn = total_words / Elapsed_minutes
    return wpn


def calculate_nwpnn():
    """
    Beräkna och returnera Nettoord Per Minut (Nwpn) baserat på globala variabler.
    """
    global nwpnn
    nwpnn = wpn - (wrong_count / Elapsed_minutes)
    return nwpnn


def start_typing_test(file_name):
    """
    Starta en skrivtest, mät tid, beräkna noggrannhet och spara resultat.
    """
    with open(file_name, "r") as file:
        text_lines = file.readlines()

    correct_text = "".join(text_lines)
    user_text = ""

    print("Skriv av följande text:")

    start_time = time.time()

    for line in text_lines:
        print(line.strip())
        user_input = input()
        user_text += user_input + " "

    end_time = time.time()
    elapsed_time = end_time - start_time

    global Elapsed_minutes
    Elapsed_minutes = round_elapsed_time(elapsed_time)

    word_precision = calculate_word_precision(correct_text, user_text)
    tecken_precision = calculate_letter_precision(correct_text, user_text)
    fel_error = fel_tecken(correct_text, user_text)

    input("Tryck Enter för att se resultat och skriva ditt namn...")
    print(f"Tid för test: {Elapsed_minutes} minuter")
    print(f"Wpn : {calculate_wpn()} ")
    print(f"Nwpn : {calculate_nwpnn()} ")
    print(f"Din ordprecision : {word_precision:.2%}")
    print(f"Din tecken precision: {tecken_precision:.2%}")
    print(f"Fel: {fel_error}")

    user_name = input("Ange ditt namn: ")

    with open("score.txt", "a") as score_file:
        score_file.write(f"{word_precision * 100:.2f}|")
        score_file.write(f"{Elapsed_minutes}|")
        score_file.write(f"{user_name}|")
        score_file.write(f"{fel_error}|")
        score_file.write(f"{calculate_nwpnn()}|")
        score_file.write(f"{calculate_wpn()}|")
        if calculate_nwpnn() <= 10:
            score_file.write("Sengångare")
        elif 10 < calculate_nwpnn() <= 20:
            score_file.write("Snigel")
        elif 20 < calculate_nwpnn() <= 30:
            score_file.write("Sjöko")
        elif 30 < calculate_nwpnn() <= 40:
            score_file.write("Människa")
        elif 40 < calculate_nwpnn() <= 50:
            score_file.write("Gasell")
        elif 50 < calculate_nwpnn() <= 60:
            score_file.write("Struts")
        elif 60 < calculate_nwpnn() <= 70:
            score_file.write("Gepard")
        elif 70 < calculate_nwpnn() <= 80:
            score_file.write("Svärdfisk")
        elif 80 < calculate_nwpnn() <= 90:
            score_file.write("Sporrgås")
        elif 90 < calculate_nwpnn() <= 100:
            score_file.write("Taggstjärtseglare")
        elif 100 < calculate_nwpnn() <= 120:
            score_file.write("Kungsörn")
        else:
            score_file.write("Pilgrimsfalk")
        score_file.write("\n")


def read_and_sort_file(filename):
    """
    Läs och sortera en fil som innehåller resultat från skrivtester och formatera dem.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    sorted_lines = sorted(lines, key=lambda line: float(
        line.split('|')[0]), reverse=True)

    for key, value in enumerate(sorted_lines):
        sorted_lines[key] = value.split("|")
    for line in sorted_lines:
        line[0] = line[0] + "%" + " " + "ordprecision"
        line[1] = line[1] + " " + "minut"
        line[2] = "namn: " + line[2]
        line[4] = "Nwpn" + ": " + line[4]
        errors = "Errors"
        line[3] = errors+": " + line[3]
        line[5] = "Gwpn" + ": " + line[5]
        line[6] = "Djur"+" " + line[6]

        print(
            f"{line[0]: <20} {line[1]: <20} {line[2]:<20} {line[3]: <20} {line[4]:<20} {line[5]:<20} {line[6]:<20}")
