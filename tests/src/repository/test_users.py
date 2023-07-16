import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session


from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email(self):
        user = UserModel(username='testname', email='test@gmail.com', password='testpass')
        self.session.query().filter().first.return_value = user

        result = await get_user_by_email(email='test@gmail.com', db=self.session)

        self.assertEqual(user, result)
        self.assertEqual(user.email, result.email)

    async def test_get_user_by_email_not_found(self):
        email = 'nonexistent@example.com'
        self.session.query().filter().first.return_value = None

        result = await get_user_by_email(email=email, db=self.session)

        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username='testname', email='test@gmail.com', password='testpass')

        result = await create_user(body=body, db=self.session)

        self.session.add.assert_called_once_with(result)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(result)

        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        token = "new_refresh_token"

        await update_token(user=self.user, token=token, db=self.session)

        self.assertEqual(self.user.refresh_token, token)
        self.session.commit.assert_called_once()

    async def test_confirmed_email(self):
        email = "test@example.com"
        user = User(email=email, confirmed=False)
        self.session.query().filter().first.return_value = user

        await confirmed_email(email=email, db=self.session)

        self.assertTrue(user.confirmed)
        self.session.commit.assert_called_once()

    async def test_update_avatar(self):
        email = "test@example.com"
        url = "https://example.com/avatar.jpg"
        user = User(email=email, avatar=None)
        self.session.query().filter().first.return_value = user

        result = await update_avatar(email=email, url=url, db=self.session)

        self.assertEqual(result, user)
        self.assertEqual(result.avatar, url)
        self.session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
