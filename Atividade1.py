import time
from operator import itemgetter
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Page:
    def __init__(self):
        self.driver = Chrome(executable_path='./chromedriver/chromedriver.exe')
        self.url = 'https://www.discourse.org/'
        self.demo = (By.PARTIAL_LINK_TEXT, 'Demo')
        self.table = (By.CSS_SELECTOR, 'table')
        self.latest = (By.PARTIAL_LINK_TEXT, 'Latest')

    def load(self):
        self.driver.get(self.url)

    def navigateToDemo(self):
        self.driver.find_element(*self.demo).click()

    def goToEndOfPage(self):
        #press end button to load the rest of the table
        html = self.driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(3)
        #press end button again to array at the botton of the page
        html.send_keys(Keys.END)

    def changeSeleniumFocus(self):
        #change the selenium focus to the Demo tab
        window1= self.driver.window_handles[1]
        self.driver.switch_to_window(window1)

    def waitTable(self):
        #wait until table is located
        self.driver.find_element(*self.latest).click()
        WebDriverWait(self.driver, timeout=20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table')))

    def getTopics(self):
        table = self.driver.find_element(*self.table)
        return table.find_elements_by_css_selector('tr')[2:]


dictionary = dict()
highest_views = 0
highest_views_topic = ''
locked_topics = []

discourse = Page()
discourse.load()
discourse.navigateToDemo()
discourse.changeSeleniumFocus()
discourse.waitTable()
discourse.goToEndOfPage()

topics = discourse.getTopics()

#interact with each row
for topic in topics:
    views = 0
    tds = topic.find_elements_by_css_selector('td')
    title = tds[0].text.split('\n')
    
    #identify if a topic is locked
    try:
        locked = tds[0].find_element_by_class_name('topic-statuses')
        locked_topics.append(title[0])
        pass
    except:
        pass


    #fill a dictionary with categories and count uncategorized topics
    categories = title[1:]
    if len(categories) == 0:
        categories.append('uncategorized')

    for category in categories:
        if dictionary.get(category) == None:
            dictionary[category] = 1
        else:
            valor_atual = dictionary.get(category)
            dictionary[category] = valor_atual + 1


    #identify the most viewed topic
    try:
        views = int(tds[3].text)
    except:
        number = float((tds[3].text)[:-1])
        views = int(number * 1000)
        pass

    if views > highest_views:
        highest_views = views
        highest_views_topic = title[0]

sorted_dict = sorted(dictionary.items(), key=itemgetter(1), reverse=True)

#print results
print('\nLocked Topics: \n')
for topic in locked_topics:
    print(topic)

print(' \nCategories:\n')
for category, quantity in sorted_dict:
    print(f'category: {category} | quantity: {quantity}')

print('\nThe most viewed topic:\n')
print(highest_views_topic)