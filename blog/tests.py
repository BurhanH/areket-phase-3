from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from . import models


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@email.com',
            password='user_password'
        )

        self.post = models.Post.objects.create(
            title='Test title',
            body='Test body content',
            author=self.user
        )

    def test_string_representation(self):
        post = models.Post(title='A sample')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'Test title')
        self.assertEqual(f'{self.post.author}', 'test_user')
        self.assertEqual(f'{self.post.body}', 'Test body content')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test body content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test title')
        self.assertTemplateUsed(response, 'post_detail.html')
        no_response = self.client.get('/post/100000')
        self.assertEqual(no_response.status_code, 404)
