from . import facebook_blueprint
from classes.facebook import Facebook


@facebook_blueprint.route('/getPageContentActivityByAgeGenderUnique', methods=['POST'])
def page_content_activity_by_age_gender_unique():
	return Facebook.typeMethodGenderAge("page_content_activity_by_age_gender_unique") 


@facebook_blueprint.route('/getPageImpressionsByAgeGenderUnique', methods=['POST'])
def page_impressions_by_age_gender_unique():
	return Facebook.typeMethodGenderAge("page_impressions_by_age_gender_unique")


@facebook_blueprint.route('/getPageFansGenderAge', methods=['POST'])
def page_fans_gender_age():
	return Facebook.typeMethodGenderAge("page_fans_gender_age")