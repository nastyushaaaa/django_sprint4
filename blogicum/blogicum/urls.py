from django.contrib import admin  # type: ignore[import-untyped]
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import include, path, reverse_lazy

urlpatterns: list[path] = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    # path('posts/', include('blog.urls')),
    # path('category/', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration',
    ),
]


# Обработчики ошибок
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
