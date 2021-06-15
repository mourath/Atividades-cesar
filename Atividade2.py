from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Page:
    def __init__(self):
        self.driver = Chrome(executable_path='./chromedriver/chromedriver.exe')
        self.url = 'https://www.cesar.school/'
        self.articles = (By.CSS_SELECTOR, 'article')
        self.school_menu = (By.XPATH, '//*[@id="menu-item-15376"]/a/span[2]')
        self.blogButton = (By.PARTIAL_LINK_TEXT, 'Blog')
        self.title = (By.CLASS_NAME, 'entry-title')
        self.posted_on = (By.CLASS_NAME, 'posted-on')
        self.author = (By.CLASS_NAME, 'author-name')
        self.page2 = (By.XPATH, '//*[@id="primary"]/div/nav/div/a[1]')
        self.onde = (By.CLASS_NAME, 'onde')
        self.aceptCookies = (By.PARTIAL_LINK_TEXT, 'Aceitar Cookies')


    def load(self): 
        self.driver.get(self.url)
        try:
            self.driver.find_element(*self.aceptCookies).click()
        except:
            pass

    def navigateToBlogArea(self):
        school = self.driver.find_element(*self.school_menu)
        hover = ActionChains(self.driver).move_to_element(school)
        hover.perform()
        self.driver.find_element(*self.blogButton).click()
    
    def navigateToPage2(self):
        self.driver.find_element(*self.page2).click()

    def getArticles(self):
        return self.driver.find_elements(*self.articles)

    def getTitle(self, article):
        return article.find_element(*self.title).text
    
    def getDate(self, article):
        date =  article.find_element(*self.posted_on).text
        publish = date.split('\n')
        return publish[1] +' de ' + publish[0] + ' de ' + publish[2]

    def getAuthor(self, article):
        return article.find_element(*self.author).text
    
    def navigateToEndOfPage(self):
        html = self.driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)

    def getAddress(self):
        address = self.driver.find_element(*self.onde)
        return address.find_element_by_css_selector('p').text

cesar = Page()
cesar.load()
cesar.navigateToBlogArea()
cesar.navigateToPage2()
articles = cesar.getArticles()

print('\n Segundo Post \n')
print(f'Titulo {cesar.getTitle(articles[1])}')
print (f'Publicado em: {cesar.getDate(articles[1])}')

print('\nTerceiro Post: \n')
print(f'Titulo: {cesar.getTitle(articles[2])}')
print(f'Author: {cesar.getAuthor(articles[2])}')

cesar.navigateToEndOfPage()

print(f'\nCesar School Adrress: {cesar.getAddress()}')
