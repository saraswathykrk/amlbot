# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

#from rasa_core.domain import Domain
#from rasa_core.trackers import EventVerbosity
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import Restarted
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher


from typing import Any, Text, Dict, List
from operator import itemgetter

import json
import logging
import nltk
import urllib3
import requests
import asyncio

logger = logging.getLogger(__name__)
#nltk.download('punkt')


class ActionSlotReset(Action): 	
	def name(self): 		
		return 'action_slot_reset' 	
	def run(self, dispatcher, tracker, domain): 		
		return[SlotSet("previous", None), SlotSet("prev_count", "0")]


		
from bs4 import BeautifulSoup
import re


def topicnews(topic):
	"""api call for getting news based on specific topic"""
	response=requests.get("https://www.regxsa.com/aml-updates/posts-list-sra/") #"https://amlabc.com/aml-updates/posts-list-sra/")
	#print("resp:",response)
	quote_page = "https://www.regxsa.com/aml-updates/posts-list-sra/" #"https://amlabc.com/aml-updates/posts-list-sra/"
	http = urllib3.PoolManager()
	page=http.request('GET',quote_page)
	data=page.data
	#print(data)
	return data


def check(sentence1, words1):
	sentence = [x.lower() for x in sentence1]
	words = [x.lower() for x in words1]
	res = [all([k in s for k in words]) for s in sentence]
	return [sentence1[i] for i in range(0, len(res)) if res[i]]


class ActionGetInfo(Action):
	def name(self) -> Text:
		return 'action_get_info'


def run(self, dispatcher, tracker, domain):
	#request = await requests.get('http://api.icndb.com/jokes/random').json()  # make an api call
	joke = "test joke" #request['value']['joke']  # extract a joke from returned json response
	print("joke:",joke)
	dispatcher.utter_message(text=joke)  # send the message back to the user
	return []