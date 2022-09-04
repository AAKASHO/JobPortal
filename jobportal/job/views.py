from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
# Create your views here.
def index(request):
    return render(request,'index.html')
def admin_login(request):
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
                 error="yes"
    d={'error':error}
    return render(request,'admin_login.html',d)
def user_login(request):
    error=""
    if request.method == "POST":
        u=request.POST['uname'];
        p=request.POST['pwd'];
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1=StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request,'user_login.html',d)
def recruiter_login(request):
    error=""
    if request.method == "POST":
        u=request.POST['uname'];
        p=request.POST['pwd'];
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1=Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status!="pending":
                    login(request,user)
                    error="no"
                else:
                    error="not"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request,'recruiter_login.html',d)
def recruiter_signup(request):
    error=""
    if(request.method=='POST'):
        f=request.POST['fname']
        l=request.POST['lname']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        comp=request.POST['company']
        try:
            user=User.objects.create_user(first_name=f,username=e,password=p,last_name=l)
            Recruiter.objects.create(user=user,mobile=con,gender=gen,company=comp,type="recruiter",status="pending")
            error="no"
        except:
            error="yes"
    d={'error':error}

    return render(request,'recruiter_signup.html',d)
def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    error=""
    if(request.method=='POST'):
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        student.user.first_name=f
        student.user.last_name=l
        student.mobile=con

        try:
            student.save()
            error="no"
        except:
            error="yes"

    d={'student':student,'error':error}
    return render(request,'user_home.html',d)
def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request,'admin_home.html')

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    error=""
    if(request.method=='POST'):
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        recruiter.user.first_name=f
        recruiter.user.last_name=l
        recruiter.mobile=con

        try:
            recruiter.save()
            error="no"
        except:
            error="yes"

    d={'recruiter':recruiter,'error':error}
    return render(request,'recruiter_home.html',d)


def Logout(request):
    logout(request)
    return render(request,'index.html')
def user_signup(request):
    error=""
    if(request.method=='POST'):
        f=request.POST['fname']
        l=request.POST['lname']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        try:
            user=User.objects.create_user(first_name=f,username=e,password=p,last_name=l)
            StudentUser.objects.create(user=user,mobile=con,type="student")
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'user_signup.html',d)

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request,'view_users.html',d)

def delete_users(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student=StudentUser.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def delete_recruiters(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter=Recruiter.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')

def delete_job(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    job=Job.objects.get(id=pid)
    job.delete()
    return redirect('job_list')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='pending')
    d={'data':data}
    return render(request,'recruiter_pending.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter=Recruiter.objects.get(id=pid)
    if request.method =="POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    d={'recruiter':recruiter,'error':error}
    return render(request,'change_status.html',d)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Accept')
    d={'data':data}
    return render(request,'recruiter_accepted.html',d)

def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Reject')
    d={'data':data}
    return render(request,'recruiter_accepted.html',d)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request,'recruiter_all.html',d)

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    if request.method =="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_passwordadmin.html',d)

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method =="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_passworduser.html',d)

def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method =="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_passwordrecruiter.html',d)


def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if(request.method=='POST'):
        jt=request.POST['jobtitle']
        sd=request.POST['startdate']
        ed=request.POST['enddate']
        sal=request.POST['salary']
        exp=request.POST['experience']
        loc=request.POST['location']
        skills=request.POST['skills']
        des=request.POST['description']
        user=request.user
        recruiter= Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,start_date=sd,end_date=ed,title=jt,salary=sal,description=des,experience=exp,location=loc,skills=skills,creationdate=date.today())
            error="no"
        except:
            error="yes"
    d={'error':error}

    return render(request,'add_job.html',d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter= Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request,'job_list.html',d)

def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job=Job.objects.get(id=pid)
    if(request.method=='POST'):
        jt=request.POST['jobtitle']
        sd=request.POST['startdate']
        ed=request.POST['enddate']
        sal=request.POST['salary']
        exp=request.POST['experience']
        loc=request.POST['location']
        skills=request.POST['skills']
        des=request.POST['description']
        job.title=jt
        job.salary=sal
        job.experience=exp
        job.location=loc
        job.skills=skills
        job.description=des
        try:
            job.save()
            error="no"
        except:
            error="yes"
        if sd:
            try:
                job.start_date=sd
                job.save()
            except:
                pass
        else:
            pass
        if ed:
            try:
                job.end_date=ed
                job.save()
            except:
                pass
        else:
            pass

    d={'error':error,'job':job}

    return render(request,'edit_jobdetail.html',d)

def latest_jobs(request):
    job=Job.objects.all().order_by('-start_date')
    d={'job':job}
    return render(request,'latest_jobs.html',d)

def user_latestjobs(request):
    job=Job.objects.all().order_by('-start_date')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)

    d={'job':job,'li':li}
    return render(request,'user_latestjobs.html',d)

def job_detail(request,pid):
    job=Job.objects.get(id=pid)

    d={'job':job}
    return render(request,'job_detail.html',d)

def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    user=request.user
    student=StudentUser.objects.get(user=user)
    job=Job.objects.get(id=pid)

    date1=date.today()
    if job.end_date<date1:
        error="close"
    elif job.start_date>date1:
        error="notopen"
    else:
        if request.method == 'POST':
            r=request.FILES['resume']
            Apply.objects.create(student=student,resume=r,applydate=date.today(),job=job)
            error="done"

    d={'error':error}



    return render(request,'applyforjob.html',d)


def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    data=job=Apply.objects.all()

    d={'data':data}



    return render(request,'applied_candidatelist.html',d)