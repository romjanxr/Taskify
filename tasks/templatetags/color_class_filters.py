from django import template
from tasks.models import Task, TaskDetail

register = template.Library()

PRIORITY_COLORS = {
    TaskDetail.HIGH: 'bg-red-100 text-red-800',  # High
    TaskDetail.MEDIUM: 'bg-yellow-100 text-yellow-800',  # Medium
    TaskDetail.LOW: 'bg-blue-100 text-blue-800',  # Low
}

STATUS_COLORS = {
    Task.PENDING: 'bg-purple-100 text-purple-800',
    Task.IN_PROGRESS: 'bg-yellow-100 text-yellow-800',
    Task.COMPLETED: 'bg-green-100 text-green-800',
}


@register.filter(name='priority_color_class')
def priority_color_class(priority):
    # Default color if priority not found
    return PRIORITY_COLORS.get(priority, 'bg-gray-100 text-gray-800')


@register.filter(name='status_color_class')
def status_color_class(priority):
    # Default color if priority not found
    return STATUS_COLORS.get(priority, 'bg-gray-100 text-gray-800')
