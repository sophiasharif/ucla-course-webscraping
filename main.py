from selenium import webdriver
from prereqs import scrape_reqs

# set up driver
path = "/Users/sophiasharif/Desktop/projects/chromedriver_mac64/chromedriver"
webdriver = webdriver.Chrome(path)

website = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=23S&subj_area_cd=COM%20SCI&crs_catlg_no=0146%20%20M%20&class_id=187576200&class_no=%20001%20%20"

prereqs, coreqs = scrape_reqs(website, webdriver)
print(prereqs)
print(coreqs)
print(type(webdriver))

webdriver.quit()