from django.db import models
from datetime import date
from django.db.models.signals import post_save
# Create your models here.
class Signup(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)


class Address(models.Model):
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    country=models.CharField(max_length=50)


class Profile(models.Model):
    user=models.OneToOneField(Signup,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile', default='pic.jpg')
    dob = models.DateField(default=date.today)
    choices=(('Male','Male'),('Female','Female'),('Other','Other'))
    gender = models.CharField(max_length=9,choices=choices)
    friends=models.ManyToManyField("Profile",blank=True)



def make_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(make_profile,sender=Signup)


def update_address(sender,instance,created,**kwargs):
    if created:
        print(instance)
        Profile.objects.create(paddr=instance)
        Profile.objects.create(company=instance)
post_save.connect(update_address,sender=Address)
class FriendRequest(models.Model):
    to_user=models.ForeignKey(Signup,related_name="to_user",on_delete=models.CASCADE)
    from_user=models.ForeignKey(Signup,related_name="from_user",on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"From {self.to_user} ,to {self.from_user}"


##user=admin pass=12345@admin
