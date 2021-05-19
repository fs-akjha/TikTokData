from app import ma


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "email_address", "role", "is_active")

class CompanySchema(ma.Schema):
    class Meta:
        fields=("id","name","seat_limit","seats_used","campaign_limit","campaigns_used","facebook_limit","facebook_searches_used","instagram_limit","instagram_searches_used","twitter_limit","twitter_searches_used","youtube_limit","youtube_searches_used","created_date","modified_date")

class MessageSchema(ma.Schema):
    class Meta:
        fields=("id","message_template","is_active","created_date")

class BatchSchema(ma.Schema):
    class Meta:
        fields=("id","send_date","subject","batch_status")



company_schema=CompanySchema()
companies_schema = CompanySchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

batch_schema=BatchSchema()
batches_schema=BatchSchema(many=True)