class UserBO:
    def __init__(self, email: str, password: str, external_id: int | None = None):
        self.email = email
        self.password = password
        self.external_id = external_id