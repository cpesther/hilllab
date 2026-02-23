# Christopher Esther, Hill Lab, 2/23/2026
import tkinter as tk

class Tooltip:

    """
    A class used for displaying nice litte floating tooltips above 
    widgets. 
    """

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.move_tooltip)


    def show_tooltip(self, event=None):
        if self.tooltip or not self.text:
            return
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)  # remove window decorations
        self.tooltip.attributes("-topmost", True)

        label = tk.Label(self.tooltip, text=self.text, background="#b6d4db", relief='solid', 
                         borderwidth=1, wraplength=200, justify='left')
        label.pack(ipadx=5, ipady=2)

        self.move_tooltip(event)


    def move_tooltip(self, event):
        if self.tooltip:
            x = event.x_root + 10
            y = event.y_root + 10
            self.tooltip.wm_geometry(f"+{x}+{y}")


    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
