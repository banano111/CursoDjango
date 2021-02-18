from django.urls import path
from .views import GetGroup, GetGroups, CreateGroup, UpdateGroup, RemoveUser, DeleteGroup

app_name = 'groups'

urlpatterns = [
    path('', GetGroups, name='list'),
    path('<int:id>', GetGroup, name='detail'),
    path('create/', CreateGroup.as_view(), name='create'),
    path('update/<int:id>/', UpdateGroup.as_view(), name='update'),
    path('delete/<int:id>', DeleteGroup, name='delete'),
    path('delete_user/<int:id>', RemoveUser, name="remove_user")
]
