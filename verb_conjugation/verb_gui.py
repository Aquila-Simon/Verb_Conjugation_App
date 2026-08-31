import random
import tkinter as tkin
from verb_conjugation.verb_conjugation import conjugate_て_form
from verb_conjugation.verb_conjugation import conjugate_ます_form
from shared.csv_loader import load_verbs

# Creating a Dictionary to simplify tags when used in Functions
test_state = {
    "current_question": 0,
    "score": 0,
    "skipped_count": 0,
    "mistakes": [],
    "verbs": [],
    "conjugation_types": ["て", "ます"],
    "conjugation_type": "",
    "verb": "",
    "verb_type": "",
    "correct_answer": "",
}


def generate_correct_answer():
    if test_state["conjugation_type"] == "て":
        test_state["correct_answer"] = conjugate_て_form(
            test_state["verb"], test_state["verb_type"]
        )
    if test_state["conjugation_type"] == "ます":
        test_state["correct_answer"] = conjugate_ます_form(
            test_state["verb"], test_state["verb_type"]
        )


def check_answer(event=None):  # Function for Receiving the answer and verifying it
    answer = answer_entry.get()  # Gets Answer from Answer Entry Box

    # Answer Verification and Response
    if answer == test_state["correct_answer"]:
        answer_label.config(text="Correct!", fg="green", font=("Arial", 18, "bold"))
        test_state["score"] += 1
    else:
        answer_label.config(
            text=f"Incorrect. The correct answer is {test_state['correct_answer']}",
            fg="red",
            font=("Arial", 18, "bold"),
        )
        test_state["mistakes"].append(
            (test_state["verb"], answer, test_state["correct_answer"])
        )

    test_state["current_question"] += 1

    score_label.config(
        text=f"Score: {test_state['score']}/{len(test_state['verbs'])}",
        font=("Arial", 16, "bold"),
    )

    # Checks whether we need more questions of if the test is done
    if test_state["current_question"] < len(test_state["verbs"]):
        unpacked_verb = test_state["verbs"][test_state["current_question"]]
        test_state["verb"], test_state["verb_type"] = unpacked_verb
        generate_correct_answer()
        question_label.config(text=f"Question #{test_state['current_question'] + 1}")
        question_bar.config(
            text=f"What is the {test_state['conjugation_type']}-form of {test_state['verb']}?"
        )
        answer_entry.delete(0, tkin.END)
    else:
        review_text = ""
        for mistake_verb, user_answer, mistake_correct_answer in test_state["mistakes"]:
            review_text += f"Verb: {mistake_verb}\n"
            review_text += f"Answer: {user_answer}\n"
            review_text += f"Correct Answer: {mistake_correct_answer}\n\n"

        finish_label.config(text="Test Complete", fg="yellow")  # Marks Test as Done

        # Lists Mistakes for Review on the end of the test
        if test_state["mistakes"]:
            mistake_text.pack(pady=10)
            mistake_text.config(fg="orange", bg=root.cget("bg"), highlightthickness=0)
            mistake_text.insert("1.0", review_text)
            mistake_text.config(state="disabled")
        answer_entry.delete(0, tkin.END)
        answer_entry.unbind("<Return>")
        answer_entry.config(state="disabled")
        submit_bt.pack_forget()
        restart_bt.pack(pady=10)


def restart_test(
    event=None,
):  # Function to call for resetting the test for Endless Fun lol
    test_state["current_question"] = 0
    test_state["score"] = 0
    test_state["mistakes"].clear()
    test_state["verbs"], test_state["skipped_count"] = load_verbs()
    test_state["conjugation_type"] = random.choice(test_state["conjugation_types"])
    random.shuffle(test_state["verbs"])
    unpacked_verb = test_state["verbs"][test_state["current_question"]]
    test_state["verb"], test_state["verb_type"] = unpacked_verb
    generate_correct_answer()

    score_label.config(
        text=f"Score: {test_state['score']}/{len(test_state['verbs'])}",
        font=("Arial", 16, "bold"),
    )
    question_label.config(text=f"Question #{test_state['current_question'] + 1}")
    question_bar.config(
        text=f"What is the {test_state['conjugation_type']}-form of {test_state['verb']}?"
    )
    answer_label.config(text="")
    finish_label.config(text="")
    mistake_text.config(state="normal")

    mistake_text.delete("1.0", tkin.END)
    answer_entry.delete(0, tkin.END)
    answer_entry.bind("<Return>", check_answer)
    mistake_text.config(state="disabled")
    mistake_text.pack_forget()
    restart_bt.pack_forget()
    submit_bt.pack(pady=5)
    answer_entry.config(state="normal")


# Initialize Test upon Boot as far as variables and lists
test_state["current_question"] = 0
test_state["score"] = 0
test_state["mistakes"] = []

# Creates the very first question
test_state["verbs"], test_state["skipped_count"] = load_verbs()
test_state["conjugation_type"] = random.choice(test_state["conjugation_types"])
random.shuffle(test_state["verbs"])
unpacked_verb = test_state["verbs"][test_state["current_question"]]
test_state["verb"], test_state["verb_type"] = unpacked_verb
generate_correct_answer()

# Main Screen Setup
root = tkin.Tk()
root.title(
    "Japanese Conjugations Test"
)  # Placeholder name for now, I can probably come up with a better one later
root.geometry("400x500")  # FYI: Width x Height

# Sets up the Score Display
score_label = tkin.Label(root, text="Score: 0", font=("Arial", 16, "bold"))
score_label.pack(anchor="w", padx=10, pady=10)

# Sets up the Question Number Display
question_label = tkin.Label(root, text="")
question_label.pack(anchor="center", padx=10, pady=10)
question_label.config(text=f"Question #{test_state['current_question'] + 1}")

# Sets up the Actual Question Display
question_bar = tkin.Label(
    root,
    text=f"What is the {test_state['conjugation_type']}-form of {test_state['verb']}?",
    font=("Arial", 20, "bold"),
)
question_bar.pack(
    pady=10
)  # Places the Question onto the screen with a 10px padding (Duh, I should know that lol)

# Creates the Field to input answers
answer_entry = tkin.Entry(root)
answer_entry.pack(pady=5)

# Creates a Frame for the Buttons to live in (Prevents the issue of havigng to precisely pack them to appear)
button_frame = tkin.Frame(root)
button_frame.pack(pady=5)

# Creates the buttons to be used
submit_bt = tkin.Button(
    button_frame, text="Submit", command=check_answer, font=("Arial", 16, "bold")
)
submit_bt.pack(pady=5)

restart_bt = tkin.Button(
    button_frame, text="Restart", command=restart_test, font=("Arial", 16, "bold")
)
# Unlike the submit_bt, I don't pack the restart_bt until after the test is done cause duh you can figure it out

# This line just makes it so we can press "Enter/Return" to send the answer
answer_entry.bind("<Return>", check_answer)

# Initialization of the "Correct/Not Correct", "Test Finished", and the Mistake Review at the end
answer_label = tkin.Label(root, text="")
finish_label = tkin.Label(root, text="")
mistake_text = tkin.Text(root, height=8, width=40)
answer_label.pack(pady=0)
finish_label.pack(pady=0)

# Starts the tkinter loop, waiting for user input
root.mainloop()
