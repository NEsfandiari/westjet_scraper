from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def scrape_airport(departure_time, origin_code, dest_code, flight_number):
    url = f'https://www.westjet.com/booking/Create.html?lang=en&type=search&origin={origin_code}&destination={dest_code}&adults=1&children=0&infants=0&outboundDate={departure_time}&returnDate=&companionvoucher=false&iswestjetdollars=false&promo=&currency=USD&caller=https%3A%2F%2Fwww.westjet.com%2Fen-us%2Findex'

    driver = webdriver.Chrome()
    driver.implicitly_wait(300)
    driver.get(url)

    flight_info_modals = driver.find_elements_by_class_name('link-modal')
    flight_price_modals = driver.find_elements_by_class_name('cabin-container')

    #Find the right flight number
    for flight_info_e, flight_price_e in zip(flight_info_modals,
                                             flight_price_modals):
        flight_info_e.click()

        if flight_number in driver.page_source:

            # Exit Search Page
            driver.find_element_by_id('lightbox-close').click()
            price_toggle = flight_price_e.find_element_by_class_name("btn")
            price_toggle.click()
            drawer_modal = driver.find_element_by_class_name('normal')
            drawer_modal.find_element_by_tag_name("button").click()

            #Confirmation Page
            while len(driver.find_elements_by_class_name("primary")) == 1:
                try:
                    driver.find_element_by_class_name("primary").click()
                except:
                    continue

            # User Info Page
            while True:
                try:
                    driver.find_element_by_class_name("icon-X").click()
                    break
                except:
                    continue
            dropdowns = driver.find_elements_by_tag_name('select')
            for select in dropdowns:
                options = select.find_elements_by_tag_name('option')
                if options[0].text != "Select program":
                    options[-1].click()
            driver.find_element_by_css_selector('input[type=tel]').send_keys(
                "111-111-1111")
            driver.find_element_by_css_selector('input[type=email]').send_keys(
                "a@a.com")
            driver.find_element_by_css_selector(
                '#adult-1-firstName').send_keys("a")
            driver.find_element_by_css_selector('#adult-1-lastName').send_keys(
                "a")
            driver.find_element_by_id('continue').click()

            #Seat Map Page
            seats = driver.find_elements_by_class_name('regular')
            for seat in seats:
                print(seat.text)
            import pdb
            pdb.set_trace()
            break
        else:
            driver.find_element_by_id('lightbox-close').click()

    driver.quit()


print(scrape_airport("2019-05-26T10:30", "YYC", "SFO", "WS1508"))
