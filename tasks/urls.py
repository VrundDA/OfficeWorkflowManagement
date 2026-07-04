from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),
    path("my-tasks/", views.success_url, name="success_page"),
    path("logout/", views.logout_page, name="logout_page"),
    path("pending-approval/", views.pendingUser, name="pending_user_page"),
    path("approval/<int:id>", views.approve_request, name="approving"),
    path("rejection/<int:id>", views.reject_request, name="rejecting"),
    path("all-users/", views.AllUsers, name="all_users"),
    path("all-tasks/", views.AllTasks, name="all_tasks"),
    path("create-tasks/", views.CreateTasks, name="create_tasks"),
    path("create-tasks/<int:id>", views.EditTask, name="edit_task"),
    path("approve/<int:id>", views.ApproveTasks, name="approve-tasks"),
    path("remove/<int:id>", views.RemoveTask, name="remove-task"),
    path("completed/", views.CompletedTasks, name="completed-tasks"),
    path("unassigned/", views.UnassignedTasks, name="unassigned-tasks"),
    path("in-review/", views.InreviewTasks, name="in-review-tasks"),
    path("assigned/", views.AssignedTasks, name="assigned-tasks"),
    path("do-tasks/", views.DoTasks, name="do-tasks"),
    path("complete-subtask/<int:id>", views.DoSubTask, name="do-subtask"),
    path("put-in-review/<int:id>", views.PutInReview, name="put-in-review"),
    path("review-list/", views.ReviewList, name="review-list"),
    path("approve/reviewed/<int:id>", views.ApprovedReviewedTasks, name="approve-reviewed-tasks"),
    path("complete-subtask-2/<int:id>", views.DoSubTask2, name="do-subtask-2"),
    path("mark-task-as-completed/<int:id>", views.MarkAsCompleted, name="mark-as-completed"),
    path("password-reset/",auth_views.PasswordResetView.as_view(template_name="tasks/password_reset.html"),name="password_reset"),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="tasks/password_reset_done.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="tasks/password_reset_form.html"),name="password_reset_confirm"),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="tasks/password_reset_complete.html"),name="password_reset_complete"),
    path("remove-user/<int:id>",views.RemoveUser, name="removing-user"),
    path("do-my-tasks/",views.DoingTask,name="doing-user-tasks"),
    path("user/<slug:slug>/", views.UserTasks, name="user-tasks-display")
]
