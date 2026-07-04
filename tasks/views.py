from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Case,When,Value,IntegerField
from .forms import RegisterForm
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404
from .models import Tasks, SubTask
import json

def login_page(request):
    
    if request.method == "POST":
        login_input = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user_obj = User.objects.get(email=login_input)
            username = user_obj.username
        except User.DoesNotExist:
            username = login_input
            
        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect("/login/")
        elif user.username == "vrundkan":
            login(request, user)
            return redirect("/pending-approval/")
        else:
            login(request, user)
            return redirect("/success/")
        
    return render(request, "tasks/login_page.html")

def register_page(request):
        
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            user = User.objects.filter(username = username)
            
            if user.exists():
                messages.info(request, "Username already taken")
                return redirect("/register/")
            
            user = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
            )
            user.set_password(password)
            user.is_active = False
            user.save()
            
            messages.success(request, "Request sent successfully")
            return redirect("/register/")
    else:
        form = RegisterForm()
        
    return render(request, "tasks/register_page.html", {
        "form": form
    })

def logout_page(request):
    logout(request)
    return redirect("/login/")

@login_required(login_url="/login/")
def success_url(request):
    tasks = Tasks.objects.annotate(
        order = Case(
            When(status="PENDING", then=Value(1)),
            When(status="REVIEW", then=Value(2)),
            When(status="COMPLETED", then=Value(3))
        )
    )
    tasks = tasks.filter(assigned_to=request.user)
    subtasks = SubTask.objects.all()
    return render(request, "tasks/success_login.html", {
        "tasks": tasks,
        "subtasks": subtasks
    })

@login_required(login_url="/login/")
def pendingUser(request):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    users = User.objects.filter(
        is_active = False
    )
    return render(request, "tasks/approval_page.html", {
        "users": users
    })

@login_required(login_url="/login/")
def approve_request(request,id):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    user = get_object_or_404(User,id=id)
    group = Group.objects.get(name="TaskDoer")
    user.is_active = True
    user.groups.add(group)
    user.save()
    return redirect("/pending-approval/")

@login_required(login_url="/login/")
def reject_request(request, id):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    user = User.objects.get(id = id)
    user.delete()
    return redirect("/pending-approval/")

@login_required(login_url="/login/")
def AllUsers(request):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    users = User.objects.all()
    return render(request, "tasks/all_users.html", {
        "users": users
    })
    
@login_required(login_url="/login/")
def AllTasks(request):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    tasks = Tasks.objects.annotate(
        order = Case(
            When(status="PENDING", assigned_to=None, then=Value(1)),
            When(status="PENDING", then=Value(2)),
            When(status="REVIEW", then=Value(3)),
            When(status="COMPLETED", then=Value(4)),
            default=Value(5),
            output_field=IntegerField(),
        )
    ).order_by("order")
    subtasks = SubTask.objects.all()
    users = User.objects.all()
    
    if request.method == "POST":
        users = User.objects
    return render(request, "tasks/all_tasks.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "users": users
    })

@login_required(login_url="/login/")
def CreateTasks(request):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    if request.method == "POST":
        subtasks = json.loads(
            request.POST.get("list-subtasks")
        )
        task_title = request.POST.get("title")
        task_description = request.POST.get("description")
        task_deadline = parse_datetime(request.POST.get("deadline"))
        creator = request.user
        
        if task_title == "" or task_description == "":
            messages.error(request, "Task title or description cannot be empty.")
            return redirect("/create-tasks/")
        
        task = Tasks.objects.create(
            title = task_title,
            description = task_description,
            created_by = creator,
            deadline = task_deadline
        )
        
        for subtask in subtasks:
            SubTask.objects.create(
                task = task,
                title = subtask
            )
        
        messages.success(request, "Task created successfully.")
        return render(request, "tasks/create_task.html")

    return render(request, "tasks/create_task.html")

@login_required(login_url="/login/")
def EditTask(request, id):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    task = Tasks.objects.get(id = id)
    subtasks = SubTask.objects.filter(task = task)
    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.deadline = parse_datetime(request.POST.get("deadline"))
        
        task.save()
        
        SubTask.objects.filter(
            task = task
        ).delete()
        
        subtasks = json.loads(
            request.POST.get(
                "list-subtasks",
                "[]",
            )
        )
        
        subtasksComplete = json.loads(
            request.POST.get(
                "list-subtasks-complete",
                "[]",
            )
        )

        index = 0
        for title in subtasks:
            SubTask.objects.create(
                task = task,
                title = title,
                completed = subtasksComplete[index]
            )
            index += 1
        return redirect("/all-tasks/")
    
    subtasks_json = json.dumps([
        subtask.title
        for subtask in subtasks
    ])
    subtasksComplete_json = json.dumps([
        subtask.completed
        for subtask in subtasks
    ])
    return render(request, "tasks/create_task.html", {
        "task": task,
        "subtasks_json": subtasks_json,
        "subtasksComplete_json": subtasksComplete_json
    })
    
@login_required(login_url="/login/")
def ApproveTasks(request,id):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    tasks = Tasks.objects.all()
    subtasks = SubTask.objects.all()
    users = User.objects.all()
    
    if request.method == "POST":
        
        user_id = request.POST.get(f"assigned-user-{id}")
        task = Tasks.objects.get(id = id)
        if user_id in ["",'0',None]:
            task.assigned_to = None
            task.status = "PENDING"
            task.save()
        
        else:
            task.assigned_to = User.objects.get(id = user_id)
            task.status = "PENDING"
            task.save()
            
        return redirect("/all-tasks/")
    
    return render(request, "tasks/all_tasks.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "users": users
    })
    
@login_required(login_url="/login/")
def RemoveTask(request,id):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    if request.method == "POST":
        task = Tasks.objects.get(id = id)
        task.delete()
        
        return redirect("/all-tasks/")

@login_required(login_url="/login/")    
def CompletedTasks(request):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    tasks = Tasks.objects.filter(status = "COMPLETED")
    subtasks = SubTask.objects.all()
    users = User.objects.all()
    
    return render(request, "tasks/all_tasks.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "users": users
    })

@login_required(login_url="/login/")
def UnassignedTasks(request):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    tasks = Tasks.objects.filter(assigned_to__isnull = True)
    subtasks = SubTask.objects.all()
    users = User.objects.all()
    
    return render(request, "tasks/all_tasks.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "users": users
    })
    
@login_required(login_url="/login/")    
def InreviewTasks(request):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    tasks = Tasks.objects.filter(status = "REVIEW")
    subtasks = SubTask.objects.all()
    users = User.objects.all()
    
    return render(request, "tasks/all_tasks.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "users": users
    })

@login_required(login_url="/login/")
def AssignedTasks(request):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    tasks = Tasks.objects.filter(assigned_to__isnull = False)
    subtasks = SubTask.objects.all()
    users = User.objects.all()
    
    return render(request, "tasks/all_tasks.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "users": users
    })

def DoTasks(request):
    tasks = Tasks.objects.filter(assigned_to = request.user, status="PENDING")
    subtasks = SubTask.objects.all()
    
    tasks_json = json.dumps([
        task.id
        for task in tasks
    ])
    
    task_list = []
    for task in tasks:
        subtasks_list = []
        for subtask in subtasks:
            if subtask.task == task:
                subtasks_list.append(subtask.id)
        task_list.append(subtasks_list)
    
    subtasks_json = json.dumps([
        task
        for task in task_list
    ])
    
    return render(request, "tasks/do_tasks.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "subtasks_json": subtasks_json,
        "tasks_json": tasks_json
    })
    
def DoSubTask(request, id):
    subtask = SubTask.objects.get(id = id)
    if (subtask.completed):
        subtask.completed = False
    else:
        subtask.completed = True
    subtask.save()
    
    return redirect("/do-tasks/")

def PutInReview(request,id):
    task = Tasks.objects.get(id = id)
    subtasks = SubTask.objects.filter(task = task)
    
    for subtask in subtasks:
        if subtask.completed == False:
            if request.user.username == "vrundkan":
                messages.error(request,"All subtasks are not completed")
                return redirect("/do-tasks/")
            messages.error(request," All subtasks are not completed")
            return redirect("/do-my-tasks/")
    task.status = "REVIEW"
    task.save()
    
    if request.user.username == "vrundkan":
        return redirect("/all-tasks/")
    return redirect("/my-tasks/")

@login_required(login_url="/login/")
def ReviewList(request):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    tasks = Tasks.objects.filter(status = "REVIEW")
    subtasks = SubTask.objects.all()
    users = User.objects.all()
    
    tasks_json = json.dumps([
        task.id
        for task in tasks
    ])
    
    task_list = []
    for task in tasks:
        subtasks_list = []
        for subtask in subtasks:
            if subtask.task == task:
                subtasks_list.append(subtask.id)
        task_list.append(subtasks_list)
    
    subtasks_json = json.dumps([
        task
        for task in task_list
    ])
    
    return render(request, "tasks/review_tasks.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "users": users,
        "tasks_json": tasks_json,
        "subtasks_json": subtasks_json
    })
    
@login_required(login_url="/login/")
def ApprovedReviewedTasks(request,id):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    tasks = Tasks.objects.all()
    subtasks = SubTask.objects.all()
    users = User.objects.all()
    
    if request.method == "POST":
        
        user_id = request.POST.get(f"assigned-user-{id}")
        task = Tasks.objects.get(id = id)
        if user_id in ["",'0',None]:
            task.assigned_to = None
            task.status = "PENDING"
            task.save()
        
        else:
            task.assigned_to = User.objects.get(id = user_id)
            task.status = "PENDING"
            task.save()
            
        return redirect("/all-tasks/")
    
    return render(request, "tasks/all_tasks.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "users": users
    })
    
def DoSubTask2(request, id):
    subtask = SubTask.objects.get(id = id)
    if (subtask.completed):
        subtask.completed = False
    else:
        subtask.completed = True
    subtask.save()
    
    return redirect("/review-list/")

@login_required(login_url="/login/")
def MarkAsCompleted(request,id):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    
    task = Tasks.objects.get(id = id)
    task.status = "COMPLETED"
    task.save()
    
    return redirect("/all-tasks/")

@login_required(login_url="/login/")
def RemoveUser(request,id):
    if not request.user.groups.filter(name="TaskAssigner").exists():
        return redirect("/login/")
    if request.method != "POST":
        return redirect("/all-tasks/")
    user = User.objects.get(id = id)
    if user.username == "vrundkan":
        messages.error(request,"You cannot delete a SUPERUSER!")
        return redirect("/all-users/")
    user.delete()
    messages.info(request,"User deleted successfully")
    return redirect("/all-users/")
    
@login_required(login_url="/login/")
def DoingTask(request):
    tasks = Tasks.objects.filter(assigned_to = request.user, status="PENDING")
    subtasks = SubTask.objects.all()
    
    tasks_json = json.dumps([
        task.id
        for task in tasks
    ])
    
    task_list = []
    for task in tasks:
        subtasks_list = []
        for subtask in subtasks:
            if subtask.task == task:
                subtasks_list.append(subtask.id)
        task_list.append(subtasks_list)
    
    subtasks_json = json.dumps([
        task
        for task in task_list
    ])
    
    return render(request, "tasks/user_task.html", {
        "tasks": tasks,
        "subtasks": subtasks,
        "subtasks_json": subtasks_json,
        "tasks_json": tasks_json
    })
    
@login_required(login_url="/login/")
def UserTasks(request,slug):
    user = User.objects.get(username=slug)
    tasks = Tasks.objects.filter(assigned_to=user)  
    tasks = tasks.annotate(
        order = Case(
            When(status="PENDING", then=Value(1)),
            When(status="REVIEW", then=Value(2)),
            When(status="COMPLETED", then=Value(3))
        )
    )
    subtasks = SubTask.objects.all()
    
    return render(request, "tasks/user_task_page.html", {
        "tasks": tasks,
        "subtasks": subtasks
    })