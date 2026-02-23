# Christopher Esther, Hill Lab, 2/23/2026
import tkinter as tk

class Popup:

    """
    Displays a popup window with either a warning, error, or informational
    message. 
    """

    COLORS = {
        'warning': 'orange',
        'error': 'red',
        'info': 'blue'
    }


    def __init__(self, message, type='info', title=None):
        
        """
        type: 'info', 'warning', 'error'
        title: Optional window title, defaults to capitalized type
        """

        self.message = message
        self.type = type.lower()
        self.title = title or self.type.capitalize()


    def show(self):

        # Create the window above any others
        window = tk.Toplevel()
        window.geometry('350x150')
        window.title(self.title)
        window.resizable(False, True)
        window.attributes('-topmost', True)

        # Small type text
        color = self.COLORS.get(self.type, 'blue')
        type_text = tk.Label(window, text=f'{self.type.upper()}', font=('Helvetica', 10, 'bold'), fg=color,
                         justify='left')
        type_text.pack(anchor='w', pady=(20, 0), padx=20)

        # Title
        title = tk.Label(window, text=f'{self.title}', font=('Helvetica', 12, 'bold'),
                         justify='left')
        title.pack(anchor='w', padx=20)
        
        # Message
        message = tk.Label(window, text=self.message, font=('Helvetica', 11), wraplength=310, justify='left')
        message.pack(anchor='w', padx=20)

        # OK button to close
        button = tk.Button(window, text='OK', command=window.destroy, width=10)
        button.pack(pady=(10,0), anchor='s', padx=20)
