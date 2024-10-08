from typing import Dict, Any

from django.shortcuts import render
from . models import *
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.
def index(request):
    sdata=slider.objects.all().order_by('-id')[0:6]
    cdata=category.objects.all().order_by('-id')[0:12]
    cdata1=category.objects.all().order_by('-id')[0:25]
    ndata=mynews.objects.all().order_by('-id')[0:12]
    vdata=vnews.objects.all().order_by('-id')[0:12]
    citydata = city.objects.all().order_by('-id')[0:24]
    jobdata=jobs.objects.all().order_by('-id')[0:10]
    mydict = {"sd": sdata,"catdata": cdata,"ndata":ndata,"vdata":vdata,"cdata":citydata,"cdata1":cdata1,"jobdata":jobdata}
    return render(request,'user/index.html',mydict)

def about(request):
    return  render(request,template_name='user/about.html')

def contact(request):
    if request.method=="POST":
        a=request.POST.get('name')
        b=request.POST.get('email')
        c=request.POST.get('mobile')
        d=request.POST.get('msg')
        contactus(name=a,email=b,mobile=c,message=d).save()
        return HttpResponse("<script>alert('Thanks for contacting with us..');location.href='/user/contact/'</script>")
    return  render(request,template_name='user/contact.html')

def myjobs(request):
    x=jobs.objects.all().order_by('-id')
    md={"jdata":x}
    return render(request,'user/jobs.html',context=md)

def videos(request):
    ctid=request.GET.get('cityid')
    catid = request.GET.get('catid')
    cdata=category.objects.all().order_by('-id')
    ctdata=city.objects.all().order_by('-id')
    vdata=vnews.objects.all().order_by('-id')
    if ctid is not None:
        vdata=vnews.objects.filter(city=ctid)
    elif catid is not None:
        vdata=vnews.objects.filter(vcategory=catid)
    else:
        vdata=vnews.objects.all().order_by('-id')
    md={"cdata":cdata,"ctdata":ctdata,"vdata":vdata,}
    return render(request,'user/videos.html',md)

def news(request):
    sdata =request.GET.get('search')
    cid=request.GET.get('x')#2
    ctid=request.GET.get('y')
    citydata=city.objects.all().order_by('-id')
    cdata=category.objects.all().order_by('-id')
    if cid is not None:
        newsdata=mynews.objects.filter(news_category=cid)
    elif ctid is not None:
        newsdata=mynews.objects.filter(news_city=ctid)
    elif sdata is not None:
        newsdata=mynews.objects.filter(Q(news_headlines__icontains=sdata) | Q(news_discription__icontains=sdata))
    else:
        newsdata=mynews.objects.all().order_by('-id')

    md={"cdata":citydata,"catdata":cdata,"ndata":newsdata}
    return  render(request,'user/news.html',md)

def viewnews(request):
    vnid = request.GET.get('xyz')
    nid = request.GET.get('msg')
    ndata = mynews.objects.all().filter(id=nid)
    vdata = vnews.objects.filter(id=vnid)
    md = {"newsdata": ndata, "vdata": vdata}
    return render(request, 'user/viewnews.html', md)


def myprofile(request):
    return render(request, 'user/myprofile.html')