"""
Core models module.

Will contain:
    - BaseModel: UUID primary key, timestamps
    - TimeStampedMixin: created_at, updated_at
    - SoftDeleteMixin: is_deleted, deleted_at
    - TenantAwareMixin: Tenant scoping

These base models will be implemented in Phase 3.
"""

# from django.db import models  # noqa: ERA001
