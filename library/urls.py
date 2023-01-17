from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from library.views import *

from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import routers

# router = routers.SimpleRouter()







urlpatterns = [
    path('', index, name='home'),  # домашняя страница
    path('books', books_list, name='books_list'),  # Каталог книг
    path('book/<int:book_id>/', detail_books, name='detail_books'),  # Подробная информация о книге
    path('genre/<int:genre_id>/', get_genre, name='genre'),  # Вывод списка книг по жанрам
    path('autors', autor_list, name='list_autors'),
    path('autors/<int:supplier_id>/', detail_autors, name='detail_autors'),
    path('autors/add/',supplier_form, name='add_supp'),

    # LISTVIEW
    path('autors/view/list/', SupplierListView.as_view(), name='list_supp_view'),

    # DETAILVIEW
    path('autors/view/<int:supplier_id>', SupplierDetailView.as_view(), name='info_supp_view'),

    # CREATEVIEW
    path('autors/view/add/', SupplierCreateView.as_view(), name='add_supp_view'),

    # UPDATEVIEW
    path('autors/view/edit/<int:pk>', SupplierUpdateView.as_view(), name='edit_supp_view'),

    # DELETEVIEW
    path('autors/view/delete/<int:pk>', SupplierDeleteView.as_view(), name='delete_supp_view'),


    # Ключ pk по умолчанию в SupplierDetailView(DetailView)
    # path('supplier/view/<int:pk>', SupplierDetailView.as_view(), name='info_supp_view'),

    # Ключ supplier_id после переопределения атрибута pk_url_kwarg в SupplierDetailView(DetailView)
    # path('autors/view/<int:supplier_id>', SupplierDetailView.as_view(), name='info_supp_view'),






# Registration Authorization
    path('login/', user_login, name='login'),
    path('registration/', user_registration, name='registration'),
    path('logout/', user_logout, name='logout'),

    path('is_login/', is_login),
    path('is_login_decorator/', is_login_decorator),

    path('is_perm/', is_permession),
    path('is_perm_add/', is_perm_add),
    path('is_perm_change/', is_perm_change),
    path('is_perm_change_view/', is_perm_change_view),





    # # email
    path('contact/', send_contact_email, name='send_contact'),
    #
    # # API
    # path('api/fruit/', fruit_api_list, name='api_fruit_list'),
    # path('api/fruit/<int:pk>', fruit_api_detail, name='api_fruit_detail'),
    #
    # path('api/', include(router.urls)),
    #


]


# urlpatterns = format_suffix_patterns(urlpatterns)