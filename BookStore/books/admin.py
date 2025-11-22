from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Настройки админ-панели для модели Author
    """
    # Поля, которые отображаются в списке авторов
    list_display = ('name', 'birth_date', 'books_count')
    
    # Поля, по которым можно искать
    search_fields = ('name', 'bio')
    
    # Фильтры справа
    list_filter = ('birth_date',)
    
    # Поля в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'birth_date')
        }),
        ('Биография', {
            'fields': ('bio',),
            'classes': ('wide',)
        }),
    )
    
    # Пустое значение для даты рождения
    empty_value_display = 'Не указано'
    
    def books_count(self, obj):
        """Количество книг автора"""
        return obj.books.count()
    books_count.short_description = 'Количество книг'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Настройки админ-панели для модели Book
    """
    # Поля, которые отображаются в списке книг
    list_display = ('title', 'author', 'published_date', 'pages', 'isbn')
    
    # Поля, по которым можно искать
    search_fields = ('title', 'isbn', 'author__name')
    
    # Фильтры справа
    list_filter = ('published_date', 'author')
    
    # Поля в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'published_date')
        }),
        ('Детали', {
            'fields': ('isbn', 'pages')
        }),
    )
    
    # Автозаполнение поля slug (если бы оно было)
    # prepopulated_fields = {'slug': ('title',)}
    
    # Порядок полей в форме
    # fields = ('title', 'author', 'published_date', 'isbn', 'pages')
    
    def get_queryset(self, request):
        """Оптимизация запроса с использованием select_related"""
        return super().get_queryset(request).select_related('author')