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

	def run(self, 
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		keyword_dets=tracker.get_slot('keyword')
		category_dets=tracker.get_slot('category')
		latest_dets=tracker.get_slot('latest')
		previous_dets=tracker.get_slot('previous')
		prev_count_dets=tracker.get_slot('prev_count')
		date_dets=tracker.get_slot('dated')
		print(keyword_dets)

		if category_dets is None:
			ret_category='news articles'
		else:
			ret_category=category_dets

		if previous_dets is None and keyword_dets is None:
			dispatcher.utter_message(template="utter_keyword",category_item=ret_category)
		else:
			print(category_dets)
			if category_dets is None:
				category_dets = 'aml-news'
			elif category_dets.lower() in ('news','information','links','details','detail','data'):
				category_dets = 'aml-news'
			elif category_dets.lower() in ('cases','case','report', 'reports'):
				category_dets = 'aml-case-studies'
			elif category_dets.lower() in ('fine','fines'):
				category_dets = 'aml-sanctions-fines'
			else:
				category_dets = 'aml-news'

			if latest_dets is None:
				latest_flag = False
			else:
				latest_flag = True

			pop_flag=False

			#print("prev_count_dets:",prev_count_dets)

			if previous_dets is None:
				pop_flag=False
				prev_count_dets1 = "0"
			else:
				if prev_count_dets is None:
					prev_count_dets1 = "1"
				elif prev_count_dets == "0":
					prev_count_dets1 = "1"
				else:
					prev_count_dets1 = int(prev_count_dets) + 1

				for i in previous_dets:	
					if i in ('previous','previously','earlier','first','help','more','few'):
						pop_flag=True
						#print("pop flag True")
					else:
						print("all ok")

			quote_page = "https://www.regxsa.com/aml-updates/posts-list-sra/" #"https://amlabc.com/aml-updates/posts-list-sra/"
			http = urllib3.PoolManager()
			#print('keyword:', keyword_dets)
			#print('category:', category_dets)
			
			page=http.request('GET',quote_page)
			soup = BeautifulSoup(page.data, 'html.parser')

			list1=[]
			list2=[]
			list3=[]
			list4=[]

			tweetArr = []
			for tweet in soup.findAll('tr',attrs={"id": re.compile("TR_")}):
				tweetObject = {"post_id": tweet.find('td', attrs={"id": "post_id"}).text,#.encode('utf-8'),
					"post_title": tweet.find('td', attrs={"id": "post_title"}).text,#.encode('utf-8'),
					"post_date": tweet.find('td', attrs={"id": "post_date"}).text,#.encode('utf-8'),
					"post_url": tweet.find('td', attrs={"id": "post_url"}).text,#.encode('utf-8'),
					"post_source": tweet.find('td', attrs={"id": "post_source"}).text,#.encode('utf-8'),
					"post_via": tweet.find('td', attrs={"id": "post_via"}).text,#.encode('utf-8'),
					"post_content": tweet.find('td', attrs={"id": "post_content"}).text.replace("\n","")#.encode('utf-8')
				}
				tweetArr.append(tweetObject)
			
			tweetArr1 = sorted(tweetArr, key=itemgetter('post_date'), reverse = True)
			

			data=tweetArr1
			counter=0
			leng=len(data)
			out_flag=False
			for i in range(leng):
				list_tmp=[]
				list_tmp.extend(nltk.tokenize.sent_tokenize(data[i]['post_content']))
				keyword_dets=nltk.tokenize.word_tokenize(' '.join(map(str, keyword_dets)))
				print('nltk',i,list_tmp)
				output = check(list_tmp,keyword_dets)
				print(output)
				if output:
					#print('in here::',prev_count_dets1)
					out_flag=True
					if category_dets == data[i]['post_url'].split('/')[4]:
						#print(output[0],data[i]['post_url'],data[i]['post_title'],data[i]['post_date'])
						list1.append(output[0])
						list2.append(data[i]['post_url'])
						list3.append(data[i]['post_title'])
						list4.append(data[i]['post_date'])
						#print(list1[0],list2[0],list3[0],list4[0])
					
						if pop_flag:
							print('in if of pop',int(prev_count_dets1),i, counter)
							if counter == int(prev_count_dets1):
								break
							else:
								counter=counter+1
							
						else:
							break
			'''if not out_flag:
				for i in range(leng):
					list_tmp=[]
					list_tmp.extend(nltk.tokenize.sent_tokenize(data[i]['post_content']))
					keyword_dets=nltk.tokenize.word_tokenize(' '.join(map(str, keyword_dets)))
					print('nltk',keyword_dets)
					output = check_sub(list_tmp,keyword_dets)'''


			
			print_yes=False
			#print("list1:",len(list1))
			if len(list1) > 0:
				if pop_flag:
					#if len(list2) > 1 and int(prev_count_dets1) < len(list2):
					if len(list2) > 1 and counter < len(list2):
						print("prev_count_dets1",prev_count_dets1,counter)
						print(list1[counter],list2[counter],list3[counter],list4[counter])
						title=list3[counter]
						link=list2[counter]
						output=list1[counter]
						dated=list4[counter]
						dispatcher.utter_message(   template="utter_output",
												dated=dated,
												output=output,
												title=title,
												link=link)
						dispatcher.utter_message(template="utter_help")
					else:
						dispatcher.utter_message(template="utter_rephrase",category_item=ret_category)
				else:
					#print(list1[0],list2[0],list3[0],list4[0])
					print_yes=True
				if latest_flag or print_yes:
					print(list1[0],list2[0],list3[0],list4[0])
					title=list3[0]
					link=list2[0]
					output=list1[0]
					dated=list4[0]
					
					dispatcher.utter_message(   template="utter_output",
												dated=dated,
												output=output,
												title=title,
												link=link)
					dispatcher.utter_message(template="utter_help")
			else:
				dispatcher.utter_message(template="utter_rephrase", category_item=ret_category)

		
		return [SlotSet('prev_count',prev_count_dets1)]