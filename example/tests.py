from django.test import TestCase
from example.models import Movie, Genre
from example.forms import MovieForm, GenreForm
from django.shortcuts import reverse


class SimpleTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Horror")
        self.movie = Movie.objects.create(
            name="Dracula",
            year=1987,
            released="02-11-1987",
            genre=self.genre,
        )

    def tearDown(self):
        self.movie.delete()
        self.genre.delete()

    def test_max_length(self):
        form = MovieForm(data={'name': 'X' * 200})
        self.assertFalse(form.is_valid())

    def test_initial(self):
        form = MovieForm(instance=self.movie)
        self.assertEqual(form.initial["name"], self.movie.name)
        self.assertEqual(form.initial["year"], self.movie.year)
        self.assertEqual(form.initial["released"], self.movie.released)
        self.assertTrue(isinstance(self.movie.year, int))

    def test_year_integar(self):
        form = MovieForm(
            data={'name': 'Braveheart', 'year': 1998, 'released': '28-09-2019',
                  'genre': self.genre.id})
        self.assertTrue(form.is_valid())

    def test_max_length_genre(self):
        form = GenreForm(data={'name': 'X' * 200})
        self.assertFalse(form.is_valid())

    def test_initial_genre(self):
        form = GenreForm(instance=self.genre)
        self.assertTrue(isinstance(self.genre.name, str))


class SimpleTestCase2(TestCase):
    hello_world_url = reverse('hello_world')

    def test_display_view(self):
        response = self.client.get(self.hello_world_url)
        content = str(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.view_name, 'hello_world')
        self.assertEqual(content, "b'Hello World!'")


class SimpleTestCase3(TestCase):
    hello_world_url = reverse('hello_world_template')

    def test_display_view(self):
        response = self.client.get(self.hello_world_url)
        content = str(response.content)
        self.assertEqual(response.resolver_match.view_name,
                         'hello_world_template')


class SimpleTestCase(TestCase):
    form_view_url = reverse('genre_add')

    def test_display_view(self):
        data = {'name': ''}
        expected_error = ['This field is required.']
        response = self.client.post(self.form_view_url, data)

        self.assertFormError(response, 'form', 'name', expected_error)
