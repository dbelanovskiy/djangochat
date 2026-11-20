from django.shortcuts import render
from .models import Articles
from .forms import AriclesForm
from django.views.generic import DetailView
def news_home(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'news/news.html', {'news': news})

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'
def create(request):
    error = ''
    if request.method == 'POST':
        form = AriclesForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error="Форма была неверной"
    form = AriclesForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html', data)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})
