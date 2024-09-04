import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from matplotlib.animation import FuncAnimation
import mplcursors  # For interactive plots

# Create the main application window
root = tk.Tk()
root.title("Calculus and GDP Visualizer")
root.geometry("700x600")

# Define the normal distribution parameters
mu = 0
sigma = 1

# Function to generate and display the plot for partial derivatives (energy surface)
def plot_energy_surface():
    clear_plot_frame()

    def energy_function(T, P):
        return T**2 + 3*T*P + P**2

    T = np.linspace(0, 10, 100)
    P = np.linspace(0, 10, 100)
    T, P = np.meshgrid(T, P)

    E = energy_function(T, P)

    fig, ax = plt.subplots(figsize=(6, 4))
    contour = ax.contourf(T, P, E, cmap='viridis')  # Using a vibrant colormap
    ax.set_xlabel('Temperature (T)')
    ax.set_ylabel('Pressure (P)')
    ax.set_title('Energy Surface E(T, P)')
    ax.grid(True, linestyle='--', alpha=0.7)

    # Add color bar for better visual interpretation
    fig.colorbar(contour, ax=ax)

    def init():
        for coll in contour.collections:
            coll.set_alpha(0)
        return contour.collections

    def animate(i):
        alpha = i / 100
        for coll in contour.collections:
            coll.set_alpha(alpha)
        return contour.collections

    ani = FuncAnimation(fig, animate, init_func=init, frames=100, interval=5, blit=True, repeat=False)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to generate and display the plot for integration (distribution PDF)
def plot_distribution_pdf():
    clear_plot_frame()

    x = np.linspace(-5, 5, 1000)
    fig, ax = plt.subplots(figsize=(6, 4))
    line, = ax.plot([], [], lw=2, color='blue', label='Normal Distribution')
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('Probability Density')
    ax.set_title('Area Under Probability Density Function')
    ax.grid(True, linestyle='--', alpha=0.7)

    # Shade the area under the curve between -1 and 1
    x_fill = np.linspace(-1, 1, 1000)
    ax.fill_between(x_fill, norm.pdf(x_fill, mu, sigma), color='orange', alpha=0.3, label='Shaded Area')

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        line.set_data(x[:i], norm.pdf(x[:i], mu, sigma))
        return line,

    ani = FuncAnimation(fig, animate, init_func=init, frames=len(x), interval=1, blit=True, repeat=False)

    mplcursors.cursor(ax, hover=True)  # Make the plot interactive

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to generate and display the plot for maxima minima (profit maximization)
def plot_maxima_minima():
    clear_plot_frame()

    def profit(x):
        return -0.1 * x**3 + 2 * x**2 + 10 * x - 50

    x = np.linspace(0, 15, 100)

    fig, ax = plt.subplots(figsize=(6, 4))
    line, = ax.plot([], [], lw=2, color='green', label='Profit Function')
    ax.set_xlim(0, 15)
    ax.set_ylim(-50, 200)
    ax.set_xlabel('Quantity')
    ax.set_ylabel('Profit')
    ax.set_title('Profit Maximization')
    ax.grid(True, linestyle='--', alpha=0.7)

    res = minimize_scalar(lambda x: -profit(x))
    max_profit = -res.fun
    max_profit_x = res.x

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        line.set_data(x[:i], profit(x[:i]))
        if i == len(x) - 1:
            ax.scatter(max_profit_x, max_profit, color='red', marker='o', label=f'Max Profit: {max_profit:.2f} at x={max_profit_x:.2f}')
            ax.legend()
        return line,

    ani = FuncAnimation(fig, animate, init_func=init, frames=len(x), interval=5, blit=True, repeat=False)

    mplcursors.cursor(ax, hover=True)  # Make the plot interactive

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to plot only the GDP graph
def plot_gdp():
    clear_plot_frame()

    x = np.linspace(0, 10, 100)
    y_gdp = gdp_function(x)

    fig, ax = plt.subplots(figsize=(6, 4))
    line, = ax.plot([], [], lw=2, color='purple')
    ax.set_xlim(0, 10)
    ax.set_ylim(4000, 6000)
    ax.set_xlabel('Time')
    ax.set_ylabel('GDP')
    ax.set_title('GDP Over Time')
    ax.grid(True, linestyle='--', alpha=0.7)

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        line.set_data(x[:i], y_gdp[:i])
        return line,

    ani = FuncAnimation(fig, animate, init_func=init, frames=len(x), interval=5, blit=True, repeat=False)

    mplcursors.cursor(ax, hover=True)  # Make the plot interactive

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to display the explanation for partial derivatives (energy surface)
def explain_energy_surface():
    explanation_text = ("This plot represents the energy surface E(T, P), which illustrates how the energy of a system "
                        "varies with changes in temperature (T) and pressure (P). It is calculated using the function "
                        "E(T, P) = T^2 + 3*T*P + P^2.")
    messagebox.showinfo("Explanation - Energy Surface", explanation_text)

# Function to display the explanation for integration (distribution PDF)
def explain_distribution_pdf():
    explanation_text = ("This plot represents the probability density function (PDF) of a normal distribution. "
                        "The shaded area under the curve between -1 and 1 demonstrates the concept of integrating "
                        "a probability density function over a specified range.")
    messagebox.showinfo("Explanation - Distribution PDF", explanation_text)

# Function to display the explanation for maxima minima (profit maximization)
def explain_maxima_minima():
    explanation_text = ("This plot illustrates the profit function, showing how profit varies with quantity produced. "
                        "The red point represents the maximum profit achieved, calculated using optimization techniques.")
    messagebox.showinfo("Explanation - Profit Maximization", explanation_text)

# Function to display explanation for differentiation
def explain_differentiation():
    explanation_text = ("Differentiation is used to calculate the rate of change of a function with respect to its variable. "
                        "In this plot, the graph shows the GDP over time.")
    messagebox.showinfo("Explanation - Differentiation", explanation_text)

# Example GDP function
def gdp_function(x):
    return 1000 * np.sin(x) + 5000

# Function to clear the plot frame
def clear_plot_frame():
    for widget in plot_frame.winfo_children():
        widget.destroy()

# Function to add hover effect to buttons
def on_enter(e):
    e.widget['background'] = 'lightblue'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

# Create a frame to contain buttons
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=0, padx=10, pady=10)

# Create a frame for the plot
plot_frame = tk.Frame(root)
plot_frame.grid(row=1, column=0, padx=10, pady=10)

# Create buttons for calculus concepts
energy_button = tk.Button(button_frame, text="Energy Surface", command=plot_energy_surface)
energy_button.grid(row=0, column=0, padx=5, pady=5)
energy_button.bind("<Enter>", on_enter)
energy_button.bind("<Leave>", on_leave)

energy_explain_button = tk.Button(button_frame, text="Explain Energy Surface", command=explain_energy_surface)
energy_explain_button.grid(row=0, column=1, padx=5, pady=5)
energy_explain_button.bind("<Enter>", on_enter)
energy_explain_button.bind("<Leave>", on_leave)

distribution_button = tk.Button(button_frame, text="Distribution PDF", command=plot_distribution_pdf)
distribution_button.grid(row=1, column=0, padx=5, pady=5)
distribution_button.bind("<Enter>", on_enter)
distribution_button.bind("<Leave>", on_leave)

distribution_explain_button = tk.Button(button_frame, text="Explain Distribution PDF", command=explain_distribution_pdf)
distribution_explain_button.grid(row=1, column=1, padx=5, pady=5)
distribution_explain_button.bind("<Enter>", on_enter)
distribution_explain_button.bind("<Leave>", on_leave)

maxima_minima_button = tk.Button(button_frame, text="Maxima Minima (Profit)", command=plot_maxima_minima)
maxima_minima_button.grid(row=2, column=0, padx=5, pady=5)
maxima_minima_button.bind("<Enter>", on_enter)
maxima_minima_button.bind("<Leave>", on_leave)

maxima_minima_explain_button = tk.Button(button_frame, text="Explain Maxima Minima (Profit)", command=explain_maxima_minima)
maxima_minima_explain_button.grid(row=2, column=1, padx=5, pady=5)
maxima_minima_explain_button.bind("<Enter>", on_enter)
maxima_minima_explain_button.bind("<Leave>", on_leave)

# Create buttons for GDP visualization
differentiation_button = tk.Button(button_frame, text="GDP", command=plot_gdp)
differentiation_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
differentiation_button.bind("<Enter>", on_enter)
differentiation_button.bind("<Leave>", on_leave)

explanation_button = tk.Button(button_frame, text="Explain GDP", command=explain_differentiation)
explanation_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
explanation_button.bind("<Enter>", on_enter)
explanation_button.bind("<Leave>", on_leave)

# Run the Tkinter event loop
root.mainloop()
