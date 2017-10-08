from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.template import loader
from PIL import Image
from webapp import settings
from django.utils import timezone
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageUpload
from .models import Post

#This is a function that processes the data and passes it to the HTML files for the viewer's page along with user's page
def home(request):
    if request.user.is_authenticated:   #if user is authenticated he stays in the user view
        if request.method == 'POST':
            form = ImageUpload(request.POST,request.FILES)
            if form.is_valid():
                updated_post = Post(image_field=request.FILES['image_field'],user=request.user,caption=form.cleaned_data['caption'],pub_date=timezone.datetime.now())
                updated_post.save()
                try:
                    check_image = Image.open(settings.MEDIA_ROOT +'/'+str(updated_post.image_field))
                    if check_image.format not in ('GIF', 'PNG', 'JPEG'):
                        Omit(updated_post.id)
                except Exception:
                    Omit(updated_post.id)
                return HttpResponseRedirect('#')
        else:
            form=ImageUpload()
        uploads = Post.objects.filter(user=request.user).order_by('-pub_date')
        paginator = Paginator(uploads, 10) #Displays only 10 images per page
        page = request.GET.get('page')
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)

        template = loader.get_template('instagram/homepage.html')
        context = {
            'uploads': photos,
            'username':request.user,
            'form':form
        }
        return HttpResponse(template.render(context, request))
    
    #if user is not authenticated then he is directed to the only viewer page. 

    else:   
        uploads = Post.objects.order_by('-pub_date')
        paginator = Paginator(uploads, 10) 
        page = request.GET.get('page')
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)
        template = loader.get_template('instagram/homepage.html') 
        context = {
            'uploads': photos,
            'username':request.user,
        }
        return HttpResponse(template.render(context, request))

#this is the function that processes data and passes it on to the User View HTML file 
def homepage(request):
    if request.user.is_authenticated: #if user is authenticated he stays in the user view
        if request.method == 'POST':
            form = ImageUpload(request.POST,request.FILES)
            if form.is_valid():
                updated_post = Post(image_field=request.FILES['image_field'],user=request.user,caption=form.cleaned_data['caption'],pub_date=timezone.datetime.now())
                updated_post.save()
                try:
                    check_image = Image.open(settings.MEDIA_ROOT +'/'+str(updated_post.image_field))
                    if check_image.format not in ('GIF', 'PNG', 'JPEG'):
                        Omit(updated_post.id)
                except Exception:
                    Omit(updated_post.id)
                return HttpResponseRedirect('#')
        else:
            form=ImageUpload()
        uploads = Post.objects.filter(user=request.user).order_by('-pub_date')
        paginator = Paginator(uploads, 10) #Displays only 10 images per page
        page = request.GET.get('page')
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)

        template = loader.get_template('instagram/homepage.html') 
        context = {
            'uploads': photos,
            'username':request.user,
            'form':form
        }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('instagram/login.html')
        return HttpResponse(template.render(None, request))


#this is a signup function for the user to signup for an account
def signup(request):
    if request.method =='POST':
        if request.POST['password1'] == request.POST['password2']: #processes only if both passwords are the same
            try:
                user= User.objects.get(username=request.POST['username'])
                return render(request, 'instagram/signup.html',{'error':'Username has already been taken'}) #sends error if username already exists
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password= request.POST['password1'])
                login(request, user)
                return render(request, 'instagram/login.html')
        else:
            return render(request, 'instagram/signup.html',{'error':'Passwords didn\'t match'}) #otherwise sends an error message 
    else:
        return render(request, 'instagram/signup.html')


#this is a login function for the user to login to his account

def login1(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/instagram')
        else:
            return render(request, 'instagram/login.html',{'error':'Username and Password didn \'t match'}) #sends error if username and password don't match
    else:
        return render(request, 'instagram/login.html')

#this is a logout function for the user to logout of his account

def logout1(request):
    if request.user.is_authenticated:
	    logout(request)
    return HttpResponseRedirect('/')

#This is a function that edits the caption of the image
def edit(request): 
	caption_update = request.GET.get('caption')
	fetch=Post.objects.filter(id=request.GET.get('id')).update(caption=caption_update)
	return HttpResponseRedirect('/instagram')

#this is a delete function that deletes a photo 

def delete(request):
	fetch=Post.objects.filter(id=request.GET.get('id'))
	deleteFile(settings.MEDIA_ROOT +'/'+str(fetch[0].image_field))
	fetch.delete()
	return HttpResponseRedirect('/instagram')

#this function deletes a photo from the database using the ID.
def Omit(pid):
	fetch=Post.objects.filter(id=pid)
	deleteFile(settings.MEDIA_ROOT +'/'+str(fetch[0].image_field))
	fetch.delete()

#photo deleted from the filesystem
def deleteFile(filename):
	try:
		os.remove(filename)
	except OSError:
		print('couldnt delete file')



