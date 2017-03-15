#!/usr/bin/pythons
# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk     # Python 2.x
    import tkMessageBox as mb
else:
    import tkinter as tk     # Python 3.x
    from tkinter import messagebox as mb

import webbrowser

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import sys
sys.path.append('..')
import EASE.ease as ease


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title('EASE')
        self.wm_minsize(600, 490)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for i in (License, MainPage):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(6, weight=1)
            frame.grid_columnconfigure(6, weight=1)

        self.show_frame(License)

    def show_frame(self, frame_):
        frame = self.frames[frame_]
        frame.tkraise()


class License(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.image = tk.PhotoImage(file='EASE.gif')
        logo = tk.Label(self, image=self.image)
        logo.image = self.image
        logo.pack(side='top')

        tk.Label(self, text='\nEASE_v1.0', highlightthickness=0, bd=0).pack(side='top')
        tk.Label(self, text='Jiarong I. Cui, Tai-Yu D. Pan,\nJiayuan Guo, Yongquan Xie\n',
                 highlightthickness=0, bd=0).pack(side='top')

        text_frame = tk.Frame(self)
        text_frame.pack()
        text = tk.Text(text_frame, width=50, height=8, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        text.pack(side="left", fill="both", expand=True)
        text.insert('1.0',
                    'License :\n'
                    'This work is under GNU GPLv3 licence, such that it requires anyone who distributes this code or a '
                    'derivative work to make the source available under the same terms, and also provides an express '
                    'grant of patent rights from contributors to users.\n'
                    '\nAcknowledgements:\n'
                    'David A. Beck and Jim Pfaendtner, eScience Institue, Chemical Engineering Department, as well as'
                    ' Directors for the DIRECT program at University of Washington, served as mentors for the'
                    ' development of this package.')
        text.config(state=tk.DISABLED)

        tk.Label(self, text='\nPlease visit our website for more information: ',
                 highlightthickness=0, bd=0).pack()
        website = tk.Label(self, text='https://github.com/danielfather7/EASE-Project',
                           highlightthickness=0, bd=0, fg='blue', font="Verdana 12 underline")
        website.pack()
        website.bind("<Button-1>", lambda x: webbrowser.open_new(r"https://github.com/danielfather7/EASE-Project"))
        website.bind("<Enter>", lambda x: website.configure(fg='red'))
        website.bind("<Leave>", lambda x: website.configure(fg='blue'))

        tk.Label(self, text=' ', highlightthickness=0, bd=0).pack()

        tk.Button(self, text='Quit', command=controller.destroy, highlightthickness=0, bd=0).pack(side='bottom')
        tk.Button(self, text='Agree', command=lambda: controller.show_frame(MainPage), highlightthickness=0,
                  bd=0).pack(side='bottom')


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.logo()
        tk.Label(self, text=' ', highlightthickness=0, bd=0).pack()

        # frame for widgets
        self.frame = tk.Frame(self)
        self.frame.pack()

        # widgets
        self.temp_sum(controller)
        self.temp_wint(controller)
        self.precipitation()
        self.wind_speed()
        self.capacity()

        self.ease_but = tk.Button(self, text="Let's EASE (may take a while)", highlightthickness=0, bd=0,
                                  command=lambda: self.avoid_double_click(controller))
        self.ease_but.pack()
        tk.Button(self, text='Quit', command=lambda: controller.quit(), highlightthickness=0,
                  bd=0).pack()

    def logo(self):
        logo_frame = tk.Frame(self)
        logo_frame.pack()
        self.image = tk.PhotoImage(file='EASE.gif')
        logo = tk.Label(logo_frame, image=self.image)
        logo.image = self.image
        logo.pack()

    def temp_sum(self, controller):
        tk.Label(self.frame, text='Average Temperature in Summer:', highlightthickness=0, bd=0).grid(
            row=1, column=0, pady=5, padx=5, sticky='e')
        tk.Label(self.frame, text='( \u2109 )', highlightthickness=0, bd=0).grid(
            row=1, column=1, pady=5, padx=5, sticky='e')

        text = 'Eg:\nThe summer temperature in California is about 75 \u2109, suitable to wear short-sleeved T-shirt.'
        ref = tk.Label(self.frame, text='Ref.', highlightthickness=0, bd=0, font="Verdana 12 underline",
                       foreground='blue')
        ref.grid(row=1, column=2, pady=5, padx=5, sticky='e')
        Tooltip(ref, text=text, wraplength=200)

        controller.ts = tk.DoubleVar()
        tk.Entry(self.frame, textvariable=controller.ts, bg='grey', width=5).grid(
            row=1, column=3, pady=5, padx=5, sticky='w')

    def temp_wint(self, controller):
        tk.Label(self.frame, text='Average Temperature in Winter:', highlightthickness=0, bd=0).grid(
            row=2, column=0, pady=5, padx=5, sticky='e')
        tk.Label(self.frame, text='( \u2109 )', highlightthickness=0, bd=0).grid(
            row=2, column=1, pady=5, padx=5, sticky='e')

        text = 'Eg:\nThe winter temperature in New York is about 30 \u2109, suitable to wear coat.'
        ref = tk.Label(self.frame, text='Ref.', highlightthickness=0, bd=0, font="Verdana 12 underline",
                       foreground='blue')
        ref.grid(row=2, column=2, pady=5, padx=5, sticky='e')
        Tooltip(ref, text=text, wraplength=200)

        controller.tw = tk.DoubleVar()
        tk.Entry(self.frame, textvariable=controller.tw, bg='grey', width=5).grid(
            row=2, column=3, pady=5, padx=5, sticky='w')

    def precipitation(self):
        tk.Label(self.frame, text='Precipitation:', highlightthickness=0, bd=0).grid(
            row=3, column=0, pady=5, padx=5, sticky='e')
        tk.Label(self.frame, text='( inch\u00B3/cm\u00B2 )', highlightthickness=0, bd=0).grid(
            row=3, column=1, pady=5, padx=5, sticky='e')

        text = 'Eg:\nWashington was the leading producer of electricity from hydroelectric sources. In 2015, the ' \
               'total monthly precipitation in Washington is 2.52 inch\u00B3/cm\u00B2, and it rains about 172.5 days' \
               ' annually, which can be classed as “half of the time”.'
        ref = tk.Label(self.frame, text='Ref.', highlightthickness=0, bd=0, font="Verdana 12 underline",
                       foreground='blue')
        ref.grid(row=3, column=2, pady=5, padx=5, sticky='e')
        Tooltip(ref, text=text, wraplength=300)

        self.prec = tk.StringVar()
        self.prec.set('Anticipated annual rain fall :')
        self.prec_dict = {'Anticipated annual rain fall :': None, 'Almost never rain ( <1 )': 0.5,
                          'A few days a year ( 1~1.5 )': 1.25, 'A few weeks a year ( 1.5~2 )': 1.75,
                          'A few months a year ( 2~2.5 )': 2.25, 'Half of the time ( 2.5~3 )': 2.75,
                          'More than Half of the time ( 3~4 )': 3.5, 'Almost every single day (>4)': 4.8}

        option_list = ['Anticipated annual rain fall :', 'Almost never rain ( <1 )', 'A few days a year ( 1~1.5 )',
                       'A few weeks a year ( 1.5~2 )', 'A few months a year ( 2~2.5 )', 'Half of the time ( 2.5~3 )',
                       'More than Half of the time ( 3~4 )', 'Almost every single day (>4)']
        om = tk.OptionMenu(self.frame, self.prec, *option_list)
        om.grid(row=3, column=3, pady=5, padx=5, sticky='w')
        om.config(width=25)

    def get_prec(self, controller):
        controller.prec = self.prec_dict[self.prec.get()]

    def wind_speed(self):
        tk.Label(self.frame, text='Wind Speed:', highlightthickness=0, bd=0).grid(
            row=4, column=0, pady=5, padx=5, sticky='e')
        tk.Label(self.frame, text='( m/s )', highlightthickness=0, bd=0).grid(
            row=4, column=1, pady=5, padx=5, sticky='e')

        text = 'Wind Speed:\nLight air : Smoke drifts and leaves rustle.\nLight breeze : Wind felt on face.\n' \
               'Gentle breeze : Flags extended, leaves move.\nModerate breeze : Dust and small branches move.\n' \
               'Fresh breeze : Small trees begin to sway.\nStrong wind : Umbrella are difficult to control.\n' \
               'Gale : Inconvenience in walking.'
        ref = tk.Label(self.frame, text='Ref.', highlightthickness=0, bd=0, font="Verdana 12 underline",
                       foreground='blue')
        ref.grid(row=4, column=2, pady=5, padx=5, sticky='e')
        Tooltip(ref, text=text, wraplength=500)

        self.ws = tk.StringVar()
        self.ws.set('Feeling about wind :')
        self.ws_dict = {'Feeling about wind :': None, 'Light air ( <5 )': 2.5, 'Light breeze ( 5~6 )': 5.5,
                        'Gentle breeze ( 6~7 )': 6.5, 'Moderate breeze ( 7~8 )': 7.5, 'Fresh Breeze ( 8~9 )': 8.5,
                        'Strong wind ( 9~10 )': 9.5, 'Gale ( 10~14 )': 12}
        option_list = ['Feeling about wind :', 'Light air ( <5 )', 'Light breeze ( 5~6 )', 'Gentle breeze ( 6~7 )',
                       'Moderate breeze ( 7~8 )', 'Fresh Breeze ( 8~9 )', 'Strong wind ( 9~10 )', 'Light air ( <5 )',
                       'Gale ( 10~14 )']
        om = tk.OptionMenu(self.frame, self.ws, *option_list)
        om.grid(row=4, column=3, pady=5, padx=5, sticky='w')
        om.config(width=25)

    def get_ws(self, controller):
        controller.ws = self.ws_dict[self.ws.get()]

    def capacity(self):
        self.scale_frame = tk.Frame(self)
        self.scale_frame.pack()

        self.cap = tk.Scale(self.scale_frame, label="Capacity: ( 10\u00B3 Mwh )", from_=0, to=3500, resolution=5,
                            length=500, orient='horizontal', tickinterval=500)
        self.cap.grid(row=0, column=0, pady=5, padx=5, sticky='nsew')

        text = 'Capacity:\nA small electricity plant generate less than 50,000 MWh a year, which can provide ' \
               'electricity for a city block.\nA medium electricity plant generate 50,000~200,000 MWh a year, ' \
               'which can provide about 10,000 households.\nA large electricity plant generate more than 200,000 MWh ' \
               'a year, which can provide electricity for the total Bellevue in WA.\nThe largest plant capacity ' \
               'in 2015 in U.S. is about 3,500,000 MWh a year. \nNote : The average annual electricity consumption ' \
               'for one household in U.S. is 10 MWh.'
        ref = tk.Label(self.scale_frame, text='Ref.', highlightthickness=0, bd=0, font="Verdana 12 underline",
                       foreground='blue')
        ref.grid(row=0, column=1, pady=5, padx=5, sticky='e')
        tk.Label(self.scale_frame, text=' ', highlightthickness=0, bd=0).grid(row=1)
        Tooltip(ref, text=text, wraplength=500)

    def get_cap(self, controller):
        controller.cap = self.cap.get() * 1000

    def check_value(self, controller):
        self.get_prec(controller)
        self.get_ws(controller)
        self.get_cap(controller)
        self.n = True
#        print(ease.rf(2, 75, 30, 1.5))
        while True:
            try:
                controller.ts.get()
            except tk.TclError:
                self.n = False
                mb.showerror(title='Error', message='Please insert a correct value of temperature in summer.')
                break
            try:
                controller.tw.get()
            except tk.TclError:
                self.n = False
                mb.showerror(title='Error', message='Please insert a correct value of temperature in winter.')
                break
            if controller.ts.get() == controller.tw.get() and controller.ts.get() == 0:
                self.n = False
                mb.showerror(title='Error', message='Please insert a value of temperature.')
                break
            if controller.prec == None:
                self.n = False
                mb.showerror(title='Error', message='Please choose a precipitation.')
                break
            if controller.ws == None:
                self.n = False
                mb.showerror(title='Error', message='Please choose a wind speed.')
                break
            if controller.cap == 0:
                self.n = False
                mb.showerror(title='Error', message='Please choose a value of capacity.')
                break
            if controller.ts.get() < controller.tw.get():
                self.n = False
                mb.showerror(title='Error', message='Please insert correct values of summer temperature and and '
                                                    'winter temperature.')
                break
            break

    def ease_result(self, controller):
        self.check_value(controller)
        self.ease_but.config(state=tk.DISABLED)
        try:
            controller.result.clear()
        except:
            pass
        while self.n == True:
            result_page = tk.Toplevel(controller)
            result_frame = tk.Frame(result_page)
            result_frame.pack()
            button_frame = tk.Frame(result_page)
            button_frame.pack()
            result_page.title('EASE Result')

            controller.result = ease.suggest(
                controller.prec, controller.ts.get(), controller.tw.get(), controller.ws, controller.cap)

            canvas = FigureCanvasTkAgg(controller.result, result_frame)
            canvas.show()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

            toolbar = NavigationToolbar2TkAgg(canvas, result_frame)
            toolbar.update()
            controller.result.tight_layout()

            tk.Button(button_frame, text='Quit all', command=lambda: controller.quit(), highlightthickness=0,
                      bd=0).pack(side='bottom')
            tk.Button(button_frame, text='Close this window', command=result_page.destroy, highlightthickness=0,
                      bd=0).pack(side='bottom')
            break
        return

    def avoid_double_click(self, controller):
        self.ease_but.config(state=tk.DISABLED)
        self.ease_but.update()
        self.ease_result(controller)
        self.ease_but.after(1500)
        self.ease_but.config(state=tk.NORMAL)
        self.ease_but.update()


class Tooltip:
    def __init__(self, widget, bg='#FFFFEA', pad=(5, 3, 5, 3),
                 text='widget info', waittime=400, wraplength=250):

        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onLeave)
        self.bg = bg
        self.pad = pad
        self.id = None
        self.tw = None

    def onEnter(self, event=None):
        self.schedule()
        self.widget.configure(foreground="red")

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()
        self.widget.configure(foreground="blue")

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show(self):
        def tip_pos_calculator(widget, label, tip_delta=(10, 5), pad=(5, 3, 5, 3)):

            w = widget

            s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

            width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                             pad[1] + label.winfo_reqheight() + pad[3])

            mouse_x, mouse_y = w.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.

                # TIP:
                # A further mod might automagically augment the
                # wraplength when the tooltip is too high to be
                # kept inside the screen.
                y1 = 0

            return x1, y1

        bg = self.bg
        pad = self.pad
        widget = self.widget

        # creates a toplevel window
        self.tw = tk.Toplevel(widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = tk.Frame(self.tw, background=bg, borderwidth=0)
        label = tk.Label(win, text=self.text, justify=tk.LEFT, background=bg, relief=tk.SOLID, borderwidth=0,
                         wraplength=self.wraplength)

        label.grid(padx=(pad[0], pad[2]), pady=(pad[1], pad[3]), sticky=tk.NSEW)
        win.grid()

        x, y = tip_pos_calculator(widget, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        tw = self.tw
        if tw:
            tw.destroy()
        self.tw = None


if __name__ == '__main__':
    app = App()
    app.mainloop()
