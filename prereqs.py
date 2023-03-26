from selenium import webdriver

department_to_code = {"Mathematics": "MATH", "Program in Computing": "PIC", "Computer Science": "COM SCI", "Civil and Environmental Engineering": "C&EE", "Electrical and Computer Engineering": "EC ENGR", "Statistics": "STATS", "Physics": "PHYSICS"}

# set up driver
path = "/Users/sophiasharif/Desktop/projects/chromedriver_mac64/chromedriver"
driver = webdriver.Chrome(path)


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


def parse_prerequisites(prerequisites: str):
    # edge case
    if prerequisites == "":
        return []

    # Separate required courses and optional groups
    components = split_string(prerequisites)
    parsed_output = []

    for component in components:
        # If there are parentheses, it's an optional group
        if '(' in component:
            optional_courses = component.split(' or ')
            parsed_output.append([process_course(course) for course in optional_courses])
        else:
            parsed_output.append(process_course(component))

    return parsed_output


def process_course(course: str):
    course = course.strip("() ")
    department = course[:course.rfind(" ")]
    return course.replace(department, department_to_code[department])


def scrape_reqs(website) :
    driver.get(website)

    # locate pre-req table
    host_element = driver.find_element_by_tag_name("ucla-sa-soc-app")
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", host_element)
    table = driver.execute_script("return arguments[0].getElementById('course_requisites')", shadow_root)
    rows = driver.execute_script("return arguments[0].querySelectorAll('tr')", table)

    # create infix pre-req data string
    prereqs = ""
    coreqs = ""
    for row in rows[1:]:
        cells = driver.execute_script("return arguments[0].querySelectorAll('td')", row)
        course = cells[0].text
        # check if it's co-requisite
        if cells[3].text == "Yes":
            coreqs += course + " "
        prereqs += course + " "

    return parse_prerequisites(prereqs), parse_prerequisites(coreqs)


website = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=23S&subj_area_cd=COM%20SCI&crs_catlg_no=0148%20%20M%20&class_id=187588200&class_no=%20001%20%20"

prereqs, coreqs = scrape_reqs(website)
print(prereqs)
print(coreqs)

driver.quit()

