import random
import csv

verbs = []
recorded_verbs = set()
conjugation_types = ["て-form"]
skipped_count = 0

with open("verbs.csv", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row

    for row in reader:
        if not row:
            print("This row is empty or does not contain enough data.")
            skipped_count += 1
            continue
        elif len(row) < 2:
            print(f"This row does not contain enough data: {row}")
            skipped_count += 1
            continue

        verb = row[0]
        verb_type = row[1]

        verb = verb.strip()
        verb_type = verb_type.strip().lower()

        if verb == "" or verb_type == "":
            print(f"This row contains empty fields: {row}")
            skipped_count += 1
            continue

        if verb_type not in ["ichidan", "godan", "irregular"]:
            print(
                f"Unknown verb type '{verb_type}' for verb '{verb}'. Skipping this row."
            )
            skipped_count += 1
            continue

        if verb not in recorded_verbs:
            verbs.append((verb, verb_type))
        else:
            print(f"Duplicate verb '{verb}' found. Skipping this row.")
            skipped_count += 1
            continue

        recorded_verbs.add(verb)

random.shuffle(verbs)

correct_count = 0
incorrect_count = 0

mistakes = []


def conjugate_て_form(verb, verb_type):
    # Semi Auto Conjugation Functions for each group of verbs
    def conjugate_て_ichidan(verb):
        # Takes ichidan verbs and replaces the る to て
        return verb[:-1] + "て"

    def conjugate_て_godan(verb):
        # Takes godan verbs and replaces the final character with the   appropriate て-form ending
        if verb.endswith(("う", "つ", "る")):
            return verb[:-1] + "って"
        elif verb.endswith(("む", "ぶ", "ぬ")):
            return verb[:-1] + "んで"
        elif verb == "行く":
            return "行って"
        elif verb == "いく":
            return "いって"
        elif verb.endswith("く"):
            return verb[:-1] + "いて"
        elif verb.endswith("ぐ"):
            return verb[:-1] + "いで"
        elif verb.endswith("す"):
            return verb[:-1] + "して"
        else:
            raise ValueError(f"Unknown godan verb ending for {verb}")

    def conjugate_て_irregular(verb):
        # Handles the two irregular verbs
        if verb == "する":
            return "して"
        elif verb == "来る":
            return "来て"
        elif verb == "くる":
            return "きて"
        else:
            raise ValueError(f"Unknown irregular verb: {verb}")

    if verb_type == "ichidan":
        return conjugate_て_ichidan(verb)
    elif verb_type == "godan":
        return conjugate_て_godan(verb)
    elif verb_type == "irregular":
        return conjugate_て_irregular(verb)
    else:
        raise ValueError(f"Unknown verb type: {verb_type}")


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
