from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm
from . import wiki
import json
from django.views.decorators.http import require_http_methods

import os
from django.conf import settings
from gtts import gTTS

# Create your views here.


@require_http_methods(['GET'])
def index(request) :
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'books/index.html', context)

@require_http_methods(['GET', 'POST'])
def create(request) :
    if request.method == 'POST' :
        form = BookForm(request.POST, request.FILES)
        if form.is_valid() :
            form.save()
            return redirect('books:index')
    else :
        form = BookForm()
    context = {
        'form' : form
    }
    return render(request, 'books/create.html', context)

@require_http_methods(['GET'])
def detail(request, book_pk) :
    book = Book.objects.get(pk=book_pk)
    text=wiki.wiki(book.author)
    gpt_text=wiki.gpt(text)
    author_description=json.loads(gpt_text)
    # author_image = wiki.get_author_image(book.author)
    # author_description=json.loads(wiki.gpt(wiki.wiki(book.author)))

    tts = gTTS(text=author_description["author_info"], lang='ko')  # 한국어

    audio_filename = f"summary_{book_pk}.mp3"
    audio_path = os.path.join(settings.MEDIA_ROOT, audio_filename)
    tts.save(audio_path)  # 음성 파일 저장

    context = {
        'book': book,
        'author_description':author_description,
        # 'author_image': author_image
        'audio_file': f"{settings.MEDIA_URL}{audio_filename}"
    }
    return render(request, 'books/detail.html', context)

@require_http_methods(['GET', 'POST'])
def update(request, book_pk) :
    book = Book.objects.get(pk=book_pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('books:detail', book.pk)
    else:
        form = BookForm(instance=book)
    context = {
        'book': book,
        'form': form
    }
    return render(request, 'books/update.html', context)

@require_http_methods(['POST'])
def delete(request, book_pk) :
    book = Book.objects.get(pk=book_pk)
    book.delete()
    return redirect('books:index')
