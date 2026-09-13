import secrets


class TokenService:
    def __call__(self) -> str:
        return secrets.token_hex(32)