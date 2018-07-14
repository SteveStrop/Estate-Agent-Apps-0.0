import os
import tkinter as tk
from shutil import copyfile
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from math import trunc
import ptpy as pt
from PIL import Image as PIL_Image
from PIL import ImageTk as PIL_ImageTK

gui_width = 1024
gui_height = 640
data_save_folder = os.path.join('G:', 'Estate Agents')


def download_photo(camera, handle, img):
    obj = camera.get_object(handle)
    with open(img, mode='wb') as f:
        f.write(obj.Data)


def get_photos(progress_bar):
    """
    Downloads photos on sd card in nikon D800

    :param source_text:
    :return:
    """
    # setup folder naming-------------------------------------------------------------------------
    i = 100  # index for folder name
    folder = ''
    # sd card ParentObjects are in format 3#########
    sd = 300000000  # use sd = 200000000 if only sd card in camera (Careful NOT tested)
    try:
        camera = pt.PTPy()
    except pt.ptp.PTPError:  # camera not connected
        return

    with camera.session():
        handles = camera.get_object_handles(0, all_storage_ids=True, all_formats=True, )
        parent_objs = []  # a list of sd card folder ids

        import_folder = os.path.join('G:', 'Imports')
        step = trunc(100 / len(handles))
        # loop through the list of photos on the sd card downloading as necessary
        for handle in handles:
            progress_bar.step(step)
            progress_bar.update()
            info = camera.get_object_info(handle)
            parent_obj = info.ParentObject
            if not (parent_obj // sd):  # sd card ParentObjects are in format 3########
                pass
            else:

                # map sd card folder structure to import folder
                if parent_obj not in parent_objs:  # is this a new sd folder

                    # add the folder id  to list of folder ids
                    parent_objs.append(parent_obj)

                    # create the local folder mapped from the sd folder
                    while True:
                        folder = '{:3}ND800'.format(i)
                        try:
                            os.mkdir(os.path.join(import_folder, folder))
                            i += 1  # increment the folder name ready for the next one
                            break
                        except FileExistsError:  # that folder already exists so increment the name and try again
                            i += 1

                #  download the photo
                download_photo(camera=camera,
                               handle=handle,
                               img=os.path.join(import_folder, folder, info.Filename),
                               )


def clear_frame(frm):
    """
    destroys all widgets from a tkinter frame
    :param frm: tk inter frame object
    :return: none
    """
    for widget in frm.winfo_children():
        widget.destroy()
        frm.update()


def btn_select_photos_clicked(canvas, root, canvas_window, thumb_frame, source_text, btn_import, rename_combobox,
                              rename_example_text):
    global thumb_list
    source_text.set('Connecting to photo storage location. Please wait...')
    root.update_idletasks()
    fld = 'G:/Imports'
    thumb_list = filedialog.askopenfilenames(initialdir=fld, title='Select photos for import...')
    try:
        update_rename_example_text(rename_combobox.current(), rename_example_text, thumb_list[0])
    except IndexError:
        pass
    source_text.set('Displaying thumbnails. Please wait...')
    root.update_idletasks()
    populate_thumb_frame(canvas=canvas, thumbnail_list=thumb_list, frm=canvas_window)
    btn_import.state(['!disabled'])
    rename_combobox.state(['!disabled', 'readonly'])
    source_text.set(fld)  # TODO make sure all \ point the same way
    thumb_frame.update_idletasks()

    return thumb_list


def btn_import_clicked(thumb_list, destination, thumb_frame, rename_style, frame_to_clear):
    for index, src in enumerate(thumb_list):
        dst = rename_file(os.path.join(destination, os.path.split(src)[1]), rename_style, index)
        if os.path.isfile(dst):
            tk.messagebox.showerror('Photo import', 'File exists, choose a different location', parent=thumb_frame)
            return
        else:
            copyfile(src, dst)  # TODO add option to overwrite if folder not empty
    tk.messagebox.showinfo('Photo import', 'Photos imported to {}'.format(os.path.split(dst)[0]), icon='info',
                           parent=thumb_frame)
    clear_frame(frame_to_clear)


def btn_add_dest_clicked(destination_folders, dest_frame, destination):
    new_destination = filedialog.askdirectory(initialdir=data_save_folder, title='Add a destination...')
    destination_folders.append(new_destination)
    radio = tk.Radiobutton(dest_frame, text=os.path.split(new_destination)[1],
                           value=new_destination,
                           variable=destination)
    radio.grid(sticky='w', padx=5, pady=5)
    radio.select()


def btn_cancel_clicked(root):
    root.destroy()


def populate_thumb_frame(canvas, thumbnail_list, frm, width=5):
    size = 100, 100  # thumbnail size (max_x , max_y)

    # remove any existing thumbnails
    clear_frame(frm)

    # create a thumbnail for each photo
    for i, thumb in enumerate(thumbnail_list):
        im = PIL_Image.open(thumb)
        im.thumbnail(size)
        tkimage = PIL_ImageTK.PhotoImage(im)
        label = tk.Label(frm, image=tkimage)
        label.image = tkimage
        # grid thumbnail into the canvas window
        row = i // width
        column = i % width
        label.grid(sticky='nw', column=column, row=row, padx=5, pady=5)
        frm.update_idletasks()

        # Configure size of canvas's scrollable zone
        canvas.configure(scrollregion=(0, 0, frm.winfo_width(), frm.winfo_height()))


def rename_file(file, rename, i):
    opts = [(None, None), ('2', 1), ('3', 1), ('2', 0), ('3', 0)]
    try:
        name = ('{:0' + str(opts[rename][0]) + '}').format(i + opts[rename][1])
        file = os.path.join(os.path.split(file)[0], name + str(os.path.splitext(file)[1]))
    except TypeError:
        pass
    return file


def update_rename_example_text(value, rename_example_text, example):
    opts = ['', ' 01', '001', ' 00', '000']
    if value == 0:
        rename_example_text.set('Example: {}'.format(os.path.split(example)[1]))
    else:
        rename_example_text.set('Example: {}{}'.format(opts[value], os.path.splitext(example)[1].lower()))


def create_gui():
    # set up gui container--------------------------------------------------------------------------set up gui container
    root = tk.Tk()
    root.title('PyGrab - Camera photo grabber')
    root.geometry('{}x{}'.format(gui_width, gui_height))
    destination = tk.StringVar()

    # set up gui frames--------------------------------------------------------------------------------set up gui frames
    container_frame = tk.Frame(master=root,  # empty containing frame
                               padx=10,
                               pady=10
                               )
    source_frame = tk.LabelFrame(master=container_frame,  # frame for selecting import location of photos
                                 text='Source'
                                 )
    thumb_frame = tk.LabelFrame(master=container_frame,  # frame for displaying selected photos
                                text='Thumbnails'
                                )
    canvas = tk.Canvas(master=thumb_frame)  # canvas for scroll bars displaying photo thumbnails
    canvas_window = tk.Frame(master=canvas)  # frame within canvas to display thumbnails
    destination_frame = tk.LabelFrame(master=container_frame,
                                      text='Destination'
                                      )
    import_frame = tk.LabelFrame(master=container_frame,  # frame for renaming files
                                 text='Photo import'
                                 )

    # set up source frame widgets------------------------------------------------------------set up source frame widgets
    source_text = tk.StringVar()
    source_label = tk.Label(source_frame,
                            textvariable=source_text,
                            justify='left',
                            anchor='nw',
                            )
    btn_select_photos = ttk.Button(source_frame,
                                   text='Select photos...',
                                   command=
                                   lambda: btn_select_photos_clicked(canvas=canvas,
                                                                     root=root,
                                                                     canvas_window=canvas_window,
                                                                     thumb_frame=thumb_frame,
                                                                     source_text=source_text,
                                                                     btn_import=btn_import,
                                                                     rename_combobox=rename_combobox,
                                                                     rename_example_text=rename_example_text
                                                                     )
                                   )
    progress_bar = ttk.Progressbar(source_frame, length=200)
    # set up destination frame widgets--------------------------------------------------set up destination frame widgets

    # get list of currently open jobs which are valid save destinations for the photos
    destination_folders = [folder
                           for folder in os.listdir(data_save_folder)
                           if folder.startswith('1000') or folder.startswith('HSS')
                           ]

    # set up the radio buttons for the destination folders
    for i, file in enumerate(destination_folders):
        filename = os.path.join(data_save_folder, file)

        radio = tk.Radiobutton(destination_frame, text=str(file),
                               value=filename,
                               variable=destination)
        radio.grid(sticky='w', padx=5, pady=5)
        radio.deselect()
    destination.set(os.path.join(data_save_folder, destination_folders[0]))
    # str(data_save_path / destination_folders[0]))  # select first radio

    # set up the add destination button
    btn_add_dest = ttk.Button(destination_frame,
                              text="Add...",
                              command=
                              lambda: btn_add_dest_clicked(destination_folders=destination_folders,
                                                           dest_frame=destination_frame,
                                                           destination=destination)
                              )

    # set up import frame widgets------------------------------------------------------------set up import frame widgets

    # set up import button
    btn_import = ttk.Button(import_frame,
                            state='disabled',
                            text="Import",
                            command=lambda: btn_import_clicked(thumb_list=thumb_list,
                                                               destination=destination.get(),
                                                               thumb_frame=thumb_frame,
                                                               rename_style=rename_combobox.current(),
                                                               frame_to_clear=canvas_window,
                                                               )
                            )

    # set up cancel button
    btn_cancel = ttk.Button(import_frame,
                            text="Cancel",
                            command=lambda: btn_cancel_clicked(root=root)
                            )

    # setup rename combobox
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
                         lambda _: update_rename_example_text(value=rename_combobox.current(),
                                                              rename_example_text=rename_example_text,
                                                              example=thumb_list[0])
                         )

    # set up example rename text
    rename_example_text = tk.StringVar()
    rename_example_text.set('Example:')
    rename_example_label = tk.Label(import_frame,
                                    textvariable=rename_example_text,
                                    justify='left',
                                    anchor='nw',
                                    )

    # grid the frames------------------------------------------------------------------------------------grid the frames

    container_frame.grid(column=0,  # child of root
                         row=0,
                         sticky='news'
                         )
    thumb_frame.grid(column=0,  # child of canvas
                     row=1,
                     rowspan=3,
                     padx=10,
                     pady=10,
                     sticky='news'
                     )
    canvas.grid(column=0,  # child of container_frame
                row=0,
                sticky='news'
                )
    source_frame.grid(column=0,
                      row=0,
                      padx=10,
                      pady=(0, 10),
                      sticky='new'
                      )
    destination_frame.grid(column=1,  # child of container_frame
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
    # configure frame resize behaviour--------------------------------------------------configure frame resize behaviour

    # configure root frame to expand evenly on window resize
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # configure container window
    container_frame.grid_columnconfigure(0, weight=1)  # TODO
    container_frame.grid_columnconfigure(1, weight=0)  # TODO
    container_frame.grid_rowconfigure(0, weight=0)  # TODO
    container_frame.grid_rowconfigure(1, weight=1)  # TODO
    container_frame.grid_rowconfigure(2, weight=0)  # TODO
    destination_frame.grid_columnconfigure(0, weight=1)  # TODO
    destination_frame.grid_rowconfigure(0, weight=1)  # TODO
    # canvas.grid_columnconfigure(0, weight=1)  # TODO
    # canvas.grid_rowconfigure(0, weight=1)  # TODO
    thumb_frame.grid_rowconfigure(0, weight=1)  # TODO
    thumb_frame.grid_columnconfigure(0, weight=1)  # TODO

    # scrollbars for canvas------------------------------------------------------------------------Scrollbars for canvas
    v_scroll = tk.Scrollbar(master=thumb_frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scroll.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=v_scroll.set)

    # pts the canvas window in the canvas scrollable zone
    canvas.create_window(0, 0, window=canvas_window, anchor='nw')

    # grid the widgets into their frames----------------------------------------------grid the widgets into their frames

    btn_select_photos.grid(column=0,
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
    rename_example_label.grid(column=0,  # 'Example: 001.jpg'
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
    # download photos from camera------------------------------------------------------------download photos from camera
    source_text.set('Downloading photos from camera. Please wait...')
    progress_bar.grid(column=2, row=0, pady=(0, 10))
    root.update()
    get_photos(progress_bar)
    source_text.set('Choose folder for import')
    progress_bar.destroy()

    # initialise the gui------------------------------------------------------------------------------------------------
    root.mainloop()


if __name__ == '__main__':
    create_gui()
