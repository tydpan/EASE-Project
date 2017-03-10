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
        for i in (License, Main_page):
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
        tk.Button(self, text='Agree', command=lambda: controller.show_frame(Main_page), highlightthickness=0,
                  bd=0).pack(side='bottom')


class Main_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        logo_frame = tk.Frame(self)
        logo_frame.pack()
        self.image = tk.PhotoImage(file='EASE.gif')
        logo = tk.Label(logo_frame, image=self.image)
        logo.image = self.image
        logo.pack()

        frame = tk.Frame(self)
        frame.pack()

        tk.Label(frame, text='Average Temperature in Summer:', highlightthickness=0, bd=0).grid(
            row=1, column=0, pady=5, padx=5, sticky='e')
        tk.Label(frame, text='( \u2109 )', highlightthickness=0, bd=0).grid(
            row=1, column=1, pady=5, padx=5, sticky='e')
        ts = tk.Entry(frame, bg='grey', width=5).grid(row=1, column=2, pady=5, padx=5, sticky='w')


        tk.Label(frame, text='Average Temperature in Winter:', highlightthickness=0, bd=0).grid(
            row=2, column=0, pady=5, padx=5, sticky='e')
        tk.Label(frame, text='( \u2109 )', highlightthickness=0, bd=0).grid(
            row=2, column=1, pady=5, padx=5, sticky='e')

        self.tw = tk.IntVar()
        tk.Entry(frame, textvariable=self.tw, bg='grey', width=5).grid(row=2, column=2, pady=5, padx=5, sticky='w')
        tk.Button(frame, text='try', command=self.try_()).grid(row=0)
        #lambda: print(self.tw.get() + 1)

        tk.Label(frame, text='Precipitation:', highlightthickness=0, bd=0).grid(
            row=3, column=0, pady=5, padx=5, sticky='e')
        tk.Label(frame, text='( inch )', highlightthickness=0, bd=0).grid(
            row=3, column=1, pady=5, padx=5, sticky='e')

        tk.Label(frame, text='Wind Speed:', highlightthickness=0, bd=0).grid(
            row=4, column=0, pady=5, padx=5, sticky='e')
        tk.Label(frame, text='( m/s )', highlightthickness=0, bd=0).grid(
            row=4, column=1, pady=5, padx=5, sticky='e')

        tk.Label(frame, text='Capacity:', highlightthickness=0, bd=0).grid(
            row=5, column=0, pady=5, padx=5, sticky='e')
        tk.Label(frame, text='( Mwh )', highlightthickness=0, bd=0).grid(
            row=5, column=1, pady=5, padx=5, sticky='e')

    def try_(self):
        print(self.tw.get() + 1)


if __name__ == '__main__':
    app = App()
    app.mainloop()