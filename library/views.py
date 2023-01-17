from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

import library
from book_magazine import settings
from .forms import LoginForm, RegistrationForm, SupplierForm, ContactForm
from .models import Book, Genre
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .models import Book, Supplier, Order, Pos_order, Cheque



# Create your views here.

# рендорим главную страницу
from .utils import Default_value


def index(request):
    return render(request, 'library/index.html')






# определяем функцию вывода списка книг
def books_list(request):
    books = Book.objects.all().order_by('title')  # получаем все книги из базы данных и отсортируем по названию
    # передаем в контекст обьект books
    context = {
        'books': books,
    }
    return render(request, 'library/books_list.html', context)


# определяем функцию вывода подробной информации о книге
def detail_books(request, book_id):
    book = get_object_or_404(Book, pk=book_id)  # по PK получаем объект или отдаем 404 ошибку, если объект не найден
    # полученный объект передаем в контекст
    context = {
        'book': book
    }
    return render(request, 'library/book_detail.html', context)

# определяем функцию получения книг по жанрам
def get_genre(request, genre_id):
    books = Book.objects.filter(
        genres=genre_id)  # получаем все книги из базы данных, которые соответствуют выбранному жанру
    # полученный объект передаем в контекст
    context = {
        'books': books,
    }
    return render(request, 'library/books_genre.html', context)




def autor_list(request):
    context = {'title': 'Авторы'}

    fruits = Supplier.objects.all()
    context['autor_list'] = fruits

    # Paginator
    paginator = Paginator(fruits, 3)  # Создаем пагинатор из списка фруктов и делаем страницы по 3 элемента
    page_num = request.GET.get('page', 1)  # Получение страницы, на которой находится наш пользователь
    page_objects = paginator.get_page(page_num)  # Получение группы элементов(3) по номеру страницы
    context['page_obj'] = page_objects  # Передача данных на .html

    print(page_objects.object_list)
    # context = {
    #     'title': 'Фрукты',
    #     'fruit_list': fruits,
    #     'fruit_one': fruit_one,
    #     'name': name
    # }
    return render(
        request=request,
        template_name='library/autor_list.html',
        context=context
    )


def detail_autors(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)  # по PK получаем объект или отдаем 404 ошибку, если объект не найден
    # полученный объект передаем в контекст
    context = {
        'supplier': supplier
    }
    return render(request, 'library/autor_detail.html', context)



class SupplierListView(ListView, Default_value):  # Возврат листа объектов
    model = Supplier  # определение таблицы для взаимодействия
    template_name = 'library/supplier/supplier-list.html'  # путь шаблона (<Имя приложения>/<Имя модели>_list.html)
    context_object_name = 'suppliers'  # Отправка данных по заданному ключу (object_list)
    extra_context = {'title': 'Авторы из класса'}  # Доп. значения (статичные данные)

    # Paginator
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Получение атрибутов из класса
        print(context)
        # context['title'] = 'Главная страница поставщиков'  # Переопределение ключа title

        # Использование миксина из utils
        # Dv = Default_value()
        # context = Dv.add_title_context(context=context, title_name='Страница поставщиков')

        context = self.add_title_context(context=context, title_name='Страница авторов')

        context['info'] = 'Рабочая страница авторов'  # Добавление ключа info
        return context  # Возврат словаря значений

    def get_queryset(self):
        return Supplier.objects.filter(exist=True).order_by('title')

    # Права доступа
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)




# Supplier Detail
def supplier_detail(request, supplier_id):
    object = Supplier.objects.get(pk=supplier_id)
    # object = get_object_or_404(library, pk=supplier_id)
    return render(request, 'library/supplier/supplier-info.html', {'one_supplier': object})


# ==
class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'library/supplier/supplier-info.html'
    context_object_name = 'one_supplier'  # (object)
    pk_url_kwarg = 'supplier_id'  # Переопределение ключа ID при получении (pk)
    allow_empty = False  # Возврат 404 при отсутствии данных

    # без get_absolute_url ссылается на шаблон по умолчанию (supplier_detail.html)
    # с get_absolute_url ссылается на данный метод
    # (info_supp_view -> path(SupplierDetailView.as_view()) -> fruit/supplier/supplier-info.html)

    # Права доступа
    @method_decorator(permission_required('library.view_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# Supplier create
def supplier_form(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            # Supplier.objects.create(
            #     title=form.cleaned_data['title'],
            #     agent_name=form.cleaned_data['agent_name'],
            #     agent_firstname=form.cleaned_data['agent_firstname'],
            #     agent_patronymic=form.cleaned_data['agent_patronymic'],
            #     exist=form.cleaned_data['exist'],
            #     birthday=form.cleaned_data['birthday'],
            #     photo_cover = form.cleaned_data['photo_cover']
            # )

            Supplier.objects.create(
                **form.cleaned_data
            )

            # return HttpResponseRedirect('/fruit/supplier/add/') # в методе указ. URL-адрес
            return redirect('list_autors')  # в методе указ. URL-адрес, название пути, модель
        else:
            context = {'form': form}
            return render(request, 'library/supplier/supplier-add.html', context)
    else:
        form = SupplierForm()
        context = {'form': form}
        return render(request, 'library/supplier/supplier-add.html', context)


# ==

class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm  # Определение формы для взаимодействия
    template_name = 'library/supplier/supplier-add.html'
    context_object_name = 'form'  # Переопределение ключа формы (object)
    success_url = reverse_lazy('list_supp_view')

    # success_url = '/fruit/supplier/view/list'

    # Права доступа
    @method_decorator(permission_required('library.add_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# Supplier update

class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy('list_autors')
    template_name = 'library/supplier/supplier-edit.html'
    context_object_name = 'form'

    # Права доступа
    @method_decorator(permission_required('library.change_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# Supplier delete

class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy('list_autors')
    template_name = 'library/supplier/supplier-delete.html'

    # Права доступа
    @method_decorator(permission_required('library.delete_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
















def user_registration(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST) # Форма создания пользователя из auth
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Запись нового пользователя
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Не удалось зарегистрировать')
    else:
        # form = UserCreationForm()
        form = RegistrationForm()
    return render(request, 'library/auth/registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            print(request.user.is_authenticated)
            print(request.user.is_anonymous)
            login(request, user)
            print(request.user.is_authenticated)
            print(request.user.is_anonymous)
            messages.success(request, 'Вы успешно авторизовались')
            messages.info(request, 'Каталог товаров обновился')
            return redirect('books_list')
        messages.error(request, 'Авторизация прошла с ошибкой, перепроверьте логин и/или пароль')
    else:
        form = LoginForm()
    return render(request, 'library/auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('login')


def is_login(request):
    if request.user.is_anonymous:
        return HttpResponse('<h1>Вы аноним</h1>')
    else:
        return HttpResponse('<h1>Зарегистрированы</h1>')


@login_required
def is_login_decorator(request):
    return HttpResponse('<h1>Зарегистрированы</h1>')


def is_permession(request):
    text = ''
    if request.user.has_perm('library.add_supplier'):  # <Название приложения>.<операция>_<название модели>
        text += '<h1>Вы можете добавлять поставщиков</h1>'
    if request.user.has_perm('library.change_supplier'):
        text += '<h1>Вы можете изменять поставщиков</h1>'
    if request.user.has_perm('library.view_supplier'):
        text += '<h1>Вы можете просматривать поставщиков</h1>'
    if request.user.has_perms(['library.change_supplier', 'library.view_supplier']):
        text += '<h1>Вы можете просматривать и изменять поставщиков</h1>'
    if text == '':
        HttpResponse('<h1>У вас нет прав</h1>')
    return HttpResponse(text)


@permission_required('library.add_supplier')
def is_perm_add(request):
    return HttpResponse('<h1>Добавление поставщика</h1>')


@permission_required('library.change_supplier')
def is_perm_change(request):
    return HttpResponse('<h1>Изменение поставщика</h1>')


@permission_required(['library.change_supplier', 'Fruit.view_supplier'])
def is_perm_change_view(request):
    return HttpResponse('<h1>Изменение и просмотр поставщика</h1>')


def error_404(request, exception):
    context = dict()
    context['title'] = 'Упс, вы попали куда-то не туда'
    response = render(request, 'library/error/404.html', context)
    response.status_code = 404
    return response






def send_contact_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            mail = send_mail(  # Отправка письма
                form.cleaned_data['subject'],  # Заголовок письма
                form.cleaned_data['content'],  # Тело письма
                settings.EMAIL_HOST_USER,  # Отправитель письмо
                (form.cleaned_data['recipient'],),  # Получатель письма
                fail_silently=False,  # Режим отображения ошибок (True - исключения не будет)
                #                               (False - исключения выведутся на страницу)
            )
            if mail:
                messages.success(request, 'Письмо было успешно отправлено')
                return redirect('books_list')
            else:
                messages.error(request, 'Письмо не удалось успешно отправить')
        else:
            messages.error(request, 'Письмо заполнено неверно')
    else:
        form = ContactForm()
    return render(request, 'library/other/contact.html', {'title': 'Предложения и пожелания', 'form': form})