import random

verbs = {
    "飲む": "飲んで",
    "書く": "書いて",
    "話す": "話して",
    "待つ": "待って",
    "食べる": "食べて",
}

verb_list = list(verbs.keys())
random.shuffle(verb_list)

correct_count = 0
incorrect_count = 0

mistakes = []

for verb in verb_list:
    answer = input(f"What is the て-form of {verb}? ")

    if answer == verbs[verb]:
        print("Correct!")
        correct_count += 1
    else:
        print(f"Incorrect. The correct て-form of {verb} is {verbs[verb]}.")
        incorrect_count += 1
        mistake = (verb, answer)
        mistakes.append(mistake)


print(f"You answered {correct_count}/{len(verb_list)} correctly.")
if incorrect_count > 0:
    print("\nYou got the following verbs incorrect:")
    for verb, answer in mistakes:
        print(f"\n- {verb}")
        print(f"Your Answer: {answer}")
        print(f"Correct Answer: {verbs[verb]}")
