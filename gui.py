import Tkinter
import ttk
import calc


# Function used to kill the program entirely.


def kill():
    sys.exit()


def calculate_pp():
    global map_link, c100, c50, miss, combo, info_l
    info_l["text"] = calc.return_values(c100.get(),
                                        c50.get(),
                                        miss.get(),
                                        combo.get(),
                                        map_link.get(),
                                        mods.get())


while True:
    root = Tkinter.Tk()
    root.resizable(width=False, height=False)
    root.title("osu-calc")

    Tkinter.Label(root, text="Map link:").grid(row=0, column=0)
    Tkinter.Label(root, text="Amount of 100s:").grid(row=1, column=0)
    Tkinter.Label(root, text="Amount of 50s:").grid(row=2, column=0)
    Tkinter.Label(root, text="Amount of misses:").grid(row=3, column=0)
    Tkinter.Label(root, text="Combo:").grid(row=4, column=0)
    Tkinter.Label(root, text="Mods:").grid(row=5, column=0)

    map_link = Tkinter.Entry(root, width=40)
    map_link.grid(row=0, column=1)

    c100 = Tkinter.Entry(root, width=40)
    c100.grid(row=1, column=1)

    c50 = Tkinter.Entry(root, width=40)
    c50.grid(row=2, column=1)

    miss = Tkinter.Entry(root, width=40)
    miss.grid(row=3, column=1)

    combo = Tkinter.Entry(root, width=40)
    combo.grid(row=4, column=1)

    mods = Tkinter.Entry(root, width=40)
    mods.grid(row=5, column=1)

    Tkinter.Button(root, fg="blue", text="Calculate pp!", command=calculate_pp).grid(row=6, column=0, columnspan=2)

    info_l = Tkinter.Label(root)
    info_l.grid(row=7, column=0, columnspan=2)

    # If window is closed, stop the program.
    root.protocol("WM_DELETE_WINDOW", kill)

    root.mainloop()
