from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    """Strona główna dla aplikacji learning_logs."""
    return render(request, 'learning_logs/index.html')

def check_topic_owner(request, topic):
    """Upewniamy się, że temat należy do bieżącego użytkownika"""
    if topic.owner != request.user:
        raise Http404

@login_required
def topics(request):
    """Wyświetlenie wszystkich tematów."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Wyświetla pojedynczy temat i powiązane z nim wpisy."""
    topic = Topic.objects.get(id=topic_id) # zapytanie do bazy danych
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added') # zapytanie do bazy danych
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Dodaj nowy temat."""
    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = TopicForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user # Bieżący użytkownik jest właścicielem nowego tematu
            new_topic.save()
            return redirect('learning_logs:topics')
    
    # Wyświetlenie pustego formularza
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Dodanie nowego wpisu dla określonego tematu."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć nowy formularz
        form = EntryForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = EntryForm(data=request.POST)
        if form.is_valid:
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Wyświetlenie pustego formularza
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context) 


@login_required
def edit_entry(request, entry_id):
    """Edycja istniejącego wpisu."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Żądanie początkowe, wypełnienie formularza aktualną treścią wpisu.
        form = EntryForm(instance=entry)
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'topic': topic, 'entry': entry, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    """Usunięcie istniejącego tematu."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    topic.delete()
    context = {'topic': topic}
    return render(request, 'learning_logs/delete_topic.html', context)

@login_required
def delete_entry(request, entry_id):
    """Usunięcie istniejącego wpisu."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)
    entry.delete()
    context = {'entry': entry, 'topic': topic}
    return render(request, 'learning_logs/delete_entry.html', context)

