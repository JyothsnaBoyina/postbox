from django.shortcuts import  render_to_response
from django.contrib import auth
from django.core.context_processors import  csrf
from django.template import RequestContext
from postbox.forms import *
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from postbox.models import *
from django.http import *
from postbox.custom_storages import *
from django.contrib.auth.forms import UserCreationForm
from django.template import loader
import pytz


class Newsfeed(ListView):
    model=Posts
    context_object_name = 'news'
    template_name = 'postbox/newsfeed.html'

    def get_context_data(self, **kwargs):
        context = super(Newsfeed, self).get_context_data(**kwargs)
        context['posts'] = Posts.objects.all().order_by('-p_date')
        context['post'] = Posts.objects.all().order_by('-p_date')
        uname=self.request._cached_user.username
        u = User.objects.filter(username=uname).values('id')
        context['categories'] = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['p']=u[0].values()[0]
        context['full_name'] = uname
        return context

class Profile(ListView):
    model=Posts
    context_object_name = 'user'
    template_name = 'postbox/user.html'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        uname=self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        context['posts'] = Posts.objects.filter(owner_id=u).order_by('-p_date')
        context['post'] = Posts.objects.filter(owner_id=u).order_by('-p_date')
        context['categories'] = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['full_name']=self.kwargs['uname']
        return context

class PostList(ListView):
    model = Posts
    context_object_name = 'post_list'
    template_name = 'postbox/Posts_list.html'

    def get_context_data(self,**kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        cid = self.kwargs.get('cid')
        u = User.objects.filter(username=uname).values('id')
        context['categories'] = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['full_name'] = self.kwargs['uname']
        context['cat'] = int(cid)
        context['post'] = Posts.objects.filter(cid_id=self.kwargs['cid']).order_by('-p_date')
        context['posts'] = Posts.objects.filter(cid_id=self.kwargs['cid']).order_by('-p_date')
        context['categories1'] = Categories.objects.filter(owner_id=u).order_by('-c_date')
        return context

class CreateCat(ListView):
    model = Categories
    context_object_name = 'cform'
    template_name = 'postbox/Categories_form.html'

    def get_context_data(self,**kwargs):
        context = super(CreateCat, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['form']=CategoryForm()
        context['categories']= categories
        context['full_name']=uname
        return context

    def post(self,*args,**kwargs):
        uname=self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context = RequestContext(self.request)

        if self.request.method == 'POST':
            form = CategoryForm(self.request.POST)
            if form.is_valid():
                try:
                    cat_form = form.save(commit=False)
                    p = u[0].values()
                    cat_form.owner_id = p[0]
                    cat_form.save()
                    return HttpResponseRedirect('/postbox/' + uname + '/profile/')
                except Exception as e:
                    mesg = 'save_invalid'
                    return render_to_response('postbox/Categories_form.html',
                                              {"mesg": mesg, 'form': form, 'full_name': uname,
                                               'categories': categories}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Categories_form.html',
                                          {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories},
                                          context)

class edit_cat(ListView):
    model = Categories
    template_name = 'postbox/Categories_form.html'
    context_object_name = 'cform_edit'

    def get_context_data(self, **kwargs):
        context = super(edit_cat, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        cid=self.kwargs['cid']
        cat = get_object_or_404(Categories, id=int(cid))
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['form'] = CategoryForm(instance=cat)
        context['categories'] = categories
        context['full_name'] = uname
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        cid = self.kwargs['cid']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        cat = get_object_or_404(Categories, id=int(cid))

        context = RequestContext(self.request)

        if self.request.method == 'POST':
            form = CategoryForm(self.request.POST, instance=cat)
            if form.is_valid():
                try:
                    cat_form = form.save(commit=False)
                    p = u[0].values()
                    cat_form.owner_id = p[0]
                    cat_form.save()
                    return HttpResponseRedirect('/postbox/' + uname + '/profile/')
                except Exception as e:
                    mesg = 'save_invalid'
                    return render_to_response('postbox/Categories_form.html',
                                              {"mesg": mesg, 'form': form, 'full_name': uname,
                                               'categories': categories},
                                              context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Posts_form.html',
                                          {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories},
                                          context)


class Create_post(ListView):
    model = Posts
    template_name = 'postbox/Posts_form.html'
    context_object_name = 'pform'

    def get_context_data(self, **kwargs):
        context = super(Create_post, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        p = u[0].values()
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['form'] = PostsForm(p[0])
        context['categories'] = categories
        context['full_name'] = self.kwargs['uname']
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context = RequestContext(self.request)

        if self.request.method == 'POST':
            p = u[0].values()
            form = PostsForm(p[0], self.request.POST, self.request.FILES)
            if form.is_valid():
                try:
                    post_form = form.save(commit=False)
                    post_form.owner_id = p[0]
                    if len(self.request.FILES) != 0:
                        file = self.request.FILES["image"]
                        filename = file.name
                        content = file.read()
                        store_in_s3(filename, content)
                        post_form.image = "https://s3-us-west-2.amazonaws.com/thoughtspost/"+filename
                    else:
                        post_form.image = ''
                    post_form.save()
                    return HttpResponseRedirect('/postbox/' + uname + '/profile/')
                except Exception as e:
                    mesg = 'save_invalid'
                    return render_to_response('postbox/Posts_form.html',
                                              {'mesg': mesg, 'form': form, 'full_name': uname,
                                               'categories': categories}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Posts_form.html',
                                          {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories},
                                          context)

class Edit_post(ListView):
    model = Posts
    template_name = 'postbox/Posts_form.html'
    context_object_name = 'pform_edit'

    def get_context_data(self, **kwargs):
        context = super(Edit_post, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        pid = self.kwargs['pid']
        post = get_object_or_404(Posts, id=int(pid))
        u = User.objects.filter(username=uname).values('id')
        p = u[0].values()
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['form'] = PostsForm(p[0],instance=post)
        context['categories'] = categories
        context['full_name'] = uname
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        pid = self.kwargs['pid']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context = RequestContext(self.request)
        post = get_object_or_404(Posts, id=pid)

        if self.request.method == 'POST':
            p = u[0].values()
            form = PostsForm(p[0], self.request.POST, self.request.FILES,instance=post)
            if form.is_valid():
                try:
                    post_form = form.save(commit=False)
                    post_form.owner_id = p[0]
                    if len(self.request.FILES) != 0:
                        file = self.request.FILES['image']
                        filename = file.name
                        content = file.read()
                        store_in_s3(filename, content)
                        post_form.image = "https://s3-us-west-2.amazonaws.com/thoughtspost/" + filename
                    post_form.save()
                    return HttpResponseRedirect('/postbox/' + uname + '/profile/')
                except Exception as e:
                    mesg = 'save_invalid'
                    return render_to_response('postbox/Posts_form.html',
                                              {'mesg': mesg, 'form': form, 'full_name': uname,
                                               'categories': categories}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Posts_form.html',
                                          {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories},
                                          context)

class CommentList(ListView):
    model = Comments
    context_object_name = 'comment_list'
    template_name = 'postbox/Comments_list.html'

    def get_context_data(self,**kwargs):
        context = super(CommentList, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        cid = self.kwargs['cid']
        u = User.objects.filter(username=uname).values('id')
        context['categories'] = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['full_name'] = self.kwargs['uname']
        context['cat'] = int(cid)
        context['post'] =Posts.objects.filter(id=self.kwargs['pid']).order_by('-p_date')
        context['c']=Comments.objects.filter(pid=self.kwargs['pid']).order_by('cm_date')
        context['uid']=u[0].values()[0]
        context['pid'] = int(self.kwargs.get('pid'))
        form = CommentForm()
        context['form'] = form
        return context

    def post(self,*args,**kwargs):
      uname = kwargs.get('uname')
      pid=int(kwargs.get('pid'))
      cat=int(kwargs.get('cid'))

      post=Posts.objects.filter(id=kwargs['pid']).order_by('-p_date')
      c=Comments.objects.filter(pid=kwargs['pid']).order_by('cm_date')

      u = User.objects.filter(username=uname).values('id')
      uid=u[0].values()[0]
      categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
      context = RequestContext(self.request)

      if self.request.method == 'POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                try:
                    cm_form = form.save(commit=False)
                    cm_form.owner_id =uid
                    cm_form.pid_id=int(kwargs.get('pid'))
                    cm_form.save()
                    return HttpResponseRedirect('/postbox/' + uname +'/'+kwargs.get('cid')+'/'+kwargs.get('pid')+'/comments')
                except Exception as e:
                     mesg = 'save_invalid'
                     return render_to_response('postbox/Comments_list.html',
                                      {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories,
                                       'pid': pid, 'uid': uid, 'cat': cat, 'post': post, 'c': c}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Comments_list.html', {'mesg': mesg, 'form': form, 'full_name': uname,'categories':categories,'pid':pid,'uid':uid,'cat':cat,'post':post,'c':c},context)

class CommentList1(ListView):
    model = Comments
    context_object_name = 'comment_list1'
    template_name = 'postbox/Comments_list1.html'

    def get_context_data(self,**kwargs):
        context = super(CommentList1, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        context['full_name'] = self.kwargs['uname']
        context['categories'] = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['post'] =Posts.objects.filter(id=self.kwargs['pid']).order_by('-p_date')
        context['c']=Comments.objects.filter(pid=self.kwargs['pid']).order_by('cm_date')
        context['uid']=u[0].values()[0]
        context['pid'] = int(self.kwargs.get('pid'))
        form = CommentForm()
        context['form'] = form
        return context

    def post(self,*args,**kwargs):
      uname = kwargs.get('uname')
      pid=int(kwargs.get('pid'))

      post=Posts.objects.filter(id=kwargs['pid']).order_by('-p_date')
      c=Comments.objects.filter(pid=kwargs['pid']).order_by('-c_date')

      u = User.objects.filter(username=uname).values('id')
      uid=u[0].values()[0]
      categories = Categories.objects.filter(owner_id=uid).order_by('cm_date')
      context = RequestContext(self.request)

      if self.request.method == 'POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                try:
                    cm_form = form.save(commit=False)
                    cm_form.owner_id =uid
                    cm_form.pid_id=int(kwargs.get('pid'))
                    cm_form.save()
                    return HttpResponseRedirect('/postbox/' + uname +'/'+kwargs.get('pid')+'/comments')
                except Exception as e:
                     mesg = 'save_invalid'
                     return render_to_response('postbox/Comments_list1.html',
                                      {'mesg': mesg, 'form': form, 'full_name': uname,
                                       'pid': pid, 'uid': uid, 'post': post, 'c': c,'categories':categories}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Comments_list1.html', {'mesg': mesg, 'form': form,'categories':categories, 'full_name': uname,'pid':pid,'uid':uid,'post':post,'c':c},context)

class EditComment(ListView):
    model = Comments
    template_name = 'postbox/Comments_list.html'
    context_object_name = 'cform_edit'

    def get_context_data(self, **kwargs):
        context = super(EditComment, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        pid = int(self.kwargs['pid'])
        cat = int(self.kwargs['cid'])
        cmid = int(self.kwargs['cmid'])
        comment = get_object_or_404(Comments, id=cmid)
        post = Posts.objects.filter(id=pid).order_by('-p_date')
        c = Comments.objects.filter(pid=pid).order_by('cm_date')
        u = User.objects.filter(username=uname).values('id')
        uid=u[0].values()[0]
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['form'] = CommentForm(instance=comment)
        context['full_name']=uname
        context['categories']=categories
        context['uid']=uid
        context['pid']=pid
        context['cat']=cat
        context['post']=post
        context['c']=c
        context['cmid']=cmid
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        pid = int(self.kwargs['pid'])
        cat = int(self.kwargs['cid'])
        cmid = int(self.kwargs['cmid'])
        comment = get_object_or_404(Comments, id=cmid)
        post = Posts.objects.filter(id=pid).order_by('-p_date')
        c = Comments.objects.filter(pid=pid).order_by('cm_date')
        u = User.objects.filter(username=uname).values('id')
        uid=u[0].values()[0]
        categories = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context = RequestContext(self.request)

        if self.request.method == 'POST':
            form = CommentForm(self.request.POST, instance=comment)
            if form.is_valid():
                try:
                    cm_form = form.save(commit=False)
                    cm_form.owner_id = uid
                    cm_form.pid_id = pid
                    cm_form.save()
                    return HttpResponseRedirect(
                        '/postbox/' + uname + '/' + self.kwargs['cid'] + '/' + self.kwargs['pid'] + '/comments')
                except Exception as e:
                    mesg = 'save_invalid'
                    return render_to_response('postbox/Comments_list.html',
                                              {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories,
                                               'pid': pid, 'uid': uid, 'cat': cat, 'post': post, 'c': c,
                                               'cmid': cmid}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Comments_list.html',
                                          {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories,
                                           'pid': pid, 'uid': uid, 'cat': cat, 'post': post, 'c': c,
                                           'cmid': cmid}, context)

class EditComment1(ListView):
    model = Comments
    template_name = 'postbox/Comments_list1.html'
    context_object_name = 'cform_edit1'

    def get_context_data(self, **kwargs):
        context = super(EditComment1, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        pid = int(self.kwargs['pid'])
        cmid = int(self.kwargs['cmid'])
        comment = get_object_or_404(Comments, id=cmid)
        post =Posts.objects.filter(id=pid).order_by('-p_date')
        c = Comments.objects.filter(pid=pid).order_by('cm_date')
        u = User.objects.filter(username=uname).values('id')
        uid=u[0].values()[0]
        context['form'] = CommentForm(instance=comment)
        context['full_name'] = uname
        context['uid'] = uid
        context['pid'] = pid
        context['post'] = post
        context['c'] = c
        context['categories'] = Categories.objects.filter(owner_id=u).order_by('-c_date')
        context['cmid'] = cmid
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        pid = int(self.kwargs['pid'])
        cmid = int(self.kwargs['cmid'])
        comment = get_object_or_404(Comments, id=cmid)
        u = User.objects.filter(username=uname).values('id')
        uid = u[0].values()[0]
        post = Posts.objects.filter(id=pid).order_by('-p_date')
        categories= Categories.objects.filter(owner_id=u).order_by('-c_date')
        c = Comments.objects.filter(pid=pid).order_by('cm_date')
        context = RequestContext(self.request)

        if self.request.method == 'POST':
            form = CommentForm(self.request.POST, instance=comment)
            if form.is_valid():
                try:
                    cm_form = form.save(commit=False)
                    cm_form.owner_id = int(uid)
                    cm_form.pid_id = int(pid)
                    cm_form.save()
                    return HttpResponseRedirect(
                        '/postbox/' + uname + '/' +self.kwargs['pid'] + '/comments')
                except Exception as e:
                    mesg = 'save_invalid'
                    return render_to_response('postbox/Comments_list1.html',
                                              {'mesg': mesg, 'form': form, 'full_name': uname,
                                               'pid': pid, 'uid': uid, 'post': post, 'c': c,
                                               'cmid': cmid, 'categories':categories}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Comments_list1.html',
                                          {'mesg': mesg, 'form': form, 'full_name': uname,
                                           'pid': pid, 'uid': uid, 'post': post, 'c': c, 'cmid':cmid,'categories':categories},
                                          context)

def login(request):
    c={}
    c.update(csrf(request))
    return render_to_response('registration/login.html', c)

def auth_view(request):
    username=request.POST.get('username','')
    password= request.POST.get('password','')
    user=auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/postbox/')
    else:
        return HttpResponseRedirect('/accounts/invalid/')

def invalid_login(request):
     return render_to_response('registration/invalid.html')

def base(request):
    return HttpResponseRedirect('/postbox/')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/postbox/')

def register_user(request):
    context=RequestContext(request)
    if request.method=='POST' :
        form=UserCreationForm(request.POST)
        if form.is_valid():
            try:
               form.save()
               return HttpResponseRedirect('/')
            except Exception as e:
                mesg = 'user not registered.Try again'
                return render_to_response('registration/register.html',
                                          {'mesg': mesg, 'form': form,}, context)
        else:
            mesg = 'form_invalid'
            return render_to_response('registration/register.html',
                                      {'mesg': mesg, 'form': form,}, context)
    args={}
    args.update(csrf(request))

    args['form']=UserCreationForm()
    print args
    return render_to_response('registration/register.html',args)

def delete_post(request, uname, pid):
    note = get_object_or_404(Posts, id=pid).delete()
    return HttpResponseRedirect('/postbox/' + uname + '/profile')

def delete_comment(request,uname,cid,pid,cmid):
    note = get_object_or_404(Comments, id=cmid).delete()
    return HttpResponseRedirect('/postbox/'+uname+'/'+cid+'/'+pid+'/comments/')

def delete_comment1(request,uname,pid,cmid):
    note = get_object_or_404(Comments, id=cmid).delete()
    return HttpResponseRedirect('/postbox/'+uname+'/'+pid+'/comments/')

def delete_cat(request,uname,cid):
    note = get_object_or_404(Categories, id=cid).delete()
    return HttpResponseRedirect('/postbox/'+uname+'/profile/')

