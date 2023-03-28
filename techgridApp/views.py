from django.shortcuts import render,redirect
from passlib.hash import sha512_crypt as sha512
from .models import User, Surveys, Accessable,Responses
import random
import string
from django.contrib import messages
from django.http import  JsonResponse
from django.core.mail import send_mail
import os
from dotenv import load_dotenv
load_dotenv()

otp=""
# Create your views here.
def index(request):
    if 'techgridPrivateKey' not in request.session:
        return render(request,'index.html',{'username':'Login'})
    else:
        if User.objects.filter(private_key=request.session['techgridPrivateKey']).exists():
            user = User.objects.get(private_key=request.session['techgridPrivateKey'])
            name = user.name
            return render(request,'index.html',{'username':name})
        else:
            return render(request,'index.html',{'username':'Login'})
    # # Checks if private key element is present in request.session
    # if 'techgridPrivateKey' not in request.session:
    #     return redirect('login')
    # else:
    #     # If present now checks if private key is present in database
    #     if User.objects.filter(private_key=request.session['techgridPrivateKey']).exists():
    #         # If yes User is logged in
    #         return redirect('home')
    #     else:
    #         return redirect('login')

def home(request):
    user = User.objects.get(private_key=request.session['techgridPrivateKey'])
    email = user.email
    name=user.name
    survey = Surveys.objects.filter(email=email)
    return render(request,'home.html',{'forms':survey,'username':name})

def login(request):
    if 'techgridPrivateKey' not in request.session:
        return render(request,'login.html')
    else:
        if User.objects.filter(private_key=request.session['techgridPrivateKey']).exists():
            user = User.objects.get(private_key=request.session['techgridPrivateKey'])
            name = user.name
            return redirect('home')
        else:
            return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def signupuser(request):
    username=request.POST['name']
    email=request.POST['email']
    email =email.lower()
    pwd=request.POST['password']
    cpwd = request.POST['cpassword']
    if pwd != cpwd:
        messages.error(request, 'Passwords do not match')
        return redirect('signup')

    if User.objects.filter(email=email).exists():
            messages.info(request,'User Already Exists !')
            return redirect('signup')
    else:
            global otp
            otp=''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
            message="OTP : "+otp + "\n If you didn't did this please ignore this"
            reciever=[str(email)]
            subject="OTP for Persev Forms"
            send_mail(subject,message,os.environ.get('EMAIL'),reciever)
            return render(request,'otp.html',{'username':username,'email':email,'pwd':pwd})

def otpverifcation(request):
    otp_provided=request.POST['otp']
    username=request.POST['username']
    email=request.POST['email']
    pwd=request.POST['password']
    global otp
    if otp == otp_provided:
        print(pwd)
        pwd=sha512.hash(pwd, rounds=5000,salt=os.environ.get('SALT'))
        email=email.lower()
        User.objects.create(name=username,password=pwd,email=email,private_key="nill")
        messages.info(request,'Sign Up Successful Please Login')
        return redirect('login')
    else :
        messages.info(request,'Wrong OTP !')
        return redirect('signup')

def loginuser(request):
    email=request.POST['email']
    pwd1=request.POST['password']
    email=email.lower()
    if User.objects.filter(email=email).exists():
        user=User.objects.get(email=email)
        password_verify=user.password
        
        pwd1=sha512.hash(pwd1, rounds=5000,salt=os.environ.get('SALT'))
        
        if pwd1==password_verify:
            privatekey=''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30))
            request.session['techgridPrivateKey']=privatekey
            user.private_key=privatekey
            user.save()
            return redirect('home')
        else:
            messages.info(request,'Wrong Password !')
            return redirect('login')
    else:
        messages.info(request,'User Does Not Exists !')
        return redirect('login')

def newform(request):
    user = User.objects.get(private_key=request.session['techgridPrivateKey'])
    email = user.email
    name=user.name
    return render(request, 'newform.html',{'username':name , 'email':email})

def sendsurveyback(request):
    surveyname=request.GET['surveyname']
    surveydesc=request.GET['surveydescription']
    json=request.GET['json']
    user = User.objects.get(private_key=request.session['techgridPrivateKey'])
    email = user.email
    name = user.name
    surveyid=''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30))
    Surveys.objects.create(surveyid=surveyid,name=name,surveyname=surveyname,description=surveydesc,json=json,email=email)
    survey = Surveys.objects.get(surveyid=surveyid)
    Accessable.objects.create(surveyid = survey.id,emailList="",allowedbyall=True)
    return JsonResponse('home', safe=False)


def opensurvey(request):
    surveyid=request.GET['surveyid']
    user = User.objects.get(private_key=request.session['techgridPrivateKey'])
    email = user.email
    username = user.name
    survey = Surveys.objects.get(id = surveyid)
    data = str(survey.json)
    if Accessable.objects.filter(surveyid=surveyid).exists():
        allowed = Accessable.objects.get(surveyid=surveyid)
        emailList = allowed.emailList
        emailList = emailList[:-1]
        emaillist = emailList.split(",")
        return render(request,'opensurvey.html',{'survey':survey,'username':username,'data':data,'emaillist':emaillist})
    else:
        return render(request,'opensurvey.html',{'survey':survey,'username':username,'data':data})

 

def updatesurvey(request):
    surveyname=request.GET['surveyname']
    surveydesc=request.GET['surveydescription']
    json=request.GET['json']
    surveyid = request.GET['surveyid']
    user = User.objects.get(private_key=request.session['techgridPrivateKey'])
    email = user.email
    name = user.name
    # surveyid=''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30))
    Surveys.objects.filter(id=surveyid).update(name=name,surveyname=surveyname,description=surveydesc,json=json,email=email)
    return JsonResponse('home', safe=False)

def deletesurvey(request):
    surveyid = request.GET['surveyid']
    Surveys.objects.get(id=surveyid).delete()
    return JsonResponse('home', safe=False)

def logout(request):
    del request.session['techgridPrivateKey']
    return redirect('login')

def responses(request):
    responses = Responses.objects.filter(surveyid = request.GET['surveyid'])
    responses_len = len(responses)
    return render(request,'responses.html',{'surveyid':request.GET['surveyid'],'survey':Surveys.objects.get(id = request.GET['surveyid']),'responses':responses,'responses_len':responses_len})

def sendshareinfoback(request):
    surveyid=request.GET['surveyid']
    emaillist=request.GET['emaillist']
    allowed = request.GET['allowed']
    limit_to_one = request.GET['limit_to_one']
    anonymous_or_not = request.GET['anonymous_or_not']
    thankyou_or_not = request.GET['thankyou_or_not']
    thankyou_message = request.GET['thankyou_message']

    if limit_to_one == "true":
        limit_to_one = True
    else:
        limit_to_one = False

    if anonymous_or_not == "true":
        anonymous_or_not = True
    else:
        anonymous_or_not = False

    if thankyou_or_not == "true":
        thankyou_or_not = True
    else:
        thankyou_or_not = False
        
    if Accessable.objects.filter(surveyid=surveyid).exists():
        Accessable.objects.filter(surveyid=surveyid).delete()

    if allowed == 'true':
        Accessable.objects.create(surveyid=surveyid,emailList=emaillist,allowedbyall = True,limit_to_one=limit_to_one,anonymous_or_not=anonymous_or_not,thankyou_or_not=thankyou_or_not,thankyou_message=thankyou_message)
    else:
        Accessable.objects.create(surveyid=surveyid,emailList=emaillist,allowedbyall = False,limit_to_one=limit_to_one,anonymous_or_not=anonymous_or_not,thankyou_or_not=thankyou_or_not,thankyou_message=thankyou_message)
    return JsonResponse('home', safe=False)
    
def takesurvey(request,surveyid):
    # Check if user is allowed if not then login page and see a way to come back to this page
    survey = Surveys.objects.get(id = surveyid)
    # After logged in get user email too 
    return render(request,'takesurvey.html',{'surveyid':surveyid,'survey':survey})

def contact(request):
    return render(request,'contact.html')

def settings(request):
    surveyid = request.GET['surveyid']
    accessable = Accessable.objects.get(surveyid=surveyid)
    emails = accessable.emailList.split(",")
    survey = Surveys.objects.get(id = surveyid)
    emails = emails[:-1]
    aon = accessable.anonymous_or_not
    lon = accessable.limit_to_one
    ton = accessable.thankyou_or_not
    tmsg = accessable.thankyou_message
    aba = accessable.allowedbyall
    return render(request,'settings.html',{'aon':aon,'survey':survey,'surveyid':surveyid,'accessable':emails,'aba':aba,'lon':lon,'ton':ton,'tmsg':tmsg})

def send_survey_settings_back(request):
    surveyid = request.GET['surveyid']
    shareable = request.GET['shareable']
    emaillist = request.GET['emaillist']
    
    anonymous_or_not = request.GET['anonymous_or_not']
    thankyou_or_not = request.GET['thankyou_or_not']
    thankyou_message = request.GET['thankyou_message']
    limit_to_one = request.GET['limit_to_one']

    if limit_to_one == "true":
        limit_to_one = True
    else:
        limit_to_one = False

    if anonymous_or_not == "true":
        anonymous_or_not = True
    else:
        anonymous_or_not = False

    if thankyou_or_not == "true":
        thankyou_or_not = True
    else:
        thankyou_or_not = False
    if shareable == "yes":
        Accessable.objects.filter(surveyid=surveyid).update(emailList=emaillist,allowedbyall=True,limit_to_one = limit_to_one,anonymous_or_not=anonymous_or_not,thankyou_or_not=thankyou_or_not,thankyou_message=thankyou_message)
    else:
        Accessable.objects.filter(surveyid=surveyid).update(emailList=emaillist,allowedbyall=False,limit_to_one = limit_to_one,anonymous_or_not=anonymous_or_not,thankyou_or_not=thankyou_or_not,thankyou_message=thankyou_message)
    return redirect('login')

def take_survey(request):
    surveyid = request.GET['surveyid']
    survey = Surveys.objects.get(id = surveyid)
    return render(request,'take_survey.html',{'surveyid':surveyid,'survey':survey})





