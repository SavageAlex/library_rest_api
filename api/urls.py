from django.urls import include, path, re_path
from rest_framework import routers
from . import views

# router = routers.DefaultRouter(trailing_slash=False)
# router.register(r'books', views.BookViewSet, basename='books')

urlpatterns = [
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('books', views.BookView.as_view()),
    path('books/<str:id>', views.DetailBookView.as_view()),
    path('db', views.CreateUpdateBookView.as_view()),
]