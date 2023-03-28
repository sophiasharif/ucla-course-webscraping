from utils import DEPARTMENT_ABBREVIATIONS
import json


def scrape_courses_to_json(websites, file_name, driver):
    courses = get_courses(websites, driver)

    with open(f'./data/courses/{file_name}.json', 'w') as file:
        json.dump(courses, file)


def get_courses(websites: list[str], driver) -> dict:
    course_info = {}
    for website in websites:
        courses_and_links = get_course_links_from_page(website, driver)
        for course in courses_and_links:
            if course not in course_info:
                course_info[course] = scrape_class_info(courses_and_links[course], driver)
    return course_info


def parse_prerequisites(prerequisites: str):
    # edge case
    if prerequisites == "":
        return []

    # change departments to abbreviations
    for dept in DEPARTMENT_ABBREVIATIONS:
        prerequisites = prerequisites.replace(dept, DEPARTMENT_ABBREVIATIONS[dept])

    # Separate required courses and optional groups
    components = split_string(prerequisites)
    parsed_output = []

    for component in components:
        # If there are parentheses, it's an optional group
        if ' or ' in component:
            optional_courses = component.split(' or ')
            parsed_output.append([course.strip("() ") for course in optional_courses])
        else:
            parsed_output.append(component.strip("() "))

    return parsed_output


def split_string(input_string):

    res = []
    in_parentheses = False
    current = ""
    i = 0
    while i < len(input_string):
        c = input_string[i]

        if c == '(':
            current += c
            in_parentheses = True
        elif c == ')':
            current += c
            in_parentheses = False
            res.append(current)
            current = ""
        elif in_parentheses:
            current += c
        elif input_string[i:i+5] == " and ":
            if current:
                res.append(current)
            current = ""
            i = i+4
        else:
            current += c

        i += 1

    if not current.isspace():
        res.append(current)

    return res


def scrape_class_info(website: str, driver) -> dict:

    driver.get(website)
    course_info = {}

    # locate pre-req table
    host_element = driver.find_element_by_tag_name("ucla-sa-soc-app")
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", host_element)

    # get title
    title_div = driver.execute_script("return arguments[0].getElementById('subject_class')", shadow_root)
    title = title_div.text
    topic = title[title.find('-') + 2:]
    course_info['title'] = topic

    # get description
    description_div = driver.execute_script("return arguments[0].getElementById('section')", shadow_root)
    description = driver.execute_script("return arguments[0].querySelector('p.section_data')", description_div)
    course_info['description'] = description.text

    # get prereqs and coreqs
    prereqs = ""
    coreqs = ""
    table = driver.execute_script("return arguments[0].getElementById('course_requisites')", shadow_root)
    rows = driver.execute_script("return arguments[0].querySelectorAll('tr')", table)
    for row in rows[1:]:
        cells = driver.execute_script("return arguments[0].querySelectorAll('td')", row)
        course = cells[0].text
        # check if it's co-requisite
        if cells[3].text == "Yes":
            coreqs += course + " "
        prereqs += course + " "
    course_info["pre-reqs"] = parse_prerequisites(prereqs)
    course_info["co-reqs"] = parse_prerequisites(coreqs)

    return course_info


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
            continue
        course_links[course_name] = link

    return course_links
