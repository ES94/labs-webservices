from . import facebook_blueprint
from classes.facebook import Facebook


@facebook_blueprint.route('/getPostImpressions', methods=['POST'])
def post_impressions():
	return Facebook.typeMethodPostsVideos("post_impressions") 


@facebook_blueprint.route('/getPostImpressionsUnique', methods=['POST'])
def post_impressions_unique():
	return Facebook.typeMethodPostsVideos("post_impressions_unique") 


@facebook_blueprint.route('/getPostImpressionsPaid', methods=['POST'])
def post_impressions_paid():
	return Facebook.typeMethodPostsVideos("post_impressions_paid")


@facebook_blueprint.route('/getPostImpressionsPaidUnique', methods=['POST'])
def post_impressions_paid_unique():
	return Facebook.typeMethodPostsVideos("post_impressions_paid_unique")


@facebook_blueprint.route('/getPostImpressionsOrganic', methods=['POST'])
def post_impressions_organic():
	return Facebook.typeMethodPostsVideos("post_impressions_organic") 


@facebook_blueprint.route('/getPostImpressionsOrganicUnique', methods=['POST'])
def post_impressions_organic_unique():
	return Facebook.typeMethodPostsVideos("post_impressions_organic_unique") 


@facebook_blueprint.route('/getPostEngagedUsers', methods=['POST'])
def post_engaged_users():
	return Facebook.typeMethodPostsVideos("post_engaged_users")


@facebook_blueprint.route('/getPostNegativeFeedbackByTypeUnique', methods=['POST'])
def post_negative_feedback_by_type_unique():
	return Facebook.typeMethodPostsVideos("post_negative_feedback_by_type_unique") 


@facebook_blueprint.route('/getPostEngagedFan', methods=['POST'])
def post_engaged_fan():
	return Facebook.typeMethodPostsVideos("post_engaged_fan") 


@facebook_blueprint.route('/getPostVideoCompleteViewsOrganicUnique', methods=['POST'])
def post_video_complete_views_organic_unique():
	return Facebook.typeMethodPostsVideos("post_video_complete_views_organic_unique")


@facebook_blueprint.route('/getPostVideoCompleteViewsPaidUnique', methods=['POST'])
def post_video_complete_views_paid_unique():
	return Facebook.typeMethodPostsVideos("post_video_complete_views_paid_unique")


@facebook_blueprint.route('/getPostVideoViewsOrganic', methods=['POST'])
def post_video_views_organic():
	return Facebook.typeMethodPostsVideos("post_video_views_organic")


@facebook_blueprint.route('/getPostVideoViewsOrganicUnique', methods=['POST'])
def post_video_views_organic_unique():
	return Facebook.typeMethodPostsVideos("post_video_views_organic_unique")


@facebook_blueprint.route('/getPostReactionsByTypeTotal', methods=['POST'])
def post_reactions_by_type_total():
	return Facebook.typeMethodPostsVideos("post_reactions_by_type_total")