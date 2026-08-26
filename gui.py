import tkinter as tkin
import random
from conjugation import conjugate_て_form
from csv_loader import load_verbs


current_question = 0
score = 0

verbs, skipped_count = load_verbs()

random.shuffle(verbs)

unpacked_verb = verbs[current_question]

verb, verb_type = unpacked_verb

correct_answer = conjugate_て_form(verb, verb_type)


def check_answer(event=None):
    global current_question, verb, verb_type, correct_answer, score
    answer = answer_entry.get()
    if answer == correct_answer:
        answer_label.config(text="Correct!", fg="green", font=("Arial", 14, "bold"))
        score += 1
    else:
        answer_label.config(
            text=f"Incorrect. The correct answer is {correct_answer}",
            fg="red",
            font=("Arial", 14, "bold"),
        )

    current_question += 1
    score_label.config(
        text=f"Score: {score}/{(len(verbs))}", font=("Arial", 16, "bold")
    )
    if current_question < len(verbs):
        unpacked_verb = verbs[current_question]
        verb, verb_type = unpacked_verb
        correct_answer = conjugate_て_form(verb, verb_type)
        question_bar.config(text=f"What is the て-form of {verb}?")
        answer_entry.delete(0, tkin.END)
    else:
        finish_label.config(text="Test Complete", fg="yellow")
        answer_entry.delete(0, tkin.END)
        answer_entry.unbind("<Return>")
        submit_bt.config(state="disabled")


root = tkin.Tk()
root.title("Japanese Conjugations Test")
root.geometry("400x400")

score_label = tkin.Label(root, text="Score: 0", font=("Arial", 16, "bold"))
score_label.pack(anchor="w", padx=10, pady=10)
question_bar = tkin.Label(
    root, text=f"What is the て-form of {verb}?", font=("Arial", 20, "bold")
)
question_bar.pack(pady=20)

answer_entry = tkin.Entry(root)
answer_entry.pack(pady=10)

submit_bt = tkin.Button(
    root, text="Submit", command=check_answer, font=("Arial", 16, "bold")
)
submit_bt.pack(pady=10)
answer_entry.bind("<Return>", check_answer)


answer_label = tkin.Label(root, text="")
finish_label = tkin.Label(root, text="")
answer_label.pack(pady=10)
finish_label.pack(pady=5)

root.mainloop()
