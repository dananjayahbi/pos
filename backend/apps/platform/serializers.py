"""Platform management serializers."""

from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from apps.platform.models import PlatformUser, SubscriptionPlan
from apps.tenants.models import Domain, Tenant


# ─── Tenant Serializers ───────────────────────────────────────────────────────

class DomainSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["id", "domain", "is_primary", "domain_type", "is_verified", "ssl_status"]


class TenantListSerializer(serializers.ModelSerializer):
    """Compact tenant info for list views."""

    primary_domain = serializers.SerializerMethodField()
    days_in_trial = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = [
            "id",
            "name",
            "slug",
            "business_type",
            "industry",
            "status",
            "on_trial",
            "paid_until",
            "days_in_trial",
            "contact_email",
            "contact_phone",
            "city",
            "created_on",
            "primary_domain",
        ]

    def get_primary_domain(self, obj):
        d = Domain.objects.filter(tenant=obj, is_primary=True).first()
        return d.domain if d else None

    def get_days_in_trial(self, obj):
        if not obj.on_trial or not obj.paid_until:
            return None
        delta = obj.paid_until - timezone.now().date()
        return delta.days


class TenantDetailSerializer(TenantListSerializer):
    """Full tenant info for detail views."""

    domains = DomainSummarySerializer(many=True, read_only=True, source="domain_set")

    class Meta(TenantListSerializer.Meta):
        fields = TenantListSerializer.Meta.fields + [
            "schema_name",
            "contact_name",
            "business_registration_number",
            "address_line_1",
            "address_line_2",
            "district",
            "province",
            "postal_code",
            "language",
            "timezone",
            "onboarding_step",
            "onboarding_completed",
            "domains",
        ]


class TenantStatusUpdateSerializer(serializers.Serializer):
    """Payload for suspend/reactivate/archive actions."""

    status = serializers.ChoiceField(choices=["active", "suspended", "archived"])
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)


# ─── PlatformUser Serializers ─────────────────────────────────────────────────

class PlatformUserListSerializer(serializers.ModelSerializer):
    """Compact platform user info."""

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = PlatformUser
        fields = [
            "id",
            "email",
            "full_name",
            "role",
            "is_active",
            "date_joined",
            "last_login",
        ]


class PlatformUserCreateSerializer(serializers.ModelSerializer):
    """Create a new platform staff member."""

    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = PlatformUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
            "confirm_password",
        ]

    def validate_role(self, value):
        # Only super_admin can create another super_admin — enforced in the view
        return value

    def validate(self, data):
        if data["password"] != data.pop("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        try:
            validate_password(data["password"])
        except Exception as exc:
            raise serializers.ValidationError({"password": list(exc.messages)}) from exc
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = PlatformUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PlatformUserUpdateSerializer(serializers.ModelSerializer):
    """Update a platform staff member (role, name, active status)."""

    class Meta:
        model = PlatformUser
        fields = ["first_name", "last_name", "role", "is_active"]


# ─── Subscription Serializers ─────────────────────────────────────────────────

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Subscription plan serializer."""

    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "monthly_price",
            "annual_price",
            "is_active",
            "max_users",
            "max_products",
        ]
