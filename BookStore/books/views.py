from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Author, Book
from .forms import AuthorForm, BookForm

def home(request):
    """
    Главная страница приложения
    Показывает общую статистику и навигацию
    """
    authors_count = Author.objects.count()
    books_count = Book.objects.count()
    
    return render(request, 'books/home.html', {
        'authors_count': authors_count,
        'books_count': books_count,
    })

def author_list(request):
    """
    Показывает список всех авторов
    """
    authors = Author.objects.all().order_by('name')
    return render(request, 'books/author_list.html', {
        'authors': authors
    })

def book_list(request):
    """
    Показывает список всех книг
    """
    books = Book.objects.all().order_by('title')
    return render(request, 'books/book_list.html', {
        'books': books
    })


def author_detail(request, pk):
    """
    Показывает детальную информацию об авторе
    и список его книг
    """
    author = get_object_or_404(Author, pk=pk)
    books = author.books.all()  # Используем related_name из модели
    
    return render(request, 'books/author_detail.html', {
        'author': author,
        'books': books
    })

def book_detail(request, pk):
    """
    Показывает детальную информацию о книге
    """
    book = get_object_or_404(Book, pk=pk)
    
    return render(request, 'books/book_detail.html', {
        'book': book
    })
    
def author_create(request):
    """
    Обрабатывает создание нового автора
    """
    if request.method == 'POST':
        # Обработка отправленной формы
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            # Перенаправляем на страницу созданного автора
            return redirect('books:home')
    else:
        # Показываем пустую форму для GET запроса
        form = AuthorForm()
    
    return render(request, 'books/author_form.html', {
        'form': form,
        'title': 'Добавить автора'
    })

def book_create(request):
    """
    Обрабатывает создание новой книги
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('books:home')
    else:
        form = BookForm()
    
    return render(request, 'books/book_form.html', {
        'form': form,
        'title': 'Добавить книгу'
    })
    
def author_edit(request, pk):
    """
    Редактирование существующего автора
    """
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        # Передаем instance для редактирования существующего объекта
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author = form.save()
            return redirect('books:home')
    else:
        form = AuthorForm(instance=author)
    
    return render(request, 'books/author_form.html', {
        'form': form,
        'title': f'Редактировать автора: {author.name}',
        'author': author
    })

def book_edit(request, pk):
    """
    Редактирование существующей книги
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('books:home')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'books/book_form.html', {
        'form': form,
        'title': f'Редактировать книгу: {book.title}',
        'book': book
    })
    
def author_delete(request, pk):
    """
    Удаление автора с подтверждением
    """
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        # Подтверждение удаления
        author.delete()
        return redirect('books:home')  # ПЕРЕНАПРАВЛЕНИЕ НА ГЛАВНУЮ
    
    return render(request, 'books/confirm_delete.html', {
        'object': author,
        'object_type': 'автор',
    })

def book_delete(request, pk):
    """
    Удаление книги с подтверждением
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('books:home')  # ПЕРЕНАПРАВЛЕНИЕ НА ГЛАВНУЮ
    
    return render(request, 'books/confirm_delete.html', {
        'object': book,
        'object_type': 'книга',
    })
    
    