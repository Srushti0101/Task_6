from datetime import date
from django import forms
from .models import Task


class TaskForm(forms.Form if False else forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. Finish Django project',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe what needs to be done...',
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'},
            ),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        error_messages = {
            'title': {'required': 'Please give your task a title.'},
            'description': {'required': 'Please add a short description.'},
            'due_date': {'required': 'Please choose a due date.',
                         'invalid': 'Enter a valid date.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Required-field validation (explicit)
        for name in ['title', 'description', 'priority', 'due_date']:
            self.fields[name].required = True

        # Highlight invalid fields with Bootstrap's red border
        if self.is_bound:
            for name in self.errors:
                css = self.fields[name].widget.attrs.get('class', '')
                self.fields[name].widget.attrs['class'] = f'{css} is-invalid'

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long.')
        return title

    def clean_due_date(self):
        due = self.cleaned_data['due_date']
        # Allow keeping an old date when editing an existing task
        if due < date.today() and not self.instance.pk:
            raise forms.ValidationError('Due date cannot be in the past.')
        return due