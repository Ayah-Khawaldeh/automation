from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Article:
    def __init__(self, headline, content):
        self.headline = headline
        self.content = content


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

    pickers = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,'divelem.-selectbox'))
    )


    driver.execute_script("arguments[0].click",pickers[0])
    arabic_choice = pickers[0].find_element(By.XPATH,'//divelem[@data-widget-value="ar"]')
    print(arabic_choice)
    driver.execute_script("arguments[0].click",arabic_choice)

    suggestion = pickers[1].find_element(By.XPATH,'//divelem[@data-widget-value="3"]')
    print(suggestion)
    driver.execute_script("arguments[0].click", suggestion)

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

    wait = WebDriverWait(driver, 60)
    wait.until(EC.url_contains('https://katteb.com/ar/dashboard/activities/'))

    print('url changed to done genration')

    elements = driver.find_element(By.CSS_SELECTOR,'div.fr-element.fr-view')
    paragraphs = elements.find_elements(By.TAG_NAME,'p')
    # Remove numbers and dots, and split the text into lines
    titles = []
    for paragraph in paragraphs:
        lines = [line.strip().strip("1234567890.-[] ") for line in paragraph.text.splitlines() if line.strip()]
        titles.extend(lines)
    # Print each line and store them in an array
    formatted_lines = []
    with open('titles.txt', mode='w',encoding='utf-8') as titles_file:
        titles_file.write('\n'.join(titles))


    driver.get('https://katteb.com/ar/dashboard/generate-full-article/')
    form = driver.find_elements(By.TAG_NAME,'multistep-form-body-field')

    title = form[0].click()
    form[0].find_element(By.NAME, 'topic_title').send_keys('this is test keys 0')


    title = form[1].click()
    arabic_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'multistep-form-body-field-fill-selectbox-item[data-value="ar"]')))
    arabic_option.click()

    title = form[2].click()
    search = driver.find_elements(By.CSS_SELECTOR,'input.-multistep-selectbox-search')[-1]
    driver.execute_script("arguments[0].value = 'Jordan';", search)
    search.send_keys(Keys.ENTER)
    jordan_aud = driver.find_element(By.CSS_SELECTOR, 'multistep-form-body-field-fill-selectbox-item[data-value="JO"')
    jordan_aud.click()

    title = form[3].click()
    numbers_of_lines = driver.find_element(By.ID, 'topic_numberofwords')
    driver.execute_script("arguments[0].value = 1200", numbers_of_lines)

    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, "multistep-form-next"))
    )

    next_button.click()

    write_button = WebDriverWait(driver,40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'div.-start-generating-button.hoverable.activable'))
    )

    write_button.click()

    show_article = WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'عرض المقال'))
    )

    show_article.click()


    articles_holder = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                      'div.fr-element.fr-view'))
    )  # Replace 'your_div_id' with the actual ID of the div element

    p_elements = articles_holder.find_elements(By.TAG_NAME,'p')

    article = Article(headline=p_elements[0],content=str(articles_holder.text).replace(p_elements[0].text, ''))

    print(article.headline)
    print(article.content)




if __name__ == '__main__':
    main()
