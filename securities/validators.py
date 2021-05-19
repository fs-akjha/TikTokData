from werkzeug.security import generate_password_hash,check_password_hash
from app import ma
from persistance.users_dao import user_dao


class loginRequestValidator(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("username", "password")

    def validate_username(self, value):
        try:
            user = user_dao.get_by_email(value)
            if user:
                return user
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def validate_password(self, existing_pass, value):
        # return True
        try:
            if check_password_hash(existing_pass, value):
                return True
            else:
                return False
        except Exception as err:
            print(err)
            return False

    def validate_data(self, data):
        try:
            result = self.load(data)
            user = self.validate_username(data["username"])
            if user:
                password = self.validate_password(user.hashed_password, data["password"])
                if password:
                    return user
                else:
                    return False
            else:
                return False
        except Exception as err:
            print(err)
            return False


loginRequestValidator = loginRequestValidator()
