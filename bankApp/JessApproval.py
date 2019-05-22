import requests
import xml.etree.ElementTree as ET

class JessApproval:
    # Jess server url stores the url to the jess server api to support integration
    JESS_SERVER_URL = "http://localhost:8080/bankAppApiServer/rest/api"
    # The headers required when performing a POST request
    headers = {'Content-Type':'application/xml'}
    # The initial value of permit which allows the app to commit a transaction
    permit = False
    # The initial value of the response message which is rendered when the app fails to connect to the Jess server
    resMsg = "The application could not connect to the Jess server"

    def __init__(self,amount):
        self.amount = amount

    def setAmount(self,amount):
        self.amount = amount

    def setLimit(self,limit):
        self.limit = limit
    
    def setDifferent(self,diff):
        self.different = diff
   
    def setNumOfTrans(self,num):
        self.numOfTrans = num

    def perform_request(self):
        #Pass in the request data
        self.reqData = """<transaction>
                            <amount>{}</amount>
                            <limit>{}</limit>
                            <different>{}</different>
                            <averageNumberOfTrans>{}</averageNumberOfTrans>
                          </transaction>""".format(self.amount,int(self.limit),self.different,int(self.numOfTrans))

        #Read the response data in xml     
        self.resData = requests.post(self.JESS_SERVER_URL,data=self.reqData, headers = self.headers).text.encode("utf-8")
        self.tree = ET.fromstring(self.resData)
        self.resMsg = self.tree.find('resMsg').text
        self.permit = self.tree.find('continue').text
        