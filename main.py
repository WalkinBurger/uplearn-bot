#! .venv/bin/python3.12
from dotenv import load_dotenv
import threading
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get logins from .env
load_dotenv()
email = os.getenv("email")
password = os.getenv("password")

url = "https://web.uplearn.co.uk/"

# Function for doing assignment's subsections
def do_subsec(subsec, href):
    # Driver
    options = Options()
    options.set_preference("media.volume_scale", "0.0")
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 30)
    # Login
    driver.get("https://web.uplearn.co.uk/login")
    wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys(email)
    wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[2]/button"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/nav/div/div/ul/ul[1]/li/a")))
    print(f"-> Subsection: {subsec}")
    driver.get(href)
    q_lookup = []
    if subsec[0] != 'Q':
        # x2 speed
        speed = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/media-controller/media-control-bar/media-playback-rate-button")))
        while speed.text[-3:].strip() != '2x':
            speed.click()
        # Play video
        play = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/media-controller/media-control-bar/media-play-button")))
        if play.get_attribute('aria-label') == 'play':
            play.click()
        q_last = None
        while True:
            # Video playing & print time every 10 sec in video passed
            try:
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/button[2]")
                # Contine to next subsection
                print("Subsection done\n")
                break
            except:
                pass
            try:
                submit = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[2]/div/button")))
                # Found question
                # Get video time
                vid_time = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/media-controller/media-control-bar/media-time-display"))).text
                q_current = [vid_time[:4]]
                submit = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[2]/div/button")))
                driver.execute_script("arguments[0].click();",submit)
                view_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[2]/div/button[1]")))
                driver.execute_script("arguments[0].click();",view_ans)
                qn = 0
                last_q = False
                while not last_q:
                    qn += 1
                    if qn == 1:
                        try:
                            ans = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[2]/button[2]")))
                        except:
                            ans = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[1]/div[2]/button[2]")))
                    else:
                        try:
                            ans = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div[1]/div[2]/button[2]")))
                        except:
                            ans = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[2]/button[2]")))
                    if next_ans.text == "Finish":
                        last_q = True
                    if ans.find('missed') != -1:
                        q_current.append(ans[11])
                    elif ans.find('missing:\n') != -1:
                        q_current.append(ans[25:])
                    elif ans.find('correct answer is') != -1:
                        q_current.append(ans[22:])
                    else:
                        q_current.append(ans)
                    next_ans.click()
                if q_current != q_last:
                    print(q_current)
                    q_lookup.append(q_current)
                    q_last = q_current
                wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[2]/div/button[2]"))).click()
            except:
                pass
    else:
        # Subsection is quiz
        print("quiz")
    driver.quit()



# Function for initialising driver and get assignment
def main():
    # Driver
    options = Options()
    options.set_preference("media.volume_scale", "0.0")
    # options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 30)
    # Login
    driver.get("https://web.uplearn.co.uk/login")
    wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys(email)
    wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[2]/button"))).click()
    print("Logged in \n\n")

    # Get assignments
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

    # Get assignment's subsections
    print(f"\nCurrent assignment: {asms[0].text.splitlines()[0]}")
    driver.get(asms[0].get_attribute("href"))
    subsecs_parent = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/ul")))
    subsecs_href = []
    for subsec_href in subsecs_parent.find_elements(By.XPATH, "./li/a"):
        subsecs_href.append([' '.join(subsec_href.text.splitlines()[:2]), subsec_href.get_attribute("href")])

    for subsec,href in subsecs_href:
        t = threading.Thread(target=do_subsec, args=(subsec,href))
        t.start()
        if threading.active_count() > 3:
            t.join()
    driver.quit()

if __name__ == '__main__':
    main()