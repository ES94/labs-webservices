from . import facebook_blueprint
from classes.facebook import Facebook


@facebook_blueprint.route('/getPageFansOnline', methods=['POST'])
def page_fans_online():
	return Facebook.typeMethodTypeOfOrdered("page_fans_online")