from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User,Group
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.contrib.auth.models import User
import datetime

"""class Bug(models.Model):
    name = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    done = models.BooleanField(default=False)
    fixed = models.BooleanField(default=False)
    fixed_date = models.DateTimeField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)

class BugAdmin(admin.ModelAdmin):
    list_display = ["name", "priority", "difficulty", "created", "done"]
    search_fields = ["name"]

admin.site.register(Bug, BugAdmin)"""

#class List(models.Model):
#    name = models.CharField(max_length=60)
    
class DateTime(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return unicode(self.datetime.strftime("%b, %d, %Y, %I,:%M %p"))

class Bug(models.Model):
    name = models.CharField(max_length=140)
    priority = models.IntegerField(default=0,max_length=3)
    difficulty = models.IntegerField(default=0)
    created = models.ForeignKey(DateTime)
    #add_date = models.DateTimeField(auto_now_add=True)
    fixed = models.BooleanField(default=False)
    fixed_date = models.DateTimeField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    progress = models.IntegerField(default=0)

    def progress_(self):
       # return "<div style='width: 100px; border: 1px solid #ccc;'>" + "<div style='height: 4px; width: %dpx; background: #555;'></div></div>" % self.progress
        return """
        <div id="progress_cont_%s" class="progress_cont">
            <div id="progress_btns_%s" class="progress_btns">
                <ul>
                    <li>10</li>
                    <li>20</li>
                    <li>30</li>
                    <li>40</li>
                    <li>50</li>
                    <li>60</li>
                    <li>70</li>
                    <li>80</li>
                    <li>90</li>
                    <li>100</li>
                </ul>
            </div>
            <div id="progress_on_%s" class="progress_on">&nbsp;</div>
            <div id="progress_%s" style="visibility: hidden"></div>
        </div>
        """ % (self.pk, self.pk, self.pk, self.pk)
    progress_.allow_tags = True
    
    def mark_done(self):
        return "<a href='%s'>Done</a>" % reverse('bug-list-master.buglist.views.mark_done', args=[self.pk])
    mark_done.allow_tags = True


class BugAdmin(admin.ModelAdmin):
    list_display = ["name", "priority", "difficulty", "created", "fixed", "fixed_date", "notes", "user"]
    search_fields = ["name"]

class BugInline(admin.TabularInline):
    model = Bug

class DateAdmin(admin.ModelAdmin):
    list_display = ["datetime"]
    inlines = [BugInline]
    def response_add(self, request, obj, post_url_continue='../%s/'):
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = "Item(s) were added successfully."
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse(
                '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");'
                '</script>' % (escape(pk_value), escape(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            return HttpResponseRedirect(reverse("admin:buglist_bug_changelist")) 
        for bug in Bug.objects.filter(created=obj):
            if not bug.user:
                bug.user = request.user
                bug.save()
        return HttpResponseRedirect(reverse("admin:buglist_bug_changelist"))
    
    def done_(self):
        if self.done:
            btn = "<div id='done_%s'><img class='btn' src='%smysite/media/icon-on.png' /></div>"
        else:
            btn = "<div id='done_%s'><img class='btn' src='%smysite/media/icon-off.png' /></div>"
        return btn % (self.pk, MEDIA_URL)
    done_.allow_tags = True
    done_.admin_order_field = "done"



admin.site.register(Bug, BugAdmin)
admin.site.register(DateTime, DateAdmin)
