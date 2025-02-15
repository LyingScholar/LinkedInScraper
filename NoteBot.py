import os
import time
import random

from selenium import webdriver
from bs4 import BeautifulSoup

# import random
# import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
# chrome_options.add_argument("--headless")  # Optional: run without opening a browser window


#Loggin in to LinkedIn
#os.getcwd()
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.linkedin.com/uas/login")
time.sleep(random.randrange(6,9))  #avoiding detection

try:
    # email
    driver.find_element(By.ID, 'username').send_keys('annoyingcracks@gmail.com')
    word= driver.find_element(By.ID, 'password')
    # password
    word.send_keys(f'U9Wi7rd#&fPm%%c')
    word.submit()
    print("Login Sucessful")
except NoSuchElementException:
    print("Login elemet missing")
    driver.quit()
    exit()


time.sleep(random.randrange(6,9))
#Click 'Not Now' button when asked to remember user profile
try:
    not_now_button = driver.find_element(By.XPATH, '//button[text()="Not now"]')
    not_now_button.click()
except:
    print('Button Not now not found')
    pass


#Change keywords here
keywords="RIT+Cybersecurity+Alumni"
pages = 10 #Enter number of pages to stop at


# file = open('LinkedInConnectBot-main/visited.txt')
# visited = file.readlines()
# visited = visited[0].split()
# queued = []

# Load Visited Profiles
try:
    with open('visited.txt', 'r') as file:
        visited = file.read().split()
except FileNotFoundError:
    visited = []

queued = []

#Function to get profile links
def getProfiles(soup, queued):
    profiles = []
    results = soup.find('ul', {'class': 'reusable-search__entity-results-list list-style-none'})
    photo = results.findAll('a', {'class':'app-aware-link','aria-hidden': 'false'})
    for link in photo:
        href = link.get('href')
        if ((href not in visited) and (href not in queued)): profiles.append(href)
    return profiles



for page in range(1, pages+1):
    #Searching stuff
    driver.get("https://www.linkedin.com/search/results/people/?keywords="+keywords+"&origin=CLUSTER_EXPANSION&page="+str(page))
    
    queued.extend(getProfiles(BeautifulSoup(driver.page_source, features="html.parser"), queued))
    
    print('Profiles Visited: ', len(visited))
    
    while queued:
        try:
            visiting = queued.pop()
            visited.append(visiting)
            driver.get(visiting)
            name = driver.find_element_by_class_name("text-heading-xlarge").get_attribute('innerHTML')
            message = "Hi "+name.split()[0]+"!\n\n Thanks for taking a moment to read my note! I’m reaching out because I noticed we share a connection through RIT—specifically in the cybersecurity/CS field. I'm a cybersecurity student at RIT with minors in Mathematics and Network and System Administration, aiming to graduate by 2027 and desperately looking for internships and co-ops. I hope to broaden my network by conencting with like minded experts such as yourself. I’d love to hear more about your journey and any insights you have from the field. Let’s stay in touch, share experiences, and potentially collaborate down the road. Looking forward to connecting!"
            
            #driver.find_element_by_xpath('//button[text()="Connect"]').click()
            driver.find_element_by_class_name('pvs-profile-actions__action').click()
            time.sleep(5)
            
            #If there is error while connecting using the blue connect button, try to connect using the "More" dropdown button
            try:
                driver.find_element_by_class_name('artdeco-button--secondary').click()
            except:
                print("Error connecting with " + name + ". Trying with More button")
                try:
                    driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/div/button').click()
                except:
                    driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/div/button').click()
                #driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/div/div/div/ul/li[4]/div').click()
                finally:
                    time.sleep(2)
                    driver.find_element_by_xpath('//div[@data-control-name="connect"]').click()
                    time.sleep(2)
                    driver.find_element_by_class_name('mr2').click()
                    driver.find_element_by_class_name('artdeco-button--secondary').click()
            finally:
                #Sending the message
                driver.find_element_by_id('custom-message').send_keys(message)
                time.sleep(3)
                driver.find_element_by_class_name('ml1').click()
                time.sleep(5)
                
            #saving visited profile
            with open('LinkedInConnectBot-main/visited.txt', 'a') as f:
                f.write(str(visiting)+" ")
            f.close()
            
        except:
            print("Unable to connect with profile: " + name)
            
print('Completed!! Profiles Visited: ', len(visited))
driver.quit()
