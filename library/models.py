import datetime

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


# Create your models here.
# создадим модель Жанров книг
class Genre(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название жанра')

    # отобразим информацию об объекте класса в админке
    def __str__(self):
        return self.title

    # настраиваем отображение приложения в админке
    class Meta:
        verbose_name = 'Жанр книги'
        verbose_name_plural = 'Жанры книг'
        ordering = ['title']  # сортировка в админке

    # определяем метод, которым выстраиваем ссылку для получения книг по жанру
    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_id': self.pk})


# определяем выбор значений для поля cover_type
COVER_CHOISES = (
    ('мягкая', 'мягкая'),
    ('твердая', 'твердая')
)
# определяем выбор значений для поля pub_date
YEAR_CHOICES = [(y, y) for y in range(1800, datetime.date.today().year + 1)]


# создаем модель Книг
class Book(models.Model):
    # поле обязательно для заполнения и ставим ограничение в 255 символов
    title = models.CharField(max_length=250, verbose_name='Название книги')
    # у каждой книги есть автор, поле обязательно для заполнения
    author = models.CharField(max_length=150, verbose_name='Автор')
    # поле описания, к заполнению необязательно
    description = models.TextField(null=True, blank=True, verbose_name='Описание книги')
    # т.к. Integer слишком большое поле и может хранить в себе отрицательные значения
    # нам достаточно Decimal, поставим ограничение на количество знаков, и уберем цифры после запятой
    num_pages = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Количество страниц')
    # поле выбора обложки, вынесем выбор значений в отдельный список
    cover_type = models.CharField(max_length=7, choices=COVER_CHOISES, verbose_name='Тип обложки')
    # поле цены книги, особых требований к нему нет
    price = models.FloatField(verbose_name='Цена')
    # в поле размера книги поставим ограничение на количество символов и  сделаем необязательным к заполнению
    sizes = models.CharField(max_length=50, null=True, blank=True, verbose_name='Размер книги/формат издания')
    # поскольку в дате публикации указывается только год, сделаем поле Integer с выбором значений,
    # по умолчанию установим текущий год
    pub_date = models.IntegerField(choices=YEAR_CHOICES,
                                   default=datetime.datetime.now().year, verbose_name='Дата издания')
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT, null=True, verbose_name='Автор')

    # добавим поля для обложки книги, укажем допустимый тип загружаемых файлов
    photo_cover = models.ImageField(upload_to='image/%Y/%m/%d',
                                    validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                                    null=True, blank=True, verbose_name='Передняя обложка')
    photo_back = models.ImageField(upload_to='image/%Y/%m/%d',
                                   validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                                   null=True, blank=True, verbose_name='Задняя обложка')
    genres = models.ManyToManyField(Genre)

    # отобразим информацию об объекте класса в админке
    def __str__(self):
        return self.title

    # настраиваем отображение приложения в админке
    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Каталог книг'
        ordering = ['title']  # сортировка в админке

    # определяем метод, которым выстраиваем ссылку для подробного описания книги и передаем ее в шаблон
    def get_absolute_url(self):
        return reverse('detail_books', kwargs={'book_id': self.pk})





class Supplier(models.Model):
    title = models.CharField(max_length=200, verbose_name='Псевдоним')
    agent_name = models.CharField(max_length=100, verbose_name='Имя автора')
    agent_firstname = models.CharField(max_length=100, verbose_name='Фамилия автора')
    agent_patronymic = models.CharField(max_length=100, verbose_name='Отчество автора')
    description = models.TextField(null=True, blank=True, verbose_name='Биография')
    exist = models.CharField(max_length=50, verbose_name='Работает по настоящее время?')
    birthday = models.IntegerField(choices=YEAR_CHOICES,
                                   default=datetime.datetime.now().year, verbose_name='Год рождения')
    photo_cover = models.ImageField(upload_to='image/%Y/%m/%d',
                                    validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                                    null=True, blank=True, verbose_name='Фото')
    photo_back = models.ImageField(upload_to='image/%Y/%m/%d',
                                   validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                                   null=True, blank=True, verbose_name='Фото-2')

    def __str__(self):
        return self.title

    class Meta:  # Класс для названий нашей модели в админке
        verbose_name = 'Автор'  # Надпись в единственном числе
        verbose_name_plural = 'Авторы'  # Надпись во множественном числе
        ordering = ['title']  # Сортировка полей (по возрастанию)

        # определяем метод, которым выстраиваем ссылку для подробного описания книги и передаем ее в шаблон

    def get_absolute_url(self):  # тэг url для объекта (Данный метод для вывода странички одной записи)
        return reverse('detail_autors', kwargs={'supplier_id': self.pk})



class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    date_finish = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения заказа')
    price = models.FloatField(null=True, verbose_name='Стоимость заказ')
    address_delivery = models.CharField(max_length=150, verbose_name='Адрес доставки')
    status = models.CharField(max_length=150, verbose_name='Статус',
                              choices=[
                                  ('1', 'Создан'),
                                  ('2', 'Отменён'),
                                  ('3', 'Согласован'),
                                  ('4', 'В пути'),
                                  ('5', 'Завершён'),
                              ]
                              )

    # fruits = models.ManyToManyField(Fruit) # Обычное создание связи М к М, через техническую таблицу Fruit_Order
    books = models.ManyToManyField(Book, through='Pos_order')  # Создание связи М к М, через таблицу Pos_order

    def __str__(self):
        return f"{self.date_create} | {self.status} | {self.price}"

    class Meta:  # Класс для названий нашей модели в админке
        verbose_name = 'Заказ'  # Надпись в единственном числе
        verbose_name_plural = 'Заказы'  # Надпись во множественном числе
        ordering = ['date_create']  # Сортировка полей (по возрастанию)


class Pos_order(models.Model):
    books = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name='Книга')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
    count_book = models.IntegerField(verbose_name='Количество товара')
    price = models.FloatField(verbose_name='Общая цена товаров')

    def __str__(self):
        return self.books.name + " " + self.order.address_delivery + " " + self.order.status

    class Meta:  # Класс для названий нашей модели в админке
        verbose_name = 'Позиция'  # Надпись в единственном числе
        verbose_name_plural = 'Позиции'  # Надпись во множественном числе
        ordering = ['books', 'order', 'price']  # Сортировка полей (по возрастанию)


class Cheque(models.Model):
    date_print = models.DateTimeField(auto_now_add=True, verbose_name='Дата распечатки')
    address_print = models.CharField(max_length=150, verbose_name='Место создания чека')
    terminal = models.CharField(max_length=10, verbose_name='Код терминала')

    order = models.OneToOneField(Order, on_delete=models.PROTECT, primary_key=True, verbose_name='Заказ')

    # primary_key = False - Поле id (Первичный) и Поле order(Внешний) - раздельны
    # primary_key = True - Поле order - Первичный и Внешним ключом

    def __str__(self):
        return str(self.date_print) + " " + self.terminal

    class Meta:  # Класс для названий нашей модели в админке
        verbose_name = 'Чек'  # Надпись в единственном числе
        verbose_name_plural = 'Чеки'  # Надпись во множественном числе
        ordering = ['terminal', 'date_print']  # Сортировка полей (по возрастанию)


