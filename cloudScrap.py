from selenium import webdriver
from icecream import ic
from selenium.webdriver.common.by import By
# https://browsercloud.io/docs/frameworks/selenium


chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability('browsercloud:token', 'SIVWuc9VvIt10rPp')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

driver = webdriver.Remote(
    command_executor='https://8f83e16c-d55a-4c35-84a1-734d3c0846a7@chrome.browserless.io/webdriver',
    options=chrome_options
)

# driver = webdriver.Remote(
#     command_executor='https://chrome.browsercloud.io/webdriver?token=SIVWuc9VvIt10rPp',
#     options=chrome_options
# )

driver.get("https://www.bloomberg.com/news/articles/2023-09-02/the-ai-investments-to-avoid-at-all-costs-according-to-art-hogan?srnd=premium")
body_elements = driver.find_elements(By.TAG_NAME, 'body')
all_text = ''
if body_elements:
    all_text = body_elements[0].text
ic(all_text)
# ic(driver.title)
driver.quit()
