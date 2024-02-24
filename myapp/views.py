
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import LongToShort


def task(request):
    context={
        "submitted": False,
        'error':False
    }
    print(request.method)
    if request.method == 'POST':

        data = request.POST

        long_url = data['longurl']
        name = data['custom_name']
        context["long_url"] = long_url
        context["short_url"] = request.build_absolute_uri() + name
        try:
            obj = LongToShort(long_url=long_url, short_url=name)
            obj.save()
            context['date'] = obj.date
            context['clicks'] = obj.clicks
            context["submitted"] = True
         

        except:
             context['error']=True

    else:
        print("error")

    return render(request, 'index.html', context)

def redirect_url(request,short_url):

    row=LongToShort.objects.filter(short_url=short_url)
    if len(row)==0:
        return HttpResponse('error')
    obj=row[0]
    long_url=obj.long_url
    obj.clicks+=1
    obj.save()


    return redirect(long_url)

def analytic(request):
    row=LongToShort.objects.all().order_by('-clicks')
    # print(row)

    list={'value':row}
    return render(request,'all_analytics.html',list)
# Create your views here.