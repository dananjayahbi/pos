"""
POS Payment serializers.

Provides serialization for POSPayment model and
request/response payloads for payment operations.
"""

from decimal import Decimal

from rest_framework import serializers

from apps.pos.constants import PAYMENT_METHOD_CHOICES
from apps.pos.payment.models import POSPayment


class POSPaymentSerializer(serializers.ModelSerializer):
    """Full payment representation."""

    processed_by_email = serializers.EmailField(
        source="processed_by.email", read_only=True, default=None
    )

    class Meta:
        model = POSPayment
        fields = [
            "id",
            "cart",
            "processed_by",
            "processed_by_email",
            "method",
            "amount",
            "status",
            "amount_tendered",
            "change_due",
            "reference_number",
            "authorization_code",
            "transaction_id",
            "paid_at",
            "voided_at",
            "notes",
            "created_on",
            "updated_on",
        ]
        read_only_fields = [
            "id",
            "status",
            "change_due",
            "paid_at",
            "voided_at",
            "created_on",
            "updated_on",
        ]


class PaymentRequestSerializer(serializers.Serializer):
    """Validates an incoming single-payment request."""

    cart = serializers.UUIDField()
    payment_method = serializers.ChoiceField(choices=PAYMENT_METHOD_CHOICES)
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.01")
    )
    tendered_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    reference_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    authorization_code = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )


class SplitPaymentItemSerializer(serializers.Serializer):
    """One leg of a split payment."""

    payment_method = serializers.ChoiceField(choices=PAYMENT_METHOD_CHOICES)
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.01")
    )
    tendered_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    reference_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    authorization_code = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )


class SplitPaymentRequestSerializer(serializers.Serializer):
    """Validates split-payment requests."""

    cart = serializers.UUIDField()
    payments = SplitPaymentItemSerializer(many=True, min_length=2)

    def validate_payments(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Split payment requires at least two payment methods."
            )
        return value


class PaymentRefundRequestSerializer(serializers.Serializer):
    """Validates refund requests."""

    refund_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.01")
    )
    reason = serializers.CharField(max_length=500, required=False)


class PaymentCompleteRequestSerializer(serializers.Serializer):
    """Request to finalize a pending payment / transaction."""

    payment_id = serializers.UUIDField()
