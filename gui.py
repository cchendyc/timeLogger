# @ Cindy Chen xychencindy@gmail.com
# present on 12/24/2021
# Logging your reaction time
import tkinter as tk
from tkinter import font as tkFont

'''Loading Outside Sources'''
VERSION = 1.2
ASSETS_DIR = "assets/"
STRATEGY_SECONDS = 3
KEY_FILES = {
       'qs': ASSETS_DIR +  "questions.txt"
}

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

################
# Main Classes #
################
class Main(tk.Frame):
    LABEL_TEXT = [
        "Testing Testing Testing"
    ]
    def __init__(self, master):
        #preload
        tk.Frame.__init__(self, master)
        p1 = Mod(self)
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        # buttonframe.pack(side="top", fill="x", expand=False)
        # container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        # title, intro, canvas size
        self.master = master
        master.title("Time Logger GUI")
        master.geometry("1024x768+250+70")
        self.label_index = 0
        self.label_text = tk.StringVar()
        self.label_text.set(self.LABEL_TEXT[self.label_index])
        self.label = tk.Label(master, textvariable=self.label_text, font=('calibre', 50, 'bold'), justify = tk.CENTER)
        self.label.grid(row=6, column=1)

        # basic features
        name_var= tk.StringVar()

        level_label = tk.Label(master, text = 'Current Language Level:', font=('calibre', 20, 'bold'))
        level_choices = ['N5', 'N4', 'N3', 'N2', 'N1']
        level_var = tk.StringVar(master)
        level_var.set('N3')
        level_item = tk.OptionMenu(master, level_var, *level_choices)
        # helv36 = tkFont.Font(family='Helvetica', size=36)
        # level_item.config(font=helv36)
        #
        # helv20 = tkFont.Font(family='Helvetica', size=20)
        # menu = master.nametowidget(level_item.menuname)
        # menu.config(font=helv20)  # Set the dropdown menu's font
        # level_item.grid(row=0, column=0, sticky='nsew')

        passw_var=tk.StringVar()
        # creating a label for
        # name using widget Label
        name_label = tk.Label(master, text = 'Please Enter Your Name: ', font=('calibre',20, 'bold'))
        name_entry = tk.Entry(master, textvariable = name_var, font=('calibre',30,'normal'))
        # creating a label for password
        passw_label = tk.Label(master, text = 'Password', font=('calibre', 20, 'bold'))

        # creating a entry for password
        passw_entry=tk.Entry(master, textvariable = passw_var, font = ('calibre',10,'normal'), show = '*')

        # creating a button using the widget
        # Button that will call the submit function
        sub_btn=tk.Button(master,text = 'Submit', command = self.submit)
        # mod_btn = tk.Button()
        mod_btn=tk.Button(master,text = 'Administrator Login', command=p1.show)
        p1.show()

        # placing the label and entry in
        # the required position using grid
        # method
        name_label.grid(row=7,column=0)
        name_entry.grid(row=7,column=1)
        passw_label.grid(row=8,column=0)
        passw_entry.grid(row=8,column=1)
        level_label.grid(row=9,column=0)
        level_item.grid(row=9,column=1, sticky='nsew')
        sub_btn.grid(row=10,column=1)
        mod_btn.grid(row=11,column=1)
        # L1.pack(side = LEFT)
        # E1 = Entry(master, bd =5)
        # E1.pack(side = RIGHT)
        entry_text = ['e1', 'e2', 'e3']

        # add text entries
        # for x, text in enumerate(entry_text):
        #     e = tkinter.Entry(mFrame, width=80, name=text)
        #     e.grid(column=1, row=x, sticky='WE', padx=5, pady=5)
        #     e.insert(0, text)

    def start(self):
        print("Welcome!")

    # def cycle_label_text(self, event):
    #     self.label_index += 1
    #     self.label_index %= len(self.LABEL_TEXT) # wrap around
    #     self.label_text.set(self.LABEL_TEXT[self.label_index])
    def submit(self):
        name=name_var.get()
        password=passw_var.get()

        print("The name is : " + name)
        print("The password is : " + password)

        name_var.set("")
        passw_var.set("")

    def mod(self):

        return
    def get_questions(self, name):
        return KEY_FILES[name]


#mod page
class Mod(Page):
    def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 1")
       label.pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = Main(root)
    root.mainloop()
