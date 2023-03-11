from django.test import Client, TestCase
from http import HTTPStatus
from ..models import Group, Post, User


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test_slug',
            description='Тестовое описание группы',
        )

        cls.user_author = User.objects.create_user(
            username='user_author')

        cls.user_another = User.objects.create_user(
            username='user_another')

        cls.post = Post.objects.create(
            text='Текст который просто больше 15 символов...',
            group=cls.group,
            author=cls.user_author,
        )

        cls.post_author = Client()
        cls.post_author.force_login(cls.user_author)
        cls.auth_user = Client()
        cls.auth_user.force_login(cls.user_another)

    def test_unauthorized_user_urls_status_code(self):
        """Проверка status_code для неавторизованного пользователя."""
        field_urls_code = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.user_author}/': HTTPStatus.OK,
            '/create/': HTTPStatus.FOUND,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/edit/': HTTPStatus.FOUND,
            '/follow/': HTTPStatus.FOUND,
        }
        for url, response_code in field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.client.get(url).status_code
                self.assertEqual(status_code, response_code)

    def test_url_redirect_anonymous_on_admin_login(self):
        """Проверка Response для неавторизованного пользователя."""
        field_urls_code = {
            '/create/': '/auth/login/?next=/create/',
            f'/posts/{self.post.id}/edit/': '/auth/login/?next=/posts/1/edit/',
        }
        for url, redirect in field_urls_code.items():
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_auth_user_urls_status_code(self):
        """Проверка status_code для авторизованного пользователя."""
        field_urls_code = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.user_author}/': HTTPStatus.OK,
            '/create/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/edit/': HTTPStatus.FOUND,
            '/follow/': HTTPStatus.OK,
        }
        for url, response_code in field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.auth_user.get(url).status_code
                self.assertEqual(status_code, response_code)

    def test_url_redirect_auth_user(self):
        """Проверка Response для авторизованного пользователя."""
        field_urls_code = {
            f'/posts/{self.post.id}/edit/': '/posts/1/',
        }
        for url, redirect in field_urls_code.items():
            with self.subTest(url=url):
                response = self.auth_user.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_author_user_urls_status_code(self):
        """Проверка status_code для автора поста."""
        field_urls_code = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.user_author}/': HTTPStatus.OK,
            '/create/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/edit/': HTTPStatus.OK,
            '/follow/': HTTPStatus.OK,
        }
        for url, response_code in field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.post_author.get(url).status_code
                self.assertEqual(status_code, response_code)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/profile/{self.user_author}/': 'posts/profile.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
            '/follow/': 'posts/follow.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.post_author.get(address)
                self.assertTemplateUsed(response, template)

    def test_error_page(self):
        response = self.client.get('/nonexist-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html')
