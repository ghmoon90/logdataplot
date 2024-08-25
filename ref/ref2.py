import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class GraphInteraction:
    def __init__(self, ax, data_files, selected_columns):
        self.ax = ax
        self.data_files = data_files
        self.selected_columns = selected_columns
        self.selected_line = None  # Track the selected line
        self.tooltip_label = None  # Track the tooltip label

        # Connect event handlers
        self.cid_click = ax.figure.canvas.mpl_connect('button_press_event', self.on_click)
        self.cid_motion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_hover)

    def on_click(self, event):
        """Highlight the line when it's clicked."""
        if event.inaxes != self.ax:
            return

        for line in self.ax.get_lines():
            if line.contains(event)[0]:  # Check if the line contains the click event
                self.highlight_line(line)
                return

        # If no line was clicked, remove the highlight
        self.unhighlight_line()

    def on_hover(self, event):
        """Display tooltip near the cursor."""
        if event.inaxes != self.ax:
            return

        # Hide tooltip if the cursor is not near a line
        if self.tooltip_label:
            self.tooltip_label.remove()
            self.tooltip_label = None

        for line in self.ax.get_lines():
            if line.contains(event)[0]:
                xdata, ydata = line.get_xdata(), line.get_ydata()
                ind = min(range(len(xdata)), key=lambda i: abs(xdata[i] - event.xdata))
                x, y = xdata[ind], ydata[ind]

                # Show the tooltip
                self.tooltip_label = self.ax.text(event.xdata, event.ydata,
                                                  f'x: {x:.2f}, y: {y:.2f}',
                                                  fontsize=10, bbox=dict(facecolor='yellow', alpha=0.5))
                self.ax.figure.canvas.draw()
                break

    def highlight_line(self, line):
        """Highlight the selected line."""
        if self.selected_line:
            self.unhighlight_line()  # Unhighlight the previously selected line

        self.selected_line = line
        line.set_linewidth(3)  # Make the line thicker
        line.set_color('red')  # Change the line color
        self.ax.figure.canvas.draw()

    def unhighlight_line(self):
        """Unhighlight the selected line."""
        if self.selected_line:
            self.selected_line.set_linewidth(1)  # Reset line width
            self.selected_line.set_color('blue')  # Reset line color to original
            self.selected_line = None
            self.ax.figure.canvas.draw()

# Example usage:
fig, ax = plt.subplots()

# Suppose we have a data_files dictionary and selected_columns list
data_files = {
    'file1.csv': {'Column 1': [1, 2, 3], 'Column 2': [4, 5, 6]},
    'file2.csv': {'Column 1': [7, 8, 9], 'Column 2': [10, 11, 12]}
}
selected_columns = ['file1.csv/Column 1', 'file2.csv/Column 2']

# Plot the selected columns
for item in selected_columns:
    file_name, column = item.split('/')
    ax.plot(data_files[file_name][column], label=item)

ax.legend()
ax.set_title("Data Plot")
ax.set_xlabel("Index")
ax.set_ylabel("Values")

# Add graph interaction
GraphInteraction(ax, data_files, selected_columns)

plt.show()
