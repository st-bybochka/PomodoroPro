from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashService:

    def get_hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_hash_password(self, plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
