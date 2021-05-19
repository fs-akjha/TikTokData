#Serializers
from app import ma
class CampaignInfluencerSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "campaign_id", "social_network", "social_network_user_id", "total_engagements")

class CampaignDenialSchema(ma.Schema):
    class Meta:
        fields = ("id", "campaign_id", "social_network", "social_network_user_id")


influencer_schema = CampaignInfluencerSchema()
influencers_schema = CampaignInfluencerSchema(many=True)

denial_schema = CampaignDenialSchema()
denials_schema = CampaignDenialSchema(many=True)