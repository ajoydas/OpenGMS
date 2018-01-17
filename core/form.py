from django import forms
from django.template import Template
from material import *


class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    layout = Layout('username', 'password')

    template = Template("""
        {% form %}
            {% part form.username prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
            {% part form.password prefix %}<i class="material-icons prefix">lock_open</i>{% endpart %}
        {% endform %}
        """)

    buttonConfirm = Template("""
                <button class="waves-effect waves-light btn" type="submit">Sign In</button>
            """)

    buttonCancel = Template("""
                   <button class="waves-effect waves-light btn" action="" type="submit">Cancel</button>
               """)

    title = "Sign In form"