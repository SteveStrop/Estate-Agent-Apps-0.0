# TODO convert to class
import tkinter as tk
import agent_lib as al
import re
import subprocess
import os
import win32api


def mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def check_for_floorplan(folder):
    for file in os.listdir(folder):
        try:
            match = re.search(r"(?:copy|Thumbs)|([A-Za-z]+?[. ,]|[Ff]loor[ Pp]lan)", file).group(1)
            if match:
                return "bold"

        except AttributeError:

            pass
    return "normal"


def display_in_explorer(folders):
    for folder in folders:
        subprocess.run('explorer "' + folder + '"')


def scroller_bind(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


def scrolling_ok_clicked(var, candidate_folders, gui_):
    #
    gui_.destroy()
    # get list of checkboxes, see which ones are clicked and open them in windows
    display_folders = [candidate_folders[i][1] for i, v in enumerate(var) if v.get() == 1]
    display_in_explorer(display_folders)


def scrolling_cancel_clicked(gui):
    gui.destroy()


def scrolling_retry_clicked():
    pass


def checkbox_gui(folder_list, folder_name):
    global canvas, checkbox_frame
    gui_height = 350
    gui_width = 650
    gui_colour = "#4f4f4f"

    # create root
    root = tk.Tk()
    root.title("pySEARCH - Matching folders")
    root.geometry("{}x{}".format(gui_width, gui_height))

    # create main gui in which everything goes
    gui = tk.Frame(root,
                   bg=al.set_colours(gui_colour)["bg"]
                   )
    gui.grid(column=0, row=0, sticky="news")

    # tk.Label(gui, text="gui").grid()

    # create a frame to hold the scroller and canvas
    canvas_frame = tk.Frame(gui)
    canvas_frame.grid(column=0, row=0, padx=10, pady=10)
    canvas = tk.Canvas(canvas_frame,
                       highlightthickness=0,
                       bg=al.set_colours(gui_colour)["checkbox_bg"])
    checkbox_frame = tk.Frame(canvas,
                              bg=al.set_colours(gui_colour)["checkbox_bg"]
                              )  # no need to grid here it gets done  create_candidates
    my_scrollbar = tk.Scrollbar(canvas_frame,
                                highlightthickness=0,
                                bd=0,
                                orient="vertical",
                                command=canvas.yview)

    canvas.configure(yscrollcommand=my_scrollbar.set)

    my_scrollbar.grid(column=1,
                      row=0,
                      sticky="nse")
    canvas.grid(column=0,
                row=0,
                sticky="nsw")

    canvas.create_window((0, 0),
                         window=checkbox_frame,
                         anchor='nw',
                         )
    checkbox_frame.bind("<Configure>", scroller_bind)
    var, candidate_folders = create_candidates(folder_list, checkbox_frame, gui_colour)

    # place ok cancel buttons
    btn_ok = tk.Button(gui,
                       overrelief="ridge",
                       activebackground=al.set_colours(gui_colour)["btn_activebackground"],
                       fg=al.set_colours(gui_colour)["text"],
                       bg=al.set_colours(gui_colour)["btn_bg"],
                       relief="flat",
                       width=9,
                       text="OK",
                       command=lambda: scrolling_ok_clicked(var, candidate_folders, root))
    btn_retry = tk.Button(gui,
                          overrelief="ridge",
                          activebackground=al.set_colours(gui_colour)["btn_activebackground"],
                          fg=al.set_colours(gui_colour)["text"],
                          bg=al.set_colours(gui_colour)["btn_bg"],
                          relief="flat",
                          width=9,
                          text="Retry",
                          command=scrolling_retry_clicked
                          )
    btn_cancel = tk.Button(gui,
                           overrelief="ridge",
                           activebackground=al.set_colours(gui_colour)["btn_activebackground"],
                           fg=al.set_colours(gui_colour)["text"],
                           bg=al.set_colours(gui_colour)["btn_bg"],
                           relief="flat",
                           width=9,
                           text="Quit",
                           command=lambda: scrolling_cancel_clicked(root)
                           )
    # ensure widgets inside of frames resize
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    gui.grid_columnconfigure(0, weight=1)
    gui.grid_rowconfigure(0, weight=1)
    btn_pad = 20
    gui.grid_columnconfigure(10, pad=btn_pad)
    gui.grid_columnconfigure(11, pad=btn_pad)
    gui.grid_columnconfigure(12, pad=btn_pad)
    gui.grid_rowconfigure(10, pad=btn_pad)
    canvas_frame.grid_columnconfigure(0, weight=1)
    canvas_frame.grid_rowconfigure(0, weight=1)

    btn_ok.grid(column=10, row=10)
    btn_retry.grid(column=11, row=10)
    btn_cancel.grid(column=12, row=10)
    root.bind_all("<MouseWheel>", mouse_wheel)
    root.mainloop()
    return


def create_candidates(folder_list, frame, gui_colour):
    checkbox = []
    var = []
    candidate_folders = []
    i = 0
    # match_string = match_string.replace("*", ".*")
    # match_string = match_string.replace("?", ".?")
    # print("match string = {}".format(match_string))
    for folder in sorted(set(folder_list)):  # remove duplicates
        try:
            short_folder = re.search(
                r"(?:\d{10} |[Kk][Aa]|[Tt][Mm]|[Bb][Ss]|[Hh][Ss][Ss]\d{5})([a-zA-Z0-9 ,]*)",
                folder).group(1)
            var.append(tk.IntVar())
            candidate_folders.append([i, folder])
            checkbox.append(
                tk.Checkbutton(frame,
                               selectcolor=al.set_colours(gui_colour)["checkbox_bg"],
                               bg=al.set_colours(gui_colour)["checkbox_bg"],
                               fg=check_for_floorplan(folder) == "bold" and al.set_colours(gui_colour)[
                                   "checkbox_bold_text"] or al.set_colours(gui_colour)["checkbox_text"],
                               text=short_folder + "…",
                               font=("", 9, check_for_floorplan(folder)),
                               variable=var[i])
            )
            checkbox[i].grid(sticky="w")
            i += 1
        except AttributeError:
            pass
            # short_folder = ""

        # print(i, folder.title(), "\n", match_string, short_folder)
    return var, candidate_folders


def ok_clicked(event):
    # TODO change cursor
    root.configure(cursor="watch")
    root.update()
    search_str = input_search_str.get().replace(" ", "*")  # catch dodgey punctuation

    # search in A drive and Completed folder for folders containing search_str using wildcards as input by user
    found_in_archive = al.find_folders(root_folder='A:\\Estate Agent Archive\\All Estate Agents\\',
                                       target_folder=search_str)
    found_in_completed = al.find_folders(root_folder='F:\\My Documents\\My Pictures\Estate Agents\\completed\\',
                                         target_folder=search_str)
    # close input form
    root.destroy()
    # open checkbox form
    checkbox_gui(found_in_completed + found_in_archive, search_str)


def retry_clicked():
    input_search_str.delete(0, tk.END)
    input_search_str.focus()


def cancel_clicked():
    root.destroy()


# initialise GUI window
gui_height = 260
gui_width = 500
gui_colour = "##4f4f4f"
root = tk.Tk()
root.title("pySEARCH")

mouse_x, mouse_y = win32api.GetCursorPos()
mouse_y -= 340

root.geometry("{}x{}+{}+{}".format(gui_width, gui_height, mouse_x, mouse_y))

# set up frame to contain gui
master_frame = tk.Frame(master=root,
                        width=gui_width,
                        height=gui_height,
                        bg=al.set_colours(gui_colour)["bg"]
                        )

# create widgets
label_instructions = tk.Label(master_frame,
                              fg=al.set_colours(gui_colour)["text"],
                              bg=al.set_colours(gui_colour)["bg"],
                              justify="left",
                              font=("", 10, ""),
                              text="Enter the text you want to search for. It is not case sensitive")
label_hint = tk.Label(master_frame,
                      fg=al.set_colours(gui_colour)["text"],
                      bg=al.set_colours(gui_colour)["bg"],
                      justify="left",
                      font=("", 8, ""),
                      text="Wildcards (can be combined):\n"
                           "Use ? for any character\n"
                           "e.g 2? Green Lane will find 20-29 Green Lane and 2A-2Z Green Lane\n\n"
                           "Use * for any number of characters \n"
                           "e.g. 6*Green Lane will find '6 Green Lane' and '6, "
                           "Green Lane' and '67 Green Lane'\n"
                           "and '67, Green Lane' etc")
input_search_str = tk.Entry(master_frame,
                            width=75,
                            fg=al.set_colours(gui_colour)["input_text"],
                            bg=al.set_colours(gui_colour)["input_bg"],
                            relief="flat"
                            )
input_search_str.bind("<Return>", ok_clicked)
btn_ok = tk.Button(master_frame,
                   overrelief="ridge",
                   activebackground=al.set_colours(gui_colour)["btn_activebackground"],
                   fg=al.set_colours(gui_colour)["btn_text"],
                   bg=al.set_colours(gui_colour)["btn_bg"],
                   relief="flat",
                   width=9,
                   text="OK",
                   command=lambda: ok_clicked("")
                   )
btn_retry = tk.Button(master_frame,
                      overrelief="ridge",
                      activebackground=al.set_colours(gui_colour)["btn_activebackground"],
                      fg=al.set_colours(gui_colour)["btn_text"],
                      bg=al.set_colours(gui_colour)["btn_bg"],
                      relief="flat",
                      width=9,
                      text="Retry",
                      command=retry_clicked
                      )
btn_cancel = tk.Button(master_frame,
                       overrelief="ridge",
                       activebackground=al.set_colours(gui_colour)["btn_activebackground"],
                       fg=al.set_colours(gui_colour)["btn_text"],
                       bg=al.set_colours(gui_colour)["btn_bg"],
                       relief="flat",
                       width=9,
                       text="Quit",
                       command=cancel_clicked)

# position widgets
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
master_frame.grid_columnconfigure(0, weight=1)
master_frame.grid_rowconfigure(3, weight=1)

master_frame.grid(column=0,
                  row=0,
                  sticky="nwse"
                  )
label_instructions.grid(column=0,
                        row=0,
                        columnspan=3,
                        padx=10,
                        pady=10,
                        sticky="nw"
                        )
input_search_str.grid(column=0,
                      row=1,
                      columnspan=3,
                      padx=10,
                      sticky="nw"
                      )
label_hint.grid(column=0,
                row=2,
                columnspan=3,
                padx=10,
                pady=10,
                sticky="nw"
                )
btn_ok.grid(column=0,
            row=3,
            padx=10,
            pady=10,
            sticky="se"
            )
btn_retry.grid(column=1,
               row=3,
               padx=10,
               pady=10,
               sticky="se"
               )
btn_cancel.grid(column=2,
                row=3,
                padx=10,
                pady=10,
                sticky="se"
                )
input_search_str.focus()
root.mainloop()
