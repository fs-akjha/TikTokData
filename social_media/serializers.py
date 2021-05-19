from app import ma


class SocialMediaSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("query", "user_id")


social_media_schema = SocialMediaSchema()