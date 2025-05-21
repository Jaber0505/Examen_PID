from django.urls import path
from account.views import auth, assign_role, dashboard

app_name = "account"

urlpatterns = [
    path("register/", auth.register, name="register"),
    path("login/", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),
    path("profile/", auth.profile_view, name="profile"),
    path("profile/edit/", auth.edit_profile, name="edit-profile"),
    path("profile/delete/", auth.delete_account, name="delete-account"),
    
    path('users/', assign_role.user_list, name='user_list'),
    path('user/<int:user_id>/assign-roles/', assign_role.assign_roles_view, name='assign_roles'),
    
    path("dashboard/", dashboard.dashboard, name="dashboard"),
    path("dashboard/roles/", dashboard.dashboard_roles, name="dashboard-roles"),
    path("dashboard/roles/edit/<int:user_id>/", dashboard.dashboard_edit_role, name="dashboard-edit-role"),
]