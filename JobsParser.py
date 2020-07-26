import warnings
warnings.filterwarnings("ignore")
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as soup
sear=str(input("What type of job are you looking for?"))
location=str(input("What location do you want to search around?"))
import csv
csv.register_dialect('escaped', escapechar='\\', doublequote=True, quoting=csv.QUOTE_ALL)
monsterurl=f'https://www.monsterindia.com/srp/results?sort=1&limit=100&query={sear.replace(" ", "%20")}&locations={location.replace(" ", "+")}'
print(monsterurl)
filename = f"{sear} jobs in {location} by monstercom.csv"
# f = open(filename, "w", encoding = 'ANSI')
with open(filename, "w", newline='') as myfile:
    spamWriter = csv.writer(myfile, dialect='excel')
    spamWriter.writerow(["Job Title", "Company", "Location", "Salary", "Link"])
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver=webdriver.Chrome(executable_path="chromedriver.exe")
    except:
        binary: str = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        options = Options()
        options.set_headless(headless=True)
        options.binary = binary
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = True #optional
        driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path="geckodriver.exe")
    driver.get(monsterurl)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    src=driver.page_source
    driver.close()
    page_soup = soup(src, "lxml")
    containers = page_soup.findAll("div", {"class": "job-tittle"})
    print("no of jobs =", len(containers))
    for container in containers:
        name_container1 = container.find("h3", {"class": "medium"})
        link_container = name_container1.find("a")
        link = link_container.get('href')[2:]
        jobtitle = link_container.text
        spanner= container.find("span", {"class": "company-name"})
        link_container = spanner.find("a")
        if link_container is None:
            com=spanner.text
        else:
            com = link_container.text
        loc = str(container.find("span", {"class": "loc"}).text).strip()
        sal = container.findAll("span", {"class": "loc"})
        salary = sal[2].text
        spamWriter.writerow([str(str(jobtitle)), str(str(com.strip())), str(str(loc)), str(str(salary)), str(str(link))])
from subprocess import Popen
p = Popen(filename, shell=True)
