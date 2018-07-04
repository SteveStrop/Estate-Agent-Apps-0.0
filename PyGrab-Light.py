import tkinter as tk
from tkinter import ttk
import wmi as wmi

dir(wmi)

gui_colour = "4f4f4f"
gui_width = 650
gui_height = 400


def set_colours(base_colour):
    """
    Returns a dict of colours {name(str):value(str)} either brighter or darker than base_colour for use in a gui
    The dict entries
    :param base_colour: string representing hex number "#xxxxxx"
    :return: dict of colour options as strings "#xxxxxx"
    """

    colour_set = {
        "bg": 0,
        "text": 0x797979,

        "checkbox_text": 0x797979,
        "checkbox_bold_text": 0xa9a9a9,
        "checkbox_bg": 0x272727,

        "input_text": -0x3e3e3e,
        "input_bg": 0x797979,

        "btn_text": 0x797979,
        "btn_bg": -0x242424,
        "btn_activebackground": -0x3e3e3e
    }
    base_colour = int(base_colour.strip("#"), 16)
    colours = {colour: "#{:06x}".format(min(max(base_colour + offset, 0), 0Xffffff)) for colour, offset in
               colour_set.items()}

    return colours


def select_clicked():
    print('select clicked')


def browse_clicked():
    print('browse clicked')


def de_select_clicked():
    print('Deselect clicked')


def media_clicked():
    print('Get media clicked')


def cancel_clicked():
    print('Cancel clicked')


def create_gui():
    # set up gui container
    root = tk.Tk()
    root.title("PyGrab - Camera photo grabber")
    root.geometry('{}x{}'.format(gui_width, gui_height))

    # set up gui frames
    container_frame = tk.Frame(master=root,
                               bg=set_colours(gui_colour)["bg"],
                               padx=10,
                               pady=10
                               )
    source_frame = tk.LabelFrame(master=container_frame,
                                 bg=set_colours(gui_colour)["bg"],
                                 text='Source'
                                 )
    canvas_frame = tk.Frame(master=container_frame,
                            bg=set_colours(gui_colour)["bg"]
                            )
    select_frame = tk.LabelFrame(master=container_frame,
                                 bg=set_colours(gui_colour)["bg"]
                                 )
    save_frame = tk.LabelFrame(master=container_frame,
                               bg=set_colours(gui_colour)["bg"],
                               text='Save options'
                               )

    # set up source frame widgets

    source_frame_text = tk.Label(source_frame,
                                 bg=set_colours(gui_colour)["bg"],
                                 fg=set_colours(gui_colour)["text"],
                                 anchor='nw',
                                 text='Get photos from: ',
                                 justify='left'
                                 )
    s = ttk.Style()
    s.configure('TCombobox',
                foreground=set_colours(gui_colour)["text"],
                background=set_colours(gui_colour)["btn_bg"],
                )

    source_frame_combobox = ttk.Combobox(source_frame,
                                         width=25,
                                         height=5,
                                         values='Dummy-1 Dummy-2',
                                         justify=tk.LEFT,
                                         )
    print(source_frame_combobox.winfo_class())
    # set up select frame widgets
    btn_select = tk.Button(select_frame,
                           overrelief="ridge",
                           fg=set_colours(gui_colour)["text"],
                           bg=set_colours(gui_colour)["btn_bg"],
                           relief="flat",
                           text="Select all",
                           command=select_clicked
                           )

    btn_de_select = tk.Button(select_frame,
                              overrelief="ridge",
                              fg=set_colours(gui_colour)["text"],
                              bg=set_colours(gui_colour)["btn_bg"],
                              relief="flat",
                              text="Deselect all",
                              command=de_select_clicked
                              )
    btn_get_media = tk.Button(select_frame,
                              overrelief="ridge",
                              fg=set_colours(gui_colour)["text"],
                              bg=set_colours(gui_colour)["btn_bg"],
                              relief="flat",
                              text="Get media",
                              command=media_clicked
                              )

    btn_cancel = tk.Button(select_frame,
                           overrelief="ridge",
                           fg=set_colours(gui_colour)["text"],
                           bg=set_colours(gui_colour)["btn_bg"],
                           relief="flat",
                           text="Cancel",
                           command=cancel_clicked
                           )

    # set up save frame widgets

    location_label = tk.Label(save_frame,
                              bg=set_colours(gui_colour)["bg"],
                              fg=set_colours(gui_colour)["text"],
                              text='Location:',
                              justify='left',
                              anchor='nw'
                              )
    location_text = tk.Label(save_frame,
                             bg=set_colours(gui_colour)["bg"],
                             fg=set_colours(gui_colour)["text"],
                             text='D:\\Ummy\\File\\Location',
                             justify='left',
                             anchor='nw'
                             )
    rename_text = tk.Label(save_frame,
                           bg=set_colours(gui_colour)["bg"],
                           fg=set_colours(gui_colour)["text"],
                           text='Rename Files:',
                           justify='left',
                           anchor='nw'
                           )
    example_label = tk.Label(save_frame,
                             bg=set_colours(gui_colour)["bg"],
                             fg=set_colours(gui_colour)["text"],
                             text='Example:',
                             justify='left',
                             anchor='nw'
                             )
    example_text = tk.Label(save_frame,
                            bg=set_colours(gui_colour)["bg"],
                            fg=set_colours(gui_colour)["text"],
                            text='001.jpg',
                            justify='left',
                            anchor='nw'
                            )

    btn_browse = tk.Button(save_frame,
                           overrelief="ridge",
                           fg=set_colours(gui_colour)["text"],
                           bg=set_colours(gui_colour)["btn_bg"],
                           relief="flat",
                           text="Browse...",
                           command=browse_clicked
                           )

    rename_combobox = ttk.Combobox(save_frame,
                                   width=25,
                                   height=5,
                                   values='"Do not rename" 00 01 000 0001 0000 0001',
                                   justify=tk.LEFT,
                                   )
    rename_combobox.set('Do not rename')
    # grid the frames

    container_frame.grid(column=0,
                         row=0,
                         sticky='news'
                         )
    source_frame.grid(column=0,
                      row=0,
                      padx=10,
                      pady=10,
                      sticky='nw'
                      )
    canvas_frame.grid(column=0,
                      row=1,
                      padx=10,
                      pady=10,
                      sticky='nw'
                      )
    select_frame.grid(column=0,
                      columnspan=2,
                      row=3,
                      padx=10,
                      pady=10,
                      sticky='swe'
                      )
    save_frame.grid(column=1,
                    row=0,
                    padx=10,
                    pady=10,
                    sticky='ne'
                    )

    # grid the widgets into their frames
    source_frame_text.grid(column=0,
                           row=0,
                           padx=5,
                           pady=5,
                           sticky='nw'
                           )

    source_frame_combobox.grid(column=1,
                               row=0,
                               padx=5,
                               pady=5,
                               sticky='e'
                               )

    btn_select.grid(column=0,
                    row=0,
                    padx=5,
                    pady=5,
                    sticky='sw'
                    )
    btn_de_select.grid(column=1,
                       row=0,
                       padx=5,
                       pady=5,
                       sticky='sw'
                       )
    btn_get_media.grid(column=2,
                       row=0,
                       padx=5,
                       pady=5,
                       sticky='se'
                       )
    btn_cancel.grid(column=3,
                    row=0,
                    padx=5,
                    pady=5,
                    sticky='se'
                    )

    location_label.grid(column=0,  # 'Location'
                        row=0,
                        padx=5,
                        pady=5,
                        sticky='w'
                        )

    location_text.grid(column=0,  # 'D:\Ummy\File\Location'
                       row=1,
                       padx=5,
                       pady=5,
                       sticky='w'
                       )
    rename_text.grid(column=0,  # 'Rename Files'
                     row=2,
                     padx=5,
                     pady=5,
                     sticky='w'
                     )
    rename_combobox.grid(column=0,
                         row=3,
                         padx=5,
                         pady=5,
                         sticky='w'
                         )

    example_label.grid(column=0,  # 'Example:'
                       row=4,
                       padx=5,
                       pady=5,
                       sticky='w'
                       )

    example_text.grid(column=1,  # '001,jpg"
                      row=4,
                      padx=5,
                      pady=5,
                      sticky='w'
                      )

    btn_browse.grid(column=1,
                    row=1,
                    padx=5,
                    pady=5,
                    sticky='e'
                    )

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    container_frame.columnconfigure(0, weight=1)
    container_frame.rowconfigure(0, weight=1)

    save_frame.grid_columnconfigure(0, weight=1)
    save_frame.grid_rowconfigure(0, weight=1)

    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_rowconfigure(0, weight=1)

    source_frame.grid_columnconfigure(0, weight=1)
    source_frame.grid_rowconfigure(0, weight=1)

    select_frame.grid_columnconfigure(2, weight=1)
    select_frame.grid_columnconfigure(3, weight=0)

    root.mainloop()


create_gui()
