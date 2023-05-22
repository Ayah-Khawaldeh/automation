import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains




def main():
    # Specify the path to the ChromeDriver executable
    chrome_driver_path = 'Users\Ayahk\Downloads\chromedriver_win32\chromedriver.exe'

    options = Options()
    options.add_experimental_option('detach', True)

    # Create an instance of Chrome WebDriver
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    # Open the webpage
    driver.get('https://katteb.com/ar/sign-in/')
    driver.maximize_window()

    email_element = driver.find_element(By.ID, 'username')
    email_element.send_keys('abdullah@swiftandsmart.com')
    password_element = driver.find_element(By.ID, 'password')
    password_element.send_keys('kalmeeh2023kalmeeh')

    # Find and click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button.validation-submit-btn')
    login_button.click()

    wait = WebDriverWait(driver, 15)
    wait.until(EC.url_contains('/dashboard/'))

    kaleema_admin_email = 'admin@kalmeeh.com'
    kaleema_admin_password = 'kalmeeh2023kalmeeh*'
    main_window_handle = driver.current_window_handle

    driver.execute_script("window.open('about:blank', 'new_window')")

    # Switch to the new window
    driver.switch_to.window("new_window")

    # Navigate to a URL
    url = "https://kalmeeh.com/"
    driver.get(url)

    login_popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'li.has-title.popup-login-icon.menu-item.custom-menu-link'))
    )
    login_popup.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.container-wrapper'))
    )

    email_field = driver.find_element(By.NAME, 'log')
    password_field = driver.find_element(By.NAME, 'pwd')

    email_field.send_keys(kaleema_admin_email)
    password_field.send_keys(kaleema_admin_password)

    kaleema_submit = driver.find_element(By.CSS_SELECTOR, 'button.button.fullwidth.login-submit')
    kaleema_submit.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains('https://kalmeeh.com/wp-login.php')
    )

    captcha = driver.find_element(By.XPATH, '//label[@for="jetpack_protect_answer"]')
    captcha_result = eval(captcha.text.replace('&nbsp', '').replace(' ', '').replace('=', ''))

    captcha_input = driver.find_element(By.ID, 'jetpack_protect_answer')
    captcha_input.send_keys(captcha_result)

    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    email_field = driver.find_element(By.NAME, 'log')
    password_field = driver.find_element(By.NAME, 'pwd')

    email_field.send_keys(kaleema_admin_email)
    password_field.send_keys(kaleema_admin_password)

    driver.find_element(By.CSS_SELECTOR, 'input[name="wp-submit"]').click()

    WebDriverWait(driver, 10).until(
        EC.url_contains('https://kalmeeh.com/wp-admin/')
    )

    driver.switch_to.window(main_window_handle)


    print('url changed to dashboard')




    try:
        iframe_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'LOU_PLAYER_MAINFRAME'))
        )
        driver.switch_to.frame(iframe_element)
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
        if link.get_attribute('textContent') == match_word or link.get_attribute('textContent') == 'Headlines':
            driver.execute_script("arguments[0].click();", link)


    wait = WebDriverWait(driver, 10)
    popup = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "-instant-form-popup")))

    # driver.switch_to.window(driver.window_handles[-1])

    # Find the textarea element inside the popup
    textarea = WebDriverWait(driver,20).until(
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

    wait = WebDriverWait(driver, 90)
    wait.until(EC.url_contains('/activities/'))

    print('url changed to done genration')

    elements = driver.find_element(By.CSS_SELECTOR,'div.fr-element.fr-view')
    paragraphs = elements.find_elements(By.TAG_NAME,'p')
    # Remove numbers and dots, and split the text into lines
    titles = []
    for paragraph in paragraphs:
        lines = [line.strip().strip("1234567890.-[] ") for line in paragraph.text.splitlines() if line.strip()]
        titles.extend(lines)
    # Print each line and store them in an array
    with open('titles.txt',mode='a',encoding='utf-8') as file:
        for title in titles:
            file.write(f"{title}\n")


    def make_article():
        driver.switch_to.window(main_window_handle)
        driver.get('https://katteb.com/ar/dashboard/generate-full-article/')
        form = driver.find_elements(By.TAG_NAME, 'multistep-form-body-field')

        title = form[0].click()
        form[0].find_element(By.NAME, 'topic_title').send_keys('this is test keys 0')

        title = form[1].click()
        arabic_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'multistep-form-body-field-fill-selectbox-item[data-value="ar"]')))
        arabic_option.click()

        title = form[2].click()
        search = driver.find_elements(By.CSS_SELECTOR, 'input.-multistep-selectbox-search')[-1]
        driver.execute_script("arguments[0].value = 'Jordan';", search)
        search.send_keys(Keys.ENTER)
        jordan_aud = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'multistep-form-body-field-fill-selectbox-item[data-value="JO"'))
        )
        jordan_aud.click()

        title = form[3].click()
        numbers_of_lines = driver.find_element(By.ID, 'topic_numberofwords')
        driver.execute_script("arguments[0].value = 1200", numbers_of_lines)

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "multistep-form-next"))
        )

        next_button.click()

        write_button = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.-start-generating-button.hoverable.activable'))
        )

        write_button.click()

        show_article = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'عرض المقال'))
        )

        show_article.click()

        articles_holder = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'div.fr-element.fr-view'))
        )  # Replace 'your_div_id' with the actual ID of the div element

        ActionChains(driver).click(articles_holder).key_down(Keys.CONTROL).send_keys('a').send_keys('c').key_up(
            Keys.CONTROL).perform()

        # Copy the selected text to clipboard
        driver.execute_script('document.execCommand("copy");')

        driver.switch_to.window('new_window')

        driver.get('https://kalmeeh.com/wp-admin/post-new.php')

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[aria-label="إضافة عنوان"]'))
        )

        headline = driver.find_element(By.CSS_SELECTOR, 'h1[aria-label="إضافة عنوان"]')

        driver.execute_script('arguments[0].textContent = arguments[1];', headline, "مرحبا بك في مدونتنا")

        medical_checkbox = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'label[for="inspector-checkbox-control-6"]'))
        )
        health_checkbox = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'label[for="inspector-checkbox-control-5"]'))
        )

        medical_checkbox.click()
        health_checkbox.click()

        add_component = driver.find_element(By.CSS_SELECTOR,
                                            'button.components-button.block-editor-inserter__toggle.has-icon')
        add_component.click()

        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input.components-search-control__input'))
        )

        search.send_keys('Table')

        driver.find_element(By.CSS_SELECTOR,
                            'button.components-button.block-editor-block-types-list__item.editor-block-list-item-rank-math-toc-block').click()
        headline.click()
        add_component = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'button.components-button.block-editor-inserter__toggle.has-icon'))
        )

        add_component.click()
        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input.components-search-control__input'))
        )

        search.send_keys('عنوان')

        driver.find_element(By.CSS_SELECTOR,
                            'button.components-button.block-editor-block-types-list__item.editor-block-list-item-heading').click()

        head = driver.find_element(By.CSS_SELECTOR,
                                   'h2.block-editor-rich-text__editable.block-editor-block-list__block.wp-block.is-selected.wp-block-heading.rich-text')

        ActionChains(driver).click(head).key_down(Keys.CONTROL).send_keys('V').key_up(
            Keys.CONTROL).perform()

        draft_button = driver.find_element(By.CSS_SELECTOR, 'button.components-button.is-tertiary')
        draft_button.click()

    for i in range(30):
        make_article()



if __name__ == '__main__':
    main()