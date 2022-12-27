from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user (self, cpf, password = None, **extra_fields):
        if not cpf:
            raise ValueError('informe o cpf')
        user = self.model(cpf = cpf, **extra_fields)
        user.set_password(password)
        user.save(using = self.db)
    
    def create_superuser(self, cpf, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(cpf, password, **extra_fields)