from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Articles


class NewsTests(TestCase):
    def setUp(self):
        self.article = Articles.objects.create(
            title='Запуск чата',
            anons='Краткий анонс новости',
            full_text='Полный текст первой новости на сайте.',
            date=timezone.now()
        )

    def test_article_str_representation(self):
        self.assertEqual(str(self.article), 'Запуск чата')

    def test_news_home_page_displays_article(self):
        # Если в news/urls.py маршрут называется иначе (не 'news_home'), замените имя в reverse()
        try:
            url = reverse('news_home')
        except Exception:
            url = '/news/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Запуск чата')
