import json
import requests
import time
import os
from functools import wraps


class Credentials:

    def __init__(self, internal_ip_address=None, username=None):

        self.internal_ip_address = internal_ip_address
        self.username = username

    def _get_internal_ip_address(self):
        """
        Gets the internal ip address for the hue bridge within the current network
        """
        req = requests.get('https://discovery.meethue.com/')
        self.internal_ip_address = req.json()[0]['internalipaddress']

        return

    def _save_credentials(self):

        with open('./hueSignalCredentials.json', 'w') as file:
            json.dump({"username": self.username,
                       "internal_ip_address": self.internal_ip_address}, file)

        print("Credentials saved to {}".format(os.getcwd()))

        return

    def create(self):
        """
        Finds the internal ip address and creates a username. The user should physically press the bridge button.
        """

        self._get_internal_ip_address()

        requests.post('http://{}/api'.format(self.internal_ip_address),
                      data=json.dumps({"devicetype": "hueSignal"}))

        print("Please go and press the button on the bridge!")

        i = 20
        while i > 0:
            time.sleep(1)
            print('{} seconds remaining.'.format(i), end='\r')
            i -= 1
        req = requests.post('http://{}/api'.format(self.internal_ip_address),
                            data=json.dumps({"devicetype": "hueSignal"}))

        if 'success' in req.json()[0]:
            self.username = req.json()[0]['success']['username']
            self._save_credentials()
        else:
            print("You didn't press the button, didn't you? Try again.")
        return


class HueSignal:

    def __init__(self):

        self.red = {'on': True, 'sat': 254, 'bri': 254, 'hue': 65535, 'xy': [0.675, 0.322]}
        self.green = {'on': True, 'sat': 254, 'bri': 254, 'hue': 21845, 'xy': [0.409, 0.518]}
        self.blue = {'on': True, 'sat': 254, 'bri': 254, 'hue': 43690, 'xy': [0.167, 0.04]}
        self.good = self.green
        self.bad = self.red
        self.light = 'http://{}/api/{}/lights/1/state'.format(self.internal_ip_address, self.username)

        if os.path.isfile('./hueSignalCredentials.json'):
            self._get_credentials_from_file()
        else:
            self._create_new_credentials()

    def _get_credentials_from_file(self):

        print("hueSignalCredentials loaded from file.")
        with open('./hueSignalCredentials.json', 'r') as reader:
            credentials = json.load(reader)
        self.username = credentials["username"]
        self.internal_ip_address = credentials["internal_ip_address"]

    def _create_new_credentials(self):
        credentials = Credentials()
        credentials.create()
        self.username = credentials.username
        self.internal_ip_address = credentials.internal_ip_address

    def __call__(self, func):

        @wraps(func)
        def hue_signal_wrapper(*args, **kwargs):

            try:
                result = func(*args, **kwargs)
                requests.put(self.light, data=json.dumps(self.good))

            except Exception as e:

                requests.put(self.light, data=json.dumps(self.bad))
                raise e

            return result

        return hue_signal_wrapper
