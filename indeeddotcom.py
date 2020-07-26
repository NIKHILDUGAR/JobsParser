from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
csv.register_dialect('escaped', escapechar='\\', doublequote=True, quoting=csv.QUOTE_ALL)
sear=str(input("What type of job are you looking for?"))
location=str(input("What location do you want to search around?"))
# sear="python"
# location="kolkata"
my_url= f'https://www.indeed.co.in/jobs?q={sear.replace(" ", "+")}&l={location.replace(" ", "+")}'
print(my_url)
filename = f"{sear} jobs in {location}.csv"
with open(filename, "w", newline='') as myfile:
    spamWriter = csv.writer(myfile, dialect='excel')
    spamWriter.writerow(["Job Title","Company","Location","Salary","Link"])
    myurll=[my_url,my_url+"&start=10",my_url+"&start=20"] # first 30 jobs
    for my_url in myurll:
        uClient = uReq(my_url)
        page = uClient.read()
        uClient.close()
        page_soup = soup(page, "lxml")
        containers = page_soup.findAll("div", {"class": "jobsearch-SerpJobCard"})
        for container in containers:
            name_container1 = container.find("h2",{"class": "title"})
            link_container = name_container1.find("a")
            link='https://www.indeed.co.in'+link_container.get('href')
            jobtitle=link_container.get("title")
            cycontainer=container.find("span",{"class": "company"})
            com=cycontainer.text
            loc=container.find("div",{"class": "location"})
            if loc is None:
                loc = container.find("span", {"class": "location"})
            salary=container.find("span",{"class": "salaryText"})
            if salary is None:
                salaryt="Salary not mentioned"
                spamWriter.writerow([str(str(jobtitle)) , str(str(com.strip())), str(str(loc.text)) , str(str(salaryt)),str(str(link)) ])
            else:
                spamWriter.writerow([str(str(jobtitle)) , str(str(com.strip())) , str(str(loc.text)) ,str(str(salary.text).encode('utf-8')).replace("\\xe2\\x82\\xb9","Rs.").replace("b'\\n","").replace("'",""),str(str(link)) ])

from subprocess import Popen
p = Popen(filename, shell=True)
