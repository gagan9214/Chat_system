from django.shortcuts import render,HttpResponse,redirect
from chatbot.models import User,Chat
from django.contrib import messages
import hashlib
from django.utils import timezone

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def loginPage(request):
    if request.method=='POST':
        uname= request.POST.get('username')
        password= hash_password(request.POST.get('pass1'))
        try:
            user = User.objects.get(username=uname, password=password)
            request.session['user_id']=user.id
            return redirect('home')
        except User.DoesNotExist:
            messages.error(request, 'Invalid Username or Password')
            
        
    return render(request,'login.html')


def signupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        
        if not pass1 or not pass2:
            messages.error(request, 'Both password fields are required.')
            return render(request, 'signup.html')
        if pass1!=pass2:
            messages.error(request,"Password do not match")
            return render(request,'signup.html')
        
        if User.objects.filter(username=uname).exists():
            messages.error(request,'Username already exists!')
            return render(request,'signup.html')
        
        hashed_password=hash_password(pass1)
        new_user=User(username=uname ,password=hashed_password)
        new_user.save()
        messages.success(request,'user created successfully!')
        return redirect('loginPage')
    return render(request,'signup.html')


def chat(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('loginPage')

    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        
        # Check if the user has at least 100 tokens
        if user.tokens < 100:
            messages.error(request, 'Insufficient tokens. You need at least 100 tokens to chat.')
            return render(request, 'chat.html', {'user': user})

        # Deduct 100 tokens
        user.tokens -= 100
        user.save()
        
        # Generate response and save chat
        response = generate_response(message)  # Placeholder for response generation logic
        Chat.objects.create(user=user, message=message, response=response, timestamp=timezone.now())
        
    chats = Chat.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'chat.html', {'user': user, 'chats': chats})


def generate_response(message):
    # Placeholder function for generating responses
    return "This is a sample response."

def home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('loginPage')

    user = User.objects.get(id=user_id)
    return render(request, 'home.html', {'user': user})

def logoutUser(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('loginPage')