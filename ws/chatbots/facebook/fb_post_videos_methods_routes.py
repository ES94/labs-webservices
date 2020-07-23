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

from . import facebook_blueprint
from .fb_settings import FbSettings
from classes.database import Database
from classes.settings import Settings
from classes.utils import Utils


graphUrl = FbSettings.graphUrl
graphUrlId = FbSettings.graphUrlId
graphUrlPosts = FbSettings.graphUrlPosts
graphUrlVideos = FbSettings.graphUrlVideos


def buildUrlPost(pageId, postId, token, metric, date_since, date_until):
	return "https://graph.facebook.com/v4.0/" + pageId + "_" + postId + "/insights?" + "access_token=" + token + "&metric=" + metric + "&since=" + str(date_since) + "&until=" + str(date_until)


def typeMethodPostsVideos(method_name): #Numero de visitas a post o reproducciones de videos (VER)
	try:
		isValid = Utils.isValidJsonData(request)
		if isValid:
			jsonData = request.get_json()
			validArgs = Utils.areValidPostArguments(jsonData, ["account", "date_since", "date_until", "posts"])
			if validArgs["status"] == "error":
				return json.dumps(validArgs)
			if Utils.areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):
				if Utils.areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
					res_token = Utils.getToken(Settings.host, Settings.user, Settings.pswd, jsonData["account"])
					token = res_token["message"]
					pageId = Utils.getPageId(FbSettings.graphUrlId, token)
					jRes = [] #lista de datos que se muestran en json response
					for post in jsonData["posts"]:
						url = Utils.buildUrlPost(pageId, post, token, method_name, jsonData["date_since"], jsonData["date_until"])
						print(url)
						req = requests.get(url)
						res = json.loads(req.text)
						for data in res["data"]:
							for value in data["values"]:
								valor_dato = value["value"]                       
								jRes.append({
									post : valor_dato  #idPost : valor
								})
					jsonResponse = Utils.getResponseJson("success", "", False)
					jsonResponse["data"] = jRes
					return json.dumps(jsonResponse)
				else:
					return getResponseJson("error", "The maximum range is 90 days", False)
		else:
			return getResponseJson("error", "Invalid data format or not data available")
	except:
		Utils.setLog()
		return Utils.getResponseJson("error", "Programming failure")


@facebook_blueprint.route('/getPostImpressions', methods=['POST'])
def post_impressions():
	return typeMethodPostsVideos("post_impressions") 


@facebook_blueprint.route('/getPostImpressionsUnique', methods=['POST'])
def post_impressions_unique():
	return typeMethodPostsVideos("post_impressions_unique") 


@facebook_blueprint.route('/getPostImpressionsPaid', methods=['POST'])
def post_impressions_paid():
	return typeMethodPostsVideos("post_impressions_paid")


@facebook_blueprint.route('/getPostImpressionsPaidUnique', methods=['POST'])
def post_impressions_paid_unique():
	return typeMethodPostsVideos("post_impressions_paid_unique")


@facebook_blueprint.route('/getPostImpressionsOrganic', methods=['POST'])
def post_impressions_organic():
	return typeMethodPostsVideos("post_impressions_organic") 


@facebook_blueprint.route('/getPostImpressionsOrganicUnique', methods=['POST'])
def post_impressions_organic_unique():
	return typeMethodPostsVideos("post_impressions_organic_unique") 


@facebook_blueprint.route('/getPostEngagedUsers', methods=['POST'])
def post_engaged_users():
	return typeMethodPostsVideos("post_engaged_users")


@facebook_blueprint.route('/getPostNegativeFeedbackByTypeUnique', methods=['POST'])
def post_negative_feedback_by_type_unique():
	return typeMethodPostsVideos("post_negative_feedback_by_type_unique") 


@facebook_blueprint.route('/getPostEngagedFan', methods=['POST'])
def post_engaged_fan():
	return typeMethodPostsVideos("post_engaged_fan") 


@facebook_blueprint.route('/getPostVideoCompleteViewsOrganicUnique', methods=['POST'])
def post_video_complete_views_organic_unique():
	return typeMethodPostsVideos("post_video_complete_views_organic_unique")


@facebook_blueprint.route('/getPostVideoCompleteViewsPaidUnique', methods=['POST'])
def post_video_complete_views_paid_unique():
	return typeMethodPostsVideos("post_video_complete_views_paid_unique")


@facebook_blueprint.route('/getPostVideoViewsOrganic', methods=['POST'])
def post_video_views_organic():
	return typeMethodPostsVideos("post_video_views_organic")


@facebook_blueprint.route('/getPostVideoViewsOrganicUnique', methods=['POST'])
def post_video_views_organic_unique():
	return typeMethodPostsVideos("post_video_views_organic_unique")


@facebook_blueprint.route('/getPostReactionsByTypeTotal', methods=['POST'])
def post_reactions_by_type_total():
	return typeMethodPostsVideos("post_reactions_by_type_total")