class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user_id = None
            cls._instance.jwt_token_access = None
            cls._instance.jwt_token_refresh = None
            cls._instance.invoice_path = None
        return cls._instance

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def set_jwt_token_access(self, jwt_token_access):
        self.jwt_token_access = jwt_token_access

    def get_jwt_token_access(self):
        return self.jwt_token_access

    def set_jwt_token_refresh(self, jwt_token_refresh):
        self.jwt_token_refresh = jwt_token_refresh

    def get_jwt_token_refresh(self):
        return self.jwt_token_refresh

    def set_invoice_path(self, invoice_path):
        self.invoice_path = invoice_path

    def get_invoice_path(self):
        return self.invoice_path
