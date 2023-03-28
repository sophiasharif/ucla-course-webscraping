from selenium import webdriver
import json

def get_major_courses(website, driver):
    driver.get(website)
    single_option_reqs = driver.find_elements_by_xpath('//div[@data-level="1"]//a[@tabindex="-1"]')

    codes = []
    for match in single_option_reqs:
        text = driver.execute_script("return arguments[0].textContent;", match).strip()
        partition = text.find('-')
        code = text[0:partition - 1]
        codes.append(code)
    return codes

def scrape_major_to_json(website, file_name, driver):
    major = get_major_courses(website, driver)

    with open(f'./data/major-courses/{file_name}.json', 'w') as file:
        json.dump(major, file)