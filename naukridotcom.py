import warnings
warnings.filterwarnings("ignore")
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as soup
import csv
csv.register_dialect('escaped', escapechar='\\', doublequote=True, quoting=csv.QUOTE_ALL)
sear=str(input("What type of job are you looking for?"))
location=str(input("What location do you want to search around?" ))
# sear="python"
# location="kolkata"
naukriurl= f'https://www.naukri.com/{sear.replace(" ", "-")}-jobs-in-{location.replace(" ", "+")}'
filename = f"{sear} jobs in {location} naukri.csv"
seen=set()
with open(filename, "w", newline='') as myfile:
    spamWriter = csv.writer(myfile, dialect='excel')
    spamWriter.writerow(["Job Title","Company","Location","Salary","Link"])
    naukriurls = [naukriurl, naukriurl + "-2", naukriurl + "-3"]
    for naukriurl in naukriurls:
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            driver = webdriver.Chrome(executable_path="chromedriver.exe")
        except:
            binary: str = r'C:\Program Files\Mozilla Firefox\firefox.exe'
            options = Options()
            options.set_headless(headless=True)
            options.binary = binary
            cap = DesiredCapabilities().FIREFOX
            cap["marionette"] = True
            driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path="geckodriver.exe")
        driver.get(naukriurl)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        src = driver.page_source
        driver.close()
        page_soup = soup(src, "lxml")
        print(naukriurl)

        containers = page_soup.findAll("div", {"class": "jobTupleHeader"})
        for container in containers:
            name_container1 = container.find("a", {"class": "title"})
            link = name_container1.get('href')
            jobtitle = name_container1.text
            cycontainer = container.find("div", {"class": "companyInfo"})
            cy=cycontainer.find("a")
            com = cy.text
            loc = container.find("li", {"class": "location"})
            locs=loc.find("span")
            loc=locs.text
            salary = container.find("li", {"class": "salary"})
            sal= salary.find("span")
            salary=sal.text
            l=[str(str(jobtitle).strip()), str(str(com.strip())), str(str(loc).strip()), str(str(salary).strip()),
                 f'=HYPERLINK("{str(str(link).strip())}")']
            if l[1] not in seen:
                spamWriter.writerow(l)
                seen.add(l[1])
from subprocess import Popen
p = Popen(filename, shell=True)
