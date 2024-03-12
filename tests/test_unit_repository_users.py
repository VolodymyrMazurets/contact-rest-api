import unittest
from unittest.mock import MagicMock, AsyncMock, Mock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import get_user_by_email, create_user, update_token, confirmed_email


class TestAsyncUser(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password="qwerty", email="test@gmail.com", confirmed=False)
        self.session = AsyncMock(spec=Session)

    async def test_get_user_by_email(self):
        email = "test@gmail.com"
        self.session.query().filter().first.return_value = self.user
        result = await get_user_by_email(email, self.session)
        self.assertEqual(result, self.user)

    async def test_create_user(self):
        user_data = UserModel(username="new_user", email="new@example.com", password='123456')
        new_user = User(username="new_user", email="new@example.com", id=2, created_at="2021-01-01T00:00:00.000000", avatar="sss")

        self.session.add = Mock()
        self.session.commit = AsyncMock()
        self.session.refresh = AsyncMock()

        result = await create_user(user_data, self.session)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()

        self.assertEqual(result.username, new_user.username)
        self.assertEqual(result.email, new_user.email)

    async def test_update_token(self):
        user = User(id=1, username="test_user", email="test@example.com")
        token = "new_refresh_token"

        self.session.commit = AsyncMock()

        await update_token(user, token, self.session)
        self.assertEqual(user.refresh_token, token)
        self.session.commit.assert_called_once()

    async def test_confirmed_email(self):
        user = User(id=1, username="test_user", email="test@gmail.com")
        self.session.commit = AsyncMock()
        await confirmed_email(user.email, self.session)
        user_updated = await get_user_by_email(user.email, self.session)
        self.assertTrue(user_updated.confirmed)