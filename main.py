from selenium import webdriver
from prereqs import scrape_reqs
from courses import get_course_links_from_page

# set up driver
path = "/Users/sophiasharif/Desktop/projects/chromedriver_mac64/chromedriver"
driver = webdriver.Chrome(path)
#
# # Math courses
# website = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23W&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# # CS courses
website = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Computer+Science+(COM+SCI)&t=23W&sBy=subject&subj=COM+SCI&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"

links = get_course_links_from_page(website, driver)
print(links)

course_prereqs = {}
course_coreqs = {}
for course in links:
    prereqs, coreqs = scrape_reqs(links[course], driver)
    course_prereqs[course] = prereqs
    course_coreqs[course] = coreqs

print(course_prereqs)
print(course_coreqs)
driver.quit()