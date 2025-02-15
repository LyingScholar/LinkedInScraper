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
def get_profiles(soup, queued):
    profiles = []
    results = soup.find('ul', {'class': 'reusable-search__entity-results-list list-style-none'})
    photo = results.findAll('a', {'class':'app-aware-link','aria-hidden': 'false'})
    for link in photo:
        href = link.get('href')
        if ((href not in visited) and (href not in queued)): profiles.append(href)
    return profiles



for page in range(1, pages+1):
    #Searching stuff
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords}&origin=CLUSTER_EXPANSION&page={page}"
    driver.get(search_url)
    time.sleep(random.uniform(4, 20))
    # driver.get("https://www.linkedin.com/search/results/people/?keywords="+keywords+"&origin=CLUSTER_EXPANSION&page="+str(page))
    
    # queued.extend(getProfiles(BeautifulSoup(driver.page_source, features="html.parser"), queued))
    
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    queued.extend(get_profiles(soup, queued))

    print('Profiles Visited: ', len(visited))
    
    while queued:
        
        visiting = queued.pop()
        visited.append(visiting)
        driver.get(visiting)
        time.sleep(random.uniform(6,9))
        
        
        try:
            # Extract Profile Name
            name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-heading-xlarge"))
            )
            name = name_element.get_attribute('innerHTML').strip()
            # name = driver.find_element_by_class_name("text-heading-xlarge").get_attribute('innerHTML')
            # message = "Hi "+name.split()[0]+"!\n\n Thanks for taking a moment to read my note! I’m reaching out because I noticed we share a connection through RIT—specifically in the cybersecurity/CS field. I'm a cybersecurity student at RIT with minors in Mathematics and Network and System Administration, aiming to graduate by 2027 and desperately looking for internships and co-ops. I hope to broaden my network by conencting with like minded experts such as yourself. I’d love to hear more about your journey and any insights you have from the field. Let’s stay in touch, share experiences, and potentially collaborate down the road. Looking forward to connecting!"
            
            message = f"Hi {name.split()[0]}!\n\nThanks for taking a moment to read my note! " \
                    "I’m reaching out because I noticed we share a connection through RIT—specifically in the " \
                    "cybersecurity/CS field. I'm a cybersecurity student at RIT with minors in Mathematics and " \
                    "Network and System Administration, aiming to graduate by 2027 and looking for internships. " \
                    "I’d love to hear about your journey and any insights you have. Looking forward to connecting!"

            #driver.find_element_by_xpath('//button[text()="Connect"]').click()
            
            time.sleep(5)


            # try connect buttom
            # driver.find_element_by_class_name('pvs-profile-actions__action').click()
            try:
                connect_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "pvs-profile-actions__action"))
                )
                connect_button.click()
                time.sleep(random.uniform(6, 9))
            except (NoSuchElementException, ElementClickInterceptedException):
                print(f"Error: Could not find Connect button for {name}")
                continue

            

            #If cant use connect button, try using the "More" dropdown button
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

            #alternate way of clicking the more button
            try:
                more_button = driver.find_element(By.CLASS_NAME, "artdeco-button--secondary")
                more_button.click()
                time.sleep(2)

                connect_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@data-control-name="connect"]'))
                )
                connect_option.click()
                time.sleep(2)

                # Click 'Add Note'
                driver.find_element(By.CLASS_NAME, 'mr2').click()
                driver.find_element(By.CLASS_NAME, 'artdeco-button--secondary').click()
            except NoSuchElementException:
                print(f"Error: Could not connect with {name} using More button")
                continue


            finally:
                #Sending the message
                
                # driver.find_element_by_id('custom-message').send_keys(message)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'custom-message'))
                ).send_keys(message)
                
                time.sleep(random.randrange(6,9))
                
                # driver.find_element_by_class_name('ml1').click()
                driver.find_element(By.CLASS_NAME, 'ml1').click()

                time.sleep(random.randrange(6,9))
                
            #saving visited profile
            with open('LinkedInConnectBot-main/visited.txt', 'a') as f:
                f.write(str(visiting)+" ")
            f.close()
            
        except:
            print("Unable to connect with profile: " + name)
            
print('Completed!! Profiles Visited: ', len(visited))
driver.quit()
