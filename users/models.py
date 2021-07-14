from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
