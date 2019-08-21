import requests
import xml.etree.ElementTree as ET
from .models import JessSettings


class JessApproval:
    # Jess server url stores the url to the jess server api to support integration
    JESS_SERVER_URL = "http://localhost:8080/JessBankApp/rest/api"
    # The headers required when performing a POST request
    headers = {'Content-Type': 'application/xml'}
    # The initial value of permit which allows the app to commit a transaction
    permit = False
    # The initial value of the response message which is rendered when the app fails to connect to the Jess server
    resMsg = "The application could not connect to the Jess server"

    def __init__(self, amount):
        self.amount = amount

    def setAmount(self, amount):
        self.amount = amount

    def setLimit(self, limit):
        self.limit = limit

    def setDifferent(self, diff):
        if diff == "no":
            self.different = 0
        else:
            self.different = 1

    def setNumOfTrans(self, num):
        self.numOfTrans = num

    def perform_request(self):
        jess_settings = JessSettings.objects.get(pk=1)
        # Pass in the request data
        self.reqData = """<transaction>
                            <amount>{}</amount>
                            <limit>{}</limit>
                            <different>{}</different>
                            <averageNumberOfTrans>{}</averageNumberOfTrans>
                            <setAverageNumberOfTrans>{}</setAverageNumberOfTrans>
                            <rule1Rank>{}</rule1Rank>
                            <rule2Rank>{}</rule2Rank>
                            <rule3Rank>{}</rule3Rank>
                          </transaction>""".format(self.amount, int(self.limit), self.different, int(self.numOfTrans),
                                                   jess_settings.no_of_transactions_limit, jess_settings.rule_one_rank,
                                                   jess_settings.rule_two_rank, jess_settings.rule_three_rank)

        # Read the response data in xml
        self.resData = requests.post(self.JESS_SERVER_URL, data=self.reqData, headers=self.headers).text.encode("utf-8")
        self.tree = ET.fromstring(self.resData)
        self.resMsg = self.tree.find('resMsg').text
        self.permit = self.tree.find('continue').text

    def print_reqData(self):
        print(self.reqData)
