import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_experimental_option("detach", True) # Keeps window open
# options.add_experimental_option("detach", False) # Closes window

FOOTBALL_STATS_URL = 'https://www.soccerstats.com/'


def get_league_links(driver):
    leagues = ['Premier League', 'Serie A', 'La Liga', 'Ligue 1', 'Bundesliga']
    league_links = []

    for num, league_name in enumerate(leagues):
        league_a_tag = driver.find_elements("xpath", f"//a[@href][contains(., '{league_name}')]")[0]
        league_link = league_a_tag.get_attribute('href')
        league_links.append(league_link)

        print(f"Got link for {league_name}: {league_links[num]}")

if __name__ == "__main__":
    driver = webdriver.Chrome(options=options)
    driver.get(FOOTBALL_STATS_URL)

    # Click agree to cookies
    driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[2]/div/button[3]').click()

    get_league_links(driver)