from django.contrib.auth import get_user
from rest_framework.test import APITestCase, APIClient
from users.models import User, UserContactApplication
from rest_framework.authtoken.models import Token


class UserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(email='test@mail.com', password='test')

    def test_login_only_admin_users(self):
        token_count = Token.objects.count()

        response = self.client.post('/api/v1/admin/users/users/login/', data={
            'email': 'test@mail.com',
            'password': 'test'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

        token_count = Token.objects.count()
        self.assertEqual(token_count, 1)

    def test_user_login_failed(self):
        token_count = Token.objects.count()

        response = self.client.post('/api/v1/admin/users/users/login/', data={
            'email': 'tes@mail.com',
            'password': 'test'
        })

        self.assertEqual(response.status_code, 401)
        self.assertNotIn('token', response.data)

        token_count = Token.objects.count()
        self.assertEqual(token_count, 0)

    def test_get_all_users_list(self):
        User.objects.create_user(email='test1@mail.com', password='test1')
        User.objects.create_user(email='test2@mail.com', password='test2')

        self.client.login(email='test@mail.com', password='test')

        response = self.client.get('/api/v1/admin/users/users/')
        users = User.objects.count()
        admin_users = User.objects.filter(is_staff=True).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(users, 3)
        self.assertEqual(admin_users, 1)

    def test_user_detail(self):
        self.client.login(email='test@mail.com', password='test')

        response = self.client.get('/api/v1/admin/users/users/1/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.password)

    def test_user_delete(self):
        self.client.login(email='test@mail.com', password='test')
        response = self.client.delete('/v1/admin/users/users/1/delete/')

        self.assertEqual(response.status_code, 204)

    def test_user_edit_method_put(self):
        self.client.login(email='test@mail.com', password='test')
        data = {
            'full_name': 'test_test',
            'phone': '+14541220',
            'email': 'test1@mail.com',
            'password': 'test',
        }
        response = self.client.put('/api/v1/admin/users/users/1/update/', data=data)

        user = User.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.full_name, 'test_test')

    def test_user_edit_method_patch(self):
        self.client.login(email='test@mail.com', password='test')
        data = {
            'full_name': 'test_test',
        }
        response = self.client.patch('/api/v1/admin/users/users/1/update/', data=data)

        user = User.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.full_name, 'test_test')

    def test_user_create(self):
        self.client.login(email='test@mail.com', password='test')

        response = self.client.post('/api/v1/admin/users/users/create/', data={
            'email': 'new_user@mail.com',
            'full_name': 'new_user',
            'password': 'new_pass',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], 'new_user@mail.com')
        self.assertEqual(response.data['full_name'], 'new_user')


class UserContactApplicationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(email='test@mail.com', password='test')

    def test_all_users_contacts(self):
        self.client.login(email='test@mail.com', password='test')
        UserContactApplication.objects.create(full_name='test', phone='+95555', is_contacted=True)
        UserContactApplication.objects.create(full_name='test1', phone='+95555142', is_contacted=True)
        UserContactApplication.objects.create(full_name='test2', phone='+9555514772')

        response = self.client.get('/api/v1/admin/users/user_contacts/')

        user_contacts = UserContactApplication.objects.count()
        user_contacts_contacted = UserContactApplication.objects.filter(is_contacted=True).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_contacts, 3)
        self.assertEqual(user_contacts_contacted, 2)

    def test_user_contact_delete(self):
        self.client.login(email='test@mail.com', password='test')
        UserContactApplication.objects.create(full_name='test', phone='+95555', is_contacted=True)

        response = self.client.delete('/api/v1/admin/users/user_contact/1/')

        self.assertEqual(response.status_code, 204)

    def test_user_contact_edit_put(self):
        self.client.login(email='test@mail.com', password='test')
        UserContactApplication.objects.create(full_name='test', phone='+95555', is_contacted=True)

        response = self.client.put('/api/v1/admin/users/user_contact/1/update/', data={
            'is_contacted': False
        })

        user_contact = UserContactApplication.objects.get(full_name='test')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user_contact.is_contacted)

    def test_user_contact_edit_patch(self):
        self.client.login(email='test@mail.com', password='test')
        UserContactApplication.objects.create(full_name='test', phone='+95555', is_contacted=True)

        response = self.client.patch('/api/v1/admin/users/user_contact/1/update/', data={
            'is_contacted': False
        })

        user_contact = UserContactApplication.objects.get(full_name='test')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user_contact.is_contacted)

    def test_user_contact_get(self):
        self.client.login(email='test@mail.com', password='test')
        UserContactApplication.objects.create(full_name='test', phone='+95555', is_contacted=True)

        response = self.client.get('/api/v1/admin/users/user_contact/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], 'test')