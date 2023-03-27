from selenium import webdriver
from prereqs import scrape_reqs

def get_link_from_course_button(button, shadow_root, driver):
    # open course
    button.click()

    # find container with more info icon, click on icon
    button_id = button.get_attribute("id")
    container_id = button_id.replace("title", "container")
    script = f"return arguments[0].getElementById('{container_id}')"
    class_info = driver.execute_script(script, shadow_root)

    while not class_info:
        driver.implicitly_wait(2)
        class_info = driver.execute_script(script, shadow_root)

    icon = driver.execute_script("return arguments[0].querySelector('i.icon-warning-sign')", class_info)

    while not icon:
        icon = driver.execute_script("return arguments[0].querySelector('i.icon-info-sign')", class_info)
        if icon:
            break;
        driver.implicitly_wait(2)
        icon = driver.execute_script("return arguments[0].querySelector('i.icon-warning-sign')", class_info)

    icon.click()

    # wait for popup to load
    driver.implicitly_wait(2)

    # get the link and return it
    more_details_link = driver.execute_script("return arguments[0].querySelector('a')", class_info)
    return more_details_link.get_attribute("href")


def get_course_links_from_page(url, driver):

    # open page
    driver.get(url)

    # get department

    # get all course buttons
    host_element = driver.find_element_by_tag_name("ucla-sa-soc-app")
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", host_element)
    courses = driver.execute_script("return arguments[0].getElementById('resultsTitle')", shadow_root)
    buttons = driver.execute_script("return arguments[0].querySelectorAll('button')", courses)

    # get department abbreviation
    dept = driver.execute_script("return arguments[0].getElementById('spanSearchResultsHeader')", shadow_root).text
    dept_abbr = dept[dept.find('(')+1:dept.find(')')]

    course_links = {}
    for button in reversed(buttons):
        course = button.text
        first_space = course.find(' ')
        course_name = f"{dept_abbr} {course[:first_space]}"
        link = get_link_from_course_button(button, shadow_root, driver)
        # if getting link failed, change to None
        if link == 'javascript:void(0)':
            link = None
        course_links[course_name] = link

    return course_links


website = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23W&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
path = "/Users/sophiasharif/Desktop/projects/chromedriver_mac64/chromedriver"
driver = webdriver.Chrome(path)

links = get_course_links_from_page(website, driver)
print(links)

# print("Scraping " + link)
# reqs, prereqs = scrape_reqs(link, driver)
# print(reqs)
