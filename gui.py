import tkinter

class Tooltip:
    
    def __init__(self, parent, text="Tooltip text"):
        self.parent = parent
        self.text = text
        self.parent.bind("<Enter>", self.enter)
        self.parent.bind("<Leave>", self.leave)
        self.tooltip = None
    
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.parent.bbox("insert")
        x += self.parent.winfo_rootx() - 250
        y += self.parent.winfo_rooty() - 20
        # creates a toplevel window
        self.tooltip = tkinter.Toplevel(self.parent)
        # Leaves only the label and removes the app window
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tkinter.Label(self.tooltip, text=self.text, justify='left',
                       background='yellow', relief='solid', borderwidth=1)
        label.pack(ipadx=1)
        
    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
