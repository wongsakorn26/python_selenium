import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("https://www.selenium.dev/selenium/web/web-form.html")
time.sleep(3) #  load all page success

print("Page Title:", driver.title)



#
#method 1
input_text_field_element1 = driver.find_element(By.ID, "my-text-id")

#method 2
input_text_field_element2 = driver.find_element(By.XPATH, '//*[@id="my-text-id"]')


#action on web click
btn1 = driver.find_element(By.XPATH, '/html/body/main/div/form/div/div[2]/div[1]/label[2]').click()
time.sleep(2) # dont want to spam click
btn1 = driver.find_element(By.XPATH, '/html/body/main/div/form/div/div[2]/div[1]/label[2]').click()


#action with input field 
input1 = driver.find_element(By.XPATH, '//*[@id="my-text-id"]')
# input1.send_keys("Somsai" + Keys.ENTER) 
input1.send_keys("Somsai") 

#action with dropdown
dropdown = Select(driver.find_element(By.CLASS_NAME, 'form-select'))

#have many choice to selected
# dropdown.select_by_visible_text("One")    #1
# dropdown.select_by_index("1")               #2
dropdown.select_by_value("2")             #3 #value = 2 

# driver.quit()
# selenium 3

