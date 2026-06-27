from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from .validators import validate_username_format, validate_image_size, validate_image_extension

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    """
    Form for user registration. Handles email, username, password, and terms validation.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    agree_terms = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must agree to the Terms and Conditions.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        validate_username_format(username)
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
            
        return cleaned_data


class LoginForm(forms.Form):
    """
    Form for user login. Allows authentication via email or username.
    """
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username or email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating a user's profile details.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Email is read-only
        self.fields['email'] = forms.EmailField(
            initial=self.instance.email,
            required=False,
            widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
        )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        validate_username_format(username)
        if User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
        
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and picture is not False and getattr(picture, 'file', None):
            validate_image_size(picture)
            validate_image_extension(picture)
        return picture


class ChangePasswordForm(PasswordChangeForm):
    """
    Form for changing the user's password, styled with Bootstrap.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
