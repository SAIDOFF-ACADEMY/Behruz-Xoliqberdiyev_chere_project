from PIL import Image
import tempfile
from rest_framework.test import APITestCase, APIClient
from common.models import Settings, Page, GalleryPhoto
from users.models import User


def example_image():
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


class SettingsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(email='test@mail.com', password='test')
        if not Settings.objects.exists():
            self.settings = Settings.objects.create(
                contact_telegram='test',
                longitude=0,
                latitude=0,
                location_text='test',
                working_hours_start='12:00:00',
                working_hours_end='12:00:00',
                telegram_bot='testbot'
            )

    def test_put_settings(self):
        self.client.login(email='test@mail.com', password='test')
        data = {
            'contact_telegram': 'test.uz',
            'longitude': 0,
            'latitude': 0,
            'location_text': 'test',
            'working_hours_start': '12:00:00',
            "working_hours_end": '12:00:00',
            'telegram_bot': 'testbot'
        }
        response = self.client.put('/api/v1/admin/common/settings/', data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['contact_telegram'], 'test.uz')

    def test_patch_settings(self):
        self.client.login(email='test@mail.com', password='test')
        data = {
            'contact_telegram': 'test.uz',
            'longitude': 0,
            'latitude': 0,
            'location_text': 'test',
            'working_hours_start': '12:00:00',
            "working_hours_end": '12:00:00',
            'telegram_bot': 'testbot'
        }
        response = self.client.patch('/api/v1/admin/common/settings/', data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['contact_telegram'], 'test.uz')


class PageTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(email='test@mail.com', password='test')
        self.page = Page.objects.create(title='test', slug='test', content='test')

    def test_all_get_page(self):
        self.client.login(email='test@mail.com', password='test')
        Page.objects.create(title='test1', slug='test1', content='test1')
        Page.objects.create(title='test2', slug='test2', content='test2')
        Page.objects.create(title='test3', slug='test3', content='test3')

        response = self.client.get('/api/v1/admin/common/pages/')

        pages = Page.objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(pages, 4)

    def test_get_page(self):
        self.client.login(email='test@mail.com', password='test')
        response = self.client.get('/api/v1/admin/common/page/test/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'test')

        response = self.client.get('/api/v1/landing/common/page/1/')

        self.assertEqual(response.status_code, 404)

    def test_put_page(self):
        self.client.login(email='test@mail.com', password='test')
        data = {
            'title': 'test1',
            'slug': 'test1',
            'content': 'test1'
        }
        response = self.client.put('/api/v1/admin/common/page/test/', data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'test1')
        self.assertEqual(response.data['slug'], 'test1')
        self.assertEqual(response.data['content'], 'test1')

    def test_patch_page(self):
        self.client.login(email='test@mail.com', password='test')
        data = {
            'title': 'test1',
            'slug': 'test',
            'content': 'test'
        }
        response = self.client.put('/api/v1/admin/common/page/test/', data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'test1')

    def test_delete_page(self):
        self.client.login(email='test@mail.com', password='test')
        response = self.client.delete('/api/v1/admin/common/page/test/')

        self.assertEqual(response.status_code, 204)

    def test_create_page(self):
        self.client.login(email='test@mail.com', password='test')
        data = {
            'title': 'test2',
            'title_ru': 'test2',
            'title_uz': 'test2',
            'slug': 'test2',
            'content': 'test2',
            'content_uz': 'test2',
            'content_ru': 'test2',
        }
        response = self.client.post('/api/v1/admin/common/pages/add/', data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'test2')


class GalleryPhotoTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(email='test@mail.com', password='test')

    def test_all_photos_get(self):
        self.client.login(email='test@mail.com', password='test')
        self.photo = GalleryPhoto.objects.create(photo='test1.png')
        GalleryPhoto.objects.create(photo='test.png')
        response = self.client.get('/api/v1/admin/common/photos/')

        photos = GalleryPhoto.objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(photos, 2)

    def test_delete_photo(self):
        self.client.login(email='test@mail.com', password='test')
        GalleryPhoto.objects.create(photo='test.png')

        response = self.client.delete('http://127.0.0.1:8000/api/v1/admin/common/photo/1/')

        self.assertEqual(response.status_code, 204)

    def test_create_photo(self):
        self.client.login(email='test@mail.com', password='test')
        data = {
            'photo': example_image()
        }

        response = self.client.post('/api/v1/admin/common/photo/create/', data=data, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertIn('photo', response.data)
