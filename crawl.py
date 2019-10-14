from selenium import webdriver
from bs4 import BeautifulSoup as bs
from credentials import my_id, my_pw

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)
driver.get('https://kulms.korea.ac.kr')

driver.implicitly_wait(5)

# send id
id_element = driver.find_element_by_name('user_id')
id_element.send_keys(my_id)

# send pw
pw_element = driver.find_element_by_name('user_password')
pw_element.send_keys(my_pw)

# submit
pw_element.submit()

driver.implicitly_wait(3)
cookie_agree = driver.find_element_by_id('agree_button')
cookie_agree.click()

course_element = driver.find_element_by_xpath('//*[@id="$fixedId"]/div/p/a')
course_element.click()

# find course list
course_ul_element = driver.find_element_by_xpath('//*[@id="_22_1termCourses__65_1"]/ul')
course_ul_html = course_ul_element.get_attribute('innerHTML')
soup = bs(course_ul_html, 'html.parser')

course_anchor_raw = soup.find_all('a', href=True)
course_list = []

for e in course_anchor_raw:
  course_id = str(e).split('id=')[1].split('&amp')[0]
  course_list.append(course_id)

f = open('./notification.txt', 'w')

for cid in course_list:
  driver.get('https://kulms.korea.ac.kr/webapps/blackboard/execute/announcement?method=search&context=course_entry&course_id={}'.format(cid))
  driver.implicitly_wait(5)

  try:
    notice_ul_element = driver.find_element_by_xpath('//*[@id="announcementList"]')
    notice_ul_html = notice_ul_element.get_attribute('innerHTML')
    #print(notice_ul_html)
    soup = bs(notice_ul_html, 'html.parser')

    notice_li_element = soup.select('li.clearfix')

    for notice in notice_li_element:
      f.write(notice.text)
      f.write('\n-----------------------------------------------------------\n')
  except:
    pass

f.close()