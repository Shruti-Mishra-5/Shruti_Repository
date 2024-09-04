
# Tkinter Data Visualizer

This Python application provides an interactive and visually appealing way to explore various calculus concepts and GDP visualization using a Tkinter-based GUI. The application features animated plots, color-enhanced graphs, and interactive elements that help users understand complex mathematical functions more easily.

## Features

- **Energy Surface Plot**: Visualizes the energy surface \( E(T, P) = T^2 + 3TP + P^2 \) with an animated contour plot.
- **Distribution PDF Plot**: Displays the probability density function (PDF) of a normal distribution, highlighting specific areas under the curve.
- **Maxima and Minima Plot**: Shows the profit function and dynamically identifies the point of maximum profit.
- **GDP Over Time Plot**: Illustrates GDP over time with an animated line plot.
- **Interactive Plots**: Hover over plot elements to display specific data points using `mplcursors`.
- **Colorful and Styled**: Each plot is enhanced with vibrant colors, grid lines, and custom styles for better visual appeal.

## Prerequisites

Ensure you have Python installed on your machine. The following Python libraries are required:

- **Tkinter**: Pre-installed with Python for creating the GUI.
- **NumPy**: For numerical operations.
- **Matplotlib**: For plotting and animating graphs.
- **SciPy**: For optimization functions.
- **mplcursors**: To add interactivity to the plots.

You can install the required libraries using pip:

```bash
pip install numpy matplotlib scipy mplcursors
```

## How to Run

1. **Clone or download the repository**:
   ```bash
   git clone https://github.com/yourusername/calculus-gdp-visualizer.git
   cd calculus-gdp-visualizer
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Explore the features**:
   - Click on the buttons to generate different plots.
   - Hover over the plots to see interactive data points.
   - Use the explanations provided to better understand each plot.

## File Structure

- **main.py**: The main Python script containing the application logic.
- **README.md**: This file, providing an overview of the project.

## Screenshots and Video

### Application Interface
![Application Interface](images_recordings/Screenshot%202024-09-03%20171455.png)

### Energy Surface Plot
![Energy Surface Plot](images_recordings/Screenshot%202024-09-03%20171503.png)

### Video Demonstration
[Watch the Video](images_recordings/Images-Recordings.mp4)


## Contributing

Feel free to contribute to the project by submitting pull requests or opening issues for any bugs or feature requests.
