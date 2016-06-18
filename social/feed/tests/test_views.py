# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse

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

    def acessa_feed(self):
        return self.client.get(reverse('feed:feed'))

    def test_feed_views_sem_publicacoes(self):
        """
        Quando não houverem publicações deve ser exibida uma mensagem de aviso
        """
        response = self.acessa_feed()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhuma publicação')
        self.assertQuerysetEqual(response.context['publicacao_list'], [])

    def test_feed_com_uma_publicacao(self):
        """
        Quando houver um única publicação, apenas ela deve ser exibida, sem
        exibir mensagem de aviso
        """
        publicacao = self.cria_publicacao('Publicação para teste')

        response = self.acessa_feed()

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

        response = self.acessa_feed()

        self.assertContains(response, primeira_publicacao.texto)
        self.assertContains(response, segunda_publicacao.texto)
        self.assertNotContains(response, 'Nenhuma publicação')
        self.assertEqual(len(response.context['publicacao_list']), 2)

    def test_publicar_sem_texto_e_sem_imagem(self):
        """
        Ao publicar sem inserir texto e sem inserir imagem, a publicação não
        deve ser feita e não deve existir nenhuma publicação no feed
        """
        response = self.client.post(reverse('feed:feed'), follow=True)

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
            response = self.client.post(
                reverse('feed:feed'), {'imagem': imagem}, follow=True
            )

        self.assertNotContains(response, 'imagem_para_teste')
        self.assertQuerysetEqual(response.context['publicacao_list'], [])
        self.assertEqual(len(response.redirect_chain), 1)

    def test_publiar_com_texto_e_sem_imagem(self):
        """
        Ao publicar inserindo apenas um texto, sem inserir imagem, a publicação
        deve ser feita e exibida no feed
        """
        texto_para_publicacao = 'Texto para publicação de teste'
        response = self.client.post(
            reverse('feed:feed'), {'texto': texto_para_publicacao}, follow=True
        )

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
            contexto = {'texto': texto_para_publicacao, 'imagem': imagem}
            response = self.client.post(
                reverse('feed:feed'), contexto, follow=True
            )

        self.assertContains(response, texto_para_publicacao)
        self.assertContains(response, 'imagem_para_teste')
        self.assertEqual(len(response.context['publicacao_list']), 1)
        self.assertEqual(len(response.redirect_chain), 1)
