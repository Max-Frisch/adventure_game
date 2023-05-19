# get_yn takes a question as a parameter and only accepts yes/no/y/n as possible responses.
# It returns either yes or no
def get_yn(question: str) -> str:
    while True:
        answer = input(question + " (yes / no) -> ").lower().strip()
        if answer not in ["yes", "no", "y", "n"]:
            print("Please enter yes or no.")
        else:
            if answer == "y":
                answer = "yes"
            elif answer == "n":
                answer = "no"
            return answer
