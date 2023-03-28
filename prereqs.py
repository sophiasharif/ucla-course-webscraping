from utils import DEPARTMENT_ABBREVIATIONS


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

