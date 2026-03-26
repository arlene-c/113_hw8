import json
import random
import hashlib
import os
import sys
from datetime import datetime

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def load_questions():
    if not os.path.exists('questions.json'):
        print("Error: questions.json file is missing.")
        sys.exit(1)
    with open('questions.json', 'r') as f:
        data = json.load(f)
    questions = []
    for q in data['questions']:
        required_keys = ['question', 'type', 'answer', 'hint', 'category']
        if q['type'] == 'multiple_choice':
            required_keys.append('options')
        if all(k in q for k in required_keys):
            questions.append(q)
        else:
            print(f"Warning: Skipping malformed question: {q.get('question', 'Unknown')}")
    if not questions:
        print("Error: No valid questions found in questions.json.")
        sys.exit(1)
    return questions

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

def load_scores():
    if os.path.exists('scores.json'):
        with open('scores.json', 'r') as f:
            return json.load(f)
    return {}

def save_scores(scores):
    with open('scores.json', 'w') as f:
        json.dump(scores, f, indent=2)

def login():
    users = load_users()
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None
    if username in users:
        pwd = input("Enter password: ")
        if hash_password(pwd) == users[username]:
            print(f"Welcome back, {username}!")
            return username
        else:
            print("Invalid password.")
            return None
    else:
        pwd = input("New user. Enter password: ")
        if not pwd:
            print("Password cannot be empty.")
            return None
        users[username] = hash_password(pwd)
        save_users(users)
        print(f"Account created for {username}.")
        return username

def get_quiz_params():
    while True:
        try:
            num = int(input("How many questions? "))
            if num <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    types = []
    print("Select question types (enter numbers separated by comma):")
    print("1. multiple_choice")
    print("2. short_answer")
    print("3. true_false")
    type_map = {'1': 'multiple_choice', '2': 'short_answer', '3': 'true_false'}
    while True:
        inp = input("Types: ").strip()
        selected = [type_map.get(i.strip()) for i in inp.split(',') if i.strip() in type_map]
        if selected:
            types = list(set(selected))  # remove duplicates
            break
        else:
            print("Invalid selection. Please enter valid numbers.")
    return num, types

def select_questions(questions, num, types):
    filtered = [q for q in questions if q['type'] in types]
    if len(filtered) < num:
        print(f"Warning: Only {len(filtered)} questions available of selected types. Selecting all.")
        num = len(filtered)
    # To inform next questions, sort by average rating descending if ratings exist
    def avg_rating(q):
        ratings = q.get('ratings', [])
        return sum(ratings) / len(ratings) if ratings else 3  # default 3
    filtered.sort(key=avg_rating, reverse=True)
    return random.sample(filtered, num)

def ask_question(q):
    print(f"\nQuestion: {q['question']}")
    if q['type'] == 'multiple_choice':
        for i, opt in enumerate(q['options'], 1):
            print(f"{chr(64+i)}. {opt}")
        options = [chr(64+i) for i in range(1, len(q['options'])+1)]
    elif q['type'] == 'true_false':
        print("True or False?")
        options = ['true', 'false']
    else:  # short_answer
        options = None

    hint_used = False
    score_penalty = 0
    while True:
        ans = input("Your answer (or 'hint' for help): ").strip()
        if ans.lower() == 'hint':
            if not hint_used:
                print(f"Hint: {q['hint']}")
                score_penalty = 1
                hint_used = True
            else:
                print("Hint already used for this question.")
            continue
        if options:
            if q['type'] == 'multiple_choice':
                valid = ans.upper() in options
            else:
                valid = ans.lower() in options
            if not valid:
                print(f"Invalid input. Options: {', '.join(options)}")
                continue
        break
    correct = False
    if q['type'] == 'multiple_choice':
        correct_index = q['options'].index(q['answer'])
        if ans.upper() == chr(65 + correct_index):
            correct = True
    elif q['type'] == 'true_false':
        if ans.lower() == q['answer'].lower():
            correct = True
    else:
        if ans.lower() == q['answer'].lower():
            correct = True
    if correct:
        print("Correct!")
    else:
        print(f"Wrong. The correct answer is: {q['answer']}")
    return correct, score_penalty

def ask_rating():
    while True:
        try:
            rating = int(input("Rate this question (1-5): "))
            if 1 <= rating <= 5:
                return rating
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    print("Welcome to the Python Quiz App!")
    print("This app will quiz you on Python concepts.")
    username = login()
    if not username:
        return
    questions = load_questions()
    scores = load_scores()
    if username not in scores:
        scores[username] = []
    while True:
        num, types = get_quiz_params()
        selected = select_questions(questions, num, types)
        total_score = 0
        correct_count = 0
        questions_done = 0
        for q in selected:
            correct, penalty = ask_question(q)
            total_score += (1 - penalty) if correct else 0
            if correct:
                correct_count += 1
            questions_done += 1
            rating = ask_rating()
            if 'ratings' not in q:
                q['ratings'] = []
            q['ratings'].append(rating)
            if questions_done < num:
                cont = input("Continue to next question? (y/n): ").strip().lower()
                if cont != 'y':
                    print("Exiting early.")
                    break
        percentage = (correct_count / questions_done) * 100 if questions_done > 0 else 0
        print(f"\nQuiz complete! Correct: {correct_count}/{questions_done} ({percentage:.1f}%)")
        # Save score
        session = {
            'date': datetime.now().isoformat(),
            'correct': correct_count,
            'total': questions_done,
            'score': total_score,
            'percentage': percentage
        }
        scores[username].append(session)
        save_scores(scores)
        # Update questions.json with ratings
        with open('questions.json', 'w') as f:
            json.dump({'questions': questions}, f, indent=2)
        cont = input("Do you want to take another quiz? (y/n): ").strip().lower()
        if cont != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()