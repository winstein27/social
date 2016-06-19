# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from unittest import skip
import os

from feed.models import Publicacao


class FeedViewTest(TestCase):

    @staticmethod
    def cria_publicacao(texto):
        return Publicacao.objects.create(texto=texto)

    @staticmethod
    def get_local_da_imagem():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return BASE_DIR + '/files/imagem_para_teste.png'

    @staticmethod
    def try_to_publish(instance, context):
        instance.client.force_login(user=instance.user)
        return instance.client.post(reverse('feed:feed'), context, follow=True)

    @staticmethod
    def acessa_feed(instance):
        instance.client.force_login(user=instance.user)
        return instance.client.get(reverse('feed:feed'))

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(
            username='temporary',
            email='temporary@gmail.com',
            password='tempo1234')

    @classmethod
    def tearDown(cls):
        cls.user.delete()

    def test_feed_views_sem_publicacoes(self):
        """
        Quando não houverem publicações deve ser exibida uma mensagem de aviso
        """
        response = self.acessa_feed(self)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhuma publicação')
        self.assertQuerysetEqual(response.context['publicacao_list'], [])

    def test_feed_com_uma_publicacao(self):
        """
        Quando houver um única publicação, apenas ela deve ser exibida, sem
        exibir mensagem de aviso
        """
        publicacao = self.cria_publicacao('Publicação para teste')

        response = self.acessa_feed(self)

        self.assertContains(response, publicacao.texto)
        self.assertNotContains(response, 'Nenhuma publicação')
        self.assertEqual(len(response.context['publicacao_list']), 1)

    def test_feed_com_duas_publicacoes(self):
        """
        Quando houverem publicações, apenas as publicações devem ser exibidas,
        sem exibir mensagem de aviso
        """
        primeira_publicacao = self.cria_publicacao('Primeira publicação')
        segunda_publicacao = self.cria_publicacao('Segunda publicação')

        response = self.acessa_feed(self)

        self.assertContains(response, primeira_publicacao.texto)
        self.assertContains(response, segunda_publicacao.texto)
        self.assertNotContains(response, 'Nenhuma publicação')
        self.assertEqual(len(response.context['publicacao_list']), 2)

    def test_publicar_sem_texto_e_sem_imagem(self):
        """
        Ao publicar sem inserir texto e sem inserir imagem, a publicação não
        deve ser feita e não deve existir nenhuma publicação no feed
        """
        response = self.try_to_publish(self, {})

        self.assertQuerysetEqual(response.context['publicacao_list'], [])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)

    def test_publicar_sem_texto_e_com_imagem(self):
        """
         Ao publicar sem inserir texto e inseririndo imagem, a publicação não
        deve ser feita
        """
        response = None
        with open(self.get_local_da_imagem(), 'rb') as imagem:
            response = self.try_to_publish(self, {'imagem': imagem})

        self.assertNotContains(response, 'imagem_para_teste')
        self.assertQuerysetEqual(response.context['publicacao_list'], [])
        self.assertEqual(len(response.redirect_chain), 1)

    def test_publiar_com_texto_e_sem_imagem(self):
        """
        Ao publicar inserindo apenas um texto, sem inserir imagem, a publicação
        deve ser feita e exibida no feed
        """
        texto_para_publicacao = 'Texto para publicação de teste'
        response = self.try_to_publish(self, {'texto': texto_para_publicacao})

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertContains(response, texto_para_publicacao)
        self.assertEqual(len(response.context['publicacao_list']), 1)

    def test_publicar_com_texto_e_com_imagem(self):
        """
        Ao publicar inserindo texto e imagem, a publicação deve ser feita
        exibindo o texto e a imagem
        """
        response = None
        texto_para_publicacao = 'Texto para publicação de teste'

        with open(self.get_local_da_imagem(), 'rb') as imagem:
            context = {'texto': texto_para_publicacao, 'imagem': imagem}
            response = self.try_to_publish(self, context)

        self.assertContains(response, texto_para_publicacao)
        self.assertContains(response, 'imagem_para_teste')
        self.assertEqual(len(response.context['publicacao_list']), 1)
        self.assertEqual(len(response.redirect_chain), 1)
