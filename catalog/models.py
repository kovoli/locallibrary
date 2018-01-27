from django.db import models
from django.urls import reverse
import uuid


class Genre(models.Model):
    """
    Определяет жанр книги
    """
    name = models.CharField(max_length=200, help_text='Введите жанр книги')

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Модель представляющая книги
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    #  один автор, но у автора может быть много книг
    summary = models.TextField(max_length=1000, help_text='Описание книги')
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre, help_text='Выбрать жанр')
    # книга может иметь несколько жанров, а жанр может иметь много книг.

    def __str__(self):
        return self.title


    def get_absolut_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """
    Модель, представляющая конкретную копию книги
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный идентификатор для этой конкретной книги по всей библиотеке')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Aviable'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Наличие книги')

    class Meta:
        ordering = ['due_back']


    def __str__(self):
        return '{0} {1}'.format(self.id, self.book.title)


class Author(models.Model):
    """
    Модель, представляющая автора
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к конкретному экземпляру автора
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        Строка для представления объекта Model.
        """
        return '{0} {1}'.format(self.last_name, self.first_name)