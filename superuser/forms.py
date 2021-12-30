from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

# from .models import about
from django.contrib.admin import (
      widgets,
      site as admin_site
    )

def GenForm(Model,listHiddenfield=[],disablefield=[]):
    data = {field:forms.HiddenInput() for field in listHiddenfield}
    class newform(forms.ModelForm):
        class Meta:
            model = Model
            exclude = ('id',)
            widgets = data
        def __init__(self, *args, **kwargs):
            super(newform, self).__init__(*args, **kwargs)
            for f in Model._meta.fields:
                try :
                    self.fields[f.name].widget.attrs['placeholder'] = f"enter here {f.verbose_name}".title  ()
                except:
                    pass
                if f.name in disablefield:
                    self.fields[f.name].widget.attrs['readonly'] = True
                if "DateTimeField" in str(type(f)):
                    try:
                        self.fields[f.name].widget.attrs['class'] = 'vDateTime'
                    except Exception:
                        pass
                if "DateField" in str(type(f)):
                    try:
                        self.fields[f.name].widget.attrs['class'] = 'vDateField'
                    except Exception:
                        pass
                if "ForeignKey" in str(type(f)):
                    try:
                        self.fields[f.name].widget  = widgets.RelatedFieldWidgetWrapper(
                        self.fields[f.name].widget,
                        self.instance._meta.get_field(f.name).remote_field,
                        admin_site
                    )
                    except Exception:
                        pass 
                           
    return newform  