import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    remove_contact,
    search_contact,
    get_upcoming_birthdays,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        query_mock = self.session.query.return_value
        query_mock.filter.return_value = query_mock
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock
        query_mock.all.return_value = contacts

        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactModel(first_name='test', last_name='test', email='test@gmail.com')
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(body.first_name, result.first_name)
        self.assertEqual(body.last_name, result.last_name)
        self.assertEqual(body.email, result.email)
        self.assertEqual(self.user.id, result.user_id)

    async def test_update_contact_found(self):
        body = ContactModel(first_name='test_first', last_name='test_last', email='test@gmail.com')
        contact = await create_contact(body=body, user=self.user, db=self.session)

        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None

        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)

        self.assertEqual(result.id, contact.id)
        self.assertEqual(result.first_name, contact.first_name)
        self.assertEqual(result.last_name, contact.last_name)
        self.assertEqual(result.email, contact.email)

    async def test_update_contact_not_found(self):
        body = ContactModel(first_name='test_first', last_name='test_last', email='test@gmail.com')
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_contact(self):
        search_params = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }

        contacts = [
            Contact(first_name='John', last_name='Doe', email='john.doe@example.com'),
            Contact(first_name='John', last_name='Smith', email='john.smith@example.com')
        ]

        query_mock = self.session.query.return_value
        query_mock.filter.return_value = query_mock
        query_mock.all.return_value = contacts

        result = await search_contact(search_params, user=self.user, db=self.session)

        self.assertEqual(result, contacts)

    async def test_search_contact_without_params(self):
        search_params = {}

        contacts = [
            Contact(first_name='John', last_name='Doe', email='john.doe@example.com'),
            Contact(first_name='John', last_name='Smith', email='john.smith@example.com')
        ]

        self.session.query().filter().all.return_value = contacts

        result = await search_contact(search_params, user=self.user, db=self.session)

        self.assertEqual(result, contacts)


if __name__ == '__main__':
    unittest.main()
