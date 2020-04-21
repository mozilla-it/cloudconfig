from typing import Dict
from cloudsecrets.gcp import Secrets
from google.cloud import firestore
import json

class DynamicPropertyManagementClient:
    properties: Dict[str, str] = dict()

    def __init__(self, service_name: str, program_name: str):
        def on_snapshot(doc_snapshot, changes, read_time):
            for change in changes:
                self.properties = change.document.to_dict()

        self.service = service_name
        self.program = program_name
        if not self.program or not self.service:
            raise Exception("Error: must provide service name and program name")

        self.doc_path = f"dpm-configs/{self.service}-{self.program}"
        self.firestore_client = firestore.Client()
        self.doc_ref = self.firestore_client.document(self.doc_path)
        doc_watch = self.doc_ref.on_snapshot(on_snapshot)

    def get_dynamic_properties(self) -> Dict[str, str]:
        return dict(self.properties)

    def update_property(self, key: str, value: str):
        self.properties = json.loads("""{
"sender_id": {"description": "The sender id we are using to communicate with Intacct", "value": "MOZ Corp2"}, 
"start_to_read_from_date": {"description": "", "value": "11/12/2012"}, 
"5650": {"description": "5650 - Firefox Engineering Operations", "value": "Drew Wilson"}, 
"5700": {"description": "5700 - User Experience", "value": "Drew Wilson"}, 
"1001.01": {"description": "1001.01 - OOTC, MOSS Grants", "value": "Winnie Aoieong"}, 
"DKK": {"description": "", "value": "0.1486"}, 
"1170.1": {"description": "1170.1 - G&A", "value": "Nicholas Grammater"}, 
"1170.2": {"description": "1170.2 - Finance / Accounting", "value": "Nicholas Grammater"}, 
"Australia": {"description": "", "value": "AUD"}, 
"1170.3": {"description": "1170.3 - Revenue & Sales", "value": "Nicholas Grammater"},  
"1170.4": {"description": "1170.4 - Editorial", "value": "Nicholas Grammater"}, 
"1170.5": {"description": "1170.5 - Marketing", "value": "Nicholas Grammater"}, 
"2200": {"description": "2200 - Mar Com", "value": "Nicholas Grammater"}, 
"Taiwan": {"description": "", "value": "TWD"}, 
"1170.6": {"value": "Nicholas Grammater", "description": 
"1170.6 - Community"}, "1170.7": {"description": 
"1170.7 - Engineering", "value": "Nicholas Grammater"}, 
"1170.8": {"description": "1170.8 - Product", "value": "Nicholas Grammater"}, 
"1170.9": {"description": "1170.9 - Design", "value": "Nicholas Grammater"}, 
"Chicago": {"description": "", "value": "USD"}, 
"START_TO_READ_FROM_DATE": {"value": "11/12/2012", "description": "The PO report pulls all records starting from this date"}, 
"Portland": {"description": "", "value": "USD"}, 
"Data Center - MDC1": {"description": "", "value": "USD"}, 
"2300": {"description": "2300 - Lifecycle Marketing", "value": "Nicholas Grammater"}, 
"Data Center - MDC2": {"description": "", "value": "USD"}, 
"GBP": {"description": "", "value": "1.3074"}, 
"New Zealand": {"description": "", "value": "NZD"}, 
"5900": {"description": "5900 - Program Management", "value": "Drew Wilson"}, 
"5850": {"description": "5850 - Mozilla Product Discovery", "value": "Drew Wilson"}, 
"2400": {"description": "2400 - Brand Engagement", "value": "Nicholas Grammater"}, 
"NZD": {"value": "0.6616", "description": ""}, 
"5000": {"value": "Drew Wilson", "description": "5000 - Firefox"}, 
"5010": {"value": "Drew Wilson", "description": "5010 - Advanced Technology"}, 
"2500": {"description": "2500 - Marketing Operations", "value": "Nicholas Grammater"}, 
"EUR": {"description": "", "value": "1.1104"}, 
"1000": {"description": "1000 - Office of CEO", "value": "Winnie Aoieong"}, 
"1001": {"description": "1001 - Office of Chair", "value": "Winnie Aoieong"}, 
"1002": {"value": "Winnie Aoieong", "description": "1002 - State of the Internet"}, 
"1003": {"description": "1003 - Office of CIO", "value": "Michael Standifer"}, 
"1004": {"description": "1004 - CEO Strategic Reserve", "value": "Winnie Aoieong"}, 
"1010": {"description": "1010 - Emerging Technologies", "value": "Nishanth Billa"}, 
"1005": {"description": "1005 - Corp Consolidation & Elimination", "value": "Winnie Aoieong"}, 
"1011": {"description": "1011 - Mixed Reality", "value": "Nishanth Billa"}, 
"1006": {"description": "1006 - Emerging Markets", "value": "Nicholas Grammater"}, 
"1007": {"description": "1007 - New Markets", "value": "Nicholas Grammater"}, 
"1012": {"description": "1012 - Developer Outreach", "value": "Nishanth Billa"}, 
"1013": {"description": "1013 - Advanced Development", "value": "Nishanth Billa"}, 
"1014": {"description": "1014 - Voice", "value": "Nishanth Billa"}, 
"Pocket": {"description": "", "value": "USD"}, 
"1015": {"description": "1015 - Experiences & Design", "value": "Nishanth Billa"}, 
"1020": {"value": "Michael Standifer", "description": "1020 - Internal Comms"}, 
"5100": {"description": "5100 - Desktop Product Development", "value": "Drew Wilson"}, 
"5110": {"value": "Drew Wilson", "description": "5110 - Desktop Privacy & Security"}, 
"timeout": {"description": "This is how long we will wait for a response from the Intacct service", "value": "30"}, 
"5120": {"value": "Drew Wilson", "description": "5120 - Desktop Ecosystem & Experimentation"}, 
"1100": {"description": "1100 - Global Policy", "value": "Michael Standifer"}, 
"1101": {"description": "1101 - Security and Trust", "value": "Michael Standifer"}, 
"1120": {"description": "1120 - Legal", "value": "Michael Standifer"}, 
"5200": {"description": "5200 - Firefox Web Platform", "value": "Drew Wilson"}, 
"user_id": {"description": "Our User id with Intacct", "value": "datateam"}, 
"SF": {"description": "", "value": "USD"}, 
"Toronto": {"description": "", "value": "CAD"}, 
"5210": {"description": "5210 - Gecko Platform Initiatives", "value": "Drew Wilson"}, 
"2700": {"description": "2700 - Product Marketing", "value": "Nicholas Grammater"}, 
"5220": {"description": "5220 - Web Futures", "value": "Drew Wilson"}, 
"unique_id": {"description": "This is a parameter is use to parse the base Intacct XML", "value": "true"}, 
"1145": {"description": "1145 - Data Science & Analytics", "value": "Michael Standifer"}, 
"1150": {"description": "1150 - Business Development", "value": "Michael Standifer"}, 
"include_whitespace": {"description": "This is a parameter is use to parse the base Intacct XML", "value": "false"}, 
"5230": {"description": "5230 - Gecko Platform", "value": "Drew Wilson"}, 
"1210": {"description": "1210 - Finance and Accounting", "value": "Michael Standifer"}, 
"UK": {"description": "", "value": "GBP"}, "1211": {"description": "1211 - Accounting", "value": "Michael Standifer"}, 
"1212": {"description": "1212 - Finance", "value": "Michael Standifer"}, 
"1213": {"description": "1213 - Payroll", "value": "Michael Standifer"}, 
"5240": {"description": "5240 - Engineering Efficiency", "value": "Drew Wilson"}, 
"1214": {"description": "1214 - Procurement", "value": "Michael Standifer"}, 
"1170": {"description": "1170 - Read It Later", "value": "Nicholas Grammater"}, 
"sleep_time_between_inserts": {"description": "This is how long we wait between inserts. This gives the Intacct API a break, so our calls dont saturate their API", "value": "3"}, 
"1180": {"description": "1180 - Customer Success", "value": "Michael Standifer"}, 
"dtd_version": {"description": "The version of the Intacct API we are using", "value": "3.0"}, 
"Evelyn": {"description": "", "value": "USD"}, "1250": {"description": "1250 - Facilities", "value": "Michael Standifer"}, 
"Germany": {"description": "", "value": "EUR"}, "1310": {"description": "1310 - D&I", "value": "Michael Standifer"}, 
"1256": {"description": "1256 - Environment Sustainability", "value": "Michael Standifer"}, 
"Vancouver": {"description": "", "value": "CAD"}, 
"1320": {"description": "1320 - People Operations", "value": "Michael Standifer"}, 
"url": {"description": "This is the URL that hosts the Intacct API", "value": "https://api.intacct.com/ia/xml/xmlgw.phtml"}, 
"CAD": {"description": "", "value": "0.7648"}, 
"5400": {"description": "5400 - Mobile", "value": "Drew Wilson"}, 
"1330": {"description": "1330 - Total Rewards", "value": "Michael Standifer"}, 
"1340": {"description": "1340 - People", "value": "Michael Standifer"}, 
"1400": {"description": "1400 - Information Technology Services", "value": "Michael Standifer"}, 
"1350": {"description": "1350 - Recruiting", "value": "Michael Standifer"}, 
"1410": {"description": "1410 - Infrastructure Eng and Ops (Infra)", "value": "Michael Standifer"}, 
"Belgium": {"description": "", "value": "EUR"}, 
"TWD": {"description": "", "value": "0.0333"}, 
"INTACCT_API_TIME_BETWEEN_RETRIES": {"description": "", "value": "30"}, 
"1420": {"description": "1420 - Enterprise Information Security (EIS)", "value": "Michael Standifer"}, 
"USD": {"description": "", "value": "1"}
}
""")
        self.doc_ref.update({u''+key+'': u''+value+''})


class SecretsClient:

    def __init__(self, secrets_name: str, project: str, polling_interval: int = 0):
        self.secrets_name = secrets_name
        self.polling_interval = polling_interval
        if not self.secrets_name:
            raise Exception("Error: must secret_name")
        self.secrets = Secrets(self.secrets_name, polling_interval=self.polling_interval, project=project)

    def get_secret(self, key: str) -> str:
        return dict(self.secrets).get(key)
