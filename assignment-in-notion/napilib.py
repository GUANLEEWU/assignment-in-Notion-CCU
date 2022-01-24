import requests

class db: #database object
    NOTION_URL = 'https://api.notion.com/v1/databases/'
    def __init__(self,token,id): #instantiation
        self.token = token # a database is defined by the authorization token and
        self.dbID = id # its id(can be derived from its URL)
    
    def add(sf,row): #append add a row object to the actual database
        datad = row.getJson() #get json data of the row object
        datad["parent"]["database_id"] = sf.dbID #specify target database in Json
        response = requests.post( #send a "create page" request to the endpoint
            'https://api.notion.com/v1/pages', #endpoint URL
            headers={
                "Authorization": f"Bearer {sf.token}", #authorization
                "Notion-Version": "2021-08-16", #required
                "Content-Type": "application/json" #required
            },
            json=datad #json
        )
        if response.status_code != 200:
                print("error",response)
    
    def grab(self,filter= None,sort= None): #retrive latest data of the database
        if(filter is None and sort is None): #the filter and sort parameters are for future development
            response = requests.post( #send a "retrive database" request to the endpoint
                self.NOTION_URL+self.dbID+"/query", #endpoint URL
                headers={
                    "Authorization": f"Bearer {self.token}", #authorization
                    "Notion-Version": "2021-08-16", 
                    "Content-Type": "application/json" 
                }
            )
            if response.status_code != 200: #check if there's an error
                raise Exception("Error")
            self.data_j = response.json() #store the json file they responded into data_j(it would be converted into dict object automatically)
            self.parseTolist() # parse data_j into a list of row object and save them

    def parseTolist(self): # parse data_j into a list of row object and save them
        self.lrows = list()
        for i in range(len(self.data_j["results"])): # for each entry
            self.lrows.append(row(raw=self.data_j["results"][i])) #create a row object using json data and append it to lrows

class row: # a object that represent row(entry) for database
    def __init__(self,**kwargs):
        if kwargs.get("raw"): # if "raw" is specified, use it as the json data of the row
            self.data_d = kwargs["raw"]
        else:
            self.data_d = {"parent":{},"properties":{}} # else construct a empty json data

    def getJson(sf):
        return sf.data_d

    def get(sf,prop): #retrive a property value of the row using the property name
        prop_j = sf.data_d["properties"][prop] #location of the prop property
        ptype = prop_j["type"] #access the type of prop
        #return the queried value from the correct spot in the json data according to its type 
        if(ptype == "title" or ptype == "rich_text"):
            return prop_j[ptype][0]["text"]["content"]
        elif(ptype == "number"):
            return prop_j[ptype]
        elif(ptype == "select"):
            return prop_j[ptype]["name"]
        elif(ptype == "multi_select"):
            l = list()
            for x in prop_j[ptype]:
                l.append(x["name"])
            return l # a list of all selected value
        elif(ptype == "date"):
            return prop_j[ptype]['start'] #iso format

    def set(sf,prop,val,ptype): #set the value of a property
        # manipulate its json data according to the property name,value to be set with and the type of the property
        if(ptype == "title" or ptype == "rich_text"):
            sf.data_d["properties"].update({prop:{ptype:[{"text":{"content":val}}]}})
        elif(ptype == "select"):
            sf.data_d["properties"].update({prop:{ptype:{"name":val}}})
        elif(ptype == "date"):
            sf.data_d["properties"][prop] = {ptype:{"start":val}}
        elif(ptype == "checkbox"):
            sf.data_d["properties"].update({prop:{ptype:val}})
   




    
