"""Base Celery task classes with tenant context support."""

import logging

from celery import Task
from django_tenants.utils import schema_context

logger = logging.getLogger(__name__)


class TenantTask(Task):
    """
    Base task class for tasks that operate within a single tenant schema.

    Subclass tasks that need tenant context:

        @shared_task(base=TenantTask)
        def my_task(self, tenant_schema: str, ...):
            # connection.schema_name is already set
            MyModel.objects.filter(...)

    The ``tenant_schema`` argument MUST be the first positional argument.
    The task is called as:

        my_task.delay(connection.schema_name, other_arg, ...)

    or:

        my_task.delay(tenant_schema=connection.schema_name, other_arg=...)
    """

    abstract = True

    def __call__(self, tenant_schema: str, *args, **kwargs):
        with schema_context(tenant_schema):
            return super().__call__(tenant_schema, *args, **kwargs)
