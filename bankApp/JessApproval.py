import requests
import xml.etree.ElementTree as ET

class JessApproval:
    # Jess server url stores the url to the jess server api to support integration
    JESS_SERVER_URL = "http://localhost:8080/BankApp/rest/api"
    headers = {'Content-Type':'application/xml'}
    permit = False
    resMsg = "The application could not connect to the Jess server"

    def __init__(self,amount):
        self.amount = amount

    def get_amount(self):
        return self.amount

    def set_amount(self,amount):
        self.amount = amount

    def get_limit(self):
        return self.limit

    def set_limit(self,limit):
        self.limit = limit

    def perform_request(self):
        #Pass in the request data
        self.reqData = """<transaction><amount>{}</amount><limit>{}</limit></transaction>""".format(self.amount,int(self.limit))

        #Read the response data in xml     
        self.resData = requests.post(self.JESS_SERVER_URL,data=self.reqData, headers = self.headers).text.encode("utf-8")
        self.tree = ET.fromstring(self.resData)
        self.resMsg = self.tree.find('resMsg').text
        self.permit = self.tree.find('continue').text
       

