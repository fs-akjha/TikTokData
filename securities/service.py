from persistance.users_dao import user_dao
from .serializers import user_schema, users_schema
from .validators import loginRequestValidator

class AuthService:
    def login(self, data):
        user = loginRequestValidator.validate_data(data)
        if not user:
            return None
        else:
            result = user_schema.dump(user)
            return result


auth_service = AuthService()
