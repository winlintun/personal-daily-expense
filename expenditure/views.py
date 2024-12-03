from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import Sum
from django.utils.timezone import now
from django.http import Http404

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
    """
    User register class
    - create new account
    """
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "expenditure/register.html"


class Logout(generic.View):
    """
    User logout class
    - logout user account
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


@method_decorator(login_required, name="dispatch")
class Home(generic.ListView):
    """
    Home User Class
    - show data user use daily expense 
    - add page pagination

    """

    model = Post
    template_name = "expenditure/index.html"
    paginate_by = 5
    queryset = Post.objects.filter(status=1).order_by("-create_date")
    #context_object_name = "posts"


    def get_queryset(self):
        """
        filter only publish post
        """
        return Post.objects.filter(status=1).filter(user=self.request.user).all()

    def get_context_data(self, **kwargs):
        """
        - post all list
        - total sum amount
        - money format
        """
        context = super(Home, self).get_context_data(**kwargs)
        #context['posts'] = Post.objects.filter(user=self.request.user).all()
        total_money = Post.objects.filter(user=self.request.user).aggregate(total=Sum("money"))['total']

        if total_money is not None:
            context['total_money'] = "{:.2f}".format(total_money)
        return context



@method_decorator(login_required, name="dispatch")
class PostUpdateView(generic.edit.UpdateView):
    model = Post
    fields = ['title', 'location', 'money', 'status']
    template_name = "expenditure/update.html"
    success_url = reverse_lazy("home")



@method_decorator(login_required, name="dispatch")
class PostDeleteView(generic.edit.DeleteView):
    model = Post
    template_name = "expenditure/delete.html"
    success_url = reverse_lazy("home")



class PostSearchView(generic.ListView):
    model = Post
    template_name = "expenditure/search.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET['q']
        return Post.objects.filter(Q(title__icontains=query) | Q(location__icontains=query)).filter(user=self.request.user)
    

@method_decorator(login_required, name="dispatch")
class PostCreateView(generic.CreateView):
    model = Post
    fields = ['title', 'location', 'money']
    template_name = "expenditure/post_create_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 1
        return super().form_valid(form)
    
    success_url = reverse_lazy("home")

@method_decorator(login_required, name="dispatch")
class PostMonthArchiveView(generic.MonthArchiveView):
    date_field = "create_date"
    allow_future = True
    month_format = "%m"
    year_format = "%Y"

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).all()
    

    def get_year(self):
        try:
            year = super(PostMonthArchiveView, self).get_year()
        except Http404:
            year = now().strftime(self.get_year_format())
        return super().get_year()

    def get_month(self):
        try:
            month = super(PostMonthArchiveView, self).get_month()
        except Http404:
            month = now().strftime(self.get_month_format())
        return super().get_month()