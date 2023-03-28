from prereqs import scrape_class_info
from courses import get_course_links_from_page
import json


def get_courses(websites: list[str], driver) -> dict:
    course_info = {}
    for website in websites:
        courses_and_links = get_course_links_from_page(website, driver)
        for course in courses_and_links:
            if course not in course_info:
                course_info[course] = scrape_class_info(courses_and_links[course], driver)
    return course_info


def scrape_courses_to_json(websites, file_name, driver):
    courses = get_courses(websites, driver)

    with open(f'{file_name}.json', 'w') as file:
        json.dump(courses, file)
