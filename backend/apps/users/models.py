"""
Users models module.

Will contain:
    - User: Custom user model (AbstractBaseUser)
    - UserProfile: Extended user information
    - UserPreferences: User settings
    - LoginHistory: Authentication audit

Custom user features:
    - Email as username (USERNAME_FIELD = 'email')
    - Phone support (validated +94 format)
    - Tenant awareness (ForeignKey to Tenant)
    - Role assignment (ManyToMany to Role)

These models will be implemented in Phase 3.
"""

# from django.contrib.auth.models import AbstractBaseUser  # noqa: ERA001
