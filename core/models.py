from django.db import models


class AuditLog(models.Model):

    ACTION_CHOICES = (
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("borrow", "Borrow"),
        ("return", "Return"),
    )

    user = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    model_name = models.CharField(max_length=100, blank=True)

    object_id = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
