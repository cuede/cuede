from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from enunciados.models import Carrera

class IndexTest(TestCase):
    def test_index_deberia_redireccionar_a_materias(self):
        response = self.client.get(reverse('index'))

        computacion = Carrera.objects.get(slug='computacion')
        redir_url = reverse('materias', kwargs={'carrera': computacion})
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertEquals(response.url, redir_url)