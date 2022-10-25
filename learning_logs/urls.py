from django.urls import path
from . import views

app_name = 'learning_logs'

urlpatterns = [
    # Strona główna
    path('', views.index, name='index'),
    # Wyświetlenie wszystkich tematów
    path('topics/', views.topics, name='topics'),
    # Strona szczegółowa dotycząca pojedynczego tematu
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Formularz dla dodania tematu
    path('new_topic/', views.new_topic, name='new_topic'),
    # Formularz dla dodania wpisu
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Formularz dla edycji istniejącego wpisu
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # Usunięcie tematu
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    # Usunięcie wpisu
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),


]