"""
Payment models for Talk to Me platform.

This module contains models for managing payments, subscriptions, and transactions.
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum as SQLEnum, Boolean, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class PaymentStatus(str, Enum):
    """Enum for payment statuses."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class SubscriptionStatus(str, Enum):
    """Enum for subscription statuses."""
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PENDING = "pending"


class SubscriptionPlan(str, Enum):
    """Enum for subscription plans."""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    PROFESSIONAL = "professional"


class PaymentMethod(str, Enum):
    """Enum for payment methods."""
    CARD = "card"
    MOBILE_MONEY = "mobile_money"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    FLUTTERWAVE = "flutterwave"
    AIRTIME = "airtime"


class Payment:
    """
    Represents a payment transaction.
    
    Attributes:
        id: Unique identifier for the payment
        user_id: Foreign key to the User
        amount: Payment amount
        currency: Currency code (e.g., 'UGX', 'USD')
        payment_method: Method of payment
        transaction_id: External transaction ID from payment provider
        status: Current payment status
        description: Description of what the payment is for
        receipt_url: URL to payment receipt
        error_message: Error message if payment failed
        metadata: Additional metadata/notes
        created_at: When the payment was created
        updated_at: When the payment was last updated
    """
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='UGX')  # ISO 4217 currency code
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    transaction_id = Column(String(255), nullable=True, unique=True)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    description = Column(Text, nullable=True)
    receipt_url = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)
    metadata = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', backref='payments')
    subscription = relationship('Subscription', uselist=False, back_populates='payment')
    
    def __repr__(self) -> str:
        return f"<Payment id={self.id} amount={self.amount} status={self.status}>"
    
    def to_dict(self) -> dict:
        """Convert payment to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'transaction_id': self.transaction_id,
            'status': self.status.value if self.status else None,
            'description': self.description,
            'receipt_url': self.receipt_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Subscription:
    """
    Represents a user's subscription to a plan.
    
    Attributes:
        id: Unique identifier for the subscription
        user_id: Foreign key to the User
        plan: Subscription plan type
        payment_id: Foreign key to the Payment that initiated this subscription
        status: Current subscription status
        start_date: When the subscription started
        end_date: When the subscription will end
        renewal_date: Next renewal date
        auto_renew: Whether subscription auto-renews
        billing_cycle: Billing cycle length (e.g., 'monthly', 'annual')
        is_trial: Whether this is a trial subscription
        trial_days_remaining: Days remaining in trial
        created_at: When the subscription was created
        cancelled_at: When the subscription was cancelled
    """
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plan = Column(SQLEnum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    payment_id = Column(Integer, ForeignKey('payments.id'), nullable=True)
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    renewal_date = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, default=True)
    billing_cycle = Column(String(20))  # 'monthly', 'annual', etc.
    is_trial = Column(Boolean, default=False)
    trial_days_remaining = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    cancelled_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship('User', backref='subscriptions', uselist=False)
    payment = relationship('Payment', back_populates='subscription')
    
    def __repr__(self) -> str:
        return f"<Subscription id={self.id} user_id={self.user_id} plan={self.plan}>"
    
    def to_dict(self) -> dict:
        """Convert subscription to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan': self.plan.value if self.plan else None,
            'status': self.status.value if self.status else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'renewal_date': self.renewal_date.isoformat() if self.renewal_date else None,
            'auto_renew': self.auto_renew,
            'billing_cycle': self.billing_cycle,
            'is_trial': self.is_trial,
            'trial_days_remaining': self.trial_days_remaining,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Transaction:
    """
    Represents a transaction record for audit/reporting purposes.
    
    Attributes:
        id: Unique identifier for the transaction
        user_id: Foreign key to the User
        transaction_type: Type of transaction (payment, refund, adjustment, etc.)
        amount: Transaction amount
        currency: Currency code
        description: Description of the transaction
        reference_id: Reference to related object (payment_id, subscription_id, etc.)
        balance_before: User's balance before transaction
        balance_after: User's balance after transaction
        status: Transaction status
        metadata: Additional information
        created_at: When the transaction was created
    """
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # payment, refund, adjustment, etc.
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='UGX')
    description = Column(Text, nullable=True)
    reference_id = Column(String(255), nullable=True)  # Link to related object
    balance_before = Column(Float, nullable=True)
    balance_after = Column(Float, nullable=True)
    status = Column(String(20), default='completed')
    metadata = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', backref='transactions')
    
    def __repr__(self) -> str:
        return f"<Transaction id={self.id} user_id={self.user_id} type={self.transaction_type}>"
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'currency': self.currency,
            'description': self.description,
            'reference_id': self.reference_id,
            'balance_before': self.balance_before,
            'balance_after': self.balance_after,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
