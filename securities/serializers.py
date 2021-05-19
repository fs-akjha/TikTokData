from app import ma


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "email", "role", "is_active","company_id")



user_schema = UserSchema()
users_schema = UserSchema(many=True)