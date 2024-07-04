
import random
from string import ascii_lowercase
import pathlib
import tomli


NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions.toml"
QUESTIONS = tomli.loads(QUESTIONS_PATH.read_text())


def run_quiz():
    # Preprocess
    questions = prepare_questions(QUESTIONS, num_questions=NUM_QUESTIONS_PER_QUIZ)
    
    # Process (main loop)
    num_correct = 0
    for num, (question, alternatives) in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        num_correct += ask_questions(question, alternatives)
        
    # Post process
    print(f"\nYou got {num_correct} correct out of {num} questions")


def prepare_questions(questions, num_questions):
    num_questions = min(num_questions, len(questions))
    return random.sample(list(questions.items()), k=num_questions)


def ask_questions(question, alternatives):
    # pick out the correct answer from the list of alternatives
    correct_answer = alternatives[0]
    # shuffle the alternatives
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))
    # print the question to the screen
    # print all alternatives to the screen
    # get the answer from the user
    answer = get_answer(question, ordered_alternatives)
    # check that the user's answer is valid
    # check whether the user answered correctly or not
    # Add 1 to the count of correct answers if the answer is correct
    if answer == correct_answer:
        print("⭐ Correct! ⭐")
        return 1
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")
        return 0
    
    
def get_answer(question, alternatives):
    print(f"\n{question}?")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    for label, alternative in labeled_alternatives.items():
        print(f" {label}) {alternative}")
    while (answer_label := input("\nChoice? ")) not in labeled_alternatives:
        print(f"Please answer one of {', '.join(labeled_alternatives)}")
    return labeled_alternatives[answer_label]


if __name__ == "__main__":
    run_quiz()