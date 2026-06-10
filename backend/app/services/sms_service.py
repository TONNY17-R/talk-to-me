"""
SMS Service module.

Handles SMS messaging via Africa's Talking API.
"""

import logging
import os

logger = logging.getLogger(__name__)


class SMSService:
    """Service for sending SMS messages."""
    
    def __init__(self):
        """Initialize SMS service with credentials."""
        self.api_key = os.environ.get('AFRICASTALKING_API_KEY')
        self.username = os.environ.get('AFRICASTALKING_USERNAME', 'sandbox')
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Africa's Talking client."""
        try:
            import africastalking
            africastalking.initialize(
                username=self.username,
                api_key=self.api_key
            )
            self.client = africastalking.SMS
            logger.info("SMS service initialized")
        except Exception as e:
            logger.warning(f"SMS service initialization failed: {str(e)}")
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """
        Send SMS message.
        
        Args:
            phone_number: Recipient phone number
            message: Message content
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.client:
                logger.error("SMS client not initialized")
                return False
            
            response = self.client.send(message, [phone_number])
            logger.info(f"SMS sent to {phone_number}")
            return True
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return False
    
    def send_bulk_sms(self, phone_numbers: list, message: str) -> int:
        """
        Send bulk SMS messages.
        
        Args:
            phone_numbers: List of recipient phone numbers
            message: Message content
        
        Returns:
            Number of successful sends
        """
        try:
            success_count = 0
            for phone in phone_numbers:
                if self.send_sms(phone, message):
                    success_count += 1
            
            logger.info(f"Bulk SMS sent: {success_count}/{len(phone_numbers)}")
            return success_count
        except Exception as e:
            logger.error(f"Error sending bulk SMS: {str(e)}")
            return 0
    
    def send_verification_code(self, phone_number: str, code: str) -> bool:
        """Send verification code via SMS."""
        message = f"Your Talk to Me verification code is: {code}"
        return self.send_sms(phone_number, message)
    
    def send_password_reset_sms(self, phone_number: str, reset_url: str) -> bool:
        """Send password reset link via SMS."""
        message = f"Reset your Talk to Me password: {reset_url}"
        return self.send_sms(phone_number, message)
    
    def send_appointment_reminder(self, phone_number: str, appointment_details: dict) -> bool:
        """Send appointment reminder."""
        message = f"Reminder: You have a counselling appointment on {appointment_details.get('date')} at {appointment_details.get('time')}"
        return self.send_sms(phone_number, message)
