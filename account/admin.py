from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, RoleUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username_display", 
        "email_display", 
        "first_name_display", 
        "last_name_display", 
        "is_staff_display", 
        "is_superuser_display",
        "is_active_display",
        "last_login_display",
        "date_joined_display"
    )


    @admin.display(description="Nom d'utilisateur")
    def username_display(self, obj):
        return obj.username

    @admin.display(description="Adresse email")
    def email_display(self, obj):
        return obj.email

    @admin.display(description="Prénom")
    def first_name_display(self, obj):
        return obj.first_name

    @admin.display(description="Nom")
    def last_name_display(self, obj):
        return obj.last_name

    @admin.display(description="Staff ?")
    def is_staff_display(self, obj):
        return "Oui" if obj.is_staff else "Non"

    @admin.display(description="Date d’inscription")
    def date_joined_display(self, obj):
        return obj.date_joined.strftime("%d/%m/%Y %H:%M")
    
    @admin.display(description="Superutilisateur ?")
    def is_superuser_display(self, obj):
        return "Oui" if obj.is_superuser else "Non"

    @admin.display(description="Actif ?")
    def is_active_display(self, obj):
        return "Oui" if obj.is_active else "Non"

    @admin.display(description="Dernière connexion")
    def last_login_display(self, obj):
        return obj.last_login.strftime("%d/%m/%Y %H:%M") if obj.last_login else "Jamais"
    
    @admin.register(Role)
    class RoleAdmin(admin.ModelAdmin):
        list_display = ('role',)

    @admin.register(RoleUser)
    class RoleUserAdmin(admin.ModelAdmin):
        list_display = ('user', 'role')
        list_filter = ('role',)
