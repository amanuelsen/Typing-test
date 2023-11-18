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


def calculate_word_precision(correct_text, correct_count):
    """
    Beräkna noggrannhet för ord i användarens inmatning jämfört med korrekt text.
    """

    global total_words

    correct_words = correct_text.split()
    total_words = len(correct_words)

    word_precision = correct_count / len(correct_words)

    return word_precision


def calculate_letter_precision(correct_text, wrong_count1, correct_count1):
    """
    Beräkna noggrannhet för enskilda bokstäver i användarens inmatning jämfört med korrekt text.
    """

    correct_letters = list(correct_text.strip())
    filtered_list = [
        char for char in correct_letters if char not in (' ', '\n')]

    total_letters = len(filtered_list)
    letter_precision = (correct_count1-wrong_count1) / total_letters

    return letter_precision


def fel_tecken(correct_text, user_text):
    """
    Identifiera och räkna felaktiga bokstäver i användarens inmatning jämfört med korrekt text (case-sensitive).
    """
    fel_letters = {}  # Initialize an empty dictionary to store incorrect characters and their counts.

    correct_words = correct_text.split()
    user_words = user_text.split()

    for correct_word, user_word in zip(correct_words, user_words):
        for correct_char, user_char in zip(correct_word, user_word):
            if correct_char != user_char:
                if correct_char.isalpha():
                    if correct_char not in fel_letters:
                        fel_letters[correct_char] = 1
                    else:
                        fel_letters[correct_char] += 1

        # Handle missing characters in user_word
        if len(user_word) < len(correct_word):
            missing_chars = correct_word[len(user_word):]
            for char in missing_chars:
                if char.isalpha():
                    if char not in fel_letters:
                        fel_letters[char] = 1
                    else:
                        fel_letters[char] += 1

    # Handle missing words in user_text
    if len(user_words) < len(correct_words):
        missing_words = correct_words[len(user_words):]
        for word in missing_words:
            for char in word:
                if char.isalpha():
                    if char not in fel_letters:
                        fel_letters[char] = 1
                    else:
                        fel_letters[char] += 1

    result = tuple((char, count)
                   for char, count in fel_letters.items())

    return result


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
    Den gör alla funcktioner för att få redan på reultaten
    """

    with open(file_name, "r") as file:
        text_lines = file.readlines()
    minus1 = 0
    minus = 0
    correct_text = " ".join(text_lines)
    user_text = ""
    print("Skriv av följande text:")

    start_time = time.time()
    # Initialize an empty dictionary to store incorrect characters and their counts.
    fel_error = {}
    correct_count = 0
    global wrong_count
    wrong_count = 0
    wrong_count1 = 0
    correct_count1 = 0
    last_index = 0
    for line in text_lines:
        print(line.strip())
        user_input = input()
        user_text += user_input+" "
        fel_error_line = fel_tecken(line.strip(), user_input)
        correct_words = line.split()
        user_words = user_input.split()
        user_word_letters = []
        correct_word_letters = []

        for correct_word, user_word in zip(correct_words, user_words):
            if correct_word == user_word:
                correct_count += 1
            else:
                wrong_count += 1
        if len(correct_words) > len(user_words):
            minus = len(correct_words)-len(user_words)
            wrong_count += minus
        elif len(user_words) > len(correct_words):
            minus = len(user_words)-len(correct_words)
            correct_count -= minus

        for correct_word, user_word in zip(correct_words, user_words):
            correct_word_letters = list(correct_word.strip())
            user_word_letters = list(user_word.strip())

            for correct_char, user_char in zip(correct_word, user_word):
                if correct_char == user_char:
                    correct_count1 += 1

            if len(user_word_letters) > len(correct_word_letters):
                minus1 = len(user_word_letters)-len(correct_word_letters)
                wrong_count1 += minus1
        if len(user_words) > len(correct_words):
            last_index = len(correct_words) - 1
            extra_words = user_words[last_index + 1:]
            for word in extra_words:
                for char in word:
                    wrong_count1 += 1

        # Den kominerar the errors for each line

        for char, count in fel_error_line:
            if char in fel_error:
                fel_error[char] += count
            else:
                fel_error[char] = count

    end_time = time.time()
    elapsed_time = end_time - start_time

    global Elapsed_minutes
    Elapsed_minutes = round_elapsed_time(elapsed_time)

    word_precision = calculate_word_precision(
        correct_text, correct_count)
    tecken_precision = calculate_letter_precision(
        correct_text, wrong_count1, correct_count1)

    input("Tryck Enter för att se resultat och skriva ditt namn...")
    print(f"Tid för test: {Elapsed_minutes} minuter")
    print(f"Wpn : {calculate_wpn()} ")
    print(f"Nwpn : {calculate_nwpnn()} ")
    print(f"Din ordprecision : {word_precision:.2%}")
    print(f"Din tecken precision: {tecken_precision:.2%}")

    sorted_fel_error = sorted(
        fel_error.items(), key=lambda x: x[1], reverse=True)
    print("Fel:", sorted_fel_error)

    user_name = input("Ange ditt namn: ")

    with open("score.txt", "a") as score_file:
        score_file.write(f"{word_precision * 100:.2f}|")
        score_file.write(f"{Elapsed_minutes}|")
        score_file.write(f"{user_name}|")
        # Store errors as a list
        score_file.write(f"{sorted_fel_error}|")
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
