from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ACCOUNT_TYPES = [
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='twitter')
    avatar_letter = models.CharField(max_length=1, blank=True)

    def save(self, *args, **kwargs):
        if not self.avatar_letter and self.user.username:
            self.avatar_letter = self.user.username[0].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.get_account_type_display()})"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

class UserLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_users')
    liked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'liked_user')
