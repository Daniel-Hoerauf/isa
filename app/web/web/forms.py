from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='Password', min_length=8, max_length=64, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username is None:
            self.add_error('username', "Please enter a username")
        return cleaned_data

class SignupForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='Password', min_length=8, max_length=64, widget=forms.PasswordInput)
    name = forms.CharField(label='name',max_length=100)
    year = forms.IntegerField()

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        name = cleaned_data.get('name')
        year = cleaned_data.get('year')
        if username is None:
            self.add_error('username', "Please enter a username")
        if password is None:
            self.add_error('password', "Please enter a password")
        if name is None:
            self.add_error('name', "Please enter a name")
        if year is None:
            self.add_error('year', "Please enter a year")
        return cleaned_data

class NewGroupForm(forms.Form):
    name = forms.CharField(max_length=100)
    size = forms.IntegerField()
    description = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)

    # class Meta:
    #     model = Group
    #     fields = ("name", "size", "description", "loc", "students")
