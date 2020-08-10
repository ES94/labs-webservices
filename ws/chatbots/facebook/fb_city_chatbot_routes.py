from . import facebook_blueprint
from classes.facebook import Facebook


@facebook_blueprint.route('/getPageFansCity', methods=['POST'])
def page_fans_city():
   return Facebook.typeMethodCity("page_fans_city")


@facebook_blueprint.route('/getPageImpressionsByCityUnique', methods=['POST'])
def page_impressions_by_city_unique():
	return Facebook.typeMethodCity("page_impressions_by_city_unique")