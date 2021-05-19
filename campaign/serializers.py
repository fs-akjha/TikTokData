from app import ma


class CampaignSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("name", "end_date")


campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)