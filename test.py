department_to_code = {"Mathematics": "MATH", "Program in Computing": "PIC", "Computer Science": "COM SCI", "Civil and Environmental Engineering": "C&EE", "Electrical and Computer Engineering": "EC ENGR", "Statistics": "STATS", "Physics": "PHYSICS"}


def parse_prerequisites(prerequisites: str):
    # edge case
    if prerequisites == "":
        return []

    # change departments to abbreviations
    for dept in department_to_code:
        prerequisites = prerequisites.replace(dept, department_to_code[dept])

    # Separate required courses and optional groups
    components = split_string(prerequisites)
    parsed_output = []

    for component in components:
        # If there are parentheses, it's an optional group
        if '(' in component:
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

test = "Mathematics 32B and Mathematics 33B and Mathematics 115A and ( Program in Computing 10A or Computer Science 31)	"
print(parse_prerequisites(test))