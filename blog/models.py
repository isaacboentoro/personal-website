from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(
        help_text="Write in Markdown. Use ```python for code blocks."
    )
    private = models.BooleanField(
        default=False,
        help_text="Require a password to view this post.",
    )
    password = models.CharField(
        max_length=128,
        blank=True,
        help_text="Password for private posts (hashed on save).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.password and not self._is_hashed(self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    @staticmethod
    def _is_hashed(value):
        known = (
            "pbkdf2_",
            "bcrypt",
            "argon2",
            "sha1",
            "md5",
            "crypt",
        )
        return any(value.startswith(p) for p in known)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def check_password(self, raw):
        return check_password(raw, self.password)

    def set_password(self, raw):
        self.password = make_password(raw)

    def __str__(self):
        return self.title
