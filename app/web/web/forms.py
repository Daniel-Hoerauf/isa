from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class NewGroupForm(forms.Form):
    name = forms.CharField(max_length=100)
    size = forms.IntegerField()
    description = forms.CharField(max_length=100, default='Come and learn!')
    loc = forms.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    students = forms.ManyToManyField(Student)

    class Meta:
        model = Group
        fields = ("name", "size", "description", "loc", "students")
