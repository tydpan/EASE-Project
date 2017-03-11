#!/usr/bin/pythons
#-*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk


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

        self.temp_sum(controller)
        self.temp_wint(controller)




        # prec
        self.prec = tk.StringVar()
        self.prec.set('Anticipated annual rain fall :')
        self.prec_dict = {'Anticipated annual rain fall :': None, 'Almost never rain ( <1 )': 0.5,
                     'A few days a year ( 1~1.5 )': 1.25, 'A few weeks a year ( 1.5~2 )': 1.75,
                     'A few months a year ( 2~2.5 )': 2.25, 'Half of the time ( 2.5~3 )': 2.75,
                     'More than Half of the time ( 3~4 )': 3.5, 'Almost every single day (>4)': 4.8}

        option_list = ['Anticipated annual rain fall :', 'Almost never rain ( <1 )', 'A few days a year ( 1~1.5 )',
                       'A few weeks a year ( 1.5~2 )', 'A few months a year ( 2~2.5 )', 'Half of the time ( 2.5~3 )',
                       'More than Half of the time ( 3~4 )', 'Almost every single day (>4)']
        tk.OptionMenu(self.frame, self.prec, *option_list).grid(row=3, column=2, pady=5, padx=5, sticky='w')
#        self.abc = lambda: self.prec_dict[self.prec.get()]
#        self.abc = self.abc()
        #controller.prec = self.prec_dict[self.prec.get()]
        #self.prec.trace('w', self.try3(controller))

        tk.Label(self.frame, text='Precipitation:', highlightthickness=0, bd=0).grid(
            row=3, column=0, pady=5, padx=5, sticky='e')
        tk.Label(self.frame, text='( inch )', highlightthickness=0, bd=0).grid(
            row=3, column=1, pady=5, padx=5, sticky='e')
        """
        # wind speed
        tk.Label(frame, text='Wind Speed:', highlightthickness=0, bd=0).grid(
            row=4, column=0, pady=5, padx=5, sticky='e')
        tk.Label(frame, text='( m/s )', highlightthickness=0, bd=0).grid(
            row=4, column=1, pady=5, padx=5, sticky='e')

        #capacity
        tk.Label(frame, text='Capacity:', highlightthickness=0, bd=0).grid(
            row=5, column=0, pady=5, padx=5, sticky='e')
        tk.Label(frame, text='( Mwh )', highlightthickness=0, bd=0).grid(
            row=5, column=1, pady=5, padx=5, sticky='e')


        """
        self.try2(controller)
        tk.Button(self.frame, text='try', command=lambda: [f for f in [self.try2(controller), self.try3(controller)]]).grid(row=0)


    def try11(self, value):
        print(value)

    def try2(self, controller):
        controller.prec = self.prec_dict[self.prec.get()]
        print(controller.prec)

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

        controller.ts = tk.DoubleVar()
        tk.Entry(self.frame, textvariable=controller.ts, bg='grey', width=5).grid(
            row=1, column=2, pady=5, padx=5, sticky='w')

    def temp_wint(self, controller):
        tk.Label(self.frame, text='Average Temperature in Winter:', highlightthickness=0, bd=0).grid(
            row=2, column=0, pady=5, padx=5, sticky='e')
        tk.Label(self.frame, text='( \u2109 )', highlightthickness=0, bd=0).grid(
            row=2, column=1, pady=5, padx=5, sticky='e')

        controller.tw = tk.DoubleVar()
        tk.Entry(self.frame, textvariable=controller.tw, bg='grey', width=5).grid(
            row=2, column=2, pady=5, padx=5, sticky='w')


if __name__ == '__main__':
    app = App()
    app.mainloop()