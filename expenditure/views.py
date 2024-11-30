from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponseRedirect

"""
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/login')

        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect("/login")
        else:
            login(request,user)
            return redirect("/home")
        
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            user = User.objects.filter(username=username)
            if user.exists():
                messages.error(request,"Username is already taken!")
                return redirect("/login")
            else:
                user = User.objects.create(first_name=first_name,
                                           last_name=last_name,
                                            username=username)
                user.set_password(password1)
                user.save()
            messages.info(request, "Account created successfully!")
            return redirect('/login')
        return render(request, "register.html")


"""

# def home(request):
#     post = Post.objects.filter(status=1).all()

#     return render(request, "expenditure/index.html", {
#         "posts": post,
#     })


class Register(generic.CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "expenditure/register.html"


class Logout(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class Home(generic.ListView, LoginRequiredMixin):
    model = Post
    template_name = "expenditure/index.html"
    #context_object_name = "posts"
    # login_url = reverse_lazy("login")

    def get_queryset(self):
        return Post.objects.filter(status=1)

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['posts'] = Post.objects.filter(user=self.request.user).all()
            total_money = Post.objects.filter(user=self.request.user).aggregate(total=Sum("money"))['total']

            if total_money is not None:
                context['total_money'] = "{:.2f}".format(total_money)
            return context



class PostUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Post
    fields = ['title', 'location', 'money', 'status']
    template_name = "expenditure/update.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")


class PostDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Post
    template_name = "expenditure/delete.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")



class PostSearchView(generic.ListView):
    model = Post
    template_name = "expenditure/search.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET['q']
        return Post.objects.filter(Q(title__icontains=query) | Q(location__icontains=query)).filter(user=self.request.user)
    

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'location', 'money']
    template_name = "expenditure/post_create_form.html"
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 1
        return super().form_valid(form)
    
    success_url = reverse_lazy("home")
