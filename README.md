# assignment-in-Notion
A python program specifically designed for students in CCU, it collect all your assignments available in eCourse2 and put them in a Notion database via API.\
**Since the program is originally designed for personal use, its readiblity, flexibility and efficiency is still far from perfeciton, sorry about that.**

## content
There are mainly two python file in this program.
### get&set.py
It's the file to be executed.
When executed, the program open a webdriver using the selenium library, which is designed for web scraping.\
Initially it would be directed to the login page of eCourse2, then it logs in, opens the links of the courses one by one.
For each course, the links of its assignments would be opened one by one, retriving informations about it, specifically the name of its subject, the title, the content text, deadline and whether it's handed in or not.\
The retrived information is then put into a dictionary, finally collected into a list, which contains all the information needed for the next part.

In this part, the information about each assignments is accessed one by one, processed and appended into a Notion database using the classes from another python file, napilib.\
First, a db object(database object) is instantiated with the "integration token" and "database id", both of which can obtained using the method I mentioned earlier.
And then, for each assignment, creates an empty row object, then set the value of each property with those information, via the "set" method.
When the construction of a row object is done, append it to the database using the "add" method of the db object, this will actually add this row object as an entry to Notion in real time.

When the process is done for all assignments, the program is then ended.

### napilib.py
The name "napilib" stands for "Notion API library".\
It provides classes, methods to turn databases and pages(entries) in Notion into python objects, so that we can interact with Notion directly without having to manipulate the json data and request sending.

The api contains two classes.

The class "db" represents a database, the authentication token and database id is required when such object is being instantiated.\
When the "grab" method is called, the program request from the Notion server, retriving a json object that contains every information about this database in real time.
the "parseToList" method is then called, it process the json file and produce a list that contains all the entries of this database, in the form of "row" objects.
The "add" method takes in a row object, and append it as an entry to the database in Notion.

The class "row" represents entries of a database, and can be instantiated with a json object or with nothing, creating a empty entry.
The "get" method returns the value of the property specified, using the name of the property.
The "set" method, intuitively, set the value of the property specified by its name and type, to the value specified.Please note that the type of the property is a string.






