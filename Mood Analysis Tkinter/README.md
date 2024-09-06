# Mental Health CheckUP Chatbot

## Overview

This is a simple **Mental Health Check-In** chatbot created using Python and the `Tkinter` library for the graphical user interface. The chatbot is designed to assess a user's mental health by asking a series of questions based on the PHQ-9 (Patient Health Questionnaire) format. The user's responses are collected, and the chatbot calculates an indicative depression level based on the scores provided.

## Features

- **User-Friendly Interface**: Easy-to-use graphical interface with radio buttons for selecting responses.
- **Progress Indicator**: A progress bar shows the user how far they are into the questionnaire.
- **Depression Level Assessment**: After answering all the questions, the chatbot calculates and displays the user's depression level based on their answers.

## Questionnaire

The questionnaire consists of 10 questions, and each has four possible answers:
1. Not at all
2. Several days
3. More than half the days
4. Nearly every day

The responses are used to calculate a score that correlates with different levels of depression:
- **Minimal or No Depression**: 0-5 points
- **Mild Depression**: 6-10 points
- **Moderate Depression**: 11-15 points
- **Moderately Severe Depression**: 16-20 points
- **Severe Depression**: 21+ points

## Setup and Installation

### Prerequisites

- Python 3.x
- `tkinter` library (should be included with standard Python installations)

### Installation

1. **Clone or Download the Project**: 
   - Clone the repository or download the project zip file.
   - Unzip it if downloaded as a zip file.

2. **Run the Python Script**:
   - Navigate to the project directory in your terminal or command prompt.
   - Run the Python file:
     ```bash
     python chatbot.py
     ```

   Ensure that Python is properly installed and added to your system's PATH.

## How to Use

1. **Start the Application**: Once the script is executed, the chatbot's window will open.
2. **Answer the Questions**: Select your answer for each question by clicking on the appropriate radio button.
3. **Next Question**: After selecting an answer, click the **Next** button to proceed to the next question.
4. **Depression Level**: After the last question, your indicative depression level will be displayed based on your answers.

## Project Structure

```bash
.
├── chatbot.py         # Main Python script with UI and logic
├── README.md          # This README file
└── requirements.txt   # (Optional) Add if you have external libraries
```

## Screenshots

Here are some screenshots of the Mental Health Chatbot in action:

### 1. Initial Screen

![Initial Screen](./Images/Screenshot%202024-09-05%20172036.png)

### 2. Question Interface

![Question Interface](./Images/Screenshot%202024-09-05%20172025.png)

### 3. Progress and Result

![Progress and Result](./Images/Screenshot%202024-09-05%20172011.png)


## Customization

If you'd like to change or add more questions, you can modify the `questions` list in the Python script. Each entry in the list contains a question and its corresponding answer options.

```python
questions = [
    {
        "question": "Your new question?",
        "options": [
            "1. Option 1",
            "2. Option 2",
            "3. Option 3",
            "4. Option 4"
        ]
    }
]
```

## Dependencies

- **Tkinter**: Used to create the graphical user interface.
- **Messagebox**: For displaying the final results.
