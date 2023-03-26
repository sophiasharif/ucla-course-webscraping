from selenium import webdriver
from prereqs import scrape_reqs

website = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23W&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
path = "/Users/sophiasharif/Desktop/projects/chromedriver_mac64/chromedriver"
driver = webdriver.Chrome(path)
driver.get(website)

host_element = driver.find_element_by_tag_name("ucla-sa-soc-app")
shadow_root = driver.execute_script("return arguments[0].shadowRoot", host_element)
courses = driver.execute_script("return arguments[0].getElementById('resultsTitle')", shadow_root)
buttons = driver.execute_script("return arguments[0].querySelectorAll('button')", courses)

button = buttons[0]
button.click()
button_id = button.get_attribute("id")
container_id = button_id.replace("title", "container")
print(container_id)
script = f"return arguments[0].getElementById('{container_id}')"

class_info = driver.execute_script(script, shadow_root)


icon = driver.execute_script("return arguments[0].querySelector('i.icon-warning-sign')", class_info)
icon.click()


driver.implicitly_wait(2)


# Find the "More Detail" link within the shadow DOM
more_details_link = driver.execute_script("return arguments[0].querySelector('a')", class_info)
link = more_details_link.get_attribute("href")
print("Scraping " + link)

reqs = scrape_reqs(link, driver)
print(reqs)


# Click the "More Detail" link
# more_details_link.click()
