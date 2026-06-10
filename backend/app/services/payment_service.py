"""
Payment Service module.

Handles payment processing via Flutterwave.
"""

import logging
import os
import requests
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for payment processing."""
    
    def __init__(self):
        """Initialize payment service."""
        self.public_key = os.environ.get('FLW_PUBLIC_KEY')
        self.secret_key = os.environ.get('FLW_SECRET_KEY')
        self.base_url = 'https://api.flutterwave.com/v3'
        self.headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'
        }
    
    def initiate_payment(self, amount: float, email: str, user_id: int, currency: str = 'UGX') -> Optional[Dict]:
        """
        Initiate a payment transaction.
        
        Args:
            amount: Payment amount
            email: User email
            user_id: User ID
            currency: Currency code
        
        Returns:
            Payment initialization response
        """
        try:
            payload = {
                'tx_ref': f'user_{user_id}_{int(__import__("time").time())}',
                'amount': amount,
                'currency': currency,
                'customer': {
                    'email': email
                },
                'customizations': {
                    'title': 'Talk to Me Subscription',
                    'description': 'Mental Health Support Platform'
                }
            }
            
            response = requests.post(
                f'{self.base_url}/payments',
                json=payload,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Payment initiation failed: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error initiating payment: {str(e)}")
            return None
    
    def verify_payment(self, transaction_id: str) -> Optional[Dict]:
        """
        Verify a payment transaction.
        
        Args:
            transaction_id: Flutterwave transaction ID
        
        Returns:
            Transaction verification response
        """
        try:
            response = requests.get(
                f'{self.base_url}/transactions/{transaction_id}/verify',
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Payment verification failed: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error verifying payment: {str(e)}")
            return None
    
    def process_refund(self, transaction_id: str, amount: float) -> Optional[Dict]:
        """
        Process a refund for a transaction.
        
        Args:
            transaction_id: Original transaction ID
            amount: Refund amount
        
        Returns:
            Refund response
        """
        try:
            payload = {
                'amount': amount
            }
            
            response = requests.post(
                f'{self.base_url}/transactions/{transaction_id}/refund',
                json=payload,
                headers=self.headers
            )
            
            if response.status_code == 200:
                logger.info(f"Refund processed for transaction {transaction_id}")
                return response.json()
            else:
                logger.error(f"Refund processing failed: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error processing refund: {str(e)}")
            return None
    
    def get_subscription_pricing(self) -> Dict:
        """Get subscription plan pricing."""
        return {
            'free': {'price': 0, 'features': ['Limited chat sessions', 'Basic assessments']},
            'basic': {'price': 5000, 'currency': 'UGX', 'features': ['Unlimited chat', 'Full assessments', 'Resources']},
            'premium': {'price': 15000, 'currency': 'UGX', 'features': ['Everything in Basic', 'Counselor access', 'Priority support']},
            'professional': {'price': 30000, 'currency': 'UGX', 'features': ['Everything in Premium', 'Dedicated counselor', '24/7 support']}
        }
