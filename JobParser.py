from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
sear=str(input("What type of job are you looking for?"))
location=str(input("What location do you want to search around?"))
#sear="python"
#location="kolkata"
my_url= f'https://www.indeed.co.in/jobs?q={sear.replace(" ", "+")}&l={location.replace(" ", "+")}'
print(my_url)
filename = f"{sear} jobs in {location}.csv"
f = open(filename, "w", encoding = 'ANSI')
headers = "Job Title,Company,Location,Salary,Link \n"
f.write(headers)
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
            f.write(str(str(jobtitle).replace(",", "|"))+ "," + str(str(com.strip()).replace(",", "|")) + "," + str(str(loc.text).replace(",", "|")) + "," + str(str(salaryt))+ "," +str(str(link)) + "\n")
        else:
            f.write(str(str(jobtitle).replace(",", "|")) + "," +str(str(com.strip()).replace(",", "|")) + "," + str(str(loc.text).replace(",", "|")) + "," +str(str(salary.text).replace(",", "|").encode('utf-8')).replace("\\xe2\\x82\\xb9","Rs.").replace("b'\\n","").replace("'","") + "," +str(str(link)) + "\n")
f.close()
from subprocess import Popen
p = Popen(filename, shell=True)
