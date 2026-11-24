import json
import random

def wczytaj_pytania(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {nazwa_pliku}. Upewnij się, że plik JSON jest w tym samym katalogu.")
        return []

def uruchom_quiz(pytania):
    if not pytania:
        return

    # Losowa kolejność pytań
    random.shuffle(pytania)
    
    punkty = 0
    liczba_pytan = len(pytania)

    print(f"Rozpoczęto quiz! Łącznie pytań w bazie: {liczba_pytan}\n")
    print("=" * 60)

    for i, q in enumerate(pytania, 1):
        print(f"\nPytanie {i}/{liczba_pytan}:")
        print(f"** {q['question']} **\n")

        # Kopiujemy opcje, aby nie modyfikować oryginalnej listy w pamięci na stałe,
        # a następnie losowo je mieszamy.
        opcje = list(q['options'])
        random.shuffle(opcje)

        # Przypisujemy nowe numery wyświetlane (1, 2, 3...) dla przemieszanych opcji,
        # zapamiętując jednocześnie, które z nich faktycznie są poprawne.
        poprawne_wysietlane_ids = []
        mapa_opcji = {}

        for nowy_idx, opcja in enumerate(opcje, 1):
            mapa_opcji[nowy_idx] = opcja
            print(f"  {nowy_idx}. {opcja['text']}")
            if opcja['is_correct']:
                poprawne_wysietlane_ids.append(nowy_idx)

        # Pobieranie odpowiedzi od użytkownika
        while True:
            odpowiedz_str = input("\nTwoja odpowiedź (podaj numer opcji lub numery oddzielone przecinkiem): ").strip()
            try:
                wybrane_ids = [int(x.strip()) for x in odpowiedz_str.split(',') if x.strip()]
                if wybrane_ids:
                    break
            except ValueError:
                pass
            print("Nieprawidłowy format. Wpisz numer (np. 2) lub numery po przecinku (np. 1, 3).")

        # Sprawdzenie poprawności na podstawie przemieszanych numerów
        if set(wybrane_ids) == set(poprawne_wysietlane_ids):
            print("✅ Poprawnie!")
            punkty += 1
        else:
            print("❌ Błędnie.")
            poprawne_teksty = [f"{idx}. {mapa_opcji[idx]['text']}" for idx in poprawne_wysietlane_ids]
            print(f"Prawidłowa odpowiedź to: {', '.join(poprawne_teksty)}")

        print("-" * 60)
        
        kontynuacja = input("Naciśnij Enter, aby przejść dalej (lub wpisz 'koniec', aby przerwać): ").strip().lower()
        if kontynuacja == 'koniec':
            print("\nPrzerwano quiz.")
            break

    print(f"\nKoniec quizu! Twój wynik: {punkty} / {i}")

if __name__ == "__main__":
    plik_json = "pytania.json"
    baza_pytan = wczytaj_pytania(plik_json)
    uruchom_quiz(baza_pytan)