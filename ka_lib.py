from selenium import webdriver
import ast
from agent_lib import logon


def rgba_to_hex(rgba):
    r, g, b, alpha = ast.literal_eval(rgba.strip("rgba"))
    hex_value = '#%02x%02x%02x' % (r, g, b)
    return hex_value


# find the correct link and click it
def click_hip_link(jobs_list, job_hip_number, links):
    """Searches through a list of jobs to find matching ref_num then opens the page"""

    for job in jobs_list:  # this all looks ugly
        if job.hip == job_hip_number:
            for link in links:
                if job.href in link.get_attribute("href"):
                    link.click()
                    print("You have opened {} on {} at {}".format(job.hip, job.date, job.time))
                    return True
    return False


# create class to store the Job details
class KAJob:
    def __init__(self, href, hip, address, postcode, agent, appointment, floorplan, photos):
        self.href = href
        self.hip = hip
        self.address = address
        self.postcode = postcode
        self.agent = agent
        self.floorplan = floorplan
        self.photos = photos
        self.date = appointment[0:10] if (len(appointment) - 1) else "TBA"  # self.appointment.date? is it better?
        self.time = appointment[-5:] if (len(appointment) - 1) else "TBA"


def open_jobs_list():
    # define constants
    floorplan_bg_color = '#9fd69f'  # colour used to show floor plan required
    photo_bg_color = '#9fd69f'  # colour used to show photos required

    # create a new Chrome session
    chrome_driver_path = "C:\Python36\selenium\webdriver\chrome\chromedriver.exe"
    browser = webdriver.Chrome(chrome_driver_path)

    logon(
        username="xxxxxxxxxxxxxxxx",
        password='xxxxxxxxxxxxxxxx',
        login_pg="xxxxxxxxxxxxxxxxxxx",
        landing_pg="xxxxxxxxxxxxxxxxxxxxxxxxxxx",
        username_field="xxxxxxxxxxxxxxxxxxxx",
        password_field="xxxxxxxxxxxxxxxxxxxx",
        login_btn="xxxxxxxxxxxxxxxxxxxxxxx",
        browser=browser
    )

    # read the List of Current Jobs table into Job class
    jobs_data = browser.find_elements_by_css_selector('table.staffgridview td')
    links = browser.find_elements_by_tag_name("a")
    table_cols = 18
    row_count = int(len(jobs_data) / table_cols)
    jobs = []  # list of jobs, one for each row in the table
    for row_index in range(row_count):
        jobs.append(KAJob(
            href='Select$' + str(row_index),  # indexes 'Your Current List of Jobs'-table row, containing 'Open' link
            hip=jobs_data[(table_cols * row_index) + 6].text,
            address=jobs_data[(table_cols * row_index) + 7].text,
            postcode=jobs_data[(table_cols * row_index) + 8].text,
            agent=jobs_data[(table_cols * row_index) + 9].text,
            floorplan=rgba_to_hex(jobs_data[(table_cols * row_index) + 12].value_of_css_property(
                'background-color')) == floorplan_bg_color,  # if cell is green floorplan required
            photos=rgba_to_hex(
                jobs_data[(table_cols * row_index) + 13].value_of_css_property('background-color')) == photo_bg_color,
            appointment=jobs_data[(table_cols * row_index) + 17].text
        ))

    # get a list of all links on the page

    # choose a HIP to open the corresponding jobs details
    click_hip_link(jobs_list=jobs,
                   job_hip_number=input("Choose a HIP to open"),
                   links=links)
    # add error handling here ^
    input("press enter to exit")
    browser.quit()


if __name__ == "__main__":
    open_jobs_list()
