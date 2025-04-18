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
def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # 우선 사용자 지정

            # 작가 정보 가져오기
            text = wiki(book.author)
            gpt_text = gpt(text)
            author_info_dict = json.loads(gpt_text)

            # TTS 생성
            book.save()  # 먼저 저장해서 book.pk를 확보!
            audio_file_name = f"summary_{book.pk}.mp3"
            audio_path = os.path.join(settings.MEDIA_ROOT, audio_file_name)

            tts = gTTS(text=author_info_dict["author_info"], lang='ko')
            tts.save(audio_path)

            # 모델 필드에 값 저장
            book.author_info = author_info_dict["author_info"]
            book.audio_file.name = audio_file_name  # 경로가 아닌 파일명만 저장
            book.save()

            return redirect('books:index')
    else:
        form = BookForm()

    context = {
        'form': form,
    }
    return render(request, 'books/create.html', context)


@require_safe
def detail(request, book_pk) :
    book = Book.objects.get(pk=book_pk)
    threads = book.thread_set.all()
    # text=wiki(book.author)
    # gpt_text=gpt(text)
    # author_description=json.loads(gpt_text)
    # author_image = wiki.get_author_image(book.author)
    # author_description=json.loads(wiki.gpt(wiki.wiki(book.author)))
    # tts = gTTS(text=author_description["author_info"], lang='ko')  # 한국어
    # audio_filename = f"summary_{book_pk}.mp3"
    # audio_path = os.path.join(settings.MEDIA_ROOT, audio_filename)
    # tts.save(audio_path)  # 음성 파일 저장

    # 수정한 부분
    context = {
        'book': book,
        'threads': threads,
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
    return render(request, 'books/thread_create.html', context)


@login_required
@require_safe
def thread_detail(request, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    book = thread.book
    user = thread.user
    context = {
        'thread': thread,
        'book': book,
        'user': user,
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
            'book': book,
            'thread': thread,
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