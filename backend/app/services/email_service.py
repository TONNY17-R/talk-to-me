"""
Email Service module.

Handles email sending for notifications and communications.
"""

import logging
import os
from flask_mail import Mail, Message

logger = logging.getLogger(__name__)

mail = Mail()


class EmailService:
    """Service for sending emails."""
    
    @staticmethod
    def send_email(recipient: str, subject: str, body: str, html: str = None) -> bool:
        """
        Send email.
        
        Args:
            recipient: Email recipient
            subject: Email subject
            body: Email body (plain text)
            html: HTML version of email
        
        Returns:
            True if successful
        """
        try:
            msg = Message(
                subject=subject,
                recipients=[recipient],
                body=body,
                html=html
            )
            mail.send(msg)
            logger.info(f"Email sent to {recipient}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(email: str, first_name: str) -> bool:
        """Send welcome email to new user."""
        subject = "Welcome to Talk to Me"
        body = f"Hello {first_name},\n\nWelcome to Talk to Me. We are here to support your mental health journey."
        html = f"""
        <h2>Welcome to Talk to Me</h2>
        <p>Hello {first_name},</p>
        <p>We are excited to have you on our platform.</p>
        """
        return EmailService.send_email(email, subject, body, html)
    
    @staticmethod
    def send_password_reset_email(email: str, reset_token: str) -> bool:
        """Send password reset email."""
        reset_url = f"{os.environ.get('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}"
        subject = "Reset Your Password"
        body = f"Click the link to reset your password: {reset_url}"
        html = f"""
        <h2>Password Reset</h2>
        <p><a href="{reset_url}">Click here to reset your password</a></p>
        <p>This link expires in 24 hours.</p>
        """
        return EmailService.send_email(email, subject, body, html)
    
    @staticmethod
    def send_verification_email(email: str, verification_code: str) -> bool:
        """Send email verification."""
        subject = "Verify Your Email"
        body = f"Your verification code is: {verification_code}"
        html = f"""
        <h2>Verify Your Email</h2>
        <p>Your verification code is: <strong>{verification_code}</strong></p>
        """
        return EmailService.send_email(email, subject, body, html)
    
    @staticmethod
    def send_appointment_confirmation(email: str, appointment_details: dict) -> bool:
        """Send appointment confirmation."""
        subject = "Appointment Confirmation"
        body = f"Your appointment is confirmed for {appointment_details.get('date')} at {appointment_details.get('time')}"
        html = f"""
        <h2>Appointment Confirmed</h2>
        <p>Your counselling appointment is confirmed:</p>
        <ul>
            <li>Date: {appointment_details.get('date')}</li>
            <li>Time: {appointment_details.get('time')}</li>
            <li>Counselor: {appointment_details.get('counselor_name')}</li>
        </ul>
        """
        return EmailService.send_email(email, subject, body, html)
    
    @staticmethod
    def send_crisis_notification(admin_email: str, user_info: dict, alert_details: dict) -> bool:
        """Send crisis alert notification to admin."""
        subject = "URGENT: Crisis Alert - Immediate Action Required"
        body = f"Crisis alert for user {user_info.get('email')}: {alert_details.get('description')}"
        html = f"""
        <h2 style="color: red;">URGENT: Crisis Alert</h2>
        <p><strong>User:</strong> {user_info.get('first_name')} {user_info.get('last_name')}</p>
        <p><strong>Email:</strong> {user_info.get('email')}</p>
        <p><strong>Alert:</strong> {alert_details.get('description')}</p>
        <p><strong>Risk Level:</strong> {alert_details.get('risk_level')}</p>
        """
        return EmailService.send_email(admin_email, subject, body, html)
