from . import facebook_blueprint
from classes.facebook import Facebook


@facebook_blueprint.route('/getPageImpressionsFrequencyDistribution', methods=['POST'])
def page_impressions_frequency_distribution():
	return Facebook.typeMethodTypeOf("page_impressions_frequency_distribution")


@facebook_blueprint.route('/getPagePositiveFeedbackByTypeUnique', methods=['POST'])
def page_positive_feedback_by_type_unique():
	return Facebook.typeMethodTypeOf("page_positive_feedback_by_type_unique")


@facebook_blueprint.route('/getPageFanAddsByPaidNonPaidUnique', methods=['POST'])
def page_fan_adds_by_paid_non_paid_unique():
	return Facebook.typeMethodTypeOf("page_fan_adds_by_paid_non_paid_unique")


@facebook_blueprint.route('/getPageActionsPostReactionsTotal', methods=['POST'])
def page_actions_post_reactions_total():
	return Facebook.typeMethodTypeOf("page_actions_post_reactions_total")


@facebook_blueprint.route('/getPageFansByUnlikeSourceUnique', methods=['POST'])
def page_fans_by_unlike_source_unique():
	return Facebook.typeMethodTypeOf("page_fans_by_unlike_source_unique")


@facebook_blueprint.route('/getPageViewsExternalReferrals', methods=['POST'])
def page_views_external_referrals ():
	return Facebook.typeMethodTypeOf("page_views_external_referrals") 


@facebook_blueprint.route('/getPageVideoViewsByPaidNonPaid', methods=['POST'])
def page_video_views_by_paid_non_paid():
	return Facebook.typeMethodTypeOf("page_video_views_by_paid_non_paid") 


@facebook_blueprint.route('/getPagePostsImpressionsFrequencyDistribution', methods=['POST'])
def page_posts_impressions_frequency_distribution():
	return Facebook.typeMethodTypeOf("page_posts_impressions_frequency_distribution") 


@facebook_blueprint.route('/getPageMessagesTotalMessagingConnections', methods=['POST'])
def page_messages_total_messaging_connections():
	return Facebook.typeMethodTypeOf("page_messages_total_messaging_connections")


@facebook_blueprint.route('/getPageMessagesNewConversationsUnique', methods=['POST'])
def page_messages_new_conversations_unique():
	return Facebook.typeMethodTypeOf("page_messages_new_conversations_unique")


@facebook_blueprint.route('/getPageMessagesBlockedConversationsUnique', methods=['POST'])
def page_messages_blocked_conversations_unique():
	return Facebook.typeMethodTypeOf("page_messages_blocked_conversations_unique")


@facebook_blueprint.route('/getPageMessagesReportedConversationsUnique', methods=['POST'])
def page_messages_reported_conversations_unique():
	return Facebook.typeMethodTypeOf("page_messages_reported_conversations_unique")