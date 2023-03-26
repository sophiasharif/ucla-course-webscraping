from selenium import webdriver
import pandas as pd

website = "https://catalog.registrar.ucla.edu/major/2022/AppliedMathematicsBS"
path = "/Users/sophiasharif/Desktop/projects/chromedriver_mac64/chromedriver"
driver = webdriver.Chrome(path)
driver.get(website)
single_option_reqs = driver.find_elements_by_xpath('//div[@data-level="1"]//a[@tabindex="-1"]')

codes = []
names = []
links = []

for match in single_option_reqs:
    text = driver.execute_script("return arguments[0].textContent;", match).strip()
    partition = text.find('-')
    code = text[0:partition-1]
    name = text[partition+2:]
    link = match.get_attribute('href')
    codes.append(code)
    names.append(name)
    links.append(link)

df = pd.DataFrame({'code': codes, 'name': names, 'link': links})
df.to_csv('applied_mathematics.csv')
df.to_json('applied_mathematics.json')
print(df)

driver.quit()