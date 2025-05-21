from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class RoleManager(models.Manager):
    def get_by_natural_key(self, role):
        return self.get(role=role)

class Role(models.Model):
    role = models.CharField("Nom du rôle", max_length=30, unique=True)

    objects = RoleManager()

    class Meta:
        db_table = "roles"
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
        ordering = ["role"]

    def __str__(self):
        return self.role
    
    def natural_key(self):
        return (self.role,)

class RoleUserManager(models.Manager):
    def get_by_natural_key(self, user_username, role_name):
        return self.get(
            user__username=user_username,
            role__role=role_name
        )

class RoleUser(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="role_users")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_users")

    objects = RoleUserManager()

    class Meta:
        db_table = "role_user"
        unique_together = ("user", "role")
        verbose_name = "Association rôle/utilisateur"
        verbose_name_plural = "Associations rôle/utilisateur"

    def __str__(self):
        return f"{self.user.username} - {self.role.role}"

    def natural_key(self):
        return (self.user.username, self.role.role)
    natural_key.dependencies = ['account.customuser', 'account.role']


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    
    roles = models.ManyToManyField(
        Role,
        through='RoleUser',
        related_name='users',
        blank=True,
    )

    def natural_key(self):
        return (self.username,)
    
    def has_role(self, role_name: str) -> bool:
        return self.roles.filter(role=role_name).exists()
    
    @property
    def is_admin(self):
        return self.is_authenticated and self.roles.filter(role="Admin").exists()

