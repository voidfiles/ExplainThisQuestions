# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404

from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

def index(request):
    from explainthis.questions.models import Question, Site
    
    questions = Question.objects.all()
    sites = Site.objects.all()
    
    return render_to_response('base.html',
                              {"questions":questions,"sites":sites},
                              context_instance=RequestContext(request))
                              
  
def answer(request, question_id):  
    pass

def site(request,site_id="", site_slug="",widget_type="site"):
    from explainthis.questions.models import Question, Site
    
    site = get_object_or_404(Site,slug=site_slug)
    questions = site.question_set.all()[0:10]
    
    return render_to_response('sites/main.html',
                              {"site":site,"questions":questions},
                              context_instance=RequestContext(request))
    
    
@login_required
def create_subsite(request):
    from explainthis.questions.forms import SiteForm
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():            
            subsite = form.save()
            subsite.admins.add(request.user)
            couple_tags = request.POST.get("tages", None)
            if couple_tags:
                couple_tags = [tag.strip() for tag in couple_tags.split(",")]
                subsite.tags.add(*couple_tags)
            subsite.save()
            return HttpResponseRedirect("/")
    else:
        form = SiteForm()
        
    return render_to_response('subsite/create.html',
                              {"form":form},
                              context_instance=RequestContext(request))
  
@login_required                            
def vote(request, *args, **kwargs):
    from voting.views import vote_on_object
    return vote_on_object(request, **kwargs)
def ask(request, **kwargs):
    site_id = kwargs.get("site_id",1)
    site_slug = kwargs.get("site_slug", "")
    widget_type = kwargs.get("site")
    from explainthis.questions.forms import QuestionForm
    from explainthis.questions.models import Question, Site
    from django.http import HttpResponseRedirect
    
    site = get_object_or_404(Site,slug=site_slug)
    if request.method == "POST":
        # save the question
        copy_of_post = request.POST.copy()
        
        
        copy_of_post["site"] = site.id
            
        form = QuestionForm(copy_of_post)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.site = Site.objects.get(pk=copy_of_post["site"])
            new_question.save()
            if request.user.is_authenticated():
                new_question.user = request.user
                
            couple_tags = request.POST.get("tages", None)
            if couple_tags:
                couple_tags = [tag.strip() for tag in couple_tags.split(",")]
                new_question.tags.add(*couple_tags)
            new_question.save()
            return HttpResponseRedirect(new_question.get_absolute_url()) # Redirect after POST
    else:
        if request.GET.get("title", None):
            form = QuestionForm(request.GET)
        else:
            form = QuestionForm()
    

    return render_to_response('questions/ask.html',
                          {"form":form,"site":site},
                          context_instance=RequestContext(request))
@login_required
def user_profile(request, user_slug=""):
    from explainthis.questions.models import UserProfile
    
    userProfile = get_object_or_404(UserProfile,slug=user_slug)
    

    return render_to_response('accounts/profile.html',
                          {"userProfile":userProfile},
                          context_instance=RequestContext(request))        
        
@login_required
def post_comment(request,comment_type_post, question_id, answer_id=0):
    from explainthis.questions.models import Question, Answer
    from explainthis.questions.forms import CommentForm
    from django.contrib.contenttypes.models import ContentType
    from django.utils import simplejson

    success = True
    json_errors = {}
    json_response = {
    
    }
    
    if request.method == "GET": raise Http404()
    
    
    comment_html = None
    comment = None
    form = CommentForm(request.POST)
    
    if not form.is_valid():
        for error in form.errors:
            json_errors.update({error: str(form.errors[error])})
            success = False
            
    else:
        if comment_type_post == "question":
            object_type = Question
            object_instance = Question.objects.get(pk=question_id)
        else:
            object_type = Answer
            object_instance = Answer.objects.get(pk=answer_id)
            
            
        ctype = ContentType.objects.get_for_model(object_type)
        comment = form.save(commit=False)
        comment.user = request.user
        comment.content_type = ctype
        comment.object_id = object_instance.id
        comment.content_object = object_instance
        comment.save();



    if request.is_ajax():
        if success:
            comment_html = render_to_string('comments/comment.html',
                                        {'comment': comment },
                                        context_instance=RequestContext(request))
        json_response = simplejson.dumps({
            'success': success,
            'errors': json_errors,
            'html': comment_html,
        })
        
        return HttpResponse(json_response, mimetype="application/json")
    else:
        return HttpResponseRedirect(object_instance.get_absolute_url())
        
            

    
           
def question(request,site_slug="",site_id="",question_id="",question_slug="",widget_type="site"):
    from explainthis.questions.models import Question, Site
    from explainthis.questions.forms import CommentForm,AnswerForm
    
    question = get_object_or_404(Question,slug=question_slug)
    
    question.sorted_answers()
    
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            if request.user.is_authenticated():
                answer.user = request.user

            answer.save()
    else:
        answer_form = AnswerForm()
    
    
    try:
        site = Site.objects.get(slug=site_slug)
    except Site.DoesNotExist:
        site = None
    
    comment_form = CommentForm()
    answer_form = AnswerForm()
        
    return render_to_response(
        'questions/question.html',
        {
            "question":question,
            "site":site, 
            "comment_form":comment_form,
            "answer_form":answer_form,
        },
        context_instance=RequestContext(request)
    )

def admin_site(request, site_slug=""):
    import logging
    from explainthis.questions.forms import AddAdmin
    from explainthis.questions.models import Question, Site
    from django.http import HttpResponseRedirect
    from django.contrib.auth.models import User
    site = get_object_or_404(Site,slug=site_slug)
    
    if request.user not in site.admins.all():
        return render_to_response(
            'sites/admin_denied.html',
            {"site":site},
            context_instance=RequestContext(request)
        )
        
    addAdminForm = AddAdmin()
      
    if request.method == "POST":
        action = request.POST.get("action", None)
        
        if action:
            if action == "Add User":
                
                addAdminFormSub = AddAdmin(request.POST)
                if addAdminFormSub.is_valid():
                    site.admins.add(User.objects.get(username=addAdminFormSub.cleaned_data["username"]))
                else:
                    addAdminForm = addAdminFormSub
                    
    
    return render_to_response(
        'sites/admin.html',
        {
            "site":site,
            "addAdminForm":addAdminForm,
        },
        context_instance=RequestContext(request)
    )
