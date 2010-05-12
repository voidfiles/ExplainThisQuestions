from django import forms
from django.forms import ModelForm
from explainthis.questions.models import Question, Comment, Answer, Site

class QuestionForm(ModelForm):
    tages = forms.CharField(label="Tags", required=False,help_text="Comma Seperated: Example: apple, orange, blue, red")
    class Meta:
        model = Question
        exclude = ("answered", "votes","site", "user","slug","tags")
        
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ("user","content_type","object_id","content_object")
        widgets = {
            'comment': forms.TextInput(attrs={"id":""}),
        }
        

               
class AnswerForm(ModelForm):
    
    class Meta:
        model = Answer
        exclude = ("question", "created","updated", "the_answer", "user","votes")
        
        
class SiteForm(ModelForm):
    tages = forms.CharField(label="Tags",required=False, help_text="Comma Seperated: Example: apple, orange, blue, red")
    class Meta:
        model = Site
        exclude = ("admins","slug","tags")

def validate_user_exsists(value):
    from django.contrib.auth.models import User
    from django.core.exceptions import ValidationError

    try:
        user = User.objects.get(username=value)
    except:
        raise ValidationError('The user %s does not exsist' % value)

class AddAdmin(forms.Form):
    username = forms.CharField(
        label="Username", 
        max_length=255,
        help_text="Enter the username of the person you want to add as an administrator.",
        validators=[validate_user_exsists]
    )

