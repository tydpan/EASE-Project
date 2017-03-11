#!/usr/bin/pythons
#-*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox as mb

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title('EASE')

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

        tk.Label(self, text='License page', highlightthickness=0, bd=0).pack(side='top')

        tk.Button(self, text='Quit', command=controller.destroy, highlightthickness=0, bd=0).pack(side='bottom')
        tk.Button(self, text='Agree', command=lambda: controller.show_frame(MainPage), highlightthickness=0,
                  bd=0).pack(side='bottom')


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.logo()

        # frame for widgets
        self.frame = tk.Frame(self)
        self.frame.pack()

        # widgets
        self.temp_sum(controller)
        self.temp_wint(controller)
        self.precipitation()
        self.wind_speed(controller)
        self.capacity()

        but = tk.Button(self.frame, text='try', command=lambda: self.check_value(controller))
        but.grid(row=0)


    def try11(self, value):
        print(value)

    def try3(self, controller):
        print(controller.prec)

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
        tk.Label(self.frame, text='( inch )', highlightthickness=0, bd=0).grid(
            row=3, column=1, pady=5, padx=5, sticky='e')

        text = 'Eg:\nThe winter temperature in New York is about 30 \u2109, suitable to wear coat.'
        ref = tk.Label(self.frame, text='Ref.', highlightthickness=0, bd=0, font="Verdana 12 underline",
                       foreground='blue')
        ref.grid(row=3, column=2, pady=5, padx=5, sticky='e')
        Tooltip(ref, text=text, wraplength=200)

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

    def wind_speed(self, controller):
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
        Tooltip(ref, text=text, wraplength=500)

    def get_cap(self, controller):
        controller.cap = self.cap.get() * 1000

    def check_value(self, controller):
        self.get_prec(controller)
        self.get_ws(controller)
        self.get_cap(controller)
        self.n = 0
        while True:
            try:
                controller.ts.get()
            except tk.TclError:
                mb.showerror(title='Error', message='Please insert a correct value of temperature in summer.')
                break

            if controller.prec != None:
                pass
            else:
                mb.showerror(title='Error', message='Please choose a precipitation.')
                break
            if controller.ws == None:
                mb.showerror(title='Error', message='Please choose a wind speed.')
                break
            else:
                pass
            if controller.cap == 0:
                mb.showerror(title='Error', message='Please choose a value of capacity.')
                break
            else:
                pass

            break



class Tooltip:
    def __init__(self, widget,
                 *,
                 bg='#FFFFEA',
                 pad=(5, 3, 5, 3),
                 text='widget info',
                 waittime=400,
                 wraplength=250):

        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onEnter)
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
        def tip_pos_calculator(widget, label,
                               *,
                               tip_delta=(10, 5), pad=(5, 3, 5, 3)):

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

        win = tk.Frame(self.tw,
                       background=bg,
                       borderwidth=0)
        label = tk.Label(win,
                          text=self.text,
                          justify=tk.LEFT,
                          background=bg,
                          relief=tk.SOLID,
                          borderwidth=0,
                          wraplength=self.wraplength)

        label.grid(padx=(pad[0], pad[2]),
                   pady=(pad[1], pad[3]),
                   sticky=tk.NSEW)
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