from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_date', 'bio']
        
        # Настройка меток полей (отображаются в форме)
        labels = {
            'name': 'Полное имя автора',
            'birth_date': 'Дата рождения',
            'bio': 'Биография',
        }
        
        # Настройка подсказок для полей
        help_texts = {
            'name': 'Введите полное имя автора (только буквы и пробелы)',
            'birth_date': 'Выберите дату рождения автора',
            'bio': 'Введите краткую биографию автора',
        }
        
        # Настройка виджетов (HTML-представление полей)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Лев Толстой',
                'autofocus': True
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # Для HTML5 date picker
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опишите жизнь и творчество автора...'
            }),
        }    
    def clean_name(self):
        """
        Custom валидация для поля name
        Проверяем, что имя содержит только буквы и пробелы
        """
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError("Имя автора не может быть пустым")
        
        # Проверяем, что имя содержит только буквы, пробелы и дефисы
        if not all(char.isalpha() or char.isspace() or char == '-' for char in name):
            raise ValidationError("Имя может содержать только буквы, пробелы и дефисы")
        
        # Проверяем длину имени
        if len(name) < 2:
            raise ValidationError("Имя слишком короткое")
        
        return name
    
    def clean_birth_date(self):
        """
        Custom валидация для даты рождения
        Проверяем, что автор не родился в будущем
        """
        birth_date = self.cleaned_data.get('birth_date')
        
        if birth_date and birth_date > date.today():
            raise ValidationError("Дата рождения не может быть в будущем")
        
        return birth_date

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn', 'pages']
        
        labels = {
            'title': 'Название книги',
            'author': 'Автор',
            'published_date': 'Дата публикации',
            'isbn': 'ISBN',
            'pages': 'Количество страниц',
        }
        
        help_texts = {
            'title': 'Введите полное название книги',
            'author': 'Выберите автора из списка или создайте нового',
            'published_date': 'Дата первой публикации книги',
            'isbn': 'Введите 13-значный ISBN код (только цифры)',
            'pages': 'Общее количество страниц в книге',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Война и мир'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
            'published_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '9781234567890',
                'pattern': '[0-9]{13}',  # HTML5 pattern validation
                'title': '13 цифр без пробелов и дефисов'
            }),
            'pages': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10000,
                'step': 1
            }),
        }
    
    def clean_isbn(self):
        """
        Custom валидация для ISBN
        Проверяем формат ISBN-13
        """
        isbn = self.cleaned_data.get('isbn')
        
        if not isbn:
            raise ValidationError("ISBN не может быть пустым")
        
        # Удаляем возможные дефисы
        isbn_clean = isbn.replace('-', '')
        
        # Проверяем длину
        if len(isbn_clean) != 13:
            raise ValidationError("ISBN должен содержать 13 цифр")
        
        # Проверяем, что все символы - цифры
        if not isbn_clean.isdigit():
            raise ValidationError("ISBN должен содержать только цифры")
        
        return isbn_clean  # Возвращаем очищенный ISBN
    
    def clean_pages(self):
        """
        Custom валидация для количества страниц
        """
        pages = self.cleaned_data.get('pages')
        
        if pages is None:
            raise ValidationError("Количество страниц не может быть пустым")
        
        if pages <= 0:
            raise ValidationError("Количество страниц должно быть положительным числом")
        
        if pages > 10000:
            raise ValidationError("Слишком большое количество страниц")
        
        return pages
    
    def clean_published_date(self):
        """
        Custom валидация для даты публикации
        """
        published_date = self.cleaned_data.get('published_date')
        
        if not published_date:
            raise ValidationError("Дата публикации не может быть пустой")
        
        if published_date > date.today():
            raise ValidationError("Дата публикации не может быть в будущем")
        
        return published_date
    
    def clean(self):
        """
        Валидация, зависящая от нескольких полей
        """
        cleaned_data = super().clean()
        author = cleaned_data.get('author')
        published_date = cleaned_data.get('published_date')
        
        # Проверяем, что книга не была опубликована до рождения автора
        if author and author.birth_date and published_date:
            if published_date < author.birth_date:
                raise ValidationError(
                    "Книга не может быть опубликована до рождения автора"
                )
        
        return cleaned_data