from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    # Specify the path to the ChromeDriver executable
    chrome_driver_path = 'Users\Ayahk\Downloads\chromedriver_win32\chromedriver.exe'

    options = Options()
    options.add_experimental_option('detach', True)

    # Create an instance of Chrome WebDriver
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    # Open the webpage
    driver.get('https://katteb.com/en/sign-in/')
    driver.maximize_window()

    email_element = driver.find_element(By.ID, 'username')
    email_element.send_keys('abdullah@swiftandsmart.com')
    password_element = driver.find_element(By.ID, 'password')
    password_element.send_keys('kalmeeh2023kalmeeh')

    # Find and click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button.validation-submit-btn')
    login_button.click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains('https://katteb.com/ar/dashboard/'))

    print('url changed to dashboard')

    iframe_element = driver.find_element(By.ID, 'LOU_PLAYER_MAINFRAME')
    driver.switch_to.frame(iframe_element)

    try:
        close_start_dialog = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-gPpHY.ilrxnI"))
        )

        print('yes element wsa found')
        close_start_dialog.click()

    except:
        pass

    driver.switch_to.window(driver.current_window_handle)

    links = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.XPATH,'//div[@class="owl-item active"]//a[@href]'))
    )

    for link in links:
        match_word = "عناوين جذابة"
        if link.get_attribute('textContent') == match_word:
            driver.execute_script("arguments[0].click();", link)


    wait = WebDriverWait(driver, 10)
    popup = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "-instant-form-popup")))

    driver.switch_to.window(driver.window_handles[-1])

    # Find the textarea element inside the popup
    textarea = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.TAG_NAME,"textarea"))
    )

    with open("headlines.txt", "r") as file:
        line = file.readline()
    driver.execute_script(f"arguments[0].value = '{line}';", textarea)

    # Find the custom element using its attribute values
    button = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"generate-button.hoverable.activable"))
    )

    # Execute JavaScript to click on the custom element
    driver.execute_script("arguments[0].click();", button)

    # Switch back to the main window
    driver.switch_to.window(driver.window_handles[0])

    # # Close the popup window
    # driver.close()

    wait = WebDriverWait(driver, 30)
    wait.until(EC.url_contains('https://katteb.com/ar/dashboard/activities/'))

    print('url changed to done genration')

    elements = driver.find_element(By.CSS_SELECTOR,'div.fr-element.fr-view')
    paragraph = elements.find_element(By.TAG_NAME,'p')
    # Remove numbers and dots, and split the text into lines
    lines = [line.strip().strip("1234567890.-[] ") for line in paragraph.text.splitlines() if line.strip()]

    # Print each line and store them in an array
    formatted_lines = []
    for line in lines:
        formatted_lines.append(line)


    driver.get('https://katteb.com/ar/dashboard/generate-full-article/')
    form = driver.find_elements(By.TAG_NAME,'multistep-form-body-field')

    form[0].click()

    print(form)



if __name__ == '__main__':
    main()
