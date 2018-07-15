import tkinter as tk
import configparser
from selenium import webdriver
import re
import ast
from datetime import datetime
import os
import glob
import fnmatch
import win32api
import sys
import string
from pathlib import Path


# create class to store the Job details
class HSJob:

    def __init__(self, href, ref_num, address, postcode, agent, apt, floorplan, photos):
        self.href = href
        self.ref_num = ref_num
        self.address = address
        self.postcode = postcode
        self.agent = agent
        self.floorplan = floorplan
        self.photos = photos
        self.appointment = datetime.strptime(apt, '%d/%m/%Y @ %H:%M')  # self.appointment.date? is it better?


# create class to store the Job details
class KAJob:
    def __init__(self,
                 href=" ",
                 hip=" ",
                 address=" ",
                 postcode=" ",
                 agent=" ",
                 floorplan=" ",
                 notes=" ",
                 photos=" ",
                 contact=" ",
                 appt=" ",  # len(apt) > 1 and datetime.strptime(apt, '%d-%m-%Y %H:%M') or "TBA"
                 btn_fast_upload=" ",
                 btn_confirm_floorplan=" ",
                 btn_confirm_photos=" ",
                 btn_back=" ",
                 btn_save_apt=" ",
                 btn_change_apt=" ",
                 btn_save_no_apt=" ",
                 phone_primary=" ",
                 phone_secondary=" ",
                 phone_other=" ",
                 email=" ",
                 ):
        self.href = href
        self.hip = hip
        self.address = address
        self.postcode = postcode
        self.agent = agent
        self.floorplan = floorplan
        self.notes = notes
        self.photos = photos
        self.contact = contact
        self.appt = appt  # len(apt) > 1 and datetime.strptime(apt, '%d-%m-%Y %H:%M') or "TBA"
        self.btn_fast_upload = btn_fast_upload
        self.btn_confirm_floorplan = btn_confirm_floorplan
        self.btn_confirm_photos = btn_confirm_photos
        self.btn_back = btn_back
        self.btn_save_apt = btn_save_apt
        self.btn_change_apt = btn_change_apt
        self.btn_save_no_apt = btn_save_no_apt
        self.phone_primary = phone_primary
        self.phone_secondary = phone_secondary
        self.phone_other = phone_other
        self.email = email


def find_folders(root_folder, target_folder):
    # print(root_folder, root_folder + '**' + os.sep)
    # print(target_folder)

    return [file
            for file in glob.glob(pathname=root_folder + '**' + os.sep, recursive=True)
            if fnmatch.fnmatch(file, '*' + target_folder + '*')]


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
    return folder_paths


def rgba_to_hex(rgba):
    r, g, b, alpha = ast.literal_eval(rgba.strip("rgba"))
    hex_value = '#%02x%02x%02x' % (r, g, b)
    return hex_value


def logon(username, password, login_pg, landing_pg, username_field, password_field, login_btn, browser):
    """
    login_pg (str) : with www address of login page
    landing_pg (str) : www address of page to navigate to
    username_field (str) : HTML element to place username
    password_field (str) : HTML element to place password
    login_btn (obj) : submit form link
    brwsr (selenium obj) : browser session probably put that in here
    """""
    # Navigate to the application home page
    browser.get(login_pg)

    # get input fields
    username_field = browser.find_element_by_name(username_field)
    password_field = browser.find_element_by_name(password_field)

    # enter data
    username_field.send_keys(username)
    password_field.send_keys(password)

    # get the Login button & click it
    browser.find_element_by_name(login_btn).click()

    # navigate to the home visits list page
    browser.get(landing_pg)

    return browser


def splash_screen(text, width, height, x, y, ms):
    """
    displays 'text' in a borderless splash screen window
    'width' wide, 'height' high at screen co-ords 'x', 'y' for 'ms' milliseconds
    """
    # initialise GUI window
    gui = tk.Tk()
    gui.overrideredirect(True)
    gui.geometry("{}x{}+{}+{}".format(width, height, x, y))

    tk.Label(gui, text=text).place(relx=.5, rely=.5, anchor="center")

    gui.after(ms, lambda: gui.destroy())
    gui.update()


def click_hip_link(jobs_list, hip_to_click, links):
    """Searches through job_list to find matching ref_num then opens the page
    jobs_list: KAJob objects
    links : list of html links"""

    for job in jobs_list:  # can this be simplified
        if job.hip == hip_to_click:
            for link in links:
                if job.href in link.get_attribute("href"):  # link.href is javascript
                    # job.href is unique part of the java
                    link.click()
                    print("You have opened {} on {} at {}".format(job.hip, job.appointment.date(),
                                                                  job.appointment.time()))
                    return True
    return False


#     )
# def create_HSjobsclass()
#     # get list of latest 25 jobs as displayed on
#
#     links = browser.find_elements_by_link_text("Show")
#     jobs = []  # list of jobs, one for each row in the table
#     row_index = 0
#     postcode_regex = \
#         r'([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]{0,1}[ABEHMNPRVWXY0-9]{0,1} {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)'
#     jobs_data = browser.find_elements_by_css_selector('tr')
#     print(jobs_data)
#     for row in jobs_data[1:]:
#         print(row.text)
#         cells = (row.find_elements_by_css_selector('td'))
#         print(cells)
#         address = cells[1].text
#         match = re.search(postcode_regex, address)
#         jobs.append(HSJob(
#             href=links[row_index],
#             ref_num=row_index,
#             address=address,
#             postcode=match and match.group(0) or "N/A",
#             agent="House Simple",
#             floorplan=True,
#             photos=True,
#             apt=cells[3].text
#         ))
#         row_index += 1

def open_jobs_list(gui, agent):
    chrome_driver_path = "C:\Python36\selenium\webdriver\chrome\chromedriver.exe"
    browser = webdriver.Chrome(chrome_driver_path)
    gui.destroy()
    config = configparser.ConfigParser()
    config.read('PyWEB.ini')
    logon(
        username=config[agent]['username'],
        password=config[agent]['password'],
        login_pg=config[agent]['login_pg'],
        username_field=config[agent]['username_field'],
        landing_pg=config[agent]['landing_pg'],
        password_field=config[agent]['password_field'],
        login_btn=config[agent]['login_btn'],
        browser=browser
    )

    jobs_list = html_table_read(browser, "table.staffgridview")  # a list of dictionaries for each job
    #
    #
    #
    # use browser.find_element_by_name("?????????")  # .get_attribute("href")
    #
    #
    #
    return browser
    # get a list of all links on the page

    # choose a HIP to open the corresponding jobs details


def html_table_read(browser, table_name):
    """
    Reads data from html table assuming first row are column headings
    :param browser: a selenium browser object
    :param table_name: unique css identifier of table to read
    :return: list of dicts, one for each row k,v = column heading : data
    """

    # create a dictionary of table headings
    headings = browser.find_elements_by_css_selector(table_name + ' th')
    headings_dict = {i: (heading.text.strip() or 'Col:{}'.format(i)) for i, heading in enumerate(headings)}
    rows = browser.find_elements_by_css_selector(table_name + ' tr')
    line_data = [{headings_dict[i]: data.text for i, data in enumerate(row.find_elements_by_css_selector('td'))} for row
                 in rows]
    return line_data


def get_ka_notes(browser, tag="ctl00$main$textBoxCaseNotes"):
    """
    partial scrape of KeyAGENT job page.
    :param browser: a selenium browser object pointing to the KeyAGENT job url
    :param tag: unique html identifier of notes tag to read
    :return: dictionary of notes indexed by note type
    """
    raw_text = browser.find_element_by_name(tag).text
    matches = re.findall(r"(.*?):(.*)", raw_text)
    notes_dict = {note.strip(): match.strip() for note, match in matches if match.strip() != "NA"}
    note_to_delete = "Please attempt to book the earliest appointment based on the 3 following slots chosen by the " \
                     "keyholder:  Once you input a time you can make into the system, if the keyholder is a mobile " \
                     "number, a confirmation text will be sent so you do not need to call them. If the  call to" \
                     " confirm. If you CAN’T facilitate any of the chosen slots, please call the keyholder to arrange" \
                     " an alternative date and time."
    try:
        if notes_dict["General Notes"] == note_to_delete:
            del notes_dict["General Notes"]
    except KeyError:  # if General note are NA then they don't exist
        pass

    try:
        del notes_dict["Sample Selector"]
    except KeyError:  # if SAmple Selector are NA then they don't exist
        pass

    return notes_dict


# noinspection Annotator
def read_ka_job_page(browser):
    job = KAJob

    # get hip number
    job.hip = browser.find_element_by_id("ctl00_text_LabelHipref").text

    #  get address & postcode
    raw_text = browser.find_element_by_id("ctl00_text_LabelAddress").text
    # 1st group captures address. 2nd group captures postcode
    # noinspection Annotator
    matches = re.findall(
        r"(.*?)([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]{0,1}[ABEHMNPRVWXY0-9]{0,1} {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)",
        raw_text)[0]
    job.address = matches[0].replace(",", "").strip()
    job.postcode = matches[1]

    #  get contact details
    raw_text = browser.find_element_by_id("ctl00_main_LabelVendor").text
    # 1st group captures Contact name. 2nd is primary tel 3rd is secondary tel 4th is other tel. 5th is email
    matches = re.findall(r"(?:.*?:)(.*?)DAY:(.*?)MOB:(.*?)EVE:(.*?)Email:(.*?)$", raw_text)[0]
    job.contact = matches[0].strip()
    job.phone_primary = matches[1].strip()
    job.phone_secondary = matches[2].strip()
    job.phone_other = matches[3].strip()
    job.email = matches[4].replace("N/A", "").strip()

    #  get floorplan requirements
    job.floorplan = browser.find_element_by_id("ctl00_main_LabelRequiresFloorplan").text == "Yes" or False

    #  get photos required
    raw_text = browser.find_element_by_id("ctl00_main_LabelRequiresPhotos").text
    matches = re.findall(r"(.{2,3}) -.*?(\d{1,2})", raw_text)[0]
    job.photos = matches[0] == "Yes" and matches[1] or ""

    # get appointment fields
    appt_date_field = browser.find_element_by_name("ctl00$main$TextBoxAppointmentDate")  # .get_attribute("value")
    appt_time_field = browser.find_element_by_name("ctl00$main$TextBoxAppointmentTime")  # .get_attribute("value")

    # get links
    try:
        job.btn_save_apt = browser.find_element_by_name("ctl00$main$ButtonSaveAppointment")
    except:
        job.btn_change_apt = browser.find_element_by_name("ctl00$main$ButtonChangeAppointment")

    try:
        job.btn_save_no_apt = browser.find_element_by_name("ctl00$main$ButtonSaveNoAppointment")
    except:
        job.btn_save_no_apt = ""
    job.btn_fast_upload = browser.find_element_by_name("ctl00$main$ButtonFastUpload")
    job.btn_confirm_floorplan = browser.find_element_by_name("ctl00$main$ConfirmFloorplanUpload")
    job.btn_confirm_photos = browser.find_element_by_name("ctl00$main$ConfirmPhotoUpload")
    job.btn_back = browser.find_element_by_name("ctl00$main$ButtonBack")

    # get notes
    job.notes = get_ka_notes(browser)

    return job


def populate_scrolling_win(folder_list, frame):
    checkbox = []
    var = []
    for i, folder in enumerate(folder_list):
        var.append(tk.IntVar())
        checkbox.append(tk.Checkbutton(frame, text=folder, variable=var[i]))
        checkbox[i].grid(sticky="w")


if __name__ == "__main__":
    # READ_KA_JOB_PAGE###########################################################################
    # chrome_driver_path = "C:\Python36\selenium\webdriver\chrome\chromedriver.exe"
    # browser = webdriver.Chrome(chrome_driver_path)
    # browser.get("http://www.keyagent-portal.co.uk/Site/Dea/Dea.aspx?DEA=272ca14b-8535-453f-bf30-10e5c0318651"
    #            "&Quote=a36a1465-ca4c-4950-8aab-c8d47f6df45c&Logged=True")
    # job = (read_ka_job_page(browser))
    # print("\n".join((["{}: {}".format(k, v) for k, v in job.__dict__.items() if str(k).find("__")])))
    ############################################################################################################

    # FIND_FOLDERS#########################################################################################
    find_folders("A:\Estate Agent Archive", "41 Newington")
