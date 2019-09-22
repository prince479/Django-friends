from django.shortcuts import render,redirect
from .forms import LoginForm,SignupForm,EditProfile
from .models import Signup,Profile,FriendRequest


def login(request):
    if request.session.get('user_email'):
        return redirect('homepage')
    form=LoginForm(request.POST or None)
    if form.is_valid():
        email1=form.cleaned_data.get('email')
        password1=form.cleaned_data.get('password')

        data=Signup.objects.filter(email=email1,password=password1)
        if data:
            request.session['user_email']=email1
            return  redirect('homepage')
        else:
            print("not match")
    context={
        'form':form
    }
    return render(request,'login.html',context)

def logout(request):
    del request.session['user_email']  #( TO DELETE THE SESSION)
    return redirect('login')



def signup(request):
    if request.session.get('user_email'):
        return redirect('homepage')

    signup_form=SignupForm(request.POST or None)
    if signup_form.is_valid():
        username = signup_form.cleaned_data.get('username')
        password = signup_form.cleaned_data.get('password')
        email = signup_form.cleaned_data.get('email')
        mobile = signup_form.cleaned_data.get('mobile')

        request.session['username']=username
        request.session['password']=password
        request.session['email']=email
        request.session['mobile']=mobile


    if 'register' in request.POST:
        uname=request.session.get('username')
        upass=request.session.get('password')
        uemail=request.session.get('email')
        umobile=request.session.get('mobile')



        signup=Signup(username=uname,password=upass,email=uemail,mobile=umobile)
        signup.save()
        print("user created successfully")

        return redirect('login')




    data={
        'form':signup_form
    }

    return render(request,'signup.html',data)

def profile(request):
    if  not request.session.get('user_email'):
        return redirect('login')

    login_user=request.session.get('user_email')
    usr=Signup.objects.get(email=login_user)
    p=Profile.objects.get(user=usr)
    u = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)

    friends = p.friends.all()
    count=p.friends.count()


    context = {
        'u': u,
        'p':p,
        'count':count,

        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests
    }

    return render(request, 'userprofile.html', context)

def edit_profile(request):
    if  not request.session.get('user_email'):
        return redirect('login')

    login_user=request.session.get('user_email')
    usr=Signup.objects.get(email=login_user)
    pro=Profile.objects.get(user=usr)
    form=EditProfile(request.POST or None,request.FILES or None,instance=pro)

    if form.is_valid():
        form.save()



        return redirect('homepage')


    data={
        'form':form,
        'user':usr,

    }
    return render(request, 'editprofile.html', data)

def index(request):
    if request.session.get('user_email'):
        return redirect('homepage')

    return render(request,'index.html')

def home(request):
    if  not request.session.get('user_email'):
        return redirect('login')

    login_user = request.session.get('user_email')
    usr = Signup.objects.get(email=login_user)
    users_list = Profile.objects.exclude(user=usr)
    image=Profile.objects.get(user=usr)
    search_term = None
    if 'search' in request.GET:
        search_box=request.GET.get('search')

        search_term=Signup.objects.filter(username__icontains=search_box)

    data={
        'user':usr,
        'user_list':users_list,
        'search_term':search_term,
        'image':image
    }
    return render(request,'homepage.html',data)

def profile_view(request,id):
    if  not request.session.get('user_email'):
        return redirect('login')
    login_user = request.session.get('user_email')
    usr = Signup.objects.get(email=login_user)
    p = Profile.objects.filter(id=id).first()
    u = p.user
    button_status = 'none'
    if p not in usr.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(FriendRequest.objects.filter(
                from_user=usr).filter(to_user=p.user)) == 1:
            button_status = 'friend_request_sent'
    else:
        button_status='friends'

    context = {
        'u': u,
        'p':p,
        'button_status': button_status,
    }

    return render(request,'profile.html',context)


def send_friend_request(request, id):
    if  not request.session.get('user_email'):
        return redirect('login')
    login_user = request.session.get('user_email')
    usr = Signup.objects.get(email=login_user)
    to_user=Profile.objects.get(id=id)
    frequest,created=FriendRequest.objects.get_or_create(from_user=usr,to_user=to_user.user)
    return redirect('homepage')
def cancel_friend_request(request,id):
    if  not request.session.get('user_email'):
        return redirect('login')
    login_user = request.session.get('user_email')
    usr = Signup.objects.get(email=login_user)
    to_user = Profile.objects.get(id=id)
    frequest=FriendRequest.objects.filter(from_user=usr,to_user=to_user.user).first()
    frequest.delete()

    return redirect('homepage')



def accept_friend_request(request, id):
    if  not request.session.get('user_email'):
        return redirect('login')
    login_user = request.session.get('user_email')
    usr = Signup.objects.get(email=login_user)
    from_user=Profile.objects.filter(id=id).first()
    frequest=FriendRequest.objects.filter(from_user=from_user.user, to_user=usr).first()
    user1=frequest.to_user
    user2=from_user.user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    frequest.delete()
    return redirect('myprofile')


def ignore_friend_request(request, id):
    if  not request.session.get('user_email'):
        return redirect('login')
    login_user = request.session.get('user_email')
    usr = Signup.objects.get(email=login_user)
    from_user = Profile.objects.filter(id=id).first()
    frequest = FriendRequest.objects.filter(from_user=from_user.user, to_user=usr).first()
    frequest.delete()
    return redirect('myprofile')






