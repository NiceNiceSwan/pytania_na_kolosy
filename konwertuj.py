import re
import json

def konwertuj_md_na_json(nazwa_pliku_md, nazwa_pliku_json):
    try:
        with open(nazwa_pliku_md, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {nazwa_pliku_md}. Upewnij się, że plik znajduje się w tym samym katalogu.")
        return

    # Podział tekstu na bloki pytań za pomocą nagłówków poziom 3 (###)
    blocks = re.split(r'\n?###\s+', text.strip())
    questions = []

    for block in blocks:
        if not block.strip():
            continue
        
        # Rozdzielenie bloku na linie i usunięcie pustych wierszy
        lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
        if not lines:
            continue
            
        question_text = lines[0]
        options = []
        
        for line in lines[1:]:
            # Dopasowanie linii odpowiedzi w formacie "1. Treść" lub "1. **Treść**"
            m = re.match(r'^(\d+)\.\s*(.*)$', line)
            if m:
                num = int(m.group(1))
                ans_raw = m.group(2).strip()
                is_correct = False
                
                # Jeśli odpowiedź jest pogrubiona w markdownie, oznaczamy ją jako poprawną
                if ans_raw.startswith('**') and ans_raw.endswith('**'):
                    is_correct = True
                    ans_clean = ans_raw[2:-2].strip()
                else:
                    ans_clean = ans_raw
                    
                options.append({
                    "id": num,
                    "text": ans_clean,
                    "is_correct": is_correct
                })
                
        questions.append({
            "question_id": len(questions) + 1,
            "question": question_text,
            "options": options
        })

    # Zapisanie do pliku JSON
    with open(nazwa_pliku_json, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"Pomyślnie skonwertowano plik! Przetworzono {len(questions)} pytań i zapisano do '{nazwa_pliku_json}'.")

if __name__ == "__main__":
    konwertuj_md_na_json('notatka.md', 'pytania.json')