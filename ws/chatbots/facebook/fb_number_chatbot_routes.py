from . import facebook_blueprint
from classes.facebook import Facebook


@facebook_blueprint.route('/getPageImpressionsUnique', methods=['POST'])
def page_impressions_unique():
	return Facebook.typeMethodNumberOf("page_impressions_unique")


@facebook_blueprint.route('/getPageImpressionsPaidUnique', methods=['POST'])
def page_impressions_paid_unique():
	return Facebook.typeMethodNumberOf("page_impressions_paid_unique")


@facebook_blueprint.route('/getPageImpressionsOrganicUnique', methods=['POST'])
def page_impressions_organic_unique():
	return Facebook.typeMethodNumberOf("page_impressions_organic_unique")


@facebook_blueprint.route('/getPagePostEngagements', methods=['POST'])
def page_post_engagements():
	return Facebook.typeMethodNumberOf("page_post_engagements")


@facebook_blueprint.route('/getPageEngagedUsers', methods=['POST'])
def page_engaged_users():
	return Facebook.typeMethodNumberOf("page_engaged_users")


@facebook_blueprint.route('/getPageConsumptionsUnique', methods=['POST'])
def page_consumptions_unique():
	return Facebook.typeMethodNumberOf("page_consumptions_unique")


@facebook_blueprint.route('/getPageNegativeFeedbackUnique', methods=['POST'])
def page_negative_feedback_unique ():
	return Facebook.typeMethodNumberOf("page_negative_feedback_unique")


@facebook_blueprint.route('/getPageTotalActions', methods=['POST'])
def page_total_actions():
	return Facebook.typeMethodNumberOf("page_total_actions")


@facebook_blueprint.route('/getPageFans', methods=['POST'])
def page_fans():
	return Facebook.typeMethodNumberOf("page_fans") 


@facebook_blueprint.route('/getPageFanAdds', methods=['POST'])
def page_fan_adds():
	return Facebook.typeMethodNumberOf("page_fan_adds")


@facebook_blueprint.route('/getPageFanAddsUnique', methods=['POST'])
def page_fan_adds_unique():
	return Facebook.typeMethodNumberOf("page_fan_adds_unique")


@facebook_blueprint.route('/getPageFanRemovesUnique', methods=['POST'])
def page_fan_removes_unique():
	return Facebook.typeMethodNumberOf("page_fan_removes_unique")


@facebook_blueprint.route('/getPageViewsTotal', methods=['POST'])
def page_views_total():
	return Facebook.typeMethodNumberOf("page_views_total") 


@facebook_blueprint.route('/getPageVideoViews', methods=['POST'])
def page_video_views():
	return Facebook.typeMethodNumberOf("page_video_views")


@facebook_blueprint.route('/getPageVideoViewsClickToPlay', methods=['POST'])
def page_video_views_click_to_play():
	return Facebook.typeMethodNumberOf("page_video_views_click_to_play")   


@facebook_blueprint.route('/getPageVideoViewTime', methods=['POST'])
def page_video_view_time():
	return Facebook.typeMethodNumberOf("page_video_view_time")    


@facebook_blueprint.route('/getPagePostsImpressions', methods=['POST'])
def page_posts_impressions():
	return Facebook.typeMethodNumberOf("page_posts_impressions")  


@facebook_blueprint.route('/getPagePostsImpressionsUnique', methods=['POST'])
def page_posts_impressions_unique():
	return Facebook.typeMethodNumberOf("page_posts_impressions_unique") 


@facebook_blueprint.route('/getPagePostsImpressionsPaid', methods=['POST'])
def page_posts_impressions_paid():
	return Facebook.typeMethodNumberOf("page_posts_impressions_paid") 


@facebook_blueprint.route('/getPagePostsImpressionsPaidUnique', methods=['POST'])
def page_posts_impressions_paid_unique():
	return Facebook.typeMethodNumberOf("page_posts_impressions_paid_unique") 


@facebook_blueprint.route('/getPagePostsImpressionsOrganic', methods=['POST'])
def page_posts_impressions_organic():
	return Facebook.typeMethodNumberOf("page_posts_impressions_organic")


@facebook_blueprint.route('/getPagePostsImpressionsOrganicUnique', methods=['POST'])
def page_posts_impressions_organic_unique():
	return Facebook.typeMethodNumberOf("page_posts_impressions_organic_unique")