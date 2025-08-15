from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	phone = models.CharField(max_length=20, blank=True, null=True)
	is_verified = models.BooleanField(default=False)
	verification_code = models.CharField(max_length=64, blank=True, null=True)
	verification_expiry = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return f"Profile: {self.user.username}"
