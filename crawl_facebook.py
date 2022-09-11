from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from datetime import datetime
import pandas as pd

# Khai báo browser
driver = webdriver.Chrome('D:\BuenasApp\crawl\chromedriver.exe')

# driver.get("https://www.facebook.com")
# txtUser = driver.find_element(By.ID,"email")
# txtUser.send_keys("username") # <---  Điền username thật của các bạn vào đây
# sleep(3)
# txtPass = driver.find_element(By.ID,"pass")
# txtPass.send_keys("password") #<-- điền password của các bạn vào đây
#
# # đăng nhập
# txtPass.send_keys(Keys.ENTER)

# Mở trang web cần crawl
urlPage = "https://www.facebook.com/nike" #<-- thay đổi url của page bạn cần crawl ở đây
driver.get(urlPage)


# Scroll trang
allItems = []
for i in range(1,5):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    sleep(5)
    allItem = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_1dwg _1w_m _q7o']")))
    allItems.append(allItem)
    sleep(3)

# làm phẳng mảng
count_fb_end = [item for sublist in allItems for item in sublist]

# tùy vào các xpath phù hợp các bạn thay xpath ở trong dấu " " này
for i in count_fb_end:
    links = i.find_elements(By.XPATH, "//a[@class='_5pcq']")
    likes = i.find_elements(By.XPATH,"//span[@class='_81hb']")
    interactive = i.find_elements(By.XPATH,"//div[@class='_4vn1']")

list_like = [i.get_attribute("textContent") for i in likes]
list_link = [i.get_attribute("href") for i in links]
list_cmt_share = [i.get_attribute("textContent") for i in interactive]


# Xử lý dữ liệu share and comment

list_cmt = []
list_share = []
list_link_end = []

for i in range(0,len(list_cmt_share)):
    cmt = re.findall("(?:\d*\.\d+|\d+)K comments|(?:\d*\.\d+|\d+) comments|(?:\d*\.\d+|\d+) comment",list_cmt_share[i])
    if len(cmt) != 0:
        list_cmt.append(cmt)
    else:
        list_cmt.append(['0 comment'])
    share = re.findall("(?:\d*\.\d+|\d+)K shares|(?:\d*\.\d+|\d+) shares|(?:\d*\.\d+|\d+) share",list_cmt_share[i])
    if len(share) != 0:
        list_share.append(share)
    else:
        list_share.append(['0 share'])

list_cmt = [item for sublist in list_cmt for item in sublist]
list_cmt = [re.findall("(?:\d*\.\d+|\d+)K|(?:\d*\.\d+|\d+)",i) for i in list_cmt]
list_cmt = [item for sublist in list_cmt for item in sublist]
list_share = [item for sublist in list_share for item in sublist]
list_share = [re.findall("(?:\d*\.\d+|\d+)K|(?:\d*\.\d+|\d+)",i) for i in list_share]
list_share = [item for sublist in list_share for item in sublist]

#loại bỏ những bài viết không thuộc page (như các bài mà page share lại của người khác...)
for i in range(0,len(list_link)):
    if urlPage in list_link[i]:
        list_link_end.append(list_link[i])

# lưu file
file_end = pd.DataFrame(list(zip(list_link_end,list_like,list_cmt,list_share)))
file_end.columns =['Link', 'Like', 'Comment', 'Share']
getTime = datetime.now().strftime("%H_%M_%S")
# Các bạn có thể thay đổi đường dẫn ở trong dấu ' '
saveFile = file_end.to_excel('output_{}.xlsx'.format(getTime), encoding="utf-8")
