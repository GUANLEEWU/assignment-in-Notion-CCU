# assignment-in-Notion-CCU
A Python program specifically designed for students of CCU, it collects all your assignments available in eCourse2 and put them in a Notion database via API, which allows us to view these assignments the way we want to, for example, use calendar view to show the deadlines or categorize each assignment according to its subject.

**Since the program is originally designed for personal use, its readiblity, flexibility and efficiency is still far from perfeciton, sorry about that.**
## How to use
First, make sure the following Python module is installed: **webdriver-manager**, **selenium**, **pytz**.\
You need to have a Notion account, it's free to register, and it even unlocks unlimited plan if you register your account with the school's gamil account.\
First, go to this webpage: https://lateral-havarti-7dd.notion.site/My-Assignments-10654ef5bf544c928733226d7fb0f05b

![alt](https://github.com/rTheDev/imgs/blob/main/Screen%20Shot%202022-01-24%20at%2011.01.15%20PM.png)

This is the page that shows all your assignments, sure you can use your own design if you want to.\
Now click **Duplicate** on the top-right corner.(Log in if demanded)

This will create a clone of this page on your account.\
In the cloned page in your account, click "open as page" button of the calendar view(for it's the main database), check the URL of this page, the segment after "https://www.notion.so/" and before "?" is the **database-id** of the database.
![alt](https://github.com/rTheDev/imgs/blob/main/Screen%20Shot%202022-01-24%20at%2011.01.57%20PM.png)
![alt](https://github.com/rTheDev/imgs/blob/main/Screen%20Shot%202022-01-24%20at%2011.02.53%20PM.png)
Now go to this webpage:https://www.notion.so/my-integrations
Log in, click **create new integration**, then you get your **integration token**
![alt](https://github.com/rTheDev/imgs/blob/main/Screen%20Shot%202022-01-24%20at%2011.03.52%20PM.png)
![alt](https://github.com/rTheDev/imgs/blob/main/Screen%20Shot%202022-01-24%20at%2011.04.20%20PM.png)
After the integration is created, go back to Notion(the place you went after you clicked "open as page"), click the **share** button on the top-right corner, click **invite** , then pick the integration you just created, this would allow the integration to control this particular page(in this case, the assignments database). 
![alt](https://github.com/rTheDev/imgs/blob/main/Screen%20Shot%202022-01-26%20at%2010.26.53%20PM.png)
Download the source code and open it with an IDE. Assign the **integration token** and **database-id** to the corresponding variable in **secret.py**, finally keys in your eCourse2 account and password.\
After the above setting is done, execute **get&set.py** and you will see all your assignments being added to your Notion page automatically.

## Content
There are mainly two python file in this program.
### getAndSet.py
It's the file to be executed.
When executed, the program open a webdriver using the **selenium**,a library specifically designed for web scraping.\
Initially it would be directed to the login page of eCourse2, then it logs in, opens the links of the courses one by one.
For each course, the links of its assignments would be opened one by one, retriving information from it, specifically the name of its subject, the title, the content text, deadline and whether it's handed in or not.\
The retrived information is then used to construct dictionaries, one for each assignment, ultimately forming a list, which contains all the information needed for the next part.

In this part, the information about each assignments is accessed one by one, processed and appended to a Notion database using another python file, **napilib**.\
First, a **db** object(database object) is instantiated with the **integration token** and **database id** of the target database, both of which can obtained using the method I mentioned earlier.
And then, for each assignment, creates an empty **row** object, then set the value of each property according to those information via the **set** method.
When the construction of a row object is done, append it to the database using the **add** method of **db**, this will add the **row** object to Notion as an entry ,all in real time.

When the process is done for all assignments, the program is then quitted.

### napilib.py
The name "napilib" stands for "Notion API library".\
It provides classes, methods that turns databases and pages(entries) in Notion into objects, so that we can interact with Notion indirectly without writing lines and lines of codes to manipulate json object and do request sending.

The api contains two classes.

The class **db** represents a database, the **integration token** and **database id** is required when such object is being instantiated.\
When the "grab" method is called, the program sends request to the endpoint, retriving a json object that contains information about the database.
the "parseToList" method is then called, it processes the json object and produce a list that contains all the entries of this database, in the form of **row** object.
The **add** method takes in a **row** object, and append it to the database in Notion as an entry.

The class **row** represents entries of a database, and can be instantiated with a json object, or with nothing, which creates an empty entry.
The "get" method returns the value of the property specified, using the name of the property.
The "set" method, intuitively, set the value of the property specified by its name and type, to the value specified. Note that the type of the property is a string.

## Reference
Although Notion Inc. doesn't offer an offical API for Python, it does provide a detailed webpage that explains how to interact with Notion using cURL and JSON-formatted strings.
The development of **napilib.py** is mostly based on the webpage:\
https://developers.notion.com/reference/intro






