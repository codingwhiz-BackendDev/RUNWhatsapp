from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import myContact, Profile, Status, Message, Communities, Group_comment
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
# Create your views here.

@login_required(login_url='login')
def index(request): 
    profile = Profile.objects.get(username=request.user)
    user = User.objects.get(username=request.user)
    
    if request.method == 'POST':
        search = request.POST['search']
        result = myContact.objects.filter(Q(user=user)|Q(contact__icontains = search))
        
        return render(request, 'index.html', {'result':result})
    
    mycontact = myContact.objects.filter(user_phone_number= user)
 
    people_with_mycontact = myContact.objects.filter(phone_number = user) 
    all_contact = myContact.objects.all()
    
    
    context = {
        'mycontact':mycontact,
        'profile':profile,
        'people_with_mycontact':people_with_mycontact,
        'all_contact':all_contact,
        
    }
    
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        first_name = request.POST['username']
        username = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password'] 
        password2 = request.POST['password2'] 
        
        #The phone number is the username and the first_name is the html username
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Phone number Already exists')
                return redirect('register')
                
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Phone number Already exists')
                return redirect('register') 
                
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
                user.save()
                
                user_model = User.objects.get(first_name=first_name) 
                print(user_model)
                profile = Profile.objects.create(username=user_model,)
                profile.save()
                return redirect('login')
        else:
            return redirect('register')
            messages.info(request, 'Password does not match')
        
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['phone_number']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials are Invalid')
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_contact(request): 
    profile = Profile.objects.get(username=request.user)
    if request.method == 'POST':
        name = request.POST['username']
        first_name = request.POST['first_name'] 
        loggedInUser = request.POST['loggedInUser']
        loggedInUserNumber = request.POST['loggedInUserNumber']
        user = request.user
     
        
        if str(name) == str(user):
            messages.info(request, 'Can"t add yourself on WhatsApp')
            return redirect('add_contact')
        else: 
            if User.objects.filter(username=name).exists():
                if myContact.objects.filter(user_phone_number = loggedInUserNumber , phone_number = name).exists():
                    messages.info(request, 'Number is already in your contact')
                    return redirect('add_contact')
                else: 
                    # GET CONTACT PROFILE
                    contact_user =  User.objects.get(username=name) 
                    contact_profile = Profile.objects.get(username = contact_user) 
                    contacts = myContact.objects.create(user=loggedInUser, phone_number=name, contact=first_name, user_phone_number=loggedInUserNumber, image=contact_profile.image, bio=contact_profile.bio)
                    contacts.save()
                    
                    # CREATE CONTACT AT THE OTHER END
                    contact_user2 =  User.objects.get(username=loggedInUserNumber)
                    contact_profile2 = Profile.objects.get(username = contact_user2) 
                    contacts2 = myContact.objects.create(user=contact_profile2.first_name,contact=contact_profile2.first_name , phone_number=loggedInUserNumber, user_phone_number=name, image=contact_profile2.image, bio=contact_profile2.bio)
                    
                    contacts2.save()
                    return redirect('/')
            else: 
                messages.info(request, 'Number is not on WhatsApp')
                return redirect('add_contact')

         
    return render(request, 'add_contact.html', {'profile':profile})

@login_required(login_url='login')
def settings(request): 
    profile = Profile.objects.get(username=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = profile.image
            username = request.POST['username']
            first_name =  request.POST['first_name']
            bio = request.POST['bio']
            
            profile.image = image
            profile.usernames = User.objects.get(username=request.user)
            profile.username = profile.usernames
            profile.first_name = first_name 
            profile.bio = bio
            profile.save() 
             
            mycontact = myContact.objects.filter(phone_number=username)
            for contact in mycontact:
                print(contact)
                contact.image = image 
                contact.bio = bio
                contact.save()
                print(contact.image) 
            
            
        else:
            image = request.FILES.get('image')
            username = request.POST['username']
            first_name =  request.POST['first_name']
            bio = request.POST['bio'] 
            
            profile.image = image
            profile.usernames = User.objects.get(username=request.user)
            profile.username = profile.usernames
            profile.first_name = first_name 
            profile.bio = bio
            
            profile.save() 
             
            mycontact = myContact.objects.filter(phone_number=username)
            for contact in mycontact:
                print(contact)
                contact.image = image 
                contact.bio = bio
                contact.save()
                print(contact.image) 
                 
              
    return render(request, 'settings.html', {'profile': profile})

@login_required(login_url='login')
def chat(request, pk):
    get_user =  User.objects.get(username=pk)
    profile = Profile.objects.get(username=get_user)
    pk=pk 
 
    return render(request, 'chat.html', {'profile':profile, 'get_user':get_user,'pk':pk})

@login_required(login_url='login')
def send_message(request):
    if request.method == 'POST':
        sender = request.POST['sender']
        receiver = request.POST['receiver'] 
        message = request.POST['message'] 
        receiverId =  request.POST['receiverId']
        senderId =  request.POST['senderId']
        
        mycontact = myContact.objects.filter(Q(user_phone_number = receiver)|Q(phone_number = receiver)).exclude(~Q(user_phone_number=sender),~Q(phone_number=sender))
        
        print(mycontact)
        
        messages = Message.objects.create(sender=sender,receiverId=receiverId,senderId=senderId, receiver=receiver, message=message)
        message = messages.save() 
        
        
        
        for contact in mycontact:
            contact.last_message = str(messages)
            
            contact.save()
    return HttpResponse('Message sent')
 
@login_required(login_url='login')
def get_chat_message(request, pk):
    user = request.user
    messages = Message.objects.filter(Q(sender = pk)|Q(receiver = pk)).exclude(~Q(sender=user),~Q(receiver=user))
    return JsonResponse({'messages':list(messages.values())})

@login_required(login_url='login')
def status(request): 
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(username=request.user)
    user_status = Status.objects.all()
    user_contacts = myContact.objects.filter(Q(user_phone_number = user)| Q(phone_number = user))
    # print(user_contacts)
    
    for profiles in Status.objects.all():
        profiles = User.objects.get(username=profiles)
        status_profile = Profile.objects.get(username=profiles)
        status = Status.objects.filter(user=profiles)
        print(status)
        # print(status_profile.first_name)
                
            
                
        
    return render(request, 'status.html', {'profile':profile, 'user_status':user_status})


@login_required(login_url='login')
def write_status(request):
    profile = Profile.objects.get(username=request.user)
    if request.method == 'POST': 
        user = User.objects.get(username=request.user)
        text = request.POST['text']
        status = Status.objects.create(user=user, text=text)
        status.save()
        return redirect('status')
    return render(request, 'write_status.html', {'profile':profile})

@login_required(login_url='login')
def post_status(request):
    profile = Profile.objects.get(username=request.user)
    if request.method == 'POST': 
        user = User.objects.get(username=request.user)
        text = request.POST['text']
        image = request.FILES.get('image')
        video = request.FILES.get('video') 
        status = Status.objects.create(user=user, text=text, image=image, video=video)
        status.save()
        
        return redirect('status')
    return render(request, 'post_status.html', {'profile':profile})

@login_required(login_url='login')
def delete_post(request, pk):
    post = Status.objects.get(id=pk)
    post.delete()
    return redirect('status')

@login_required(login_url='login')
def contact_profile(request,pk):
    profile = Profile.objects.get(username=request.user)
    user = User.objects.get(username=pk)
    contact = Profile.objects.get(username=user)
    mycontact = myContact.objects.get(user_phone_number=request.user, phone_number=pk) 
    
    if request.method == 'POST':
        contact_name =  request.POST['contact_name']
        mycontact.contact = contact_name
        mycontact.save()
        print(contact_name)
    return render(request, 'contact_profile.html', {'profile':profile,'contact':contact, 'mycontact':mycontact})


@login_required(login_url='login')
def communities(request): 
    profile = Profile.objects.get(username=request.user)
    group = Group.objects.all()
    communities = Communities.objects.all()
    if request.method == 'POST':
        group_name = request.POST['group_name']
        group_admin = request.POST['group_admin']
        group_pic = request.FILES.get('group_pic')
        
        if Group.objects.filter(name=group_name).exists(): 
            messages.info(request, 'Group Name Already Exists')
            return render(request, 'communities.html',{'profile':profile, 'communities':communities} )
        else:
            group = Group.objects.create(name=group_name) 
            group.save()
            group = Group.objects.get(name=group_name) 
            group_profile = Communities.objects.create(group_name=group, group_admin=group_admin, group_pic= group_pic)
            group_profile.save()
            return render(request, 'communities.html',{'profile':profile,'communities':communities} )
    else:
        return render(request, 'communities.html',{'profile':profile, 'communities':communities} )

def view_community(request,pk):
    profile = Profile.objects.get(username=request.user)
    pk=pk
    return render(request, 'community.html', {'profile':profile, 'pk':pk})


@login_required(login_url='login') 
def group_chat_comment(request):
    if request.method == 'POST':
        sender = request.POST['sender'] 
        comment = request.POST['comment']
        group_name = request.POST['group_name']
        profileimage = request.POST['profile_image']
        
        comment = Group_comment.objects.create(sender=sender,comment=comment,profileimage=profileimage,group_name=group_name) 
        comment.save()
    return HttpResponse('s')