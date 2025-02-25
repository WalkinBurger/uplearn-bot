#! .venv/bin/python3.12
from dotenv import load_dotenv
import json
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


# Function for doing assignment's subsections
def do_subsec(subsec, href):
    print(f"-> Subsection: {subsec}")
    with open("ans.json", "r") as f:
        ans_data = json.load(f)
    f.close()
    if href in ans_data:
        print("Subsection done")
        return
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
    driver.get(href)
    sub_type = None

    if subsec[0] != 'Q':
        q_lookup = {}
        sub_type = 'V'
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
            # Video playing
            try:
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/button[2]")
                # Contine to next subsection
                print("Subsection done")
                break
            except:
                pass
            try:
                submit = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[2]/div/button")))
                # Found question
                vid_time = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/media-controller/media-control-bar/media-time-display"))).text
                q_current = []
                submit = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[2]/div/button")))
                driver.execute_script("arguments[0].click();",submit)
                view_ans = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[2]/div/button[1]")))
                driver.execute_script("arguments[0].click();",view_ans)
                qn = 0
                last_q = False
                # Get all answers
                while not last_q:
                    qn += 1
                    if qn == 1:
                        try:
                            ans = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[2]/button[2]")))
                        except:
                            ans = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[1]/div[2]/button[2]")))
                    else:
                        try:
                            ans = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div[1]/div[2]/button[2]")))
                        except:
                            ans = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[2]/button[2]")))
                    if next_ans.text == "Finish":
                        last_q = True
                    if ans.find('missed') != -1:
                        q_current.append(ans[11])
                    elif ans.find('missing:\n') != -1:
                        q_current.append(ans[25:])
                    elif ans.find('correct answer is') != -1:
                        q_current.append((ans[22:]).replace('\n',' '))
                    elif ans.find('You were right not to select') != -1:
                        pass
                    else:
                        q_current.append(ans)
                    next_ans.click()
                if q_current != q_last:
                    q_lookup[vid_time[:4]] = q_current
                    q_last = q_current
                cont = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[2]/div/button[2]")))
                driver.execute_script("arguments[0].click();",cont)
            except:
                pass
    else:
        try:
            q_no = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/main/div/p/span"))).text
            q_no = int(q_no[:q_no.find(' que')])
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/main/div/button"))).click()
            # Subsection is quiz
            q_lookup = []
            q_last = None
            sub_type = 'Q'
            q_i = 1
            while q_i <= q_no:
                q_current = []
                submit = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/main/div/div[2]/div[2]/div/button/span")))
                driver.execute_script("arguments[0].click();",submit)
                view_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/main/div/div[2]/div[2]/div/button[1]")))
                driver.execute_script("arguments[0].click();",view_ans)
                qn = 0
                last_q = False
                # Get all answers
                while not last_q:
                    qn += 1
                    if qn == 1:
                        try:
                            ans = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[2]/button[2]")))
                        except:
                            ans = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[1]/div[1]/p/span/span"))).text
                            next_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div[2]/button[2]")))
                    else:
                        try:
                            ans = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div/div/div[1]/div[1]/div/p/span/span"))).text
                            next_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div[1]/div[2]/button[2]")))
                        except:
                            ans = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div/div/div[1]/div[1]/div[1]/p/span/span"))).text
                            next_ans = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div[1]/div[2]/button[2]")))
                    if next_ans.text == "Finish":
                        last_q = True
                    if ans.find('missed') != -1:
                        q_current.append(ans[11])
                    elif ans.find('missing:\n') != -1:
                        q_current.append(ans[25:])
                    elif ans.find('correct answer is') != -1:
                        q_current.append((ans[22:]).replace('\n',' '))
                    elif ans.find('You were right not to select') != -1:
                        pass
                    else:
                        q_current.append(ans)
                    next_ans.click()
                if q_current != q_last:
                    q_lookup.append(q_current)
                    q_last = q_current
                cont = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/main/div/div[2]/div[2]/div/button[2]")))
                driver.execute_script("arguments[0].click();",cont)
                q_i += 1
            print("Subsection done\n")
        except:
            pass
    driver.quit()

    if not href in ans_data:
        ans_data[href] = {"sub_type":sub_type, "q_lookup":q_lookup}
        with open("ans.json", 'w') as f:
            json.dump(ans_data, f, indent=4)
        f.close()
            



# Function for initialising driver and get assignment
def main(asm_arg):
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
    print(f"\n\n> Logged in as  [ {email} ]\n")

    # Get assignments
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/nav/div/div/ul/ul[1]/li/a")))
    driver.get("https://web.uplearn.co.uk/assignments")
    if not asm_arg:
        asms = None
        try:
            asms_parent = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div")))
            asms = asms_parent.find_elements(By.XPATH, "./a")
            print("> Incomplete assignments: ")
            asms = [asm for asm in asms if asm.text.splitlines()[1] == 'INCOMPLETE']
            for i,asm in enumerate(asms):
                print(f"╚═ {i+1}: {asm.text.splitlines()[0]}")
        except Exception as e:
            print("No assignment found",e)
            driver.quit()
        print(f"\n\n{'-'*32}")
        if asms:
            asms_subsecs = []
            for i in range(len(asms)):
                asms[i] = (asms[i].text.splitlines()[0], asms[i].get_attribute("href"))
            for asm in asms:
                # Get assignment's subsections
                print(f"\n\n> Assignment:  {asm[0]}")
                driver.get(asm[1])
                subsecs_parent = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/ul")))
                subsecs_href = []
                for subsec_href in subsecs_parent.find_elements(By.XPATH, "./li/a"):
                    if subsec_href != subsecs_parent.find_elements(By.XPATH, "./li/a")[-1]:
                        print(f"├─ {' '.join(subsec_href.text.splitlines()[:2])}")
                    else:
                        print(f"└─ {' '.join(subsec_href.text.splitlines()[:2])}")
                    subsecs_href.append([' '.join(subsec_href.text.splitlines()[:2]), subsec_href.get_attribute("href")])
                asms_subsecs.append(subsecs_href)

            driver.quit()
            print(f"\n\n{'-'*32}\n\n")
            
            # CLI for selecting assigments to do
            print("> Incomplete assignments: ")
            for i,asm in enumerate(asms):
                print(f"╚═ {i+1}: {asm[0]}")
            to_do = False
            while not to_do:
                try:
                    to_do_asm = str(input("\n> Which assigment to do?   -1:[Cancel]  0:[All(default)]  n:[nth assignment]  n,m:[n&mth assigment]  "))
                    if to_do_asm == '-1':
                        return
                    elif to_do_asm == '0' or not to_do_asm:
                        selected_asm = asms_subsecs
                        to_do_asm = [i+1 for i in range(len(asms_subsecs))]
                    elif ',' in to_do_asm:
                        to_do_asm = [int(x) for x in to_do_asm.split(',')]
                        selected_asm = [asm for asm in asms_subsecs if asms_subsecs.index(asm)+1 in to_do_asm]
                        asms = [asm for asm in asms if asms.index(asm)+1 in to_do_asm]
                    else:
                        selected_asm = [asms_subsecs[int(to_do_asm)-1]]
                        asms = [asms[int(to_do_asm)-1]]
                        to_do_asm = [int(to_do_asm)]
                    to_do = True
                except Exception as e:
                    print(e)
            print("\n> Selected assignments: ")
            for i,asm in enumerate(asms):
                print(f"╚═ {to_do_asm[i]}: {asm[0]}")

        for asm in selected_asm:
            for subsec,href in asm:
                t = threading.Thread(target=do_subsec, args=(subsec,href))
                t.start()
                if threading.active_count() > 0:
                    t.join()

    else:
        driver.get(asm_arg)
        subsecs_parent = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/ul")))
        subsecs_href = []
        for subsec_href in subsecs_parent.find_elements(By.XPATH, "./li/a"):
            if subsec_href != subsecs_parent.find_elements(By.XPATH, "./li/a")[-1]:
                print(f"├─ {' '.join(subsec_href.text.splitlines()[:2])}")
            else:
                print(f"└─ {' '.join(subsec_href.text.splitlines()[:2])}")
            subsecs_href.append([' '.join(subsec_href.text.splitlines()[:2]), subsec_href.get_attribute("href")])
        driver.quit()
        for subsec in subsecs_href:
            t = threading.Thread(target=do_subsec, args=(subsec[0],subsec[1]))
            t.start()
            if threading.active_count() > 4:
                t.join()
    
        
if __name__ == '__main__':
    main(None)

