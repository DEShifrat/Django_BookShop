from django.contrib import admin

from .models import Book, Genre, Supplier, Order, Pos_order, Cheque


# Register your models here.

# настроим отображение объектов модели Library в админке
class LibraryAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'title', 'author', 'num_pages', 'cover_type', 'price', 'sizes', 'pub_date')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('id', 'title')
    # поля по которым будет производиться поиск
    search_fields = ('id', 'title', 'author', 'price', 'pub_date')
    # поля которые будем использовать для фильтрации
    list_filter = ('author', 'cover_type', 'pub_date')
    filter_horizontal = ['genres']


# регистрирум модель и наш класс настроек
admin.site.register(Book, LibraryAdmin)


# настроим отображение объектов модели Genre в админке
class GenreAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'title')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('id', 'title')
    # поля по которым будет производиться поиск
    search_fields = ('title',)
    # поля которые будем использовать для фильтрации
    list_filter = ('title',)


# регистрирум модель и наш класс настроек
admin.site.register(Genre, GenreAdmin)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'agent_firstname', 'agent_name', 'agent_patronymic', 'exist')  # Отображение полей
    list_display_links = ('id', 'title')  # Установка ссылок на атрибуты
    search_fields = ('title', 'agent_firstname')  # Поиск по полям
    list_editable = ('exist',)  # Изменяемое поле
    list_filter = ('exist',)  # Фильтры полей


admin.site.register(Supplier, SupplierAdmin)


# Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_create', 'date_finish', 'status', 'price', 'address_delivery')
    list_display_links = ('id',)
    search_fields = ('date_create', 'address_delivery')
    list_editable = ('date_finish', 'status')
    list_filter = ('status',)


admin.site.register(Order, OrderAdmin)


# Position order
class Pos_orderAdmin(admin.ModelAdmin):
    list_display = ('id', 'books', 'order', 'count_book', 'price')
    list_display_links = ('books','order')
    search_fields = ('books', 'order')
    # list_editable = ('date_finish', 'status')
    # list_filter = ('order',)


admin.site.register(Pos_order, Pos_orderAdmin)


# Cheque
class ChequeAdmin(admin.ModelAdmin):
    list_display = ('order','date_print', 'address_print', 'terminal')
    list_display_links = ('order', 'date_print')
    search_fields = ('date_print', 'address_print')


admin.site.register(Cheque, ChequeAdmin)