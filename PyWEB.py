import tkinter as tk
from tkinter import ttk
import win32api
import time
import sys
import agent_lib as al


def ok_clicked():
    master_frame.destroy()
    # set up loading text
    loading_frame = tk.Frame(master=root)
    root.title("Opening homepage...")
    label_info = tk.Label(loading_frame, width=20,
                          font=(None, 10),
                          text=selected_agent.get() == "ka" and "Opening KeyAGENT..." or "Opening House Simple..."
                          )
    label_info.grid(pady=50, padx=40)
    loading_frame.grid()
    root.update()

    browser = al.open_jobs_list(root, selected_agent.get())

    while 1:
        time.sleep(1)
        try:
            _ = browser.find_element_by_tag_name("body")  # check if browser exists
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
master_frame = ttk.Frame(master=root)
selected_agent = tk.StringVar()  # selected holds radio button currently selected

# set default Radiobutton
selected_agent.set("KA")

radio_hs = ttk.Radiobutton(master_frame,
                           width=15,
                           text="House Simple",
                           value="HS",
                           variable=selected_agent
                           )
radio_ka = ttk.Radiobutton(master_frame,
                           width=15,
                           text="KeyAGENT",
                           value="KA",
                           variable=selected_agent
                           )
btn_ok = ttk.Button(master_frame,
                    width=9,
                    text="OK",
                    command=ok_clicked
                    )
btn_cancel = ttk.Button(master_frame,
                        width=9,
                        text="Cancel",
                        command=cancel_clicked
                        )

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
master_frame.grid_columnconfigure(0, weight=1)
master_frame.grid_columnconfigure(1, weight=1)
master_frame.grid_rowconfigure(0, weight=1)
master_frame.grid_rowconfigure(1, weight=1)

master_frame.grid(column=0,
                  row=0,
                  sticky='news'
                  )
radio_ka.grid(column=0,
              columnspan=2,
              row=0,
              padx=(30, 0),
              pady=(20, 20),
              sticky='nw'
              )
radio_hs.grid(column=0,
              columnspan=2,
              row=1,
              padx=(30, 0),
              pady=(0, 0),
              sticky='nw'
              )
btn_ok.grid(column=1,
            row=2,
            padx=5,
            pady=20,
            sticky='se'
            )
btn_cancel.grid(column=2,
                row=2,
                padx=20,
                pady=20,
                sticky='se'
                )
root.mainloop()
