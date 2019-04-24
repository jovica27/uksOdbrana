from  django.test import TestCase, Client
from  django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.home_url = reverse('home')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')


    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'uks/index.html')

    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'uks/home.html')

    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'uks/register.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'uks/login.html')

    def test_logout_GET(self):
        response = self.client.get(self.logout_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'uks/home.html')
