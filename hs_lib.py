from selenium import webdriver
import re
from agent_lib import logon
from agent_lib import splash_screen


# create class to store the Job details
class HSJob:
    def __init__(self, href, ref_num, address, postcode, agent, appointment, floorplan, photos):
        self.href = href
        self.ref_num = ref_num
        self.address = address
        self.postcode = postcode
        self.agent = agent
        self.floorplan = floorplan
        self.photos = photos
        self.date = appointment[0:10]  # self.appointment.date? is it better?
        self.time = appointment[-5:]


def open_jobs_list():
    # splash_screen(text="Please wait",width=500, height=200, x=500, y=500, ms=5000)

    chrome_driver_path = "C:\Python36\selenium\webdriver\chrome\chromedriver.exe"
    browser = webdriver.Chrome(chrome_driver_path)

    logon(
        username="steve@orella.co.uk",
        password="Floop001",
        login_pg="https://www.housesimple.com/login",
        username_field="_username",
        landing_pg="https://www.housesimple.com/admin/home-visit-supplier/list",
        password_field="_password",
        login_btn="_submit",
        browser=browser
    )

    # get list of latest 25 jobs as displayed on
    jobs_data = browser.find_elements_by_css_selector(
        'td')  # [type0,Address0,Status0,Appointment time0,Action0,type1,...]
    links = browser.find_elements_by_link_text("Show")
    table_cols = 5
    row_count = int(len(jobs_data) / table_cols)  # used to divide jobs_data into rows
    jobs = []  # list of jobs, one for each row in the table
    postcode_regex = \
        r'([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]{0,1}[ABEHMNPRVWXY0-9]{0,1} {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)'
    for row_index in range(row_count):
        address = jobs_data[(table_cols * row_index) + 1].text
        match = re.search(postcode_regex, address)
        if match:
            postcode = match.group(0)
        else:
            postcode = "N/A"
        jobs.append(HSJob(
            href=links[row_index],
            ref_num=row_index,
            address=address,
            postcode=postcode,
            agent="House Simple",
            floorplan=True,
            photos=True,
            appointment=jobs_data[(table_cols * row_index) + 3].text
        ))

    # choose a HIP to open the corresponding jobs details
    row_num = int(input("Enter (zero based) row number to open"))

    links[row_num].click()  # not jobs[row_num].href.click???
    print("You have opened {} on {} at {}".format(jobs[row_num].postcode, jobs[row_num].date, jobs[row_num].time))
    input("press enter to exit")
    browser.quit()


if __name__ == "__main__":
    open_jobs_list()
