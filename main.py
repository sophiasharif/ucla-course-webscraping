from selenium import webdriver
from scrape_courses import scrape_courses_to_json
from major import scrape_major_to_json

# set up driver
path = "/Users/sophiasharif/Desktop/projects/chromedriver_mac64/chromedriver"
driver = webdriver.Chrome(path)

# # Math courses
# math_fall_1 = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=22F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# math_fall_2 = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=22F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# math_fall_3 = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=22F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# math_winter_1 = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23W&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# math_winter_2 = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23W&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# math_winter_3 = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23W&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# math_spring_1 = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23S&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# math_spring_2 = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23S&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# math_spring_3 = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23S&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# math_courses = [math_fall_3, math_fall_2, math_fall_1, math_spring_3, math_spring_2, math_spring_1, math_winter_3, math_winter_2, math_winter_1]


# # CS courses
# cs_fall = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Computer+Science+(COM+SCI)&t=22F&sBy=subject&subj=COM+SCI&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# cs_winter = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Computer+Science+(COM+SCI)&t=23W&sBy=subject&subj=COM+SCI&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
# cs_spring = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Computer+Science+(COM+SCI)&t=23S&sBy=subject&subj=COM+SCI&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"

# PHYSICS courses
# physics_fall = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=22F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"

# scrape_courses_to_json([physics_fall], 'PHYSICS', driver)

cs_major = "https://catalog.registrar.ucla.edu/major/2022/ComputerScienceBS"

scrape_major_to_json(cs_major, "COMPUTER_SCIENCE_BS", driver)
# scrape_courses_to_json([cs_spring], "COM_SCI", driver)
driver.quit()
