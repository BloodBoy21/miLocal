from repositories.repository import Repository
from models.user import User, UserIn


class UserRepository(Repository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> User:
        return self.find_query().filter_by(email=email).first()

    def find_by_id(self, user_id: int) -> User:
        return self.find_query().filter_by(user_id=user_id).first()

    def exists(self, email: str) -> bool:
        return self.find_query().filter_by(email=email).first() is not None

    def create(self, user: UserIn) -> User:
        user_data = self.model(**user.dict())
        return super().create(user_data)
