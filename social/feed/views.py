# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Publicacao
from .forms import PublicacaoForm


class FeedView(View):
    template_name = 'feed/feed.html'
    context_object_name = 'post_list'

    def get_lista_de_publicacoes(self):
        return Publicacao.objects.all().order_by('-data_de_publicacao')

    def get(self, request):
        publicacao_list = self.get_lista_de_publicacoes()

        return render(request, self.template_name,
                      {'publicacao_list': publicacao_list})

    def post(self, request):
        form = PublicacaoForm(request.POST, request.FILES)

        if form.is_valid():
            publicacao = Publicacao()
            publicacao.texto = form.cleaned_data['texto']
            publicacao.imagem = form.cleaned_data['imagem']

            publicacao.save()

        #  Exibir mensagem de erro ao enviar formulário vazio
        return HttpResponseRedirect(reverse('feed:feed'))
