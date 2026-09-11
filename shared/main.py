import random
from verb_conjugation.verb_conjugation import conjugate_て_form
from shared.csv_loader import load_verbs

verbs, skipped_count = load_verbs()
random.shuffle(verbs)

conjugation_types = ["て-form"]

correct_count = 0
incorrect_count = 0

mistakes = []

if not verbs:
    print("All rows were skipped due to empty fields or insufficient data.")
    exit()

for verb, verb_type in verbs:
    conjugation_type = random.choice(conjugation_types)

    if conjugation_type == "て-form":
        correct_answer = conjugate_て_form(verb, verb_type)
        answer = input(f"What is the て-form of {verb}? ")
    # elif conjugation_type == "ない-form":
    # correct_answer = conjugate_ない_form(verb, verb_type)
    # answer = input(f"What is the ない-form of {verb}? ")
    else:
        print(f"Skipping {conjugation_type} for {verb} as it is not implemented.")
        continue

    if answer == correct_answer:
        print("Correct!")
        correct_count += 1
    else:
        print(
            f"Incorrect. The correct {conjugation_type} of {verb} is {correct_answer}."
        )
        incorrect_count += 1
        mistakes.append((verb, answer, correct_answer, conjugation_type))


print(f"You answered {correct_count}/{correct_count + incorrect_count} correctly.")
if incorrect_count > 0:
    print("\nYou got the following verbs incorrect:")
    for verb, answer, correct_answer, conjugation_type in mistakes:
        print(f"\n- {verb}")
        print(f"Your Answer: {answer}")
        print(f"Correct Answer: {correct_answer}")
        print(f"Conjugation Type: {conjugation_type}")

if skipped_count > 0:
    print(
        f"\n{skipped_count} rows were skipped due to empty fields, insufficient data, duplicate entries, or unknown verb types."
    )
