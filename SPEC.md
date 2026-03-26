--Overview
I want to create a command-line Python quiz app that reads questions from a JSON file and quizzes users, keeping track of the score and users' performance. 

--Expected Behavior
- The app should greet the user, giving a quick introduction to this app's functionality. 
- There should be a local login system that prompts users for a username and password (or allows them to enter a new username and password). The passwords should not be easily discoverable.
- The app should ask the user how many questions they want for their quiz, as well as the types of quiz questions they want to include (multiple choice, short answer, true/false).
- The app should randomly select questions from the quiz bank in the JSON file. 
- The app should present the questions one by one, giving the user the chance to give their response.
- Additional feature: Add a "hint" option that users can use if they need guidance. However, every time a user uses a hint, their score should decrease by one. 
- The app should tell them if their answer is right or wrong, keeping track of the user's score.
- After each question, the user should also be able to provide feedback on whether they like a question or not, and this should inform what questions they get next. This can be done by giving them an option to rank their preference on this question from 1-5. 
- After the user finishes their selected number of questions, the app should give instructions for either quitting the app, or generating a number of more questions if the user wants to practice more. 
- Make sure that there is a score history file that tracks performance and other useful statistics over time for each user. This file should not be human-readable and should be relatively secure. (This means someone could look at the file and perhaps find out usernames but not passwords or scores.)

--Data Format
- The question bank should be a JSON file. Here is an example of what this format should look like, as well as example questions and hints: 

{
  "questions": [
    {
      "question": "Which of the following is a valid variable name in Python?",
      "type": "multiple_choice",
      "options": ["2var", "my_var", "my var", "my-var"],
      "hint": "Variable names can include letters, numbers, and underscores—but cannot start with a number.",
      "answer": "my_var",
      "category": "Python Basics"
    },
    {
      "question": "What data type is the result of: print(type(3.0))?",
      "type": "multiple_choice",
      "options": ["int", "float", "double", "string"],
      "hint": "Numbers with a decimal point are treated differently than whole numbers in Python.",
      "answer": "float",
      "category": "Python Basics"
    },
    {
      "question": "What keyword is used to define a function in Python?",
      "type": "multiple_choice",
      "options": ["func", "define", "def", "function"],
      "hint": "Think about the short keyword Python uses to start a function definition, an abbreviation of the word define.",
      "answer": "def",
      "category": "Python Basics"
    },
    {
      "question": "A list in Python is immutable.",
      "type": "true_false",
      "hint": "Think about whether you can change a list after creating it—like adding, removing, or modifying elements.",
      "answer": "false",
      "category": "Data Structures"
    },
    {
      "question": "What built-in function returns the number of items in a list?",
      "type": "short_answer",
      "hint": "Think of the short built-in function name that’s an abbreviation for 'length'.",
      "answer": "len",
      "category": "Python Basics"
    }
  ]
}

--File Structure
- There should be a JSON file with the questions which the app randomly selects from.
- There should be another file for the command line interface and processing user inputs.
- Feel free to add other files if you feel it is needed and fits the project goals. 

--Additional Notes
- The questions should exist in their own human-readable .json file so that they can be easily modified. (This simply means all we have to do is generate/change the question bank if we want to use this project to study other subjects)
- None of this requires a backend, HTML, CSS, a graphical user interface, or the use of any APIs. Everything is local and should be ran in the terminal command line 

--Error Handling
- If the JSON file is missing, the program should not crash; Instead, it should inform the user of this problem and exit cleanly. 
- If the user inputs invalid input, the program should let them know that they answered something invalid and prompt them to answer again, re-showing the possible options the user can respond with. 
- If there are missing fields in the question data in the JSON file, check the keys before using and skip "malformed" questions, raising a warning to the user that it was a bad question. 

--Acceptance Criteria (this is a checklist of some specific things I'll check to decide if the implementation is "done")
- The program loads successfully with a valid JSON file, displaying questions/hints/scores without errors 
- Running the app with a missing JSON file prints a clear error message and exits cleanly.
- Once the user finishes the quiz, the program shows the total correct answers and score/percentage. 
- The program only accepts valid inputs and reprompts the user if an invalid input is given.
- If the user wants to exit early, it will cleanly do so with an appropriate exit message. 
- If the JSON question list is empty, the program should print a message and exit appropriately.  






