import random  # shuffling the order of the questions and the order of the options of the questions.
import os  # check the validity of the link provided by the user

# -----
def convert(string):  # transforms a string into a list of characters
    string_list = list(string.split(","))
    return string_list

# -----
def file_2_dictionary_and_options_array(pathFile):
    tuple_array_modified, dictionary, options_array = [], {}, []
    array_lines = [line.strip() for line in open(pathFile, 'r')]  # List that contains the lines of the file -> *path*
    non_empty_array_lines = [line for line in array_lines if line.strip() != ""]

    # Dividing the list : *array_lines* into tuples of length two :
    # *tuple_array* -> tuple_array = [ (question, options ), ... ] = [ (question, [option_1, option_2, ...] ), ... ]
    tuple_array = [(non_empty_array_lines[i], non_empty_array_lines[i + 1]) for i in
                   range(0, len(non_empty_array_lines) - 1, 2)]

    for tuple_element in tuple_array:# Convert the second element of each tuple to an array: tuple_array -> tuple_array_modified
        tuple_array_modified.append((tuple_element[0], tuple_element[1].split(",")))

    for tuple_element in tuple_array_modified:  # Dictionary filling : *dictionary*  -> key : tuple_element[0] : question
        dictionary[tuple_element[0]] = tuple_element[1][
            0]  # -> value : tuple_element[1][0] : correct option of the question

    for tuple_element in tuple_array:  # List filling : *options_array*
        temp = convert(tuple_element[1])  # temp = [ option_1, option_2, .... , option_k ]
        for i in range(len(temp)):
            temp[i] = temp[i].strip()
        temp.append(tuple_element[0])  # temp = [ option_1, option_2, .... , option_k , question ]
        options_array.append(
            temp)  # options_array = [ temp, ... ] = [ [ option_1, option_2, .... , option_k , question ], ... ]

    return dictionary, options_array

# -----
def shuffle_dictionary(dictionary):  # shuffle the given dictionary
    keys = list(dictionary.keys())
    random.shuffle(keys)  # shuffle the keys
    return dict([(key, dictionary[key]) for key in keys])  # returning a new dictionary with the new shuffled keys

# -----
def get_quiz_path():
    print("\n" +  # ASCII ART LOGO : Quiz Generator
          "   ____            _            _____                                        _                  \n" +
          "  / __ \\          (_)          / ____|                                      | |                 \n" +
          " | |  | |  _   _   _   ____   | |  __    ___   _ __     ___   _ __    __ _  | |_    ___    _ __ \n" +
          " | |  | | | | | | | | |_  /   | | |_ |  / _ \\ | '_ \\   / _ \\ | '__|  / _` | | __|  / _ \\  | '__|\n" +
          " | |__| | | |_| | | |  / /    | |__| | |  __/ | | | | |  __/ | |    | (_| | | |_  | (_) | | |   \n" +
          "  \\___\\_\\  \\__,_| |_| /___|    \\_____|  \\___| |_| |_|  \\___| |_|     \\__,_|  \\__|  \\___/  |_|   \n" +
          "                                                                               @saad_labriji\n")
    print("[SYSTEM] * user can provide uppercase or lowercase choices\n")
    print("[SYSTEM] * Enter the link of the .txt file containing the quiz : \n", end="")
    path_file = input("[USER] : ")
    while os.stat(path_file).st_size == 0:
        print("[SYSTEM] *** WARNING ***  Empty file !, try again ... \n", end="")
        path_file = input("[USER] : ")
    print()
    return path_file

# -----
def new_game(dictionary, options_array):
    cpt, score = 1, 0
    user_guesses, correct_guesses, random_options_dictionary = [], [], {}
    if user_choice() == 1:  # Random order of questions
        dictionary = shuffle_dictionary(dictionary)

    for question in dictionary.keys():
        print("- Question " + str(cpt) + "/" + str(len(dictionary)) + " : ",
              end="")  # str(len(dictionary)) -> total number of Questions
        print(question)
        for options in options_array:
            if options[-1] == question:
                random_options_dictionary = random_options(options[:-1], split("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
                # 1 option -> A. option 1 , ... , 2 options -> A. option 1 , B. option 2  ...
                print("\n--------------------------------------------")
                options_selection("ABCDEFGHIJKLMNOPQRSTUVWXYZ", len(options[:-1]))
        guess = input("[USER] : ").upper()
        while guess not in random_options_dictionary:  # loop that ensures the validity of the user's choice.
            print("[SYSTEM] *** WARNING ***  invalid option ! , TRY AGAIN ... \n", end="")
            guess = input("[USER] : ").upper()
        user_guesses.append(random_options_dictionary[guess])  # Saving user results
        correct_guesses.append(dictionary.get(question))  # Saving correct results
        score += check_answer(random_options_dictionary[guess],
                              dictionary.get(question))  # Checking the result and updating the score
        print("--------------------------------------------" + "\n")
        cpt += 1  # cpt -> question index
    display_results1(user_guesses, correct_guesses, score, len(dictionary))

# -----
def user_choice():
    print("[SYSTEM] * Do you want to activate : random order of the questions ? (yes/no) \n", end="")
    choice_random_questions = input("[USER] : ")
    while choice_random_questions.lower() not in ("yes", "no"):  # loop that ensures the validity of the user's choice.
        print("[SYSTEM] *** WARNING ***  you SHOULD type yes OR no ! \n", end="")
        choice_random_questions = input("[USER] : ")
    if choice_random_questions.lower() == "yes":
        choice_random_questions = 1
    else:
        choice_random_questions = 0
    print()
    return choice_random_questions

# -----
def check_answer(guess, answer):
    guess = guess.strip().upper()
    answer = answer.strip().upper()
    print("[SYSTEM] *", end="")
    if guess == answer:
        print(" Correct! ( you get +1 point )")
        return 1
    else:
        print(" False! ( you get 0 points :/ ) ")
        return 0

# ----
def bloc_len(list1, list2):  # list1 and list2 are lists of strings
    max = 0
    for e in list1 + list2:
        if len(e) > max:
            max = len(e)
    return max  # ( length of longest element in  list1 ∪ list2 )

# ----
def create_bloc(string, n):  # exp : create_bloc( "test_string", 5) == "| test_string   |"
    if len(string) == n:
        return "| " + string + " |"
    elif len(string) == n - 1:
        return "| " + string + "  |"
    str1 = "| " + string
    for i in range(n - len(str1) + 2):
        str1 += " "
    str1 += " |"
    return str1

# ----
def hyphens_maker(n):  # exp : hyphens_maker(4) == "----"
    hyphen = ""
    for j in range(n):
        hyphen += "-"
    return hyphen

# ----
def hyphens_line(n):  # exp : hyphens_line(5) == "|------:||:-----:||:------|"
    print("|" + hyphens_maker(n + 1) + ":||:" + hyphens_maker(n) + ":||:" + hyphens_maker(n + 1) + "|")

# ----
def hyphens_last_line(n):  # exp : hyphens_last_line(6) == "|-----------------:||:-------|"
    print("|" + hyphens_maker(2 * n + 5) + ":||:" + hyphens_maker(n + 1) + "|")

# ----
def result_calculator(str1, str2):
    str1 = str1.strip().upper()
    str2 = str2.strip().upper()
    if str1 == str2:
        return "+1 point"
    else:
        return "+0 point"

# ----
def display_results1(list1, list2, score, number_questions):
    n = max(bloc_len(list1, list2) + 4, 22)
    print("[SYSTEM] * Here is your results : \n")
    print(create_bloc(" ", n)[1:-1] + " |", end="")
    hyphens_line(n)
    print(create_bloc(" ", n)[1:-1] + " |", end="")
    print(create_bloc("User guesses ", n) + create_bloc("Correct answers  ", n) + create_bloc("Points ", n))
    print("| " + hyphens_maker(n) + " |", end="")
    hyphens_line(n)
    for i in range(len(list1)):
        print(create_bloc(" Question N°" + str(i + 1), n), end="")
        print(
            create_bloc(list1[i], n) + create_bloc(list2[i], n) + create_bloc(result_calculator(list1[i], list2[i]), n))
    print("| " + hyphens_maker(n) + " |", end="")
    hyphens_last_line(n)
    print(create_bloc(" ", n)[1:-1] + " |", end="")
    print(create_bloc("Final result", 2 * n + 4) + create_bloc(str(score) + " points", n))
    print(create_bloc(" ", n)[1:-1] + " |", end="")
    print(create_bloc("Percentage of success", 2 * n + 4) + create_bloc(
        "{:.2f}".format(score / number_questions * 100) + " %", n))
    print(create_bloc(" ", n)[1:-1] + " |", end="")
    hyphens_last_line(n)

# ----
def random_options(options_list, list_numbers):
    random_options_dictionary = {}
    n = len(options_list)
    while len(options_list) != 0:
        random_option = random.choice(options_list)
        print("      " + list_numbers[n - len(options_list)] + ". " + random_option)
        random_options_dictionary[list_numbers[n - len(options_list)]] = random_option
        options_list.remove(random_option)
    return random_options_dictionary

# -----
def split(word):  # word to list of characters
    return [char for char in word]

# -----
def select_options(string, n):  # prints the n first characters of the word : *word*
    string = string[:n]
    for e in string:
        print(e)

# ----------
def options_selection(string, n):  # exp : options_selection("ABCDEF", 4) == "[SYSTEM] * Select (A, B, C, or D) :"
    if n == 2:
        print("[SYSTEM] * Select (" + string[0] + " or " + string[1] + ") :\n", end="")
    else:
        string = string[:n]
        print("[SYSTEM] * Select (", end="")
        for e in string[:-1]:
            print(e, end=", ")
        print("or " + string[-1] + ") :\n", end="")



try:
    path = get_quiz_path()
    file_tuple = file_2_dictionary_and_options_array(path)
    new_game(file_tuple[0], file_tuple[1]) # ---------- Run the Quiz :

except Exception as exception: # Exception handling :
    print("\n[SYSTEM] *** WARNING ***  something went wrong :( ")
    print("         *** ", end="")
    print(exception)