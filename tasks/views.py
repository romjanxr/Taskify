from django.shortcuts import render, redirect
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.base import ContextMixin
from tasks.forms import TaskModelForm, TaskDetailModelForm
from tasks.models import Task, Project
from users.views import is_admin

User = get_user_model()


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


def is_employee(user):
    return user.groups.filter(name='Employee').exists()


@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('employee-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')


@login_required
@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING')),
    )

    # Retriving task data
    tasks = Task.objects.select_related(
        'details').prefetch_related('assigned_to').all()

    context = {
        "tasks": tasks,
        "counts": counts
    }
    return render(request, "dashboard/manager_dashboard.html", context)


@login_required
@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request, "dashboard/employee-dashboard.html")


class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name = 'task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get(
            'task_detail_form', TaskDetailModelForm())
        if self.request.user.groups.filter(name="Admin").exists():
            context["base_template"] = "admin/admin-dashboard.html"
        else:
            context["base_template"] = "dashboard/dashboard.html"
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            context = self.get_context_data(
                task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)


class TaskDetail(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # {"task": task}
        # {"task": task, 'status_choices': status_choices}
        context['status_choices'] = Task.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)


class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        # print(context)
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(
                instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', self.object.id)
        return redirect('update-task', self.object.id)


def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager-dashboard')


@permission_required('tasks.view_task', login_url='no-permission')
def view_task(request):
    type = request.GET.get('type', 'all')

    base_query = Task.objects.select_related(
        'details').prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()

    context = {
        "tasks": tasks
    }

    if request.user.groups.filter(name="Admin").exists():
        context["base_template"] = "admin/admin-dashboard.html"
    else:
        context["base_template"] = "dashboard/dashboard.html"

    return render(request, "task-list.html", context)
