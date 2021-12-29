"""The simple yet messy graphics module that does everything"""
#present by @Cindy Chen 12/24/2021
#xychencindy@gmail.com

import sys
import math
import shutil
import os
import time
from datetime import datetime
from pandas import DataFrame

try:
    import tkinter
except Exception as e:
    print('Could not load tkinter: ' + str(e))

import tkinter.font as fnt
from tkinter import ttk


IMG_FILES = {'rec': 'assets/img/rec_label.jpeg',
            'rd': 'assets/img/rd_label.png',
            'main_logo': 'assets/img/logo.png',
            'footer':'assets/img/logo_footer.png'
            }

class Participant:
    def __init__(self, name, level, time_in_jp):
        self.name = name
        self.level = level
        self.time_in_jp = time_in_jp
        self.time = datetime.now()


class Canvas(object):

    """A Canvas object supports drawing and animation primitives.
    Largely inspired by the Ants project constructed by UC Berkeley CS61A.
    """
    _instance = None

    def __init__(self, a, q, elst, width=1024, height=768, title='', color='White', tk=None):
        # Singleton enforcement
        if Canvas._instance is not None:
            raise Exception('Only one canvas can be instantiated.')
        Canvas._instance = self

        # Attributes
        self.color = color
        self.width = width
        self.height = height
        self.del_lst = []
        self._participant = None
        # Root window
        self._tk = tk or tkinter.Tk()
        self._tk.protocol('WM_DELETE_WINDOW', sys.exit)
        self._tk.title(title or 'Graphics Window')
        self._tk.bind('<Button-1>', self._click)
        self._click_pos = None

        # Canvas object
        self._canvas = tkinter.Canvas(self._tk, width=width, height=height)
        # self._tk.attributes('-fullscreen', True)
        self._tk.resizable(False, False)
        self._canvas.pack()
        self._draw_background()
        self._canvas.update()
        self._images = dict()
        # self._tk.mainloop()
        self.MAX = len(q.keys())
        self._ans = a
        self._quests = q
        self._elst = elst
        self._keys = list(q.keys())
        self._curr = iter(self._keys)
        self.next = 0
        self._time_report = {}
        # self.start()
        self.main_menu()
        self._tk.mainloop()
        self._canvas.mainloop()

    def main_menu(self):
        self.clear()
        rec = rectangle_points((0,0),1024,100)
        self.draw_polygon(rec,fill_color="#004074")
        self.draw_image((30,20),image_file=IMG_FILES['footer'], scale=0.3)
        self.draw_real_text('応用言語学研究科',(200, 40),color='White', size=25, style='bold')
        self.draw_real_text('Graduate School of Applied Linguistics',(200, 73),color='White', size=13, style='normal')
        self.draw_line((180,30), (180,80), color='White', width=2)

        self.start_text = self.draw_real_text('Welcome to this test, nothing is happening, \n' +
        "Please follow the instruction below:\n"
        , (50, 150), size=30, style='bold')
        self.inst_text = self.draw_real_text('1. xxxxxxxxx \n' +
        "2. xxxxxxxxx, xxxxxxxxxxx\n" +
        "3. xxxx, xxx, xxxxxx"
        , (50, 250), size=20)

        self.start_btn = self.draw_survey_button((400, 350), "       Start       ")
        self.end_btn = self.draw_end_button((400, 430),   "        End        ")
        self.mod_btn = self.draw_mod_button((400, 570),   'Administrator Login')

    def clear(self, shape='all'):
        """Clear all shapes, text, and images."""
        self._canvas.delete(shape)
        if shape == 'all':
            self._draw_background()
        for widget in self._canvas.winfo_children():
            widget.destroy()
        self._canvas.update()

    def kill(self):
        self._tk.destroy()

    def draw_polygon(self, points, color='Black', fill_color=None, filled=1, smooth=0, width=1):
        """Draw a polygon and return its tkinter id.

        points -- a list of (x, y) pairs encoding pixel positions
        """
        if fill_color == None:
            fill_color = color
        if filled == 0:
            fill_color = ""
        return self._canvas.create_polygon(flattened(points), outline=color, fill=fill_color,
                smooth=smooth, width=width)

    def draw_circle(self, center, radius, color='Black', fill_color=None, filled=1, width=1):
        """Draw a cirlce and return its tkinter id.

        center -- an (x, y) pair encoding a pixel position
        """
        if fill_color == None:
            fill_color = color
        if filled == 0:
            fill_color = ""
        x0, y0 = [c - radius for c in center]
        x1, y1 = [c + radius for c in center]
        return self._canvas.create_oval(x0, y0, x1, y1, outline=color, fill=fill_color, width=width)

    def draw_line(self, start, end, color='Blue', width=1):
        """Draw a line and return its tkinter id.

        start, end -- (x, y) pairs encoding a pixel position
        """
        x0, y0 = start
        x1, y1 = end
        return self._canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    def draw_image(self, pos, image_file=None, scale=1, anchor=tkinter.NW, behind=0):
        """Draw an image from a file and return its tkinter id."""
        key = (image_file, scale)
        if key not in self._images:
            image = tkinter.PhotoImage(file=image_file)
            if scale >= 1:
                image = image.zoom(int(scale))
            else:
                image = image.subsample(int(1/scale))
            self._images[key] = image

        image = self._images[key]
        x, y = pos
        id = self._canvas.create_image(x, y, image=image, anchor=anchor)
        if behind > 0:
            self._canvas.tag_lower(id, behind)
        return id

    def end_page(self):
        """clear all widgets and kill the root"""
        self.clear()

        ####report generating... ...
        diffs = []
        report_keys = list(self._time_report.keys())
        logs = []

        if len(self._time_report.keys()) > 1:
            for i in range (1,len(self._time_report)):
                start = report_keys[i-1]
                end = report_keys[i]
                diff = end - start
                diff_in_secs = diff.total_seconds()
                qnum, choice = self._time_report[end]

                diffs.append("Question " + str(qnum) + ":-------------------\n" +
                            "start:     " + str(start) + "\n" +
                            "end:       " + str(end) + "\n" +
                            "duration:  " + str(diff_in_secs) + " seconds\n" +
                            "selection: " + str(choice) + "\n")
                logs.append(str(diff_in_secs) + "\n")

            diffs.insert(0, "\n----------------report for " + str(self._participant.name) + "----------------\n" +
                        'name: ' + str(self._participant.name) +"\n" +
                        'level: ' + str(self._participant.level) +"\n" +
                        'years in Japan: ' + str(self._participant.time_in_jp)+ "\n\n"
                        )

            diffs.append("\n")

            logs.insert(0, str(self._participant.time_in_jp)+"\n")
            logs.insert(0, str(self._participant.level)+"\n")
            logs.insert(0, str(self._participant.name)+"\n")
            #maybe a unique id?

            with open("reports/"+str(self._participant.name)+"_"+str(self._participant.time)[:-7]+".txt", 'a+') as report:
                report.writelines(diffs)

            with open("logs/"+str(self._participant.name)+"_.txt", 'a+') as log:
                log.writelines(logs)

        self.draw_real_text("this is the end.", (100, 200), size=30, style='bold')
        self._sleep(2)
        self.kill()
        return

    def next_item(self, txt_pair, pa=None):
        """
        update both the question and the answers,
        end if there's no more question
        """
        ##paticipants create
        if not self._participant and pa:
            name = pa[0].get()
            level = pa[1].get()
            time = pa[2].get()
            self._participant = Participant(name, level, time)

        self.clear()
        curr_time = datetime.now()

        self._time_report[curr_time] = txt_pair
        curr = next(self._curr, None)

        if not curr:
            self.end_page()
            return

        self.draw_text(curr, (100, 200), size=30, style='bold')

        startrow = 100
        startcol = 350
        for ans in self._ans[curr]:
            self.draw_start_button((startrow, startcol), [curr, ans])
            startcol += 80

    def survey_canvas(self):
        self.clear()
        LABEL_TEXT = ["Testing Testing Testing"]
        label_index = 0

        surv_label_text = tkinter.StringVar()
        surv_label_text.set(LABEL_TEXT[label_index])
        surv_label = tkinter.Label(self._canvas, textvariable=surv_label_text, font=('calibre', 30, 'bold'), justify = tkinter.CENTER)
        surv_label.place(x=350, y=50)

        # basic features
        ## name
        name_var = tkinter.StringVar()
        name_label = tkinter.Label(self._canvas, text = 'Please Enter Your Name: ', font=('calibre',20, 'bold'))
        name_entry = tkinter.Entry(self._canvas, textvariable = name_var, font=('calibre',30,'normal'), width=25)
        name_label.place(x=100, y=210)
        name_entry.place(x=350, y=200)

        ## level
        level_label = tkinter.Label(self._canvas, text = 'Current Language Level:', font=('calibre', 20, 'bold'))
        level_var = tkinter.StringVar()
        level_var.set('N5')

        self._canvas.option_add("*TCombobox*Listbox*Background", 'white')
        style = ttk.Style()
        style.theme_use('clam')

        helv36 = fnt.Font(family='Helvetica', size=20, weight= fnt.BOLD)
        level_item = ttk.Combobox(self._canvas, font=helv36,textvariable=level_var, width=25, background="White")
        level_item['values'] = ('N5', 'N4', 'N3', 'N2', 'N1')
        level_label.place(x=100, y=300)
        level_item.place(x=350, y=300)

        ## year in jp
        yr_var = tkinter.StringVar()
        yr_label = tkinter.Label(self._canvas, text = 'Years in Japan: ', font=('calibre',20, 'bold'))
        yr_entry = tkinter.Entry(self._canvas, textvariable = yr_var, font=('calibre',30,'normal'), width=20)
        yr_label.place(x=185, y=390)
        yr_entry.place(x=350, y=380)

        # Start button
        self.start_btn = self.draw_start_button((400, 500), "       Start       ", pa=[name_entry, level_item, yr_entry])

        back_btn = tkinter.Button(self._canvas, text="back", width=24, height=4, bd='2', command=self.main_menu)
        self._tk.bind('<Return>', self.main_menu)
        back_btn.place(x=400, y=600)
        return

    def draw_survey_button(self, pos, txt, color='Black', font='Arial', size=12, style='normal', anchor=tkinter.NW):
        btn = tkinter.Button(self._canvas,bg="Black", text=txt, width=int(len(txt)+5), height=4, bd='10', command=self.survey_canvas)
        # self._tk.bind('<Return>', self.survey_canvas)
        xb, yb = pos
        return btn.place(x=xb, y=yb)

    def draw_start_button(self, pos, txt_pair, pa=None, color='Black', font='Arial', size=12, style='normal', anchor=tkinter.NW):
        """the start button, click to start answering """
        txt = None
        q_num = None
        if type(txt_pair) == list:
            q_num = txt_pair[0]
            txt = txt_pair[1]
        else:
            txt = txt_pair

        btn = tkinter.Button(self._canvas, text=txt, width=int(len(txt)+5), height=4, bd='10', command=lambda name=txt_pair, pa=pa: self.next_item(name,pa))
        self._tk.bind('<Return>', lambda event, name=txt_pair, pa=pa: self.next_item(name,pa))
        xb, yb = pos
        return btn.place(x=xb, y=yb)

    def draw_end_button(self, pos, txt, color='Black', font='Arial', size=12, style='normal', anchor=tkinter.NW):
        """the end button, click to end"""
        btn = tkinter.Button(self._canvas, text=txt, width=int(len(txt)+5), height=4, bd='10', command=self.end_page)
        self._tk.bind('<Return>', self.end_page)
        xb, yb = pos
        return btn.place(x=xb, y=yb)

###############
# MOD - Check #
##############
    def on_configure(self, event):
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))

    def mod_check(self):
        # self.clear()
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        root = tkinter.Tk()
        root.title("Mod Check blahblah")
        h=10000
        m=500
        # --- create canvas with scrollbar ---
        canvas = tkinter.Canvas(root, width=600,height=700,bg='white',scrollregion=[0,0,500,h])
        canvas.pack(side=tkinter.LEFT)
        scrollbar = tkinter.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        canvas.configure(yscrollcommand = scrollbar.set)

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.bind('<Configure>', on_configure)

        # --- put frame in canvas ---
        frame = tkinter.Frame(canvas)
        canvas.create_window((0,0), window=frame, anchor='nw')

        # --- add widgets in frame ---

        for i in self._quests.keys():
            l = tkinter.Label(frame, text=str(i)+". "+str(self._quests[i]), font=('calibre',15, 'bold'))
            l.pack(side=tkinter.TOP, anchor='nw')
            for j in self._ans[i]:
                ll = tkinter.Label(frame, text=j)
                ll.pack(side=tkinter.TOP, anchor='n')
        root.mainloop()
        return

################
# MOD - Delete #
################
    def draw_info_button(self, pos, txt, del_num, color='Black', font='Helvetica', size=10, style='bold', anchor=tkinter.NW):
        """provide detailed info about the deleting item"""
        btn = tkinter.Button(self._canvas, text=txt, width=int(len(txt)+5), height=3, bd='10', command=lambda d=del_num: self.del_confirm(d))
        self._tk.bind('<Return>', lambda event, d=del_num: self.del_confirm(d))
        xb, yb = pos
        btn.place(x=xb, y=yb)
        return

    def del_confirm(self, del_num):
        for i in self.del_lst:
            i.destroy()

        num = del_num.get()
        if not num.isnumeric():
            k = tkinter.Label(self._canvas, text="Your entry is invalid: [Non-numerical], please try again", font=('calibre', 10, 'bold'))
            k.place(x=300, y=150)
            k.after(2000, lambda: k.destroy())
            self.del_lst.append(k)
            return

        num = int(num)
        if num <= 0 or num > self.MAX + len(self._elst):
            k = tkinter.Label(self._canvas, text="Your entry is invalid: [Out-of-scope], please try again", font=('calibre', 10, 'bold'))
            k.place(x=300, y=150)
            k.after(2000, lambda: k.destroy())
            self.del_lst.append(k)
            return
        if num in self._elst:
            k = tkinter.Label(self._canvas, text="Your entry is invalid: [Nothing-in-q" + str(num)+"], please try again", font=('calibre', 10, 'bold'))
            k.place(x=300, y=150)
            k.after(2000, lambda: k.destroy())
            self.del_lst.append(k)
            return

        l = tkinter.Label(self._canvas, text=str(num)+". "+str(self._quests[num]), font=('calibre',15, 'bold'))
        self.del_lst.append(l)
        l.place(x=300, y=200)
        lly = 250
        for j in self._ans[num]:
            ll = tkinter.Label(self._canvas, text=j, font=('calibre',13, 'bold'))
            self.del_lst.append(ll)
            ll.place(x=300, y=lly)
            lly += 50

        del_btn = self.draw_del_button((400, 500), "Looking Good, Delete!", num)
        return

    def draw_del_button(self, pos, txt, num, color='Black', font='Helvetica', size=10, style='bold', anchor=tkinter.NW):
        btn = tkinter.Button(self._canvas, text=txt, width=int(len(txt)+5), height=3, bd='10', command=lambda d=num: self.del_item(d))
        self._tk.bind('<Return>', lambda event, d=num: self.del_item(d))
        xb, yb = pos
        btn.place(x=xb, y=yb)
        return

    def del_item(self, num):
        if num in self._elst or num <= 0 or num > self.MAX + len(self._elst):
            return
        #delete directory
        k = tkinter.Label(self._canvas, text="Succeed!", font=('calibre', 10, 'bold'))
        k.place(x=300, y=150)
        k.after(2000, lambda: k.destroy())

        del self._ans[num]
        del self._quests[num]
        self._elst.append(num)
        self.MAX = len(self._ans.keys())
        print(self._ans, self._quests, self._elst, self.MAX)
        #delete stuff in a file
        del_path_a = "a/a"+str(num)+".txt"
        del_path_q = "q/q"+str(num)+".txt"

        file = open(del_path_a,"r+")
        file.truncate(0)
        file.close()

        file = open(del_path_q,"r+")
        file.truncate(0)
        file.close()

        os.rename(del_path_a, "a/ea"+str(num)+".txt")
        os.rename(del_path_q, "q/eq"+str(num)+".txt")

        # os.remove(del_path_a)
        # os.remove(del_path_q)
        return

    def mod_delete(self):
        self.clear()
        del_var = tkinter.StringVar()
        del_label = self.draw_real_text("Enter the question# you want to del: ", (100, 50), size=30, style='bold')
        del_entry = tkinter.Entry(self._canvas, textvariable = del_var, font=('calibre',30,'normal'))
        del_entry.place(x=300, y=100)
        confirm_btn = self.draw_info_button((700, 100), "Confirm", del_entry)

        back_btn = tkinter.Button(self._canvas, text="back", width=15, height=3, bd='2', command=self.mod)
        self._tk.bind('<Return>', self.mod)
        back_btn.place(x=400, y=600)
        self._canvas.update()
        return

#############
# MOD - Add #
#############
    def draw_constr_button(self, pos, txt, add_num, color='Black', font='Helvetica', size=10, style='bold', anchor=tkinter.NW):
        """provide detailed info about the deleting item"""
        btn = tkinter.Button(self._canvas, text=txt, width=int(len(txt)+5), height=3, bd='10', command=lambda a=add_num: self.add_confirm(a))
        self._tk.bind('<Return>', lambda event, a=add_num: self.add_confirm(a))
        xb, yb = pos
        btn.place(x=xb, y=yb)
        return

    def add_confirm(self, add_num):
        entry, add_question_label, add_answer_label1, add_answer_label2, add_answer_label3, q_num = add_num
        num = entry.get()

        if not num.isnumeric():
            add_question_label.config(text="")
            add_answer_label1.config(text="")
            add_answer_label2.config(text="")
            add_answer_label3.config(text="")
            self._canvas.update()
            k = tkinter.Label(self._canvas, text="Your entry is invalid: [Non-numerical], please try again", font=('calibre', 10, 'bold'))
            k.place(x=330, y=280)
            k.after(2000, lambda: k.destroy())
            return

        num = int(num)

        if num not in self._elst and (num <= self.MAX + len(self._elst) or num == 0):
            add_question_label.config(text="")
            add_answer_label1.config(text="")
            add_answer_label2.config(text="")
            add_answer_label3.config(text="")
            self._canvas.update()

            k = tkinter.Label(self._canvas, text="Your entry is invalid: [Space-occupied], please try again", font=('calibre', 10, 'bold'))
            k.place(x=330, y=280)
            k.after(2000, lambda: k.destroy())
            return

        # add_question_label = self.draw_real_text("Enter Question "+ str(num) + " :", (100, 315), size=15, style='normal')
        add_question_label.config(text="New Question: ")
        add_question_var = tkinter.StringVar()
        add_question_entry = tkinter.Entry(self._canvas, textvariable = add_question_var, font=('calibre', 32 ,'normal'), width=38)
        add_question_entry.place(x=220, y=300)

        #answers
        # add_answer_label1 = self.draw_real_text("Enter Answer 1: ", (100, 400), size=15, style='normal')
        add_answer_label1.config(text="Enter Answer 1: ")
        add_question_var1 = tkinter.StringVar()
        add_question_entry1 = tkinter.Entry(self._canvas, textvariable = add_question_var1, font=('calibre', 30 ,'normal'), width= 37)
        add_question_entry1.place(x=230, y=390)

        # add_answer_label2 = self.draw_real_text("Enter Answer 2: ", (100, 460), size=15, style='normal')
        add_answer_label2.config(text="Enter Answer 2: ")
        add_question_var2 = tkinter.StringVar()
        add_question_entry2 = tkinter.Entry(self._canvas, textvariable = add_question_var2, font=('calibre', 30 ,'normal'), width= 37)
        add_question_entry2.place(x=230, y=450)

        # add_answer_label3 = self.draw_real_text("Enter Answer 3: ", (100, 520), size=15, style='normal')
        add_answer_label3.config(text="Enter Answer 3: ")
        add_question_var3 = tkinter.StringVar()
        add_question_entry3 = tkinter.Entry(self._canvas, textvariable = add_question_var3, font=('calibre', 30 ,'normal'), width= 37)
        add_question_entry3.place(x=230, y=510)

        add_btn = self.draw_add_button((400, 600), "Looking Good, Add!", [add_question_entry, add_question_entry1,
        add_question_entry2, add_question_entry3, q_num])
        return

    def draw_add_button(self, pos, txt, entry_lst, color='Black', font='Helvetica', size=10, style='bold', anchor=tkinter.NW):
        btn = tkinter.Button(self._canvas, text=txt, width=int(len(txt)+5), height=3, bd='10', command=lambda a=entry_lst: self.add_item(a))
        self._tk.bind('<Return>', lambda event, a=entry_lst: self.add_item(a))
        xb, yb = pos
        btn.place(x=xb, y=yb)
        return

    def add_item(self, entry_lst):
        eq, e1, e2, e3, q_num = entry_lst
        eq = eq.get()
        e1 = e1.get()
        e2 = e2.get()
        e3 = e3.get()
        q_num = int(q_num.get())
        print(eq, e1, e2, e3, q_num)

        if not eq:
            k = tkinter.Label(self._canvas, text="Your question is empty, please put something in.", font=('calibre', 10, 'bold'))
            k.place(x=400, y=560)
            k.after(1000, lambda: k.destroy())
            return
        if q_num not in self._elst and q_num <= self.MAX + len(self._elst):
            k = tkinter.Label(self._canvas, text="You just added it, please no duplicates", font=('calibre', 10, 'bold'))
            k.place(x=400, y=560)
            k.after(1000, lambda: k.destroy())
            return
        k = tkinter.Label(self._canvas, text="Succeed!", font=('calibre', 10, 'bold'))
        k.place(x=400, y=560)
        k.after(1000, lambda: k.destroy())
        new_ans = [str(e1) + "\n", str(e2)+"\n", str(e3)]
        self._ans[q_num] = new_ans
        self._quests[q_num] = str(eq)

        self.MAX += 1
        counter = q_num-1
        while q_num > self.MAX + len(self._elst):
            self._elst.append(counter)
            if counter not in self._quests.keys():
                open("a/ea"+str(counter)+".txt", 'a').close()
                open("q/eq"+str(counter)+".txt", "a").close()
            counter -= 1

        if q_num in self._elst:
            self._elst.remove(q_num)

        #add to files
        add_path_a = "a/ea"+str(q_num)+".txt"
        add_path_q = "q/eq"+str(q_num)+".txt"

        with open(add_path_q,"w+") as file:
            file.write(str(eq))
            file.close()

        with open(add_path_a,"w+") as file:
            file.writelines(new_ans)
            file.close()

        os.rename(add_path_a, "a/a"+str(q_num)+".txt")
        os.rename(add_path_q, "q/q"+str(q_num)+".txt")
        return

    def mod_add(self):
        self.clear()
        if self._elst:
            elst_label = self.draw_real_text("Questions below are still empty: ", (100, 50), size=20, style='bold')
            estr = ""
            for i in self._elst:
                estr += "q" + str(i) + ", "
            self.draw_real_text(estr[:-2], (100, 100), size=20, style='normal')

        elst_label = self.draw_real_text("Your largest existing question# is: "
        + str(self.MAX + len(self._elst)), (100, 150), size=20, style='bold')

        add_label = self.draw_real_text("Enter the question# you want to add: ", (100, 200), size=20, style='bold')
        add_label = self.draw_real_text("It should still be empty or > "+ str(self.MAX + len(self._elst)), (100, 245), size=15, style='normal')
        add_var = tkinter.StringVar()

        add_question_label = tkinter.Label(self._canvas,text="", font=('calibre', 15, 'normal'))
        add_answer_label1 = tkinter.Label(self._canvas,text="", font=('calibre', 15, 'normal'))
        add_answer_label2 = tkinter.Label(self._canvas,text="", font=('calibre', 15, 'normal'))
        add_answer_label3 = tkinter.Label(self._canvas,text="", font=('calibre', 15, 'normal'))

        add_question_label.place(x=100, y=315)
        add_answer_label1.place(x=100, y=400)
        add_answer_label2.place(x=100, y=460)
        add_answer_label3.place(x=100, y=520)

        add_entry = tkinter.Entry(self._canvas, textvariable = add_var, font=('calibre',30,'normal'))
        add_entry.place(x=330, y=230)
        confirm_btn = self.draw_constr_button((750, 230), "Confirm", [add_entry, add_question_label,
        add_answer_label1, add_answer_label2, add_answer_label3, add_entry])

        back_btn = tkinter.Button(self._canvas, text="back", width=15, height=3, bd='2', command=self.mod)
        self._tk.bind('<Return>', self.mod)
        back_btn.place(x=400, y=700)
        self._canvas.update()
        return

##############
# MOD - Edit #
##############
    def edit_btn(self, num):
        window = tkinter.Tk()
        window.title("Mod Editor")

        canvas = tkinter.Canvas(window, width=1000,height=1000,bg='white')
        canvas.pack()

        frame = tkinter.Frame(canvas)
        # canvas.create_window((0,0), window=frame, anchor='nw')
        def create_edit(num):
            edit_var_q = tkinter.StringVar(canvas, value=str(self._quests[num]))
            q_entry = tkinter.Entry(canvas, textvariable = edit_var_q, font=('calibre',30,'bold'), width=35)
            q_label = tkinter.Label(canvas, text="You're editing question " + str(num) + ": ", font=('calibre', 20, 'bold'))
            q_confirm_btn = tkinter.Button(canvas, text="save", width=10, height=3, bd='2', command=lambda a=num, b=q_entry, c=0: self.edit(a,b,c))
            window.bind('<Return>', lambda event, a=num, b=q_entry, c=1: self.edit(a,b,c))
            q_confirm_btn.place(x=820, y=200)

            q_label.place(x=100, y=100)
            q_entry.place(x=100, y=200)
            # --- add widgets in frame ---
            # l = tkinter.Entry(frame, text=str(num)+". "+str(self._quests[num]), font=('calibre',15, 'bold'))
            # l.pack(side=tkinter.TOP, anchor='nw')
            startx = 100
            starty = 300
            for i in self._ans[num]:
                avar = tkinter.StringVar(canvas, value=i.strip())
                a_entry = tkinter.Entry(canvas, textvariable = avar, font=('calibre',20,'normal'), width=20)
                confirm_btn = tkinter.Button(canvas, text="save", width=10, height=2, bd='2', command=lambda a=num, b=a_entry, c=1, d=i: self.edit(a,b,c,d))
                window.bind('<Return>', lambda event, a=num, b=a_entry, c=1: self.edit(a,b,c))
                confirm_btn.place(x=startx+280, y=starty)
                a_entry.place(x=startx, y=starty)
                starty+=70

        create_edit(num)
        back_btn = tkinter.Button(canvas, text="restart", width=15, height=3, bd='2', command= lambda a=num: create_edit(a))
        back_btn.place(x=100, y=600)
        window.mainloop()
        return
    def edit(self, q_num, entry, i, d=None):
        if i==0:
            new_q = entry.get()
            print(new_q)
            self._quests[q_num] = new_q
            with open('q/q'+str(q_num)+'.txt', "w") as f:
                f.write(new_q)
            f.close()
        else:
            new_a = entry.get()
            print(new_a)
            index = int(d[0])
            self._ans[q_num][index-1] = new_a
            print(self._ans[q_num])
            new_ans = []

            for j in self._ans[q_num]:
                new_ans.append(j+"\n")
            with open('a/a'+str(q_num)+'.txt', "w") as f:
                f.writelines(new_ans)
            f.close()

        return
    def mod_edit(self):
        self.clear()
        startx = 30
        starty = 50
        for i in self._quests.keys():
            back_btn = tkinter.Button(self._canvas, text=str(i), width=5, height=3, bd='2', command=lambda a=i: self.edit_btn(a))
            self._tk.bind('<Return>', lambda event, a=i: self.edit_btn(a))
            back_btn.place(x=startx, y=starty)
            startx += 50
            if startx >= 980:
                startx = 30
                starty += 50

        back_btn = tkinter.Button(self._canvas, text="back", width=15, height=3, bd='2', command=self.mod)
        self._tk.bind('<Return>', self.mod)
        back_btn.place(x=400, y=700)
        self._canvas.update()
        return

##############
# MOD - Data #
##############
    def export(self):
        print("aha")
        log_path = os.listdir("logs")
        frame_dict = {}
        final = 0
        for log in sorted(log_path):
            if log.endswith(".txt"):
                count = 0
                with open("logs/" + log, 'r') as f:
                    name = ""
                    col = []
                    for line in f:
                        if count == 0:
                            name += str(line).strip()
                        elif count == 1:
                            name += "(" + str(line).strip()
                        elif count == 2:
                            name += ", " + str(line).strip()+")"
                        else:
                            col.append(line)
                        count += 1
                    frame_dict[name]=col
                    print(name)
                    if final == 0:
                        final = count - 2

        export_data = DataFrame(frame_dict)
        export_data.index+=1
        export_data.to_excel('dataset.xlsx', sheet_name='overall')
        return

    def mod_data(self):
        self.clear()
        excel_btn = tkinter.Button(self._canvas, text="Export to Excel", width=20, height=4, bd='2', command=self.export)
        self._tk.bind('<Return>', self.export)
        excel_btn.place(x=400, y=200)

        back_btn = tkinter.Button(self._canvas, text="back", width=15, height=3, bd='2', command=self.mod)
        self._tk.bind('<Return>', self.mod)
        back_btn.place(x=400, y=700)
        return

##############
# MOD - MAIN #
##############
    def mod(self):
        """
        the moderator button, click to change:
        check           : existing questions
        delete          : existing questions
        add             : new questions
        edit            : existing questions
        data additionals: export/visualization/analysis
        """
        self.clear()
        self.draw_real_text("Hey Mod, how's your day :`)", (400, 70), size=30, style='bold')
        self.draw_real_text("Here's a Summary of your stats: \n", (400, 150), size=20, style='normal')
        self.draw_real_text("Total questions: " + str(self.MAX), (400, 200), size=15, style='normal')
        self.draw_real_text("Participant count: " + str(0), (400, 240), size=15, style='normal')

        check_btn = tkinter.Button(self._canvas, text="Check", width=30, height=3, bd='1', command=self.mod_check)

        del_btn = tkinter.Button(self._canvas, text="Delete", width=30, height=3, bd='1', command=self.mod_delete)
        self._tk.bind('<Return>', self.mod_delete)

        add_btn = tkinter.Button(self._canvas, text="Add", width=30, height=3, bd='1', command=self.mod_add)
        self._tk.bind('<Return>', self.mod_add)

        edit_btn = tkinter.Button(self._canvas, text="Edit", width=30, height=3, bd='1', command=self.mod_edit)
        self._tk.bind('<Return>', self.mod_edit)

        data_btn = tkinter.Button(self._canvas, text="Data", width=30, height=3, bd='1', command=self.mod_data)
        self._tk.bind('<Return>', self.mod_data)

        back_btn = tkinter.Button(self._canvas, text="back", width=20, height=3, bd='2', command=self.main_menu)
        self._tk.bind('<Return>', self.main_menu)

        rec = rectangle_points((0,0),300,768)
        self.draw_polygon(rec,fill_color="#004074")

        self.draw_circle((150,120), 60, color='White', fill_color="White", filled=1, width=1)
        self.draw_image((105,75), image_file=IMG_FILES['rd'], scale=0.5)

        check_btn.place(x=0, y=350)
        del_btn.place(x=0, y=410)
        add_btn.place(x=0, y=470)
        edit_btn.place(x=0, y=530)
        data_btn.place(x=0, y=590)
        back_btn.place(x=500, y=400)

        return

    def draw_mod_button(self, pos, txt, color='Black', font='Helvetica', size=10, style='bold', anchor=tkinter.NW):
        helv36 = fnt.Font(family=font, size=size, weight= fnt.BOLD)
        btn = tkinter.Button(self._canvas, text=txt, width=int(len(txt)+17),
             height=3, bd='1', command=self.mod, font=helv36)
        xb, yb = pos
        return btn.place(x=xb, y=yb)

    def draw_real_text(self, text, pos, color='Black', font='Arial', size=12, style='normal', anchor=tkinter.NW):

        """
        Draw real [text] and return its tkinter id.
        """
        x, y = pos
        font = (font, str(size), style)
        return self._canvas.create_text(x, y, fill=color, text=text, font=font, anchor=anchor)

    def draw_text(self, i, pos, color='Black', font='Arial', size=12, style='normal', anchor=tkinter.NW):

        """
        For drawing questions only.
        Draw text given [index] and return its tkinter id.
        """
        x, y = pos
        font = (font, str(size), style)
        return self._canvas.create_text(x, y, fill=color, text=str(self._quests[i]), font=font, anchor=anchor)


#########
# Later #
#########
    def edit_text(self, id, text=None, color=None, font=None, size=12, style='normal'):

        """Edit the text, color, or font of an existing text object."""
        if color is not None:
            self._canvas.itemconfigure(id, fill=color)
        if text is not None:
            self._canvas.itemconfigure(id, text=text)
        if font is not None:
            self._canvas.itemconfigure(id, font=(font, str(size), style))

    def animate_shape(self, id, duration, points_fn, frame_count=0):
        """Animate an existing shape over points."""
        max_frames = duration // FRAME_TIME
        points = points_fn(frame_count)
        self._canvas.coords(id, flattened(points))
        if frame_count < max_frames:
            def tail():
                """Continues the animation at the next frame."""
                self.animate_shape(id, duration, points_fn, frame_count + 1)
            self._tk.after(int(FRAME_TIME * 1000), tail)

    def slide_shape(self, id, end_pos, duration, elapsed=0):
        """Slide an existing shape to end_pos."""
        points = paired(self._canvas.coords(id))
        start_pos = points[0]
        max_frames = duration // FRAME_TIME
        def points_fn(frame_count):
            completed = frame_count / max_frames
            offset = [(e - s) * completed for s, e in zip(start_pos, end_pos)]
            return [shift_point(p, offset) for p in points]
        self.animate_shape(id, duration, points_fn)

    def wait_for_click(self, seconds=0):
        """Return (position, elapsed) pair of click position and elapsed time.

        position: (x,y) pixel position of click
        elapsed:  milliseconds elapsed since call
        seconds:  maximum number of seconds to wait for a click

        If there is still no click after the given time, return (None, seconds).

        """
        elapsed = 0
        while elapsed < seconds or seconds == 0:
            if self._click_pos is not None:
                pos = self._click_pos
                self._click_pos = None
                return pos, elapsed
            self._sleep(FRAME_TIME)
            elapsed += FRAME_TIME
        return None, elapsed

    def _draw_background(self):
        w, h = self.width - 1, self.height - 1
        corners = [(0,0), (0, h), (w, h), (w, 0)]
        self.draw_polygon(corners, self.color, fill_color=self.color, filled=True, smooth=False)

    def _click(self, event):
        self._click_pos = (event.x, event.y)

    def _sleep(self, seconds):
        self._tk.update_idletasks()
        self._tk.after(int(1000 * seconds), self._tk.quit)
        self._tk.mainloop()

def flattened(points):
    """Return a flat list of coordinates from a list of pairs."""
    coords = list()
    [coords.extend(p) for p in points]
    return tuple(coords)

def paired(coords):
    """Return a list of pairs from a flat list of coordinates."""
    assert len(coords) % 2 == 0, 'Coordinates are not paired.'
    points = []
    x = None
    for elem in coords:
        if x is None:
            x = elem
        else:
            points.append((x, elem))
            x = None
    return points

def translate_point(point, angle, distance):
    """Translate a point a distance in a direction (angle)."""
    x, y = point
    return (x + math.cos(angle) * distance, y + math.sin(angle) * distance)

def shift_point(point, offset):
    """Shift a point by an offset."""
    x, y = point
    dx, dy = offset
    return (x + dx, y + dy)

def rectangle_points(pos, width, height):
    """Return the points of a rectangle starting at pos."""
    x1, y1 = pos
    x2, y2 = width + x1, height + y1
    return [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]

def format_color(r, g, b):
    """Format a color as a string.

    r, g, b -- integers from 0 to 255
    """
    return '#{0:02x}{1:02x}{2:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
