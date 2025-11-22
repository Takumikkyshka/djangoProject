from django.db import models

class Author(models.Model):
    # Поле для имени автора
    name = models.CharField(
        max_length=100,
        verbose_name='Имя автора',
        help_text='Введите полное имя автора'
    )
    
    # Поле для даты рождения
    birth_date = models.DateField(
        null=True,                    # Может быть NULL в базе данных
        blank=True,                   # Поле может быть пустым в формах
        verbose_name='Дата рождения',
        help_text='Введите дату рождения автора'
    )
    
    # Поле для биографии
    bio = models.TextField(
        blank=True,                   # Поле может быть пустым
        verbose_name='Биография',
        help_text='Введите краткую биографию автора'
    )
    
    # Метод для строкового представления объекта
    def __str__(self):
        return self.name
    
    # Дополнительные настройки модели
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']  # Сортировка по умолчанию по имени»


class Book(models.Model):
    # Поле для названия книги
    title = models.CharField(
        max_length=200,
        verbose_name='Название книги',
        help_text='Введите полное название книги'
    )
    
    # Связь с моделью Author (внешний ключ)
    author = models.ForeignKey(
        Author,                          # Связываем с моделью Author
        on_delete=models.CASCADE,        # Что делать при удалении автора
        related_name='books',            # Имя для обратной связи
        verbose_name='Автор книги',
        help_text='Выберите автора книги'
    )
    
    # Поле для даты публикации
    published_date = models.DateField(
        verbose_name='Дата публикации',
        help_text='Введите дату первой публикации книги'
    )
    
    # Поле для ISBN
    isbn = models.CharField(
        max_length=13,                   # ISBN-13 состоит из 13 символов
        unique=True,                     # Уникальный идентификатор
        verbose_name='ISBN',
        help_text='Введите 13-значный ISBN код'
    )
    
    # Поле для количества страниц
    pages = models.IntegerField(
        verbose_name='Количество страниц',
        help_text='Введите общее количество страниц в книге'
    )
    
    # Метод для строкового представления
    def __str__(self):
        return f"{self.title} - {self.author.name}"
    
    # Дополнительные настройки модели
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']  # Сортировка по названию


