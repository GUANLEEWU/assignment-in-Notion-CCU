# encoding: utf-8
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import napilib as nal
import secret,time,datetime,pytz

intervalUnit = 1 # wait time for loading page etc.
# webdriver setting
chrome_options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_argument('--window-size=1200,900')
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
drA = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options) #initialize webdriver

#Login
drA.get("https://ecourse2.ccu.edu.tw")
eAcc = drA.find_element_by_id("username_temp") # eCourse2 account
ePas = drA.find_element_by_id("password") # eCourse2 password
eSub = drA.find_elements_by_xpath("//button[@type='submit' and text() = 'Log in']")[0]  
eAcc.send_keys(secret.accE[0]) # eCourse2 account
ePas.send_keys(secret.accE[1]) # eCourse2 password
eSub.click() #click "Login in"
while(drA.current_url != "https://ecourse2.ccu.edu.tw/my/"): #wait till home page is logged
    time.sleep(intervalUnit)
print("logged")

time.sleep(intervalUnit*2) #assure that content of the page is fully logged
lcourse = drA.find_elements_by_class_name('course-listitem')
lcID = [x.get_attribute("data-course-id") for x in lcourse] # get course-id of each courses
ldata = list() # for storing data of each assignment

# for each course
for id in lcID:
    drA.get("https://ecourse2.ccu.edu.tw/course/view.php?id="+id) #direct to the webpage of a course by appending its id to the link

    lassign = drA.find_elements_by_class_name('modtype_assign')#access all assignments of the current course
    lassignl = [x.find_element_by_css_selector('a').get_attribute('href') for x in lassign] #retrive link for each assignment
    # for each assignment
    for link in lassignl:
        drA.get(link)
        DassignCon = dict() # dictionary for stroing properties of this assignments
        time.sleep(intervalUnit)
        DassignCon.update({
            "subject":drA.find_element_by_xpath('//h1/a').text,  #retrive course nane
            "title":drA.find_element_by_css_selector('h2').text  #retrive title of the assignment
        })
        try:
            #retrive text content(it's a bit more difficult so what I did is simply concatenate the text of each html element with a whitespace)
            lsubstr = [x.text for x in drA.find_element_by_id('intro').find_elements_by_css_selector('div')[0].find_elements_by_xpath('.//*')]
            string = ' '.join(lsubstr)
            DassignCon.update({"content":string})
        except:
            DassignCon.update({'content':""}) #if no content found
        ltd = drA.find_elements_by_xpath('//table[@class = "generaltable"]//td')
        DassignCon.update({"status":ltd[1].text,"deadline":ltd[3].text})
        ldata.append(DassignCon)  #append the dict to ldata
        print(DassignCon)
    print()
drA.close() #close webdriver
print("Web scraping procedure finished")

#### put the retrived data into Notion ####

db = nal.db(secret.API_INTETOKEN,secret.DBID0) # use a db object to represent a database specified by its database_id and authentication token of the user

db.grab()
lident = [assign0.get("Subject")+assign0.get("Name") for assign0 in db.lrows] #for checking if an assignment already exist in the database

#for each assignment data
for assign in ldata:
    if(assign["subject"]+assign["title"] in lident): # check if the assignment already exist
        continue
    tempRow = nal.row() # create an empty entry which would be appended to database later on
    tempRow.set("Subject",assign['subject'],"select") #set its "Subject" property,a select type property,to the course name of the current assignment
    tempRow.set("Name",assign['title'],"title") # you get it
    tempRow.set("Note",assign['content'],"rich_text")
    tempRow.set("Done","finished" if (assign['status'] == "已繳交") else "unfinished","select")
    #processing deadline
    rawDate = assign['deadline']
    lsep = [rawDate.index("年"),rawDate.index("月"),rawDate.index("日")] #for retriving Y,M,D seperatly
    datev = datetime.datetime(int(rawDate[:lsep[0]]),int(rawDate[lsep[0]+1:lsep[1]]),int(rawDate[lsep[1]+1:lsep[2]])) #convert it into a datetime object
    datev += datetime.timedelta(hours=23,minutes=59) #set its HH:mm to 23:59
    timezone = pytz.timezone("Asia/Taipei")
    datev = timezone.localize(datev) #setting timezone
    tempRow.set("Deadline",datev.isoformat(),"date") # set the value of property to the deadline in ISO formatting(Notion requires it)
    
    db.add(tempRow) #append the current entry to the database
    print(assign["title"],"appended")
print("Task completed successfully")



