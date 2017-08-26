import django_tables2 as tables
from .models import Order_List


class OrderTable(tables.Table):
    class Meta:
        model = Order_List
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue', 'style': "font-family:arial;"}
        # template_name = 'django_tables2/bootstrap.html'