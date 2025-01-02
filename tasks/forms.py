from django import forms
from tasks.models import Task, TaskDetail
from core.mixins import StyledFormMixin


# Django Model Form


class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to', 'project']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }


class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes']
