import tkinter as tk
from tkinter import messagebox, ttk

# Define the questions and options
questions = [
    {
        "question": "How often have you felt little interest or pleasure in doing things?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    },
    {
        "question": "How often have you felt down, depressed, or hopeless?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    },
    {
        "question": "How often have you had trouble falling or staying asleep, or sleeping too much?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    },
    {
        "question": "How often have you felt tired or had little energy?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    },
    {
        "question": "How often have you had poor appetite or overeating?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    },
    {
        "question": "How often have you felt bad about yourself, or that you are a failure or have let yourself or your family down?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    },
    {
        "question": "How often have you had trouble concentrating on things, such as reading the newspaper or watching television?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    },
    {
        "question": "How often have you moved or spoken so slowly that other people could have noticed? Or the opposite - being fidgety or restless?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    },
    {
        "question": "How often have you had thoughts that you would be better off dead or of hurting yourself in some way?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    },
    {
        "question": "How often have you found it difficult to relax or unwind?",
        "options": [
            "1. Not at all",
            "2. Several days",
            "3. More than half the days",
            "4. Nearly every day"
        ]
    }
]

# Scoring function
def calculate_depression_level(scores):
    total_score = sum(scores)
    
    if total_score <= 5:
        return "Minimal or no depression."
    elif total_score <= 10:
        return "Mild depression."
    elif total_score <= 15:
        return "Moderate depression."
    elif total_score <= 20:
        return "Moderately severe depression."
    else:
        return "Severe depression."

# Function to handle user responses and calculate depression level
def handle_submit():
    depression_level = calculate_depression_level(scores)
    messagebox.showinfo("Depression Level", f"Your indicative depression level is: {depression_level}")

# Function to show the next question
def show_next_question():
    global current_question_index
    
    if current_question_index < len(questions):
        question = questions[current_question_index]
        question_label.config(text=question["question"])
        
        # Clear old radio buttons
        for widget in options_frame.winfo_children():
            widget.destroy()
        
        # Create new radio buttons for current question
        var = tk.StringVar(value=question["options"][0])
        question_vars[current_question_index] = var
        
        for option in question["options"]:
            tk.Radiobutton(
                options_frame, 
                text=option, 
                variable=var, 
                value=option, 
                font=("Arial", 12), 
                bg="#f8f8ff",
                activebackground="#d6e4ff",
                cursor="hand2",
                selectcolor="#d9eaf7"
            ).pack(anchor="w", padx=10, pady=2)
        
        # Update progress
        progress_var.set(f"Question {current_question_index + 1} of {len(questions)}")
        progress_bar['value'] = (current_question_index + 1) * 10  # Update the progress bar
        current_question_index += 1
    else:
        # End of questions, calculate result
        scores.clear()
        for i in range(len(questions)):
            score = int(question_vars[i].get().split(".")[0])  # Extract score from the option selected
            scores.append(score - 1)  # Adjusting scores to 0-based (Not at all = 0, Nearly every day = 3)
        
        handle_submit()

# Function to initialize the chatbot UI
def initialize_ui():
    global question_label, options_frame, current_question_index, question_vars, scores, progress_var, progress_bar
    
    # Create the main window
    root = tk.Tk()
    root.title("Mental Health Chatbot")
    root.geometry("600x500")
    root.configure(bg="#f0f8ff")
    
    # Gradient background
    canvas = tk.Canvas(root, width=600, height=500)
    canvas.pack(fill="both", expand=True)
    canvas.create_rectangle(0, 0, 600, 500, fill="#cfd9df", outline="")
    canvas.create_rectangle(0, 250, 600, 500, fill="#e2ebf0", outline="")
    
    # Title Label
    title_label = tk.Label(root, text="Mental Health Check-In", font=("Arial", 20, "bold"), fg="#003366", bg="#e2ebf0")
    title_label.place(x=50, y=10)

    # Progress Indicator Label
    progress_var = tk.StringVar()
    progress_label = tk.Label(
        root, 
        textvariable=progress_var, 
        font=("Arial", 12, "bold"), 
        fg="#003366", 
        bg="#e2ebf0",
        borderwidth=2, 
        relief="solid"
    )
    progress_label.place(x=200, y=60)

    # Question Label
    question_label = tk.Label(root, text="", wraplength=500, justify="left", font=("Arial", 14), bg="#e2ebf0", fg="#002244")
    question_label.place(x=50, y=100)
    
    # Frame for radio buttons
    options_frame = tk.Frame(root, bg="#e2ebf0")
    options_frame.place(x=50, y=180)

    # Progress Bar
    progress_bar = ttk.Progressbar(
        root, 
        orient="horizontal", 
        length=400, 
        mode="determinate", 
        style="TProgressbar"
    )
    progress_bar.place(x=100, y=360)
    progress_bar['maximum'] = len(questions) * 10
    progress_bar['value'] = 0  # Initial value

    # Next Button
    next_button = ttk.Button(root, text="Next", command=show_next_question, style="Accent.TButton")
    next_button.place(x=250, y=400)

    # Apply custom style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Accent.TButton", font=("Arial", 14), background="#007acc", foreground="white", padding=10)
    style.map("Accent.TButton", background=[("active", "#005f99")])
    style.configure("TProgressbar", troughcolor="#d3d3d3", background="#007acc", thickness=20)

    # Initialize variables
    question_vars = {}
    scores = []
    current_question_index = 0
    
    show_next_question()  # Start with the first question

    root.mainloop()

if __name__ == "__main__":
    initialize_ui()
