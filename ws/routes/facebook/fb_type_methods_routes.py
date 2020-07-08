import os
import inspect
import traceback
import sys
import requests
import simplejson as json
import calendar
import time
import collections
import hashlib
from time import gmtime, strftime
from datetime import date, datetime
from importlib import reload

import MySQLdb as db
from waitress import serve
from flask import Flask, request, Blueprint

from .fb_settings import FbSettings
from classes.database import Database
from classes.utils import Utils
from facebook import facebook_blueprint


graphUrl = FbSettings.graphUrl
graphUrlId = FbSettings.graphUrlId
graphUrlPosts = FbSettings.graphUrlPosts
graphUrlVideos = FbSettings.graphUrlVideos


def typeMethodTypeOf(method_name): #Datos agrupados por tipo de.. (reacciones, num. de veces, etc)
	try:
		isValid = isValidJsonData(request)
		if isValid:
			jsonData = request.get_json()
			validArgs = areValidPostArguments(jsonData, ["account", "date_since", "date_until"])
			if validArgs["status"] == "error":
					return json.dumps(validArgs)
			if areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):
				if areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
					res_token = getToken(jsonData["account"])
					token = res_token["message"]
					url = buildUrl(graphUrl,token, method_name, jsonData["date_since"], jsonData["date_until"])
					req = requests.get(url)
					res = json.loads(req.text)
					jRes = [] #lista de datos que se muestran en json response
					for data in res["data"]:
						if data["period"] == "day":
							for values in data["values"]:
								value = values["value"] #value (nro de personas)
								fecha_temp = values["end_time"].split('T') #end_time
								fecha = fecha_temp[0]
								jRes.append(
								{
									fecha: value
								})
					jsonResponse = Utils.getResponseJson("success", "", False)
					jsonResponse["data"] = jRes
					return json.dumps(jsonResponse)
				else:
					return Utils.getResponseJson("error", "The maximum range is 90 days", False)
		else:
			return Utils.getResponseJson("error", "Invalid data format or not data available")
	except:
		Utils.setLog()
		return Utils.getResponseJson("error", "Programming failure")


@facebook_blueprint.route('/getPageImpressionsFrequencyDistribution', methods=['POST'])
def page_impressions_frequency_distribution():
	return typeMethodTypeOf("page_impressions_frequency_distribution")


@facebook_blueprint.route('/getPagePositiveFeedbackByTypeUnique', methods=['POST'])
def page_positive_feedback_by_type_unique():
	return typeMethodTypeOf("page_positive_feedback_by_type_unique")


@facebook_blueprint.route('/getPageFanAddsByPaidNonPaidUnique', methods=['POST'])
def page_fan_adds_by_paid_non_paid_unique():
	return typeMethodTypeOf("page_fan_adds_by_paid_non_paid_unique")


@facebook_blueprint.route('/getPageActionsPostReactionsTotal', methods=['POST'])
def page_actions_post_reactions_total():
	return typeMethodTypeOf("page_actions_post_reactions_total")


@facebook_blueprint.route('/getPageFansByUnlikeSourceUnique', methods=['POST'])
def page_fans_by_unlike_source_unique():
	return typeMethodTypeOf("page_fans_by_unlike_source_unique")


@facebook_blueprint.route('/getPageViewsExternalReferrals', methods=['POST'])
def page_views_external_referrals ():
	return typeMethodTypeOf("page_views_external_referrals") 


@facebook_blueprint.route('/getPageVideoViewsByPaidNonPaid', methods=['POST'])
def page_video_views_by_paid_non_paid():
	return typeMethodTypeOf("page_video_views_by_paid_non_paid") 


@facebook_blueprint.route('/getPagePostsImpressionsFrequencyDistribution', methods=['POST'])
def page_posts_impressions_frequency_distribution():
	return typeMethodTypeOf("page_posts_impressions_frequency_distribution") 


@facebook_blueprint.route('/getPageMessagesTotalMessagingConnections', methods=['POST'])
def page_messages_total_messaging_connections():
	return typeMethodTypeOf("page_messages_total_messaging_connections")


@facebook_blueprint.route('/getPageMessagesNewConversationsUnique', methods=['POST'])
def page_messages_new_conversations_unique():
	return typeMethodTypeOf("page_messages_new_conversations_unique")


@facebook_blueprint.route('/getPageMessagesBlockedConversationsUnique', methods=['POST'])
def page_messages_blocked_conversations_unique():
	return typeMethodTypeOf("page_messages_blocked_conversations_unique")


@facebook_blueprint.route('/getPageMessagesReportedConversationsUnique', methods=['POST'])
def page_messages_reported_conversations_unique():
	return typeMethodTypeOf("page_messages_reported_conversations_unique")