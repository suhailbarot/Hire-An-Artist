from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator, URLValidator
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.forms.models import inlineformset_factory,BaseInlineFormSet

from app.models import *
from app.utils import generate_hash
from app.checkbox.iterator import AdvancedModelChoiceField
from django.utils.safestring import mark_safe


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


attrs_dict = {'class': 'required'}
number_validator = RegexValidator(r'^\d{10,12}$', "Please enter a valid phone number")
youtube_validator= RegexValidator(r'^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$',
                                  "Please enter a valid youtube URL")
soundcloud_validator = RegexValidator(r'^https?:\/\/(soundcloud.com|snd.sc)\/(.*)$',
                                      "Please enter a valid soundcloud URL")


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label=u'email')

    def clean_email(self):
        """
        Validate the username
        :return:
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['email'])
            return self.cleaned_data['email']
        except User.DoesNotExist:
            raise forms.ValidationError(u'No account with the provided email exists')

    def complete(self):
        email = self.cleaned_data['email']
        pr = PasswordReset.objects.create(key=generate_hash(email), email=email)
        link = "http://127.0.0.1/reset/" + pr.key
        message = 'Please click on this link to reset the password : <a href="' + link + '>' + link + '</a>'
        # send email
        # send_mail('Reset your password at X', message,
        # 'mkinom@gmail.com', [email], fail_silently=True)
        print message


class FilterSearchForm(forms.Form):
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City'}), label=u'City',required=False)
    function_type = forms.ModelChoiceField(queryset=Function.objects.filter(is_active=1).order_by('name'),required=False, empty_label=('--- Function---'))
    talents = forms.ModelChoiceField(queryset=Talent.objects.filter(is_active=1), required=False, empty_label=('--- Talent---'))
    budget_min = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    budget_max = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    outstation = forms.BooleanField(label=u'Outstation Artists?',required=False)


class HomeSearchForm(forms.Form):
    city = forms.CharField(widget=forms.HiddenInput(), label=u'City',required=True)
    function_type = forms.ModelChoiceField(queryset=Function.objects.filter(is_active=1).order_by('name'),required=False, empty_label=('Event type'))
    talents = forms.ModelChoiceField(queryset=Talent.objects.filter(is_active=1), required=False, empty_label=('Looking for..'))
    budget_min = forms.IntegerField(required=False,widget=forms.HiddenInput())
    budget_max = forms.IntegerField(required=False,widget=forms.HiddenInput())
    choices = ((None,'Outstation?'), (1,'Yes'),
                (0,'No'),
              )
    outstation = forms.ChoiceField(choices=choices,required=False,)


class HomeArtistNameSearch(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Artist Name'}), label=u'Name')


class ArtistNameSearch(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label=u'Name')


class RegisterForm(forms.Form):
    """
    Registration form for artists
    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label=u'E-mail')
    name = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label=u'Name')
    phone = forms.CharField(validators=[number_validator], widget=forms.TextInput(attrs=dict(maxlength=12)),
                            label=u'phone')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=u'Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=u'Re-Type Password')

    def clean_email(self):
        """
        Validate the username
        :return:
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(u'Seems like the email is already in use. Please log in instead')

    def clean(self):
        """
        check passwords entered are the same
        :return:
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'You must type the same password each time')
        return self.cleaned_data

    def save(self, actype):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        phone = self.cleaned_data['phone']

        new_user = User.objects.create_user(username=email, email=email, password=password)
        new_user.is_active = True
        new_user.save()
        user_profile = UserProfile.objects.create(user=new_user, full_name=name, email=email, phone=phone, type=actype)

        return user_profile


class LoginForm(forms.Form):
    """
    Login form for all
    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label=u'E-mail')
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=u'Password')

    def clean(self):
        """
        Check if user pass combination is correct

        :return:
        """
        if 'email' in self.cleaned_data and 'password' in self.cleaned_data:
            if not authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password']):
                raise forms.ValidationError(u'The user-password combination is incorrect')
        return self.cleaned_data

    def save(self):
        return authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password'])


class PhoneForm(forms.Form):
    """
    Add Phone Number Form
    """
    phone = forms.CharField(validators=[number_validator], widget=forms.TextInput(attrs=dict(maxlength=12)),
                            label=u'phone')

    def save(self, user):
        user.phone = self.cleaned_data['phone']
        user.save()


class ListingForm(forms.ModelForm):
    """
    For Artist adding listings
    """

    talents = forms.ModelChoiceField(queryset=Talent.objects.filter(is_active=1), required=True)

    tags = AdvancedModelChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Tag.objects.filter(is_active=1), required=False)

    functions = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                               queryset=Function.objects.filter(is_active=1), required=True)

    x = forms.IntegerField(widget=forms.HiddenInput(),label=u'')
    x2 = forms.IntegerField(widget=forms.HiddenInput(),label=u'')
    y = forms.IntegerField(widget=forms.HiddenInput(),label=u'')
    y2 = forms.IntegerField(widget=forms.HiddenInput(),label=u'')


    class Meta:
        model = Listing
        exclude = ('user', 'is_approved', 'is_active', 'score')

    def clean_functions(self):
        return self.cleaned_data['functions']

    # def __init__(self, *args, **kwargs):
    #     super(ListingForm, self).__init__(*args,**kwargs)
    #     self.fields['talents'].widget = forms.CheckboxSelectMultiple()
    #     self.fields['talents'].queryset = Talent.objects.filter(is_active=1)
    #     self.fields['talents'].required = True
    #
    #     self.fields['tags'].widget = forms.CheckboxSelectMultiple()
    #     self.fields['tags'].queryset = Tag.objects.filter(is_active=1)
    #     self.fields['tags'].required = True
    #
    #     self.fields['functions'].widget = forms.CheckboxSelectMultiple()
    #     self.fields['functions'].queryset = Fu.objects.filter(is_active=1)
    #     self.fields['functions'].required = True

    def clean_tags(self):
        new_list = []
        for tag in self.cleaned_data['tags']:
            if tag.talent == self.cleaned_data['talents']:
                new_list.append(tag)
        return new_list

    def save(self, commit=True, user=None):
        m = super(ListingForm, self).save(commit=False)
        if commit:
            m.user = user
            m.save()
            m.functions.clear()
            m.tags.clear()
            for fn in self.cleaned_data['functions']:
                m.functions.add(fn)
            for tg in self.cleaned_data['tags']:
                m.tags.add(tg)
        return m


class ProjectForm(forms.ModelForm):
    # def save(self, commit=True, listing=None):
    #     pf = super(ProjectForm,self).save(commit=False)
    #     if commit:
    #         pf.listing = listing
    #         pf.save()

    class Meta:
        model = Projects
        exclude = ('is_active','listing')


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name','phone')

class EditPasswordForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=u'passwordold')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=u'password1')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=u'password2')


ListingProjectFormSet = inlineformset_factory(Listing,Projects, form=ProjectForm, extra=1, can_delete=True, can_order=True,
                                              validate_max=7)