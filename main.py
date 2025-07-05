import json
import os
from difflib import get_close_matches
from typing import Optional

# Gunakan path absolut agar selalu aman
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_FILE = os.path.join(BASE_DIR, 'knowledge_base.json')

def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"questions": []}

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> Optional[str]:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question.lower():
            return q["answer"]
    return None

def chat_bot():
    knowledge_base = load_knowledge_base(KB_FILE)

    print("\n📚 Selamat datang di ChatBot Cerdas!")
    print("Ketik pertanyaanmu. Jika ingin berhenti, ketik 'quit', 'exit', atau 'keluar'.")
    print("="*60)

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'keluar']:
            print("\n👋 Terima kasih telah menggunakan ChatBot. Sampai jumpa!\n")
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: Saya belum tahu jawabannya. Mau bantu ajarin saya?")
            new_answer = input("→ Ketik jawabannya atau 'skip' untuk melewati: ").strip()

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({
                    "question": user_input,
                    "answer": new_answer
                })
                save_knowledge_base(KB_FILE, knowledge_base)
                print("✅ Bot: Terima kasih! Saya telah belajar hal baru.")

        print("-" * 60)

if __name__ == '__main__':
    chat_bot()
