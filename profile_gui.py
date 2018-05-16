import profile_calc
import Tkinter
import ttk
import tkFileDialog
import sys


# Function used to kill the program entirely.


def kill():
    sys.exit()


def sort_values(sort_by):
    global pp_info, tree, root

    if sort_by == "old_pp":
        sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[1], reverse=True)]
    elif sort_by == "new_pp":
        sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[2], reverse=True)]
    else:
        sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[2] / float(x[1]))]

    tree.destroy()

    tree = ttk.Treeview(root)

    tree.config(columns=("1", "2", "3"))
    tree.column("1", stretch=False, width=150)
    tree.column("2", stretch=False, width=150)
    tree.column("3", stretch=False, width=150)
    tree.heading("1", text="Old Performance")
    tree.heading("2", text="Proposed Performance")
    tree.heading("3", text="Percent Change")

    for i in sorted_list:
        tree.insert("", "end", text=i[0], values=("{:.2f}PP".format(i[1]),
                                                  "{:.2f}PP".format(i[2]),
                                                  "{:.2f}%".format(100 * i[2] / float(i[1]))))

    tree.pack(fill='both', expand=True)


while True:

    root = Tkinter.Tk()
    root.resizable(width=False, height=True)
    root.geometry("1200x800")
    root.title("osu-calc")

    pp_info = profile_calc.return_values("ekoro")

    old_sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[1], reverse=True)]

    old_pp = sum([old_sorted_list[i][1] * (0.95 ** i) for i in range(len(old_sorted_list))])

    new_sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[2], reverse=True)]

    new_pp = sum([new_sorted_list[i][2] * (0.95 ** i) for i in range(len(new_sorted_list))])

    Tkinter.Label(root, text="Old Total Performance: {:.2f}PP".format(old_pp)).pack()
    Tkinter.Label(root, text="New Total Performance: {:.2f}PP".format(new_pp)).pack()

    Tkinter.Button(root, fg="blue", text="Sort by Old Performance", command=lambda: sort_values("old_pp")).pack()
    Tkinter.Button(root, fg="blue", text="Sort by Proposed Performance", command=lambda: sort_values("new_pp")).pack()
    Tkinter.Button(root, fg="blue", text="Sort by Percent Change", command=lambda: sort_values("percent")).pack()

    tree = ttk.Treeview(root)

    tree.config(columns=("1", "2", "3"))
    tree.column("1", stretch=False, width=150)
    tree.column("2", stretch=False, width=150)
    tree.column("3", stretch=False, width=150)
    tree.heading("1", text="Old Performance")
    tree.heading("2", text="Proposed Performance")
    tree.heading("3", text="Percent Change")

    sorted_list = [i for i in
                   sorted(pp_info, key=lambda x: x[1], reverse=True)]

    for i in sorted_list:
        tree.insert("", "end", text=i[0], values=("{:.2f}PP".format(i[1]),
                                                  "{:.2f}PP".format(i[2]),
                                                  "{:.2f}%".format(100 * i[2] / float(i[1]))))

    tree.pack(fill="both", expand=True)

    # If window is closed, stop the program.
    root.protocol("WM_DELETE_WINDOW", kill)

    root.mainloop()
