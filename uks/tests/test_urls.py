from django.test import SimpleTestCase
from django.urls import reverse, resolve
from uks.views import index, home, login, register, logout

class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)