from selenium import webdriver
from prereqs import scrape_reqs

# set up driver
path = "/Users/sophiasharif/Desktop/projects/chromedriver_mac64/chromedriver"
driver = webdriver.Chrome(path)
website = 'https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=23S&subj_area_cd=COM%20SCI&crs_catlg_no=0111%20%20%20%20&class_id=187336200&class_no=%20001%20%20'


print(scrape_reqs(website, driver))

driver.quit()


