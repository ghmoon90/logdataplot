'''
    Made by Gun Hee Moon 
    with ChatGPT 4 
    2024 08 15 
'''

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

class DataPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotter")

        # Allow the window to be resizable
        self.root.geometry("400x700")

        # Create a frame for the top menu
        menu_frame = tk.Frame(root)
        menu_frame.pack(side=tk.TOP, fill=tk.X)

        # Button to load data files
        self.load_button = tk.Button(menu_frame, text="Load Data Files (CSV/Excel)", command=self.load_data_files)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Toggle button for grid
        self.grid_var = tk.BooleanVar(value=True)
        self.grid_button = tk.Checkbutton(menu_frame, text="Show Grid", variable=self.grid_var)
        self.grid_button.pack(side=tk.LEFT, padx=5)

        # Toggle time normalization button
        self.Tnorm_var = tk.BooleanVar(value=True)
        self.Tnorm_button = tk.Checkbutton(menu_frame, text="Time Normalize", variable=self.Tnorm_var)
        self.Tnorm_button.pack(side=tk.LEFT, padx=5)


        # Status line at the bottom
        self.status_label = tk.Label(root, text="No file loaded", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Main content frame
        content_frame = tk.Frame(root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File name dropdown
        file_label = tk.Label(content_frame, text="Select File:")
        file_label.pack(pady=5)
        self.file_var = tk.StringVar(content_frame)
        self.file_var.set("No file selected")
        self.file_dropdown = tk.OptionMenu(content_frame, self.file_var, "No file selected")
        self.file_dropdown.pack(fill=tk.X, expand=True, padx=10)

        # Bind dropdown selection event to update the columns listbox
        self.file_var.trace("w", self.update_columns_listbox)

        # Search box
        search_label = tk.Label(content_frame, text="Search Columns:")
        search_label.pack(pady=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(content_frame, textvariable=self.search_var)
        search_entry.pack(pady=5, fill=tk.X)

        search_entry.bind("<KeyRelease>", self.search_columns)

        # Available columns listbox
        selection_label = tk.Label(content_frame, text="Available Columns:")
        selection_label.pack(pady=5)
        selection_frame = tk.Frame(content_frame)
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        scrollbar = tk.Scrollbar(selection_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(selection_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.listbox.yview)

        # Control buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add to Display", command=self.add_to_display)
        add_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(button_frame, text="Remove from Display", command=self.remove_from_display)
        remove_button.pack(side=tk.LEFT, padx=5)

        plot_button = tk.Button(button_frame, text="Plot Graph", command=self.plot_graph)
        plot_button.pack(side=tk.LEFT, padx=5)

        # Display listbox
        display_label = tk.Label(content_frame, text="Columns to Display:")
        display_label.pack(pady=5)
        self.display_listbox = tk.Listbox(content_frame, selectmode=tk.MULTIPLE)
        self.display_listbox.pack(fill=tk.BOTH, expand=True, padx=10)

        # Placeholder for data and selected columns
        self.data_files = {}  # Dictionary to store data for each file
        self.selected_columns = []  # Columns selected for display
        self.filtered_columns = []  # Columns filtered by search
        self.current_file = None  # Track the currently selected file

    def load_data_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv"),("Excel files", "*.xlsx;*.xls")])
        if file_paths:
            file_names = []
            for file_path in file_paths:
                try:
                    # Load the file into a DataFrame
                    if file_path.endswith(('.xlsx', '.xls')):
                        data = pd.read_excel(file_path)
                    elif file_path.endswith('.csv'):
                        data = pd.read_csv(file_path)

                    # Store the data and add the file to the dropdown
                    file_name = file_path.split("/")[-1]
                    self.data_files[file_name] = data
                    file_names.append(file_name)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load data file: {e}")

            # Update the status label with the number of files loaded
            self.status_label.config(text=f"Loaded {len(self.data_files)} files")

            # Update the dropdown menu with the loaded file names
            menu = self.file_dropdown["menu"]
            menu.delete(0, "end")
            for file_name in file_names:
                menu.add_command(label=file_name, command=tk._setit(self.file_var, file_name))

            # Set the dropdown to the first loaded file
            if file_names:
                self.file_var.set(file_names[0])

    def update_columns_listbox(self, *args):
        """Update the columns listbox when a file is selected from the dropdown."""
        selected_file = self.file_var.get()
        if selected_file != "No file selected":
            self.current_file = selected_file
            self.populate_listbox()

    def populate_listbox(self):
        """Populates the listbox with column names of the selected file."""
        self.listbox.delete(0, tk.END)
        if self.current_file:
            self.filtered_columns = list(self.data_files[self.current_file].columns)
            for i, column in enumerate(self.filtered_columns, start=1):
                self.listbox.insert(tk.END, f"{i}. {column}")

    def search_columns(self, event):
        """Highlights columns in the listbox that match the search query."""
        search_query = self.search_var.get().lower()
        self.listbox.delete(0, tk.END)
        if self.current_file:
            self.filtered_columns = [col for col in self.data_files[self.current_file].columns if search_query in col.lower()]
            for i, column in enumerate(self.filtered_columns, start=1):
                self.listbox.insert(tk.END, f"{i}. {column}")

    def add_to_display(self):
        """Add selected columns from the listbox to the display list with filename."""
        selected_indices = self.listbox.curselection()
        selected_columns = [self.filtered_columns[int(i)] for i in selected_indices]

        for column in selected_columns:
            display_item = f"{self.current_file}\\{column}"
            if display_item not in self.selected_columns:
                self.selected_columns.append(display_item)
                self.display_listbox.insert(tk.END, display_item)

    def remove_from_display(self):
        """Remove selected columns from the display list."""
        selected_indices = list(self.display_listbox.curselection())
        selected_indices.reverse()  # Reverse to avoid index shifting issues when deleting

        for index in selected_indices:
            display_item = self.display_listbox.get(index)
            self.selected_columns.remove(display_item)
            self.display_listbox.delete(index)

    def plot_graph(self):
        if not self.selected_columns:
            messagebox.showwarning("No Selection", "Please select at least one column to plot.")
            return

        # Open a new window for the graph
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Graph")
        graph_window.geometry("800x600")

        # Plot the selected columns
        self.plot_data(graph_window)

    def plot_data(self, graph_window):
        fig, ax = plt.subplots()


        for item in self.selected_columns:
            file_name, column = item.split("\\")

            if self.Tnorm_var.get() == True:
                dx_arr = np.linspace(0,1,len(self.data_files[file_name].index))
            else :
                dx_arr = self.data_files[file_name].index 
            ax.plot(dx_arr, self.data_files[file_name][column], label=item)

        ax.legend()
        ax.set_title("Data Plot")
        ax.set_xlabel("Index")
        ax.set_ylabel("Values")
        ax.grid(self.grid_var.get())  # Set grid based on the toggle button

        # Integrate the plot into the new window
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add the Matplotlib toolbar for zooming and panning
        toolbar = NavigationToolbar2Tk(canvas, graph_window)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Connect the motion event to display the tooltip
        fig.canvas.mpl_connect("motion_notify_event", lambda event: self.show_tooltip(event, graph_window))

        # Initialize a label for the tooltip
        self.tooltip_label = tk.Label(graph_window, text="", bg="lightyellow", relief=tk.SOLID, borderwidth=1)
        self.tooltip_label.pack_forget()  # Initially hide the tooltip

    def show_tooltip(self, event, graph_window):
        if event.inaxes:
            # Get the x and y data values
            x_val = event.xdata
            y_val = event.ydata

            # Update the tooltip text
            tooltip_text = f"x: {x_val:.2f}, y: {y_val:.2f}"
            self.tooltip_label.config(text=tooltip_text)

            # Position the tooltip near the

            x, y = graph_window.winfo_pointerxy()
            self.tooltip_label.place(x=x+10, y=y-10)
            self.tooltip_label.pack()

        else:
            # Hide the tooltip if the cursor is not over the plot
            self.tooltip_label.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlotterApp(root)
    root.mainloop()
