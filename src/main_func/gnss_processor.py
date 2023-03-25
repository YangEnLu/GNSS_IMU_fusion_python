from ..common.global_constants import rtk, default_opt, obs, nav, glc
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from ..common.initrtk import initrtk
from ..common.timespan import timespan
from ..common.searchobsr import searchobsr
from ..common.exclude_sat import exclude_sat
from ..common.searchobsb import searchobsb


def gnss_processor(rtk: rtk, opt: default_opt, obsr: obs, obsb: obs, nav: nav):
    ti = 0

    # initialize figure and progressbar
    hbar = tk.Tk()
    screen_width = hbar.winfo_screenwidth()
    screen_height = hbar.winfo_screenheight()
    hbar.title("GNSS/IMU fusion toolbox")
    y = screen_height/2
    hbar.geometry(f'{500}x{100}+{int(0)}+{int(y-100)}')
    hbar.iconbitmap("LAB_logo.ico")
    bar = ttk.Progressbar(hbar, mode='determinate', length=400)
    bar.pack(pady=20)
    val = tk.StringVar()
    val.set('Processing... 0%')
    label = tk.Label(hbar, textvariable=val)
    label.pack()
    button = tk.Button(hbar, text='cancel')
    button.pack()

    hfig, ax = plt.subplots(figsize=(8, 6))

    # initialize rtk class
    rtk = initrtk(rtk, opt)

    # set time span
    tspan = timespan(rtk, obsr)
    if tspan <= 0:
        print("ERROR<gnss_processor> Time span is zero!!!")

    while True:
        if ti > tspan:
            break

        # search rover obs
        obsr_, nobs, obsr = searchobsr(obsr)
        if nobs < 0:
            string = f'Processing... {100:.1f}%'
            bar['value'] = int((ti/tspan)*100)
            val.set(string)
            hbar.update()
            break

        # exclude rover obs
        obsr_, nobs = exclude_sat(obsr_, rtk)
        if nobs == 0:
            continue
        if opt.mode >= glc().PMODE_DGNSS and opt.mode <= glc().PMODE_STATIC:
            # search base obs
            obsb_, nobs = searchobsb(obsb, obsr_[0, 0].time)
            # exclude base obs
            if nobs != 0:
                obsb_,  = exclude_sat(obsb_, rtk)
        else:
            obsb_ = np.NaN
            
        

    hbar.mainloop()
