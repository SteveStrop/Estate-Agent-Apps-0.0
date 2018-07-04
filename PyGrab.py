import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os

# gui_colour = "4f4f4f"
gui_width = 1000
gui_height = 600
data_save_path = Path('G:/Estate Agents/')
data_save_folder = (str(data_save_path))


def populate_save_win(folder_list, frm):
    """
    displays folder names in a tkinter Frame
    :param folder_list: folders
    :param frm: tkinter Frame
    :return: None
    """
    destination = tk.StringVar()
    for i, file in enumerate(folder_list):
        filename = data_save_path / file

        radio = tk.Radiobutton(frm, text=str(file),
                               value=filename,
                               variable=destination)

        radio.grid(sticky='w', padx=5, pady=5)
        radio.deselect()
    destination.set(str(data_save_path / folder_list[0]))  # select first radio
    return destination


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
    print('browseerer clicked')


def de_select_clicked():
    print('Deselect clicked')


def media_clicked(destination):
    print('Sending fiels to: ', destination)


def cancel_clicked(gui):
    gui.destroy()


def create_gui():
    # set up gui container
    root = tk.Tk()
    root.title("PyGrab - Camera photo grabber")
    root.geometry('{}x{}'.format(gui_width, gui_height))

    # set up gui frames
    container_frame = tk.Frame(master=root,  # empty containing frame
                               padx=10,
                               pady=10
                               )
    source_frame = tk.LabelFrame(master=container_frame,  # frame for selecting location of photos
                                 text='Source'
                                 )
    canvas_frame = tk.Frame(master=container_frame)  # frame for displaying photo thumbnails
    select_frame = tk.LabelFrame(master=container_frame)
    dest_frame = tk.LabelFrame(master=container_frame,
                               text='Destination'
                               )
    rename_frame = tk.LabelFrame(master=container_frame,  # frame for renaming files
                                 text='Rename files'
                                 )

    # set up source frame widgets

    source_frame_text = tk.Label(source_frame,
                                 anchor='nw',
                                 text='Get photos from: ',
                                 justify='left'
                                 )

    source_frame_combobox = ttk.Combobox(source_frame,
                                         width=25,
                                         height=5,
                                         values='Dummy-1 Dummy-2',
                                         justify=tk.LEFT,
                                         )

    # set up save frame widgets

    location_label = tk.Label(dest_frame,
                              text='Location:',
                              justify='left',
                              anchor='nw'
                              )

    path = Path('G:/Estate Agents/')
    all_folders = (os.listdir(str(path)))
    save_folders = []
    for folder in all_folders:
        if folder.startswith('1000') or folder.startswith('HSS'):
            save_folders.append(folder)
    save_folder = populate_save_win(save_folders, dest_frame)
    print(type(save_folder))

    # set up select frame widgets
    btn_select = tk.Button(select_frame,
                           text="Select all",
                           command=select_clicked
                           )

    btn_de_select = tk.Button(select_frame,
                              text="Deselect all",
                              command=de_select_clicked
                              )
    btn_get_media = tk.Button(select_frame,
                              text="Get media",
                              command=lambda: media_clicked(save_folder.get())
                              )

    btn_cancel = tk.Button(select_frame,
                           text="Cancel",
                           command=lambda: cancel_clicked(root)
                           )

    # set up rename_frame widgets

    example_text = tk.StringVar()
    example_text.set('Example: 001.jpg')
    example_label = tk.Label(rename_frame,
                             textvariable=example_text,
                             justify='left',
                             anchor='nw',
                             )

    btn_browse = tk.Button(dest_frame,
                           text="Browse...",
                           command=browse_clicked
                           )

    rename_combobox = ttk.Combobox(rename_frame,
                                   width=25,
                                   height=5,
                                   values='"Do not rename" 00 01 000 001 0000 0001',
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
    dest_frame.grid(column=1,
                    row=0,
                    padx=10,
                    pady=10,
                    sticky='ne'
                    )
    rename_frame.grid(column=1,
                      row=1,
                      padx=10,
                      pady=10,
                      sticky='news'
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

    rename_combobox.grid(column=0,
                         row=0,
                         padx=5,
                         pady=5,
                         sticky='w'
                         )

    example_label.grid(column=0,  # 'Example: 001.jpg'
                       row=1,
                       padx=5,
                       pady=5,
                       sticky='w'
                       )

    btn_browse.grid(column=1,
                    row=0,
                    padx=5,
                    pady=5,
                    sticky='e'
                    )

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    container_frame.columnconfigure(0, weight=1)
    container_frame.rowconfigure(0, weight=1)

    dest_frame.grid_columnconfigure(0, weight=1)
    dest_frame.grid_rowconfigure(0, weight=1)

    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_rowconfigure(0, weight=1)

    source_frame.grid_columnconfigure(0, weight=1)
    source_frame.grid_rowconfigure(0, weight=1)

    select_frame.grid_columnconfigure(2, weight=1)
    select_frame.grid_columnconfigure(3, weight=0)

    root.mainloop()


create_gui()
