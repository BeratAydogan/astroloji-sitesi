import datetime

from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from astrolojisitem.helpers import get_kullanici_burc, yorumgonder
from astrolojisitem.models import Burclar, Topic, Post
from .forms import UpdateProfileForm, UpdateUserForm, NewPostForm
from .tokens import generate_token
from AstrolojiSitesi import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count




def login_request(request):
    if request.user.is_authenticated:
        return redirect("anasayfa")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("anasayfa")
            else:
                return render(request, "account/login.html", {"error": "Hesabınız aktif değil! Hesabınızı doğrulayınız."})
        else:
            return render(request, "account/login.html", {
                "error": "Giriş başarısız! Kullanıcı adı ve şifrenizi kontrol ediniz. "})
    return render(request, "account/login.html")


def register_request(request):
    if request.user.is_authenticated:
        return redirect("anasayfa")
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        surname = request.POST["surname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if not User.objects.filter(username=username).exists():
                if username is "":
                    return render(request, "account/register.html",
                                  {"error": "Kullanıcı adı boş olmamalı.", "name": name, })
                else:
                    if User.objects.filter(email=email).exists():
                        return render(request, "account/register.html",
                                      {"error": "Bu email başkası tarafından kullanılmakta.", "name": name, })
                    else:
                        user = User.objects.create_user(username=username, email=email, first_name=name, last_name=surname,
                                                        password=password)
                        profile = user.profile
                        profile.gun = request.POST["gun"]
                        profile.ay = request.POST["ay"]
                        profile.yil = request.POST["yil"]
                        if profile.gun and profile.ay and profile.yil == "":
                            return render(request, "account/register.html",
                                          {"error": "Doğum tarihinizi girmeniz gerekmektedir.", "name": name, })
                        user.is_active = False
                        user.save()

                        current_site = get_current_site(request)
                        email_subject = "Confirm your email "
                        message = render_to_string('email_confirm.html', {
                            "name": user.first_name,
                            "domain": current_site.domain,
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "token": generate_token.make_token(user)

                        })
                        email = EmailMessage(
                            email_subject, message, settings.EMAIL_HOST_USER, [user.email],
                        )
                        email.fail_silently = True
                        email.send()

                        return redirect("login")
            else:
                return render(request, "account/register.html",
                              {"error": "Bu kullanıcı adı başkası tarafından kullanılmakta.",
                               "name": name,

                               })
        else:
            return render(request, "account/register.html",
                          {"error": "Parola eşleşmiyor tekrar deneyiniz.", "name": name, })

    return render(request, "account/register.html", )


@login_required
def update_user(request):
    arananburc, resim = get_kullanici_burc(request)
    topics = Topic.objects.filter(starter=request.user)
    posts = Post.objects.filter(created_by=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')

            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'account/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'kullanici_burc': arananburc, 'kullanici_burc_resim': resim,'topics':topics,'posts':posts})


def logout_request(request):
    logout(request)
    return redirect("anasayfa")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('anasayfa')
    else:
        return render(request, 'activate_fail.html')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('anasayfa')


def daily_emails(request):
    # burayı sadece admine çzel yapıcan
    if request.user.is_superuser:
        # burada günlük e-postaların içeriğini oluşturun

        recievers = []
        for user in User.objects.all():
            if user.profile.gonder:
                recievers.append(user.email)

                arananburc, resim = yorumgonder(user)
                burc = Burclar.objects.get(burc_adi=arananburc)

                message = burc.gunluk_yorum
                send_mail(
                    'Sevgili '+arananburc+' Burçları',
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

        # e-posta gönderme işlemini gerçekleştirin

        return HttpResponse("E-postalar başarıyla gönderildi.")
    else:
        return HttpResponse("E-posta göndermek için admin olmalısınız")







def new_topic(request, board_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            subject = request.POST['subject']
            message = request.POST['message']

            if subject and message:
                topic = Topic.objects.create(
                    subject=subject,
                    description=message,
                    last_updated=datetime.date.today(),
                    starter=request.user,

                )
                return redirect('all_topics')
    else:
        return redirect('login')

    return render(request, 'new_topic.html',)


def topic_posts(request, id):
    topic = get_object_or_404(Topic, id=id)
    posts = topic.posts.all()
    resim = ""
    arananburc = ""

    if request.user.is_authenticated:
        arananburc, resim = get_kullanici_burc(request)
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                post = form.save(commit=False)
                post.topic = topic
                post.created_by = request.user
                post.save()
                return redirect('topic_posts', id=id)
            else:
                return redirect('login')
    else:
        form = NewPostForm()
    top_topics = Topic.objects.annotate(num_likes=Count('posts')).order_by('-num_likes')[:5]
    liked_topics = Topic.objects.annotate(num_likes=Count('topic_likes')).order_by('-num_likes')[:5]

    return render(request, 'account/topic_posts.html', {'topic': topic, 'posts': posts, 'form': form,
                                                        'top_topics': top_topics,
                                                        'liked_topics':liked_topics,
                                                        "kullanici_burc": arananburc,
                                                        "kullanici_burc_resim": resim,
                                                        })




def all_topics(request):
    topics = Topic.objects.all()
    resim = ""
    arananburc = ""

    if request.user.is_authenticated:
        arananburc, resim = get_kullanici_burc(request)
    search_query = request.GET.get('search_query')  # Kullanıcının arama sorgusunu alın

    if search_query:
        topics = topics.filter(subject__icontains=search_query)



    return render(request, 'all_topics.html', {'topics': topics, "kullanici_burc": arananburc,
        "kullanici_burc_resim": resim,})

def delete_topic(request,id):
    topic = Topic.objects.get(id=id)
    if request.user.is_superuser:
        topic.delete()
        return redirect('all_topics')
    else:
        if topic.starter == request.user:
            topic.delete()
            return redirect('all_topics')
        else:
            return HttpResponse("Bu başlığı silmek için yetkili değilsiniz.")

def delete_post(request, id):
    post = Post.objects.get(id=id)
    if request.user.is_superuser:
        post.delete()
        return redirect('all_topics')
    else:
        if post.created_by == request.user:
            post.delete()
            return redirect('all_topics')
        else:
            return HttpResponse("Bu yorumu silmek için yetkili değilsiniz.")




def edit_post(request,id):
    post = Post.objects.get(id=id)
    if request.user.is_superuser:
        if request.method == 'POST':
            message = request.POST['message']

            post.message = message
            post.save()

            return redirect('topic_posts', id=post.topic.pk)
    else:
        if post.created_by == request.user:
            if request.method == 'POST':
                message = request.POST['message']

                post.message = message
                post.save()

                return redirect('topic_posts', id=post.topic.pk)
        else:
            return HttpResponse("Bu yorumu düzenlemek için yetkili değilsiniz.")
    context = {'post': post}
    return render(request, 'account/post_edit.html', context)


def edit_topic(request,id):
    topic = Topic.objects.get(id=id)
    if request.user.is_superuser:
        if request.method == 'POST':
            subject = request.POST['subject']
            description = request.POST['description']
            topic.subject = subject
            topic.description = description
            topic.save()
            return redirect('topic_posts', id=topic.id)
    else:
        if topic.starter == request.user:
            if request.method == 'POST':
                subject = request.POST['subject']
                description = request.POST['description']
                topic.subject = subject
                topic.description = description
                topic.save()
                return redirect('topic_posts', id=topic.id)
        else:
            return HttpResponse("Bu başlığı düzenlemek için yetkili değilsiniz.")
    context = {'topic': topic}
    return render(request, 'account/topic_edit.html', context)



def post_reply(request, post_id):
    parent = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = parent.topic
            post.created_by = request.user
            post.parent = parent
            post.save()
            return redirect('topic_posts', id=post.topic.pk)
    else:
        form = NewPostForm()
    return render(request, 'account/reply_post.html', {'form': form, 'parent_id': post_id,'parent':parent})


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if user in post.post_likes.all():
        post.post_likes.remove(user)
    else:
        post.post_likes.add(user)
    return redirect('topic_posts', id=post.topic.pk)


def like_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    user = request.user
    if user in topic.topic_likes.all():
        topic.topic_likes.remove(user)
    else:
        topic.topic_likes.add(user)
    return redirect('topic_posts', id=topic.pk)



def delete_topic2(request,id):
    topic = Topic.objects.get(id=id)
    if request.user.is_superuser:
        topic.delete()
        return redirect(request.META.get('HTTP_REFERER', ''))
    else:
        if topic.starter == request.user:
            topic.delete()
            return redirect(request.META.get('HTTP_REFERER', ''))
        else:
            return HttpResponse("Bu başlığı silmek için yetkili değilsiniz.")

def delete_post2(request, id):
    post = Post.objects.get(id=id)
    if request.user.is_superuser:
        post.delete()
        return redirect(request.META.get('HTTP_REFERER', ''))
    else:
        if post.created_by == request.user:
            post.delete()
            return redirect(request.META.get('HTTP_REFERER', ''))
        else:
            return HttpResponse("Bu yorumu silmek için yetkili değilsiniz.")








