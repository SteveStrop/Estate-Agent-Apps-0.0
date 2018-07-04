import tkinter as tk
# from tkinter.ttk import *
import agent_lib as al
import win32api
import time
import sys
import win32gui
import win32con

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)


def ok_clicked():
    master_frame.destroy()
    # set up loading text
    loading_frame = tk.Frame(master=root,
                             bg=al.set_colours(gui_colour)["bg"]
                             )
    root.title("Opening homepage...")
    label_info = tk.Label(loading_frame, width=20,
                          bg=al.set_colours(gui_colour)["bg"],
                          fg=al.set_colours(gui_colour)["text"],
                          font=(None, 10),
                          text=selected_agent.get() == "ka" and "Opening KeyAGENT..." or "Opening House Simple..."
                          )
    label_info.grid(pady=50, padx=40)
    loading_frame.grid()
    root.update()

    open_function = getattr(al, "{}_open_jobs_list".format(selected_agent.get()))  # fails with default arg added???
    browser = open_function(root)

    while 1:
        time.sleep(1)
        try:
            _ = browser.find_element_by_tag_name("body")
        except:
            sys.exit()


def cancel_clicked():
    root.destroy()


# initialise GUI window
root = tk.Tk()
root.title("Select homepage to open")
mouse_x, mouse_y = win32api.GetCursorPos()
mouse_y -= 220
gui_colour = "#4f4f4f"
root.geometry("330x150+{}+{}".format(mouse_x, mouse_y))

# set up radio buttons
master_frame = tk.Frame(master=root,
                        bg=al.set_colours(gui_colour)["bg"])
selected_agent = tk.StringVar()  # selected holds radio button currently selected

# set default Radiobutton
selected_agent.set("ka")

radio_hs = tk.Radiobutton(master_frame,
                          activebackground=al.set_colours(gui_colour)["bg"],
                          selectcolor=al.set_colours(gui_colour)["bg"],
                          bg=al.set_colours(gui_colour)["bg"],
                          fg=al.set_colours(gui_colour)["text"],
                          width=15,
                          text="House Simple",
                          value="hs",
                          variable=selected_agent
                          )
radio_ka = tk.Radiobutton(master_frame,
                          activebackground=al.set_colours(gui_colour)["bg"],
                          selectcolor=al.set_colours(gui_colour)["bg"],
                          bg=al.set_colours(gui_colour)["bg"],
                          fg=al.set_colours(gui_colour)["text"],
                          width=15,
                          text="KeyAGENT",
                          value="ka",
                          variable=selected_agent
                          )
btn_ok = tk.Button(master_frame,
                   overrelief="ridge",
                   fg=al.set_colours(gui_colour)["text"],
                   bg=al.set_colours(gui_colour)["btn_bg"],
                   relief="flat",
                   width=9,
                   text="OK",
                   command=ok_clicked
                   )
btn_cancel = tk.Button(master_frame,
                       overrelief="ridge",
                       fg=al.set_colours(gui_colour)["text"],
                       bg=al.set_colours(gui_colour)["btn_bg"],
                       relief="flat",
                       width=9,
                       text="Cancel",
                       command=cancel_clicked
                       )

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
master_frame.grid_columnconfigure(0, weight=1)

master_frame.grid(column=0,
                  row=0,
                  sticky="news"
                  )
radio_ka.grid(column=0,
              row=0,
              padx=40,
              pady=(50, 20)
              )
radio_hs.grid(column=1,
              row=0,
              pady=(50, 20)
              )
btn_ok.grid(column=0,
            row=1,
            pady=10,
            sticky="e"
            )
btn_cancel.grid(column=1,
                row=1,
                pady=10,
                )
root.mainloop()
