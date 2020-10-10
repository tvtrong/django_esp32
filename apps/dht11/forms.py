from django.forms import ModelForm
from .models import DHT11
from django import forms


class DHT11Form(ModelForm):
    class Meta:
        model = DHT11
        fields = '__all__'
    error_css_class = 'error'
    required_css_class = 'required'


# class AuthorForm(ModelForm):
#    class Meta:
#        model = Author
#        fields = ['name', 'title', 'birth_date']


# class BookForm(ModelForm):
#    class Meta:
#        model = Book
#        fields = ['name', 'authors']

# TITLE_CHOICES = [
#    ('MR', 'Mr.'),
#    ('MRS', 'Mrs.'),
#    ('MS', 'Ms.'),
# ]


# class AuthorForm(forms.Form):
#    name = forms.CharField(max_length=100)
#    title = forms.CharField(
#        max_length=3,
#        widget=forms.Select(choices=TITLE_CHOICES),
#    )
#    birth_date = forms.DateField(required=False)


# class BookForm(forms.Form):
#    name = forms.CharField(max_length=100)
#    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
