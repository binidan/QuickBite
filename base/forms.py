from django.forms import ModelForm
from .models import Customer, Address
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['customer']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UpdateForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'