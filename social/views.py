from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Follow, UserLike
from .forms import RegistrationForm, ProfileEditForm

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    login_error = None
    register_form = RegistrationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                login_error = "Invalid username or password"
        elif 'register_submit' in request.POST:
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                new_user = authenticate(username=register_form.cleaned_data['username'],
                                        password=register_form.cleaned_data['password'])
                login(request, new_user)
                return redirect('dashboard')

    return render(request, 'social/landing.html', {
        'register_form': register_form,
        'login_error': login_error,
    })

@login_required
def dashboard(request):
    current_type = request.user.profile.account_type
    other_users = User.objects.exclude(id=request.user.id).filter(profile__account_type=current_type)

    ranking = []
    for u in other_users:
        score = u.followers.count() + u.liked_by.count()
        u.is_following = Follow.objects.filter(follower=request.user, followed=u).exists()
        u.is_liked = UserLike.objects.filter(user=request.user, liked_user=u).exists()
        ranking.append((u, score))
    ranking.sort(key=lambda x: x[1], reverse=True)

    return render(request, 'social/dashboard.html', {'ranking': ranking})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
            profile = user.profile
            if user.username[0].upper() != profile.avatar_letter:
                profile.avatar_letter = user.username[0].upper()
                profile.save()
            messages.success(request, "Profile updated.")
            return redirect('profile_edit')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'social/profile_edit.html', {'form': form})

@login_required
def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    is_following = Follow.objects.filter(follower=request.user, followed=profile_user).exists()
    is_liked = UserLike.objects.filter(user=request.user, liked_user=profile_user).exists()
    return render(request, 'social/profile.html', {
        'profile_user': profile_user,
        'is_following': is_following,
        'is_liked': is_liked,
    })

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        if not created:
            follow.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def like_user(request, user_id):
    user_to_like = get_object_or_404(User, id=user_id)
    if user_to_like != request.user:
        like, created = UserLike.objects.get_or_create(user=request.user, liked_user=user_to_like)
        if not created:
            like.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
