import json, os
from django.shortcuts import render, redirect
from .models import Book, Thread
from .forms import BookForm, ThreadForm
from .utils import wiki, gpt
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.conf import settings
from gtts import gTTS


# Create your views here.
@require_safe
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
        'form' : form,
    }
    return render(request, 'books/create.html', context)


@require_safe
def detail(request, book_pk) :
    book = Book.objects.get(pk=book_pk)
    text=wiki(book.author)
    gpt_text=gpt(text)
    author_description=json.loads(gpt_text)
    # author_image = wiki.get_author_image(book.author)
    # author_description=json.loads(wiki.gpt(wiki.wiki(book.author)))
    tts = gTTS(text=author_description["author_info"], lang='ko')  # 한국어
    audio_filename = f"summary_{book_pk}.mp3"
    audio_path = os.path.join(settings.MEDIA_ROOT, audio_filename)
    tts.save(audio_path)  # 음성 파일 저장

    # 수정한 부분
    thread_form = ThreadForm()

    context = {
        'book': book,
        'author_description':author_description,
        # 'author_image': author_image
        'audio_file': f"{settings.MEDIA_URL}{audio_filename}",
        # 수정한 부분
        'thread_form': thread_form,
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
        'form': form,
    }
    return render(request, 'books/update.html', context)


@require_POST
def delete(request, book_pk) :
    book = Book.objects.get(pk=book_pk)
    book.delete()
    return redirect('books:index')


@login_required
@require_http_methods(['GET','POST'])
def thread_create(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST, request.FILES)
        if thread_form.is_valid():
            thread = thread_form.save(commit=False)
            thread.user = request.user
            thread.book = book
            thread.save()
            return redirect('books:detail', book.pk)
    else:
        thread_form = ThreadForm()
    context = {
        'book': book,
        'thread_form': thread_form,
    }
    return render(request, 'books/detail.html', context)

@login_required
@require_safe
def thread_detail(request, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    context = {
        'thread': thread,
    }
    return render(request, 'books/thread_detail.html', context)

@login_required
@require_http_methods(['GET','POST'])
def thread_update(request, book_pk, thread_pk):
    book = Book.objects.get(pk=book_pk)
    thread = Thread.objects.get(pk=thread_pk)
    if request.user == thread.user:
        if request.method == 'POST':
            thread_form = ThreadForm(request.POST, request.FILES, instance=thread)
            if thread_form.is_valid():
                thread = thread_form.save(commit=False)
                thread.user = request.user
                thread.book = book
                thread.save()
                return redirect('books:detail', book.pk)
        else:
            thread_form = ThreadForm(instance=thread)
        context = {
            'thread_form': thread_form,
        }
        return render(request, 'books/thread_update.html', context)
    return redirect('books:detail', book.pk)


@login_required
@require_POST
def thread_delete(request, book_pk, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    if request.user == thread.user:
        thread.delete()
        return redirect('books:detail', book_pk)
    

@login_required
@require_POST
def like(request, thread_pk):
    if request.user.is_authenticated:
        thread = Thread.objects.get(pk=thread_pk)
        if thread.like_users.filter(pk=request.user.pk).exists():
            thread.like_users.remove(request.user)
        else:
            thread.like_users.add(request.user)
    return redirect('books:thread_detail', thread_pk)