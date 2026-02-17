"""
Router Tests for LankaCommerce Cloud Multi-Tenancy.

Tests the TenantRouter (cross-schema relation prevention) and verifies
the DATABASE_ROUTERS configuration integrates correctly with
django-tenants' TenantSyncRouter.

Test coverage:
    - TenantRouter.allow_relation: shared↔shared, tenant↔tenant,
      dual↔any, shared↔tenant (blocked)
    - TenantRouter deferred methods: db_for_read, db_for_write,
      allow_migrate all return None
    - _get_app_classification: shared_only, tenant_only, dual, unknown
    - DATABASE_ROUTERS stack: order, count, importability
    - Edge cases: model_name=None in allow_migrate, unknown apps,
      same-app relation, empty hints

Run via Docker:
    docker compose run --rm --no-deps --entrypoint python backend
        -m pytest tests/tenants/test_routers.py -v
"""

import pytest
from django.conf import settings

from apps.tenants.routers import TenantRouter, _get_app_classification


# ════════════════════════════════════════════════════════════════════════
# FIXTURES
# ════════════════════════════════════════════════════════════════════════


class MockMeta:
    """Mock Django model _meta with an app_label."""

    def __init__(self, app_label):
        self.app_label = app_label


class MockObj:
    """Mock Django model instance for router testing."""

    def __init__(self, app_label):
        self._meta = MockMeta(app_label)


@pytest.fixture
def router():
    """Return a TenantRouter instance."""
    return TenantRouter()


# ════════════════════════════════════════════════════════════════════════
# _get_app_classification TESTS
# ════════════════════════════════════════════════════════════════════════


class TestGetAppClassification:
    """Tests for the _get_app_classification helper function."""

    def test_shared_only_apps(self):
        """Shared-only apps should return 'shared_only'."""
        shared_only_labels = ["tenants", "core", "users", "admin", "sessions"]
        for label in shared_only_labels:
            assert _get_app_classification(label) == "shared_only", (
                f"{label} should be shared_only"
            )

    def test_tenant_only_apps(self):
        """Tenant-only apps should return 'tenant_only'."""
        tenant_only_labels = [
            "products", "inventory", "vendors", "sales",
            "customers", "hr", "accounting", "reports",
            "webstore", "integrations",
        ]
        for label in tenant_only_labels:
            assert _get_app_classification(label) == "tenant_only", (
                f"{label} should be tenant_only"
            )

    def test_dual_apps(self):
        """Dual apps (in both lists) should return 'dual'."""
        assert _get_app_classification("contenttypes") == "dual"
        assert _get_app_classification("auth") == "dual"

    def test_unknown_app_defaults_to_shared(self):
        """Unknown apps should default to 'shared_only' (safe fallback)."""
        assert _get_app_classification("nonexistent_app") == "shared_only"
        assert _get_app_classification("some_random_app") == "shared_only"

    def test_third_party_shared_apps(self):
        """Third-party shared apps should return 'shared_only'."""
        labels = [
            "rest_framework", "django_filters", "corsheaders",
            "channels", "django_celery_beat", "django_celery_results",
        ]
        for label in labels:
            assert _get_app_classification(label) == "shared_only", (
                f"{label} should be shared_only"
            )


# ════════════════════════════════════════════════════════════════════════
# allow_relation TESTS
# ════════════════════════════════════════════════════════════════════════


class TestAllowRelation:
    """Tests for TenantRouter.allow_relation."""

    def test_shared_to_shared_allowed(self, router):
        """Relations between shared-only apps should be allowed."""
        obj1 = MockObj("tenants")
        obj2 = MockObj("core")
        assert router.allow_relation(obj1, obj2) is True

    def test_tenant_to_tenant_allowed(self, router):
        """Relations between tenant-only apps should be allowed."""
        obj1 = MockObj("products")
        obj2 = MockObj("sales")
        assert router.allow_relation(obj1, obj2) is True

    def test_dual_to_shared_allowed(self, router):
        """Relations from dual apps to shared-only apps should be allowed."""
        obj1 = MockObj("auth")
        obj2 = MockObj("tenants")
        assert router.allow_relation(obj1, obj2) is True

    def test_dual_to_tenant_allowed(self, router):
        """Relations from dual apps to tenant-only apps should be allowed."""
        obj1 = MockObj("contenttypes")
        obj2 = MockObj("products")
        assert router.allow_relation(obj1, obj2) is True

    def test_shared_to_dual_allowed(self, router):
        """Relations from shared-only to dual apps should be allowed."""
        obj1 = MockObj("users")
        obj2 = MockObj("auth")
        assert router.allow_relation(obj1, obj2) is True

    def test_tenant_to_dual_allowed(self, router):
        """Relations from tenant-only to dual apps should be allowed."""
        obj1 = MockObj("sales")
        obj2 = MockObj("contenttypes")
        assert router.allow_relation(obj1, obj2) is True

    def test_dual_to_dual_allowed(self, router):
        """Relations between dual apps should be allowed."""
        obj1 = MockObj("auth")
        obj2 = MockObj("contenttypes")
        assert router.allow_relation(obj1, obj2) is True

    def test_shared_to_tenant_blocked(self, router):
        """Relations from shared-only to tenant-only should be blocked."""
        obj1 = MockObj("tenants")
        obj2 = MockObj("products")
        assert router.allow_relation(obj1, obj2) is False

    def test_tenant_to_shared_blocked(self, router):
        """Relations from tenant-only to shared-only should be blocked."""
        obj1 = MockObj("products")
        obj2 = MockObj("tenants")
        assert router.allow_relation(obj1, obj2) is False

    def test_same_app_relation_allowed(self, router):
        """Relations within the same app should be allowed."""
        obj1 = MockObj("products")
        obj2 = MockObj("products")
        assert router.allow_relation(obj1, obj2) is True

    def test_cross_schema_multiple_pairs_blocked(self, router):
        """Multiple cross-schema pairs should all be blocked."""
        cross_pairs = [
            ("core", "inventory"),
            ("users", "hr"),
            ("tenants", "webstore"),
            ("core", "integrations"),
            ("users", "accounting"),
        ]
        for shared_app, tenant_app in cross_pairs:
            assert router.allow_relation(
                MockObj(shared_app), MockObj(tenant_app)
            ) is False, f"{shared_app} -> {tenant_app} should be blocked"
            assert router.allow_relation(
                MockObj(tenant_app), MockObj(shared_app)
            ) is False, f"{tenant_app} -> {shared_app} should be blocked"


# ════════════════════════════════════════════════════════════════════════
# DEFERRED METHOD TESTS
# ════════════════════════════════════════════════════════════════════════


class TestDeferredMethods:
    """Tests for methods that should return None (deferred to next router)."""

    def test_db_for_read_returns_none(self, router):
        """db_for_read should return None to defer to search_path."""
        assert router.db_for_read(MockObj("products")) is None

    def test_db_for_write_returns_none(self, router):
        """db_for_write should return None to defer to search_path."""
        assert router.db_for_write(MockObj("products")) is None

    def test_allow_migrate_returns_none(self, router):
        """allow_migrate should return None to defer to TenantSyncRouter."""
        assert router.allow_migrate("default", "products") is None

    def test_allow_migrate_with_model_name_none(self, router):
        """allow_migrate with model_name=None should return None."""
        assert router.allow_migrate("default", "products", model_name=None) is None

    def test_allow_migrate_with_hints(self, router):
        """allow_migrate with hints should still return None."""
        assert router.allow_migrate(
            "default", "products", model_name="Product",
            hints={"instance": None}
        ) is None


# ════════════════════════════════════════════════════════════════════════
# DATABASE_ROUTERS CONFIGURATION TESTS
# ════════════════════════════════════════════════════════════════════════


class TestDatabaseRoutersConfig:
    """Tests for the DATABASE_ROUTERS setting."""

    def test_two_routers_configured(self):
        """Exactly two routers should be configured."""
        assert len(settings.DATABASE_ROUTERS) == 2

    def test_tenant_router_is_first(self):
        """TenantRouter should be first in the stack."""
        assert settings.DATABASE_ROUTERS[0] == "apps.tenants.routers.TenantRouter"

    def test_tenant_sync_router_is_second(self):
        """TenantSyncRouter should be second in the stack."""
        assert settings.DATABASE_ROUTERS[1] == "django_tenants.routers.TenantSyncRouter"

    def test_routers_importable(self):
        """Both routers should be importable."""
        from importlib import import_module
        for router_path in settings.DATABASE_ROUTERS:
            module_path, class_name = router_path.rsplit(".", 1)
            mod = import_module(module_path)
            cls = getattr(mod, class_name)
            assert cls is not None, f"Failed to import {router_path}"


# ════════════════════════════════════════════════════════════════════════
# EDGE CASE TESTS
# ════════════════════════════════════════════════════════════════════════


class TestEdgeCases:
    """Tests for router edge cases."""

    def test_unknown_app_to_unknown_app_allowed(self, router):
        """Two unknown apps (both default to shared_only) should be allowed."""
        obj1 = MockObj("unknown_app_a")
        obj2 = MockObj("unknown_app_b")
        assert router.allow_relation(obj1, obj2) is True

    def test_unknown_app_to_tenant_blocked(self, router):
        """Unknown app (defaults shared_only) to tenant app should be blocked."""
        obj1 = MockObj("unknown_app")
        obj2 = MockObj("products")
        assert router.allow_relation(obj1, obj2) is False

    def test_unknown_app_to_dual_allowed(self, router):
        """Unknown app (defaults shared_only) to dual app should be allowed."""
        obj1 = MockObj("unknown_app")
        obj2 = MockObj("auth")
        assert router.allow_relation(obj1, obj2) is True

    def test_empty_hints_in_allow_relation(self, router):
        """allow_relation with explicit empty hints should work."""
        obj1 = MockObj("products")
        obj2 = MockObj("sales")
        assert router.allow_relation(obj1, obj2, **{}) is True

    def test_db_for_read_with_hints(self, router):
        """db_for_read with hints should still return None."""
        result = router.db_for_read(MockObj("products"), instance=None)
        assert result is None

    def test_db_for_write_with_hints(self, router):
        """db_for_write with hints should still return None."""
        result = router.db_for_write(MockObj("products"), instance=None)
        assert result is None
