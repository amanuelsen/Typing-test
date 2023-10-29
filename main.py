"""
Här gör man alla sina val.
"""
import function


def main():
    """
    Huvudfunktionen för programmet som hanterar menyval och skrivtester.
    Användaren kan starta olika skrivtester, visa resultatlistan eller avsluta programmet.
    """

    while True:
        print("Menyval:")
        print("1. Starta skrivtest med filen easy.txt.")
        print("2. Starta skrivtest med filen medium.txt.")
        print("3. Starta skrivtest med filen hard.txt.")
        print("4. Skriv ut resultatlistan sorterad på högst precision.")
        print("q. Avsluta programmet")

        choice = input("Välj ett menyval: ")

        if choice == "1":
            function.start_typing_test("typing/easy.txt")
        elif choice == "2":
            function.start_typing_test("typing/medium.txt")
        elif choice == "3":
            function.start_typing_test("typing/hard.txt")
        elif choice == "4":
            print(function.read_and_sort_file("score.txt"))
        elif choice == "q":
            break
        else:
            print("Ogiltigt val. Försök igen.")


if __name__ == "__main__":
    main()
