# Handy dandy Kalalua reservation checker thing.
import smtplib
import unittest
import webdriverplus
from webdriverplus import WebDriver


# Settings
SAUCELABS_EXECUTOR = 'http://benknight:e79adc51-da8e-435f-beb6-af530ec75a3f@ondemand.saucelabs.com:80/wd/hub'
LOGIN_USERNAME = 'ben@benknight.me'
LOGIN_PW = ''
CHECKIN_DATE = '08/30/2013'
MAILTO = 'ben+alert@benknight.me'
MESSAGE = "It's Kalalua time bro!!!"


class KalalauReservations(unittest.TestCase):

    def setUp(self):
        self.browser = WebDriver('remote',
            desired_capabilities=webdriverplus.DesiredCapabilities.FIREFOX,
            command_executor=SAUCELABS_EXECUTOR)
        self.smtp = smtplib.SMTP('localhost')

    def test_reservations(self):
        # Go to reservations page, asset we're forwarded to login
        self.browser.get('https://camping.ehawaii.gov/camping/all,details,1692.html')
        self.browser.find_element_by_css_selector('a[href="#ui-tabs-8"]').click()
        self.browser.switch_to_alert().accept()
        self.assertTrue(self.browser.current_url.startswith('https://lala.ehawaii.gov/lala/login'))

        # Login
        username = self.browser.find_element_by_id('username')
        username.send_keys(LOGIN_USERNAME)
        self.browser.find_element_by_id('password').send_keys(LOGIN_PW)
        username.submit()

        # Set reservation date
        # self.browser.find_element_by_id('event_checkIn').send_keys(CHECKIN_DATE)

        # Check the numbers.
        permit_count_cells = self.browser.find_element_by_link_text('Kalalau').parent().next_all('td')

        # For testing, comment this out eventually.
        # self.smtp.sendmail('ben@benknight.me', 'ben@benknight.me', 'Cron ran')

        for cell in permit_count_cells:
            print cell.text
            if cell.text and int(cell.text.strip()) > '0':
                # It's Kalalau time bro!
                self.smtp.sendmail(MAILTO, MAILTO, MESSAGE)

    def tearDown(self):
        print('Link to job: https://saucelabs.com/jobs/%s' % self.browser.session_id)
        self.browser.quit()
        self.smtp.quit()


if __name__ == '__main__':
    unittest.main()
