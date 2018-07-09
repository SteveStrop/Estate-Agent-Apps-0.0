import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os
import win32api
import string
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk as PIL_ImageTK
from PIL import Image as PIL_Image
from shutil import copyfile
import ptpy as pt

gui_width = 995
gui_height = 640
data_save_path = Path('G:/Estate Agents/')
data_save_folder = data_save_path.absolute()


def download_photo(camera, handle, img):
    # Download all things that are not groups of other things.
    obj = camera.get_object(handle)
    with open(img, mode='wb') as f:
        f.write(obj.Data)


def get_photos():
    global handle, info
    try:
        camera = pt.PTPy()
    except pt.ptp.PTPError:
        return

    with camera.session():
        handles = camera.get_object_handles(0,
                                            all_storage_ids=True,
                                            all_formats=True,
                                            )
        parent_objs = []
        folder = ''
        i = 100
        root = os.path.join('G:', 'Imports')

        for handle in handles:  # #####TODO ONLY DOWNLOAD FROM SD CARD ##################
            info = camera.get_object_info(handle)
            parent_obj = info.ParentObject
            # print(parent_obj)
            if str(parent_obj)[0] == '3' and parent_obj not in parent_objs:
                # print(parent_obj)
                parent_objs.append(parent_obj)
                while True:
                    folder = '{:3}ND800'.format(i)
                    try:
                        os.mkdir(os.path.join(root, folder))
                        break
                    except FileExistsError:
                        i += 1
                i += 1
                if info.ObjectFormat != 'Association':
                    # print(os.path.join(root, folder, info.Filename))
                    download_photo(camera=camera,
                                   handle=handle,
                                   img=os.path.join(root, folder, info.Filename)
                                   )


def clear_frame(frm):
    for widget in frm.winfo_children():
        if widget.winfo_class() != 'TButton':
            widget.destroy()
    frm.update()


def btn_select_photos_clicked(frm, label, import_btn, rename_combo, rename_text):
    global thumb_list
    data_folders = find_folder()
    fld = data_folders[0]  # root folder
    thumb_list = filedialog.askopenfilenames(initialdir=Path(fld).parent, title='Select photos for import...')
    label.set(fld)  # TODO make sure all \ point the same way
    try:
        update_rename_example(rename_combo.current(), rename_text, thumb_list[0])
    except IndexError:
        pass
    populate_thumb_frame(thumbnail_list=thumb_list, frm=frm, width=5)
    import_btn.state(['!disabled'])
    rename_combo.state(['!disabled', 'readonly'])
    return thumb_list


def btn_import_clicked(files, destination, frm, rename):
    for i, src in enumerate(files):
        src = Path(src)
        dst = os.path.join(destination, src.name)
        dst = rename_file(Path(dst), rename, i)
        copyfile(src, dst)  # TODO add option to overwrite if folder not empty
    tk.messagebox.showinfo('Photo import', 'Photos imported to {}'.format(dst.parent), icon='info', parent=frm)
    clear_frame(frm)


def btn_add_dest_clicked(root, save_folders, frm):
    new_destination = Path(filedialog.askdirectory(initialdir=Path(root), title='Add a destination...'))
    save_folders.append(new_destination)
    radio = tk.Radiobutton(frm, text=new_destination.name,
                           value=new_destination,
                           variable=destination)
    radio.grid(sticky='w', padx=5, pady=5)
    radio.select()


def populate_destination_win(folder_list, frm):
    """
    displays radio button list of folder names in a tkinter Frame
     :param folder_list: folders
    :param frm: tkinter Frame
    :return: first radio button
    """
    clear_frame(frm)

    for i, file in enumerate(folder_list):
        filename = Path(data_save_path, file)

        radio = tk.Radiobutton(frm, text=str(file),
                               value=filename,
                               variable=destination)

        radio.grid(sticky='w', padx=5, pady=5)
        radio.deselect()
    destination.set(str(data_save_path / folder_list[0]))  # select first radio
    return destination


def populate_thumb_frame(thumbnail_list, frm, width):
    """
        displays thumbnails in a tkinter Frame

    :param thumbnail_list: [full path names to thumbnails]
    :param frm: tkinter Frame
    :param width: number of thumbs per row
    :return: None
    """
    size = 100, 100  # thumbnail size (max_x , max_y)

    # remove any existing thumbnails
    clear_frame(frm)

    for i, thumb in enumerate(thumbnail_list):
        im = PIL_Image.open(thumb)
        im.thumbnail(size)
        tkimage = PIL_ImageTK.PhotoImage(im)
        label = tk.Label(frm, image=tkimage)
        label.image = tkimage
        row = i // width
        column = i % width
        label.grid(sticky='nw', column=column, row=row, padx=5, pady=5)
        frm.update_idletasks()


def find_folder(search_folder='G:/Imports', file_types=('jpg', 'nef')):  # TODO don't I only need first folder?
    folder_paths = []
    for root, dirs, files in os.walk(search_folder):
        folder_paths += (root for file in files if
                         root not in folder_paths and
                         file[-3:].lower() in file_types)
    return folder_paths


def rename_file(file, rename, i):
    opts = [(None, None), ('2', 1), ('3', 1), ('2', 0), ('3', 0)]
    try:
        name = ('{:0' + str(opts[rename][0]) + '}').format(i + opts[rename][1])
        file = Path(file.parent, name + file.suffix)
    except TypeError:
        pass
    return file


def cancel_clicked(gui):
    gui.destroy()


def widget_grid(btn_add_dest, btn_cancel, btn_get_photos, btn_import, example_label, rename_combobox, source_label):
    btn_get_photos.grid(column=0,
                        row=0,
                        padx=5,
                        pady=(5, 15),
                        sticky='nw'
                        )
    source_label.grid(column=1,
                      row=0,
                      padx=5,
                      pady=(5, 15),
                      sticky='nw'
                      )
    btn_import.grid(column=1,
                    row=1,
                    padx=5,
                    pady=5,
                    sticky='sw'
                    )
    btn_cancel.grid(column=2,
                    row=1,
                    padx=5,
                    pady=5,
                    sticky='sw'
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
    btn_add_dest.grid(column=1,
                      row=0,
                      padx=5,
                      pady=5,
                      sticky='e'
                      )


def config_resize(canvas, container_frame, dest_frame, root):
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    container_frame.columnconfigure(0, weight=1)
    container_frame.columnconfigure(1, weight=0)
    container_frame.rowconfigure(0, weight=0)
    container_frame.rowconfigure(1, weight=1)
    container_frame.rowconfigure(2, weight=0)
    dest_frame.grid_columnconfigure(0, weight=1)
    dest_frame.grid_rowconfigure(0, weight=1)
    canvas.grid_columnconfigure(0, weight=1)
    canvas.grid_rowconfigure(0, weight=1)


def grid_frames(canvas, container_frame, dest_frame, import_frame, source_frame, thumb_frame):
    container_frame.grid(column=0,  # child of root
                         row=0,
                         sticky='news'
                         )
    source_frame.grid(column=0,
                      row=0,
                      padx=10,
                      pady=(0, 10),
                      sticky='new'
                      )
    canvas.grid(column=0,  # child of container_frame
                row=1,
                rowspan=3,
                padx=10,
                pady=10,
                sticky='news'
                )
    thumb_frame.grid(column=0,  # child of canvas
                     row=0,
                     sticky='news'
                     )
    dest_frame.grid(column=1,  # child of container_frame
                    row=0,
                    rowspan=2,
                    padx=10,
                    pady=(0, 10),
                    sticky='ne'
                    )
    import_frame.grid(column=1,  # child of container_frame
                      row=2,
                      padx=10,
                      pady=10,
                      sticky='new'
                      )


def setup_gui_frames(root):
    container_frame = tk.Frame(master=root,  # empty containing frame
                               padx=10,
                               pady=10
                               )
    source_frame = tk.LabelFrame(master=container_frame,  # frame for selecting import location of photos
                                 text='Source'
                                 )
    canvas = tk.Canvas(master=container_frame)  # frame for displaying photo thumbnails
    thumb_frame = tk.LabelFrame(master=canvas,  # frame for displaying selected photos
                                text='Thumbnails'
                                )
    dest_frame = tk.LabelFrame(master=container_frame,
                               text='Destination'
                               )
    import_frame = tk.LabelFrame(master=container_frame,  # frame for renaming files
                                 text='Photo import'
                                 )
    return canvas, container_frame, dest_frame, import_frame, source_frame, thumb_frame


def update_rename_example(value, label, example):
    opts = ['', ' 01', '001', ' 00', '000']
    if value == 0:
        label.set('Example: {}'.format(Path(example).name))
    else:
        label.set('Example: {}.{}'.format(opts[value], Path(example).name[-3:].lower()))


def create_gui():
    # set up gui container
    root = tk.Tk()
    root.title('PyGrab - Camera photo grabber')
    root.geometry('{}x{}'.format(gui_width, gui_height))
    global destination
    destination = tk.StringVar()

    # set up gui frames-----------------------------------------------------------------------------
    canvas, container_frame, dest_frame, import_frame, source_frame, thumb_frame = setup_gui_frames(root)

    # set up source frame widgets----------------------------------------------------------------------------
    source_text = tk.StringVar()
    source_text.set('G:/Imports')
    source_label = tk.Label(source_frame,
                            textvariable=source_text,
                            justify='left',
                            anchor='nw',
                            )
    btn_select_photos = ttk.Button(source_frame,
                                   text='Select photos...',
                                   command=
                                   lambda: btn_select_photos_clicked(thumb_frame, source_text, btn_import,
                                                                     rename_combobox, rename_example_text)
                                   )

    # set up destination frame widgets----------------------------------------------------------------------------------
    all_folders = (os.listdir(data_save_path.absolute()))
    save_folders = []
    for folder in all_folders:
        if folder.startswith('1000') or folder.startswith('HSS'):
            save_folders.append(folder)
    save_folder = populate_destination_win(save_folders, dest_frame)
    btn_add_dest = ttk.Button(dest_frame,
                              text="Add...",
                              command=
                              lambda: btn_add_dest_clicked(data_save_path, save_folders, dest_frame)
                              )

    # set up import frame widgets---------------------------------------------------------------------------------------
    btn_cancel = ttk.Button(import_frame,
                            text="Cancel",
                            command=lambda: cancel_clicked(root)
                            )
    rename_example_text = tk.StringVar()
    rename_example_text.set('Example:')
    rename_example_label = tk.Label(import_frame,
                                    textvariable=rename_example_text,
                                    justify='left',
                                    anchor='nw',
                                    )

    btn_import = ttk.Button(import_frame,
                            state='disabled',
                            text="Import",
                            command=lambda: btn_import_clicked(thumb_list, save_folder.get(), thumb_frame,
                                                               rename_combobox.current())
                            )
    rename_combobox = tk.ttk.Combobox(import_frame,
                                      state='disabled',
                                      width=25,
                                      height=5,
                                      values='"Do not rename" '
                                             '"Sequence  starting  01" '
                                             '"Sequence  starting 001" '
                                             '"Sequence starting   00" '
                                             '"Sequence starting  000" ',
                                      justify=tk.LEFT,
                                      )
    rename_combobox.current(1)
    rename_combobox.bind('<<ComboboxSelected>>',
                         lambda _: update_rename_example(rename_combobox.current(), rename_example_text, thumb_list[0])
                         )

    # grid and configure the frames-------------------------------------------------------------------------------------
    grid_frames(canvas, container_frame, dest_frame, import_frame, source_frame, thumb_frame)
    config_resize(canvas, container_frame, dest_frame, root)

    # grid the widgets into their frames--------------------------------------------------------------------------------
    widget_grid(btn_add_dest, btn_cancel, btn_select_photos, btn_import, rename_example_label, rename_combobox,
                source_label)

    # initialise the gui------------------------------------------------------------------------------------------------
    root.mainloop()


if __name__ == '__main__':
    get_photos()
    create_gui()


def set_colours(base_colour):
    """
    Returns a dict of colours {name(str): value(str)} either brighter or darker than base_colour for use in a gui
     :param base_colour: string representing hex number "#xxxxxx"
    :return: dict of colour options as strings "#xxxxxx"
    """

    colour_set = {
        "bg"                  : 0,
        "text"                : 0x797979,

        "checkbox_text"       : 0x797979,
        "checkbox_bold_text"  : 0xa9a9a9,
        "checkbox_bg"         : 0x272727,

        "input_text"          : -0x3e3e3e,
        "input_bg"            : 0x797979,

        "btn_text"            : 0x797979,
        "btn_bg"              : -0x242424,
        "btn_activebackground": -0x3e3e3e
    }
    base_colour = int(base_colour.strip("#"), 16)
    colours = {colour: "#{:06x}".format(min(max(base_colour + offset, 0), 0Xffffff)) for colour, offset in
               colour_set.items()}

    return colours


def find_drive_folders(search_drive='D800', file_types=('jpg', 'nef')):
    """
    walks through logical drive or path that partially matches search_drive and returns all folders
    containing file_types
    :param search_drive: string
    :param file_types: tuple
    :return: folder_paths a list of folders containing files of type(s) file_types
    """
    folder_paths = []
    drives = ['{}:'.format(d) for d in string.ascii_uppercase if os.path.exists('{}:'.format(d))]
    for drive in drives:
        cam_drive = win32api.GetVolumeInformation(str(Path(drive + '/')))
        if search_drive in cam_drive[0]:  # cam_drive[0] is name of drive
            for root, dirs, files in os.walk(drive):
                folder_paths += (root for file in files if
                                 root not in folder_paths and
                                 'RECYCLE' not in root and
                                 file[-3:].lower() in file_types)
            break
    print(folder_paths)
    return folder_paths
