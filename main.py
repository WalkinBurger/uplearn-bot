#! .venv/bin/python3.12
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
email = os.getenv("email")
password = os.getenv("password")

url = "https://web.uplearn.co.uk/"

options = Options()
options.set_preference("media.volume_scale", "0.0")
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 30)
driver.get("https://web.uplearn.co.uk/login")
wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys(email)
wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(password)
wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[2]/button"))).click()
print("Logged in \n\n")

wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/nav/div/div/ul/ul[1]/li/a")))
driver.get("https://web.uplearn.co.uk/assignments")
try:
    asms_parent = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div")))
    asms = asms_parent.find_elements(By.XPATH, "./a")
    print("Assignments: ")
    for i,asm in enumerate(asms):
        print(f"{i+1}: {asm.text.splitlines()[0]}")
except Exception as e:
    print("No assignment found",e)
    driver.quit()

print(f"\nCurrent assignment: {asms[0].text.splitlines()[0]}")
driver.get(asms[0].get_attribute("href"))
subsecs_parent = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/ul")))
subsecs = subsecs_parent.find_elements(By.XPATH, "./li")
subsecs_href = []
for subsec_href in subsecs_parent.find_elements(By.XPATH, "./li/a"):
    subsecs_href.append([' '.join(subsec_href.text.splitlines()[:2]), subsec_href.get_attribute("href")])

for subsec,href in subsecs_href:
    print(f"-> Subsection: {subsec}")
    driver.get(href)

driver.quit()