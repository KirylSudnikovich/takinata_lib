from django.db import models
from django.contrib.auth.models import User as DUser
from lib.models.user import User as MyUser


class User(DUser, MyUser):
    pass

# Create your models here.
