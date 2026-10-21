from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='user_id')
    username = models.CharField(max_length=64, unique=True, db_column='user_username')
    email = models.CharField(max_length=255, null=True, blank=True, db_column='user_email')
    last_name = models.CharField(max_length=100, db_column='user_last_name')
    first_name = models.CharField(max_length=100, db_column='user_first_name')
    middle_name = models.CharField(max_length=100, null=True, blank=True, db_column='user_middle_name')
    password = models.TextField(db_column='user_password')
    active = models.BooleanField(default=True, db_column='user_active')
    created_at = models.DateTimeField(auto_now_add=True, db_column='user_created')
    first_login_at = models.DateTimeField(null=True, blank=True, db_column='user_first_login')
    class Meta:
        managed = False
        db_table = 'users'

class Role(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='role_id')
    name = models.CharField(max_length=128, unique=True, db_column='role_name')
    class Meta:
        managed = False
        db_table = 'roles'

class Module(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='module_id')
    name = models.CharField(max_length=255, unique=True, db_column='module_name')
    class Meta:
        managed = False
        db_table = 'modules'

class UserRole(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'role_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = 'user_roles'
