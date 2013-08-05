from django.template import Template, Context
from django.http import Http404, HttpResponse
from buglist.models import *
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
import datetime


def current_datetime(request):
    now = datetime.datetime.now()
    # this is bad because it doesn't account for missing files                  
    fp = open('/Users/Michael/Projects/bug-list-master/mysite/templates/buglist\
/current.html')
    t = Template(fp.read())
    fp.close()
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)

def hours_ahead(request,offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset,\
 dt)
    return HttpResponse(html)

def bug_list(request):
    html = "<html><body><h1>Bug List</h1></body></html>"
    return HttpResponse(html)

def hello(request):
    return HttpResponse("Hello World")

def landing(request):
    return HttpResponse("Landing Page")

@staff_member_required
def mark_done(request, pk):
    bug = Bug.objects.get(pk=pk)
    bug.done =True
    bug.save()
    return HttpResponseRedirect(reverse("admin:buglist_bug_changelist"))

@staff_member_required
def bug_action(request, action, pk):
    if action == "done":
        bug = Bug.objects.get(pk=pk)
        bug.done = True
        bug.savev()
    elif action == "onhold":
        bug = Bug.objects.get(pk=pk)
        if bug.onhold: bug.onhold = False
        else: bug.onhold = True
        bug.save()
    elif action == "delete":
        Bug.objects.filter(pk=pk).delete()

    return HttpResponseRedirect(reverse("admin:buglist_bug_changelist"))

@staff_member_required
def onhold_done(request, mode, action, pk):
    bug = Bug.objects.get(pk=pk)

    if action == "on":
        if mode == "done": bug.done = True
        elif mode == "onhold": bug.onhold = True
    elif action == "off":
        if mode == "done": bug.done = False
        elif mode == "onhold": bug.onhold = False

    bug.save()
    return HttpResponse('')

def progress(request,pk):
    p = request.POST
    if "progress" in p:
        bug = Bug.objects.get(pk=pk)
        bug.progress = int(p["progress"])
        bug.save()
    return HttpResponse('')
