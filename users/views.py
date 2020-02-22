
"""Users views."""

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView

# Models
from django.contrib.auth.models import User
from posts.models import Post

# Forms
from users.forms import ProfileForms, SignupForms


class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view."""

    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context


@login_required
def update_profile(request):
    """Update a user's profile view."""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForms(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']
            profile.save()

            url = reverse('users:detail', kwargs={'username': request.user.username})
            return redirect(url)

    else:
        form = ProfileForms()

    return render(
        request=request,
        template_name='users/update_profile.html',
        context={
            'profile': profile,
            'user': request.user,
            'form': form
        }
    )


def login_view(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts:feed')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username and password'})

    return render(request, 'users/login.html')

class SignupView(FormView):
    template_name = 'users/signup.html'
    form_class = SignupForms
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# def signup_view(request):
#     """Sign up view."""
#     if request.method == 'POST':
#         form = SignupForms(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('users:login')
#     else:
#         form = SignupForms()

#     return render(
#         request=request,
#         template_name='users/signup.html',
#         context={'form': form}
#     )


@login_required
def logout_view(request):
    """Logout a user."""
    logout(request)
    return redirect('users:login')
