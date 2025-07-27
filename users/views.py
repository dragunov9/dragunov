from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .api_serializers import RegisterSerializer
from imagekitio import ImageKit
from django.conf import settings
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from .forms import UserUpdateForm, ProfileUpdateForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile


def register_page(request):
    form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = p_form.save(commit=False)

            image_file = request.FILES.get('image')
            if image_file:
                imagekit = ImageKit(
                    private_key=settings.IMAGEKIT_PRIVATE_KEY,
                    public_key=settings.IMAGEKIT_PUBLIC_KEY,
                    url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
                )

                options = UploadFileRequestOptions(
                    use_unique_file_name=True,
                    is_private_file=False,
                    tags=["profile", request.user.username]
                )

                upload = imagekit.upload_file(
    file=(image_file.name, image_file.read()),
    file_name=image_file.name,
    options=options
)


                if upload.url:
                    profile.image_url = upload.url

            profile.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#follow and unfollow :

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    request.user.profile.follow(target_user.profile)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    request.user.profile.unfollow(target_user.profile)
    return redirect(request.META.get('HTTP_REFERER', 'home'))