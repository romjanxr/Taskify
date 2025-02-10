from django import forms
from tasks.models import Task, TaskDetail, TaskAsset
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


class TaskAssetForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskAsset
        fields = ['image']
