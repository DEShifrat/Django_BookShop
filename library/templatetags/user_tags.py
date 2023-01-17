from django import template
from library.models import Genre
from library.models import Supplier
from django.db.models import Count

register = template.Library()


# @register.simple_tag(name='get_list_genre')
# def get_allgenre():
#     return Genre.objects.all().order_by('title')

# регистрируем пользовательский тег и передаем полученные объекты в шаблон
@register.inclusion_tag('tags/list_genre.html')
def show_genre():
    # genre = Genre.objects.all().order_by('title')
    genre = Genre.objects.annotate(cnt=Count('book')).filter(
        cnt__gt=0).order_by('title')  # не выводим жанры в которых нет книг
    return {'genre': genre}


@register.inclusion_tag('tags/list_autors.html')
def show_autors():
    # genre = Genre.objects.all().order_by('title')
    supplier = Supplier.objects.all().order_by('title')  # не выводим жанры в которых нет книг
    return {'supplier': supplier}


@register.inclusion_tag('tags/list_other.html')
def show_other():
    # genre = Genre.objects.all().order_by('title')
    supplier = Supplier.objects.all().order_by('title')  # не выводим жанры в которых нет книг
    return {'supplier': supplier}