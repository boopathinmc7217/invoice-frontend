class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user_id = None
            cls._instance.jwt_token = None
        return cls._instance

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def set_jwt_token(self, jwt_token):
        self.jwt_token = jwt_token

    def get_jwt_token(self):
        return self.jwt_token
