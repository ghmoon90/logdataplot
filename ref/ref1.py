import tkinter as tk
import code
import numpy as np  # Ensure numpy is available to the console

class MyInteractiveConsole(code.InteractiveConsole):
    def __init__(self, locals=None):
        super().__init__(locals=locals)

    def push_command(self, command):
        """Execute a multiline command as if it were typed into the console."""
        try:
            # Using exec to execute the entire block of code
            exec(command, self.locals)
        except Exception as e:
            print(f"Error: {e}")

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter App")

        self.some_variable = "Hello, World!"

        # Create the interactive console
        self.console = MyInteractiveConsole(locals={"self": self, "np": np})

        # Buttons
        self.button_terminal = tk.Button(root, text="Open Terminal", command=self.open_terminal)
        self.button_terminal.pack(pady=10)

        self.button_send_command = tk.Button(root, text="Send Multiline Command", command=self.send_multiline_command)
        self.button_send_command.pack(pady=10)

    def open_terminal(self):
        # Automatically import numpy when the console opens
        self.console.push_command("import numpy as np")
        # Start an interactive console with the current local variables
        self.console.interact()

    def send_multiline_command(self):
        # Example of a multiline command
        multiline_command = """
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = a + b
print("Result:", c)
"""
        self.console.push_command(multiline_command)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
