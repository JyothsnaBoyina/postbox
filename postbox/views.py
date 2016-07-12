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
from django.contrib.auth.forms import UserCreationForm
from django.template import loader


class Newsfeed(ListView):
    model=Posts
    context_object_name = 'news'
    template_name = 'postbox/newsfeed.html'

    def get_context_data(self, **kwargs):
        context = super(Newsfeed, self).get_context_data(**kwargs)
        context['posts'] = enumerate(Posts.objects.all())
        u = User.objects.filter(username=self.kwargs['uname']).values('id')
        p=u[0].values()
        context['p']=p[0]
        context['full_name'] = self.kwargs['uname']
        l = []
        p = Posts.objects.values('image')
        for i in p:
            s = i.values()[0]
            lst = s.split('/', s.count('/'))
            string = 'postbox/' + lst[-1]
            l.append(string)
        context['img'] = l
        return context

class Profile(ListView):
    model=Posts
    context_object_name = 'user'
    template_name = 'postbox/user.html'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        uname=self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        context['posts'] = enumerate(Posts.objects.filter(owner_id=u))
        context['post'] = enumerate(Posts.objects.filter(owner_id=u))
        context['categories'] = Categories.objects.filter(owner_id=u)
        context['full_name']=self.kwargs['uname']
        l = []
        p = Posts.objects.values('image')
        for i in p:
            s = i.values()[0]
            lst = s.split('/', s.count('/'))
            string = 'postbox/' + lst[-1]
            l.append(string)
        context['img'] = l

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
        context['categories'] = Categories.objects.filter(owner_id=u)
        context['full_name'] = self.kwargs['uname']
        context['cat'] = int(cid)
        if(cid):
         context['post'] = enumerate(Posts.objects.filter(cid_id=self.kwargs['cid']))
        l=[]
        p=Posts.objects.filter(cid_id=self.kwargs['cid']).values('image')
        for i in p:
            s=i.values()[0]
            lst=s.split('/',s.count('/'))
            string='postbox/'+lst[-1]
            l.append(string)
        context['img']=l

        return context

class CreateCat(ListView):
    model = Categories
    context_object_name = 'cform'
    template_name = 'postbox/Categories_form.html'

    def get_context_data(self,**kwargs):
        context = super(CreateCat, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u)
        context['form']=CategoryForm()
        context['categories']= categories
        context['full_name']=uname
        return context

    def post(self,*args,**kwargs):
        uname=self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u)
        context = RequestContext(self.request)

        if self.request.method == 'POST':
            form = CategoryForm(self.request.POST)
            if form.is_valid():
                try:
                    cat_form = form.save(commit=False)
                    p = u[0].values()
                    cat_form.owner_id = p[0]
                    cat_form.save()
                    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/' + uname + '/profile/')
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
        # else:
        #     form = CategoryForm()
        #     return render_to_response('postbox/Categories_form.html',
        #                               {'form': form, 'full_name': uname, 'categories': categories}, context)

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
        categories = Categories.objects.filter(owner_id=u)
        context['form'] = CategoryForm(instance=cat)
        context['categories'] = categories
        context['full_name'] = uname
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        cid = self.kwargs['cid']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u)
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
                    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/' + uname + '/profile/')
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
        else:
            form = CategoryForm(instance=cat)
            return render_to_response('postbox/Categories_form.html',
                                      {'form': form, 'full_name': uname, 'categories': categories}, context)

class Create_post(ListView):
    model = Posts
    template_name = 'postbox/Posts_form.html'
    context_object_name = 'pform'

    def get_context_data(self, **kwargs):
        context = super(Create_post, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        p = u[0].values()
        categories = Categories.objects.filter(owner_id=u)
        context['form'] = PostsForm(p[0])
        context['categories'] = categories
        context['full_name'] = self.kwargs['uname']
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u)
        context = RequestContext(self.request)

        if self.request.method == 'POST':
            p = u[0].values()
            form = PostsForm(p[0], self.request.POST, self.request.FILES)
            if form.is_valid():
                try:
                    post_form = form.save(commit=False)
                    post_form.owner_id = p[0]
                    if len(self.request.FILES) != 0:
                        post_form.image = self.request.FILES['image']
                    else:
                        post_form.image = ''
                    post_form.save()
                    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/' + uname + '/profile/')
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

        else:
            p = u[0].values()
            form = PostsForm(p[0])
            return render_to_response('postbox/Posts_form.html',
                                      {'form': form, 'full_name': uname, 'categories': categories}, context)

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
        categories = Categories.objects.filter(owner_id=u)
        context['form'] = PostsForm(p[0],instance=post)
        context['categories'] = categories
        context['full_name'] = uname
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        pid = self.kwargs['pid']
        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u)
        context = RequestContext(self.request)
        post = get_object_or_404(Posts, id=pid)

        if self.request.method == 'POST':
            p = u[0].values()
            form = PostsForm(p[0], self.request.POST, self.request.FILES, instance=post)
            if form.is_valid():
                try:
                    post_form = form.save(commit=False)
                    post_form.owner_id = p[0]
                    if len(self.request.FILES) != 0:
                        post_form.image = self.request.FILES['image']
                    post_form.save()
                    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/' + uname + '/profile/')
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

        else:
            p = u[0].values()
            form = PostsForm(p[0], instance=post)
            return render_to_response('postbox/Posts_form.html',
                                      {'form': form, 'full_name': uname, 'categories': categories}, context)

class CommentList(ListView):
    model = Comments
    context_object_name = 'comment_list'
    template_name = 'postbox/Comments_list.html'

    def get_context_data(self,**kwargs):
        context = super(CommentList, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        cid = self.kwargs['cid']
        u = User.objects.filter(username=uname).values('id')
        context['categories'] = Categories.objects.filter(owner_id=u)
        context['full_name'] = self.kwargs['uname']
        context['cat'] = int(cid)
        # context['cat_id'] = str(cat)
        if(cid):
         context['post'] = enumerate(Posts.objects.filter(id=self.kwargs['pid']))
        l=[]
        p=Posts.objects.filter(id=self.kwargs['pid']).values('image')
        for i in p:
            s=i.values()[0]
            lst=s.split('/',s.count('/'))
            string='postbox/'+lst[-1]
            l.append(string)
        context['img']=l
        context['c']=Comments.objects.filter(pid=self.kwargs['pid'])
        context['uid']=int(self.kwargs.get('uid'))
        context['pid'] = int(self.kwargs.get('pid'))
        form = CommentForm()
        context['form'] = form
        return context

    def post(self,*args,**kwargs):
      uname = kwargs.get('uname')
      pid=int(kwargs.get('pid'))
      uid=int(kwargs.get('uid'))
      cat=int(kwargs.get('cid'))

      post=enumerate(Posts.objects.filter(id=kwargs['pid']))
      c=Comments.objects.filter(pid=kwargs['pid'])
      l = []
      p = Posts.objects.filter(id=kwargs['pid']).values('image')
      for i in p:
          s = i.values()[0]
          lst = s.split('/', s.count('/'))
          string = 'postbox/' + lst[-1]
          l.append(string)

      u = User.objects.filter(username=uname).values('id')
      categories = Categories.objects.filter(owner_id=u)
      context = RequestContext(self.request)

      if self.request.method == 'POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                try:
                    cm_form = form.save(commit=False)
                    cm_form.owner_id =int(kwargs.get('uid'))
                    cm_form.pid_id=int(kwargs.get('pid'))
                    cm_form.save()
                    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/' + uname + '/'+kwargs.get('uid')+'/'+kwargs.get('cid')+'/'+kwargs.get('pid')+'/comments')
                except Exception as e:
                     mesg = 'save_invalid'
                     return render_to_response('postbox/Comments_list.html',
                                      {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories,
                                       'pid': pid, 'uid': uid, 'cat': cat, 'post': post, 'c': c, 'img': l,}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Comments_list.html', {'mesg': mesg, 'form': form, 'full_name': uname,'categories':categories,'pid':pid,'uid':uid,'cat':cat,'post':post,'c':c,'img':l},context)

class CommentList1(ListView):
    model = Comments
    context_object_name = 'comment_list1'
    template_name = 'postbox/Comments_list1.html'

    def get_context_data(self,**kwargs):
        context = super(CommentList1, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        u = User.objects.filter(username=uname).values('id')
        context['full_name'] = self.kwargs['uname']
        context['post'] = enumerate(Posts.objects.filter(id=self.kwargs['pid']))
        l=[]
        p=Posts.objects.filter(id=self.kwargs['pid']).values('image')
        for i in p:
            s=i.values()[0]
            lst=s.split('/',s.count('/'))
            string='postbox/'+lst[-1]
            l.append(string)
        context['img']=l
        context['c']=Comments.objects.filter(pid=self.kwargs['pid'])
        context['uid']=u[0].values()[0]
        context['pid'] = int(self.kwargs.get('pid'))
        form = CommentForm()
        context['form'] = form
        return context

    def post(self,*args,**kwargs):
      uname = kwargs.get('uname')
      pid=int(kwargs.get('pid'))
      uid=int(kwargs.get('uid'))

      post=enumerate(Posts.objects.filter(id=kwargs['pid']))
      c=Comments.objects.filter(pid=kwargs['pid'])
      l = []
      p = Posts.objects.filter(id=kwargs['pid']).values('image')
      for i in p:
          s = i.values()[0]
          lst = s.split('/', s.count('/'))
          string = 'postbox/' + lst[-1]
          l.append(string)

      u = User.objects.filter(username=uname).values('id')
      context = RequestContext(self.request)

      if self.request.method == 'POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                try:
                    cm_form = form.save(commit=False)
                    cm_form.owner_id =int(kwargs.get('uid'))
                    cm_form.pid_id=int(kwargs.get('pid'))
                    cm_form.save()
                    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/' + uname + '/'+kwargs.get('uid')+'/'+kwargs.get('pid')+'/comments')
                except Exception as e:
                     mesg = 'save_invalid'
                     return render_to_response('postbox/Comments_list1.html',
                                      {'mesg': mesg, 'form': form, 'full_name': uname,
                                       'pid': pid, 'uid': uid, 'post': post, 'c': c, 'img': l,}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Comments_list1.html', {'mesg': mesg, 'form': form, 'full_name': uname,'pid':pid,'uid':uid,'post':post,'c':c,'img':l},context)

class EditComment(ListView):
    model = Comments
    template_name = 'postbox/Comments_list.html'
    context_object_name = 'cform_edit'

    def get_context_data(self, **kwargs):
        context = super(EditComment, self).get_context_data(**kwargs)
        uname = self.kwargs['uname']
        pid = int(self.kwargs['pid'])
        cat = int(self.kwargs['cid'])
        uid = int(self.kwargs['uid'])
        cmid = int(self.kwargs['cmid'])
        comment = get_object_or_404(Comments, id=cmid)
        post = enumerate(Posts.objects.filter(id=pid))
        c = Comments.objects.filter(pid=pid)
        l = []
        p = Posts.objects.filter(id=pid).values('image')
        for i in p:
            s = i.values()[0]
            lst = s.split('/', s.count('/'))
            string = 'postbox/' + lst[-1]
            l.append(string)

        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u)
        context['form'] = CommentForm(instance=comment)
        context['full_name']=uname
        context['categories']=categories
        context['uid']=uid
        context['pid']=pid
        context['cat']=cat
        context['post']=post
        context['img']=l
        context['c']=c
        context['cmid']=cmid
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        pid = int(self.kwargs['pid'])
        cat = int(self.kwargs['cid'])
        uid = int(self.kwargs['uid'])
        cmid = int(self.kwargs['cmid'])
        comment = get_object_or_404(Comments, id=cmid)
        p_id = int(pid)
        u_id = int(uid)
        post = enumerate(Posts.objects.filter(id=pid))
        c = Comments.objects.filter(pid=pid)
        l = []
        p = Posts.objects.filter(id=pid).values('image')
        for i in p:
            s = i.values()[0]
            lst = s.split('/', s.count('/'))
            string = 'postbox/' + lst[-1]
            l.append(string)

        u = User.objects.filter(username=uname).values('id')
        categories = Categories.objects.filter(owner_id=u)
        context = RequestContext(self.request)

        if self.request.method == 'POST':
            form = CommentForm(self.request.POST, instance=comment)
            if form.is_valid():
                try:
                    cm_form = form.save(commit=False)
                    cm_form.owner_id = u_id
                    cm_form.pid_id = p_id
                    cm_form.save()
                    return HttpResponseRedirect(
                        'http://127.0.0.1:8000/postbox/' + uname + '/' + self.kwargs['uid'] + '/' + self.kwargs['cid'] + '/' + self.kwargs['pid'] + '/comments')
                except Exception as e:
                    mesg = 'save_invalid'
                    return render_to_response('postbox/Comments_list.html',
                                              {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories,
                                               'pid': p_id, 'uid': u_id, 'cat': cat, 'post': post, 'c': c, 'img': l,
                                               'cmid': int(cmid)}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Comments_list.html',
                                          {'mesg': mesg, 'form': form, 'full_name': uname, 'categories': categories,
                                           'pid': p_id, 'uid': u_id, 'cat': cat, 'post': post, 'c': c, 'img': l,
                                           'cmid': int(cmid)}, context)

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
        post = enumerate(Posts.objects.filter(id=pid))
        c = Comments.objects.filter(pid=pid)
        l = []
        p = Posts.objects.filter(id=pid).values('image')
        for i in p:
            s = i.values()[0]
            lst = s.split('/', s.count('/'))
            string = 'postbox/' + lst[-1]
            l.append(string)

        u = User.objects.filter(username=uname).values('id')
        uid=u[0].values()[0]
        context['form'] = CommentForm(instance=comment)
        context['full_name'] = uname
        context['uid'] = uid
        context['pid'] = pid
        context['post'] = post
        context['img'] = l
        context['c'] = c
        context['cmid'] = cmid
        return context

    def post(self,*args,**kwargs):
        uname = self.kwargs['uname']
        pid = int(self.kwargs['pid'])
        cmid = int(self.kwargs['cmid'])
        comment = get_object_or_404(Comments, id=cmid)
        u = User.objects.filter(username=uname).values('id')
        p_id = int(pid)
        u_id = u[0].values()[0]
        post = enumerate(Posts.objects.filter(id=pid))
        c = Comments.objects.filter(pid=pid)
        l = []
        p = Posts.objects.filter(id=pid).values('image')
        for i in p:
            s = i.values()[0]
            lst = s.split('/', s.count('/'))
            string = 'postbox/' + lst[-1]
            l.append(string)

        context = RequestContext(self.request)

        if self.request.method == 'POST':
            form = CommentForm(self.request.POST, instance=comment)
            if form.is_valid():
                try:
                    cm_form = form.save(commit=False)
                    cm_form.owner_id = u_id
                    cm_form.pid_id = p_id
                    cm_form.save()
                    return HttpResponseRedirect(
                        'http://127.0.0.1:8000/postbox/' + uname + '/' + str(u_id) + '/' +self.kwargs['pid'] + '/comments')
                except Exception as e:
                    mesg = 'save_invalid'
                    return render_to_response('postbox/Comments_list1.html',
                                              {'mesg': mesg, 'form': form, 'full_name': uname,
                                               'pid': p_id, 'uid': u_id, 'post': post, 'c': c, 'img': l,
                                               'cmid': int(cmid)}, context)
            else:
                mesg = 'form_invalid'
                return render_to_response('postbox/Comments_list1.html',
                                          {'mesg': mesg, 'form': form, 'full_name': uname,
                                           'pid': p_id, 'uid': u_id, 'post': post, 'c': c, 'img': l, 'cmid': int(cmid)},
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
        return HttpResponseRedirect('/postbox/'+username+'/')
    else:
        return HttpResponseRedirect('/accounts/invalid/')

def invalid_login(request):
     return render_to_response('registration/invalid.html')

def logout(request):
    auth.logout(request)
    render_to_response('registration/login.html')
    return HttpResponseRedirect('/')

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

def delete_post(request, uname, cid, uid, pid):
    note = get_object_or_404(Posts, id=pid).delete()
    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/' + uname + '/profile')

def delete_comment(request,uname,cid,uid,pid,cmid):
    note = get_object_or_404(Comments, id=cmid).delete()
    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/'+uname+'/'+uid+'/'+cid+'/'+pid+'/comments/')

def delete_comment1(request,uname,pid,cmid):
    u = User.objects.filter(username=uname).values('id')
    p=str(u[0].values()[0])
    note = get_object_or_404(Comments, id=cmid).delete()
    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/'+uname+'/'+p+'/'+pid+'/comments/')

def delete_cat(request,uname,cid):
    note = get_object_or_404(Categories, id=cid).delete()
    return HttpResponseRedirect('http://127.0.0.1:8000/postbox/'+uname+'/profile/')

