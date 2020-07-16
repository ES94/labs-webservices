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
from . import facebook_blueprint


graphUrl = FbSettings.graphUrl
graphUrlId = FbSettings.graphUrlId
graphUrlPosts = FbSettings.graphUrlPosts
graphUrlVideos = FbSettings.graphUrlVideos


def typeMethodNumberOf(method_name): #Datos agrupados por numero de.. (personas, veces, clicks, milisegundos)
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
					url = buildUrl(graphUrl, token, method_name, jsonData["date_since"], jsonData["date_until"])
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


@facebook_blueprint.route('/getPageImpressionsUnique', methods=['POST'])
def page_impressions_unique():
	return typeMethodNumberOf("page_impressions_unique")


@facebook_blueprint.route('/getPageImpressionsPaidUnique', methods=['POST'])
def page_impressions_paid_unique():
	return typeMethodNumberOf("page_impressions_paid_unique")


@facebook_blueprint.route('/getPageImpressionsOrganicUnique', methods=['POST'])
def page_impressions_organic_unique():
	return typeMethodNumberOf("page_impressions_organic_unique")


@facebook_blueprint.route('/getPagePostEngagements', methods=['POST'])
def page_post_engagements():
	return typeMethodNumberOf("page_post_engagements")


@facebook_blueprint.route('/getPageEngagedUsers', methods=['POST'])
def page_engaged_users():
	return typeMethodNumberOf("page_engaged_users")


@facebook_blueprint.route('/getPageConsumptionsUnique', methods=['POST'])
def page_consumptions_unique():
	return typeMethodNumberOf("page_consumptions_unique")


@facebook_blueprint.route('/getPageNegativeFeedbackUnique', methods=['POST'])
def page_negative_feedback_unique ():
	return typeMethodNumberOf("page_negative_feedback_unique")


@facebook_blueprint.route('/getPageTotalActions', methods=['POST'])
def page_total_actions():
	return typeMethodNumberOf("page_total_actions")


@facebook_blueprint.route('/getPageFans', methods=['POST'])
def page_fans():
	return typeMethodNumberOf("page_fans") 


@facebook_blueprint.route('/getPageFanAdds', methods=['POST'])
def page_fan_adds():
	return typeMethodNumberOf("page_fan_adds")


@facebook_blueprint.route('/getPageFanAddsUnique', methods=['POST'])
def page_fan_adds_unique():
	return typeMethodNumberOf("page_fan_adds_unique")


@facebook_blueprint.route('/getPageFanRemovesUnique', methods=['POST'])
def page_fan_removes_unique():
	return typeMethodNumberOf("page_fan_removes_unique")


@facebook_blueprint.route('/getPageViewsTotal', methods=['POST'])
def page_views_total():
	return typeMethodNumberOf("page_views_total") 


@facebook_blueprint.route('/getPageVideoViews', methods=['POST'])
def page_video_views():
	return typeMethodNumberOf("page_video_views")


@facebook_blueprint.route('/getPageVideoViewsClickToPlay', methods=['POST'])
def page_video_views_click_to_play():
	return typeMethodNumberOf("page_video_views_click_to_play")   


@facebook_blueprint.route('/getPageVideoViewTime', methods=['POST'])
def page_video_view_time():
	return typeMethodNumberOf("page_video_view_time")    


@facebook_blueprint.route('/getPagePostsImpressions', methods=['POST'])
def page_posts_impressions():
	return typeMethodNumberOf("page_posts_impressions")  


@facebook_blueprint.route('/getPagePostsImpressionsUnique', methods=['POST'])
def page_posts_impressions_unique():
	return typeMethodNumberOf("page_posts_impressions_unique") 


@facebook_blueprint.route('/getPagePostsImpressionsPaid', methods=['POST'])
def page_posts_impressions_paid():
	return typeMethodNumberOf("page_posts_impressions_paid") 


@facebook_blueprint.route('/getPagePostsImpressionsPaidUnique', methods=['POST'])
def page_posts_impressions_paid_unique():
	return typeMethodNumberOf("page_posts_impressions_paid_unique") 


@facebook_blueprint.route('/getPagePostsImpressionsOrganic', methods=['POST'])
def page_posts_impressions_organic():
	return typeMethodNumberOf("page_posts_impressions_organic")


@facebook_blueprint.route('/getPagePostsImpressionsOrganicUnique', methods=['POST'])
def page_posts_impressions_organic_unique():
	return typeMethodNumberOf("page_posts_impressions_organic_unique")