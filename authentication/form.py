from material import *
from django.template import Template
from . import demo as forms


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=((None, ''), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')

    layout = Layout('username', 'email',
                    Row('password', 'password_confirm'),
                    Fieldset('Pesonal details',
                             Row('first_name', 'last_name'),
                             'gender', 'receive_news', 'agree_toc'))

    template = Template("""
    {% form %}
        {% part form.username prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
        {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.password prefix %}<i class="material-icons prefix">lock_open</i>{% endpart %}
    {% endform %}
    """)

    buttonConfirm = Template("""
            <button class="waves-effect waves-light btn" type="submit">Sign In</button>
        """)

    buttonCancel = Template("""
               <button class="waves-effect waves-light btn" action="" type="submit">Cancel</button>
           """)

    title = "Registration form"
