
import random
from string import ascii_lowercase
import pathlib
import tomli


NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions.toml"
QUESTIONS = tomli.loads(QUESTIONS_PATH.read_text())


def run_quiz():
    # Preprocess
    questions = prepare_questions(QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ)
    
    # Process (main loop)
    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        num_correct += ask_questions(question)
        
    # Post process
    print(f"\nYou got {num_correct} correct out of {num} questions")


def prepare_questions(path, num_questions):
    questions = tomli.loads(QUESTIONS_PATH.read_text())["questions"]
    num_questions = min(num_questions, len(questions))
    return random.sample(questions, k=num_questions)


def ask_questions(question):
    # pick out the correct answer from the list of alternatives
    correct_answers = question["answers"]
    # shuffle the alternatives
    alternatives = question["answers"] + question["alternatives"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))
    # print the question to the screen
    # print all alternatives to the screen
    # get the answer from the user
    answers = get_answers(
        question=question["question"],
        alternatives=ordered_alternatives,
        num_choices=len(correct_answers),
    )
    if set(answers) == set(correct_answers):
        print("⭐ Correct! ⭐")
        return 1
    else:
        is_or_are = " is" if len(correct_answers) == 1 else "s are"
        print("\n- ".join([f"No, the answer{is_or_are}:"] + correct_answers))
        return 0
    
    
def get_answers(question, alternatives, num_choices=1):
    print(f"{question}?")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    for label, alternative in labeled_alternatives.items():
        print(f"  {label}) {alternative}")

    while True:
        plural_s = "" if num_choices == 1 else f"s (choose {num_choices})"
        answer = input(f"\nChoice{plural_s}? ")
        answers = set(answer.replace(",", " ").split())

        # Handle invalid answers
        if len(answers) != num_choices:
            plural_s = "" if num_choices == 1 else "s, separated by comma"
            print(f"Please answer {num_choices} alternative{plural_s}")
            continue

        if any(
            (invalid := answer) not in labeled_alternatives
            for answer in answers
        ):
            print(
                f"{invalid!r} is not a valid choice. "
                f"Please use {', '.join(labeled_alternatives)}"
            )
            continue

        return [labeled_alternatives[answer] for answer in answers]
    

if __name__ == "__main__":
    run_quiz()