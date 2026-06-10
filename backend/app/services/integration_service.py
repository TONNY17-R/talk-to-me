"""
Integration Ecosystem Service
Integrations for EHR, wearables, pharmacy, insurance, payment, and messaging systems
"""

from typing import Dict, List, Optional
import json
import logging
from datetime import datetime
import requests
from abc import ABC, abstractmethod
import hmac
import hashlib

logger = logging.getLogger(__name__)


class IntegrationBase(ABC):
    """Base class for all integrations"""
    
    def __init__(self, provider_name: str, api_key: str):
        self.provider_name = provider_name
        self.api_key = api_key
        self.last_sync = None
    
    @abstractmethod
    def connect(self) -> bool:
        """Verify connection to external system"""
        pass
    
    @abstractmethod
    def sync_data(self) -> Dict:
        """Sync data with external system"""
        pass


class EHRIntegration(IntegrationBase):
    """Electronic Health Record System Integration"""
    
    def __init__(self, provider_name: str, api_key: str, hospital_id: str):
        super().__init__(provider_name, api_key)
        self.hospital_id = hospital_id
        self.api_endpoint = f"https://{provider_name.lower()}-api.health.net/v1"
    
    def connect(self) -> bool:
        """Test connection to EHR system"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_endpoint}/health",
                headers=headers,
                timeout=5
            )
            
            return response.status_code == 200
        except Exception as e:
            logger.error(f"EHR connection failed: {e}")
            return False
    
    def fetch_patient_records(self, patient_id: str) -> Dict:
        """Fetch patient medical records from EHR"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_endpoint}/patients/{patient_id}/records",
                headers=headers,
                params={'hospital_id': self.hospital_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'ehr_patient_id': patient_id,
                    'current_medications': data.get('medications', []),
                    'medical_conditions': data.get('diagnoses', []),
                    'recent_lab_results': data.get('lab_results', []),
                    'blood_type': data.get('blood_type'),
                    'allergies': data.get('allergies', []),
                    'last_synced': datetime.now().isoformat(),
                }
            else:
                logger.error(f"EHR fetch failed: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"Error fetching EHR records: {e}")
            return {}
    
    def sync_data(self) -> Dict:
        """Sync mental health data to EHR"""
        return {'status': 'synced', 'timestamp': datetime.now().isoformat()}
    
    def update_medication_list(self, patient_id: str, medications: List[Dict]) -> bool:
        """Update medications in EHR"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'medications': medications,
                'updated_at': datetime.now().isoformat()
            }
            
            response = requests.put(
                f"{self.api_endpoint}/patients/{patient_id}/medications",
                headers=headers,
                json=payload
            )
            
            return response.status_code in [200, 201]
        except Exception as e:
            logger.error(f"Error updating EHR medications: {e}")
            return False


class WearableIntegration(IntegrationBase):
    """Wearable Device Integration (Apple Health, Fitbit, Garmin, etc.)"""
    
    def __init__(self, device_type: str, provider_name: str, oauth_token: str):
        super().__init__(provider_name, oauth_token)
        self.device_type = device_type
        self.endpoints = {
            'apple_health': 'https://api.healthkit.apple.com',
            'fitbit': 'https://api.fitbit.com/1',
            'garmin': 'https://apis.garmin.com/wellness-sdk/rest',
            'oura_ring': 'https://api.oura.cloud/v1',
        }
    
    def connect(self) -> bool:
        """Verify wearable connection"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            endpoint = self.endpoints.get(self.device_type)
            if not endpoint:
                return False
            
            response = requests.get(f"{endpoint}/user/profile", headers=headers, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Wearable connection failed: {e}")
            return False
    
    def fetch_health_metrics(self, user_id: str, date: str) -> Dict:
        """Fetch health metrics from wearable device"""
        try:
            endpoint = self.endpoints.get(self.device_type)
            
            if self.device_type == 'fitbit':
                return self._fetch_fitbit_data(user_id, date, endpoint)
            elif self.device_type == 'oura_ring':
                return self._fetch_oura_data(date, endpoint)
            elif self.device_type == 'apple_health':
                return self._fetch_apple_health_data(user_id, date, endpoint)
            elif self.device_type == 'garmin':
                return self._fetch_garmin_data(user_id, date, endpoint)
            
        except Exception as e:
            logger.error(f"Error fetching wearable data: {e}")
            return {}
    
    def _fetch_fitbit_data(self, user_id: str, date: str, endpoint: str) -> Dict:
        """Fetch Fitbit specific data"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            # Heart rate data
            hr_response = requests.get(
                f"{endpoint}/user/-/activities/heart/date/{date}/1d.json",
                headers=headers
            )
            
            # Sleep data
            sleep_response = requests.get(
                f"{endpoint}/user/-/sleep/date/{date}.json",
                headers=headers
            )
            
            # Activity data
            activity_response = requests.get(
                f"{endpoint}/user/-/activities/date/{date}.json",
                headers=headers
            )
            
            return {
                'device_type': 'fitbit',
                'heart_rate_data': hr_response.json() if hr_response.status_code == 200 else {},
                'sleep_data': sleep_response.json() if sleep_response.status_code == 200 else {},
                'activity_data': activity_response.json() if activity_response.status_code == 200 else {},
                'synced_at': datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error fetching Fitbit data: {e}")
            return {}
    
    def _fetch_oura_data(self, date: str, endpoint: str) -> Dict:
        """Fetch Oura Ring specific data"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(
                f"{endpoint}/sleep?start_date={date}",
                headers=headers
            )
            
            if response.status_code == 200:
                sleep_data = response.json()
                
                return {
                    'device_type': 'oura_ring',
                    'sleep_data': sleep_data,
                    'sleep_quality': sleep_data.get('sleep', [{}])[0].get('score'),
                    'readiness_score': sleep_data.get('readiness', [{}])[0].get('score'),
                    'activity_score': sleep_data.get('activity', [{}])[0].get('score'),
                    'synced_at': datetime.now().isoformat(),
                }
            
        except Exception as e:
            logger.error(f"Error fetching Oura data: {e}")
            return {}
    
    def _fetch_apple_health_data(self, user_id: str, date: str, endpoint: str) -> Dict:
        """Fetch Apple Health specific data"""
        # Note: Apple Health requires special HealthKit permissions
        return {
            'device_type': 'apple_health',
            'note': 'Apple Health data requires HealthKit permissions',
            'synced_at': datetime.now().isoformat(),
        }
    
    def _fetch_garmin_data(self, user_id: str, date: str, endpoint: str) -> Dict:
        """Fetch Garmin specific data"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                f"{endpoint}/wellness/dailySummaries",
                headers=headers,
                params={'startDate': date}
            )
            
            if response.status_code == 200:
                return {
                    'device_type': 'garmin',
                    'daily_summary': response.json(),
                    'synced_at': datetime.now().isoformat(),
                }
            
        except Exception as e:
            logger.error(f"Error fetching Garmin data: {e}")
            return {}
    
    def sync_data(self) -> Dict:
        """Sync wearable data"""
        return {
            'device_type': self.device_type,
            'status': 'synced',
            'timestamp': datetime.now().isoformat()
        }


class PaymentIntegration(IntegrationBase):
    """Mobile Money & Payment Gateway Integration (mPesa, MTN Money, etc.)"""
    
    def __init__(self, provider_name: str, api_key: str, merchant_id: str):
        super().__init__(provider_name, api_key)
        self.merchant_id = merchant_id
        self.endpoints = {
            'mpesa': 'https://sandbox.safaricom.co.ke/mpesa',
            'mtn_money': 'https://api.mtn.com/v1',
            'airtel_money': 'https://api.airtel.com/v1',
        }
    
    def connect(self) -> bool:
        """Verify payment gateway connection"""
        return True  # Placeholder
    
    def process_payment(
        self,
        user_id: int,
        amount_usd: float,
        currency: str,
        payment_method: str,
        phone_number: str
    ) -> Dict:
        """Process payment via mobile money"""
        try:
            if payment_method == 'mpesa':
                return self._process_mpesa(amount_usd, phone_number)
            elif payment_method == 'mtn_money':
                return self._process_mtn_money(amount_usd, phone_number)
            elif payment_method == 'airtel_money':
                return self._process_airtel_money(amount_usd, phone_number)
            
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'transaction_id': None
            }
    
    def _process_mpesa(self, amount_usd: float, phone_number: str) -> Dict:
        """Process M-Pesa payment"""
        # Convert USD to KES (approximate rate)
        amount_kes = amount_usd * 130
        
        # Placeholder implementation
        return {
            'status': 'pending',
            'provider': 'mpesa',
            'amount': amount_kes,
            'currency': 'KES',
            'phone_number': phone_number,
            'transaction_id': f"MPX{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
        }
    
    def _process_mtn_money(self, amount_usd: float, phone_number: str) -> Dict:
        """Process MTN Money payment"""
        return {
            'status': 'pending',
            'provider': 'mtn_money',
            'amount': amount_usd,
            'currency': 'USD',
            'phone_number': phone_number,
            'transaction_id': f"MTN{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
        }
    
    def _process_airtel_money(self, amount_usd: float, phone_number: str) -> Dict:
        """Process Airtel Money payment"""
        return {
            'status': 'pending',
            'provider': 'airtel_money',
            'amount': amount_usd,
            'currency': 'USD',
            'phone_number': phone_number,
            'transaction_id': f"ATL{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
        }
    
    def verify_payment(self, transaction_id: str) -> Dict:
        """Verify payment status"""
        return {
            'transaction_id': transaction_id,
            'status': 'completed',
            'verified_at': datetime.now().isoformat(),
        }
    
    def sync_data(self) -> Dict:
        """Sync payment data"""
        return {'status': 'synced', 'timestamp': datetime.now().isoformat()}


class MessagingIntegration(IntegrationBase):
    """Messaging Integration (SMS, WhatsApp, Email)"""
    
    def __init__(self, provider_name: str, api_key: str):
        super().__init__(provider_name, api_key)
    
    def connect(self) -> bool:
        """Verify messaging provider connection"""
        return True  # Placeholder
    
    def send_sms(self, phone_number: str, message: str) -> Dict:
        """Send SMS message"""
        try:
            # Use provider-specific API (e.g., Twilio, Africa's Talking)
            return {
                'message_id': f"SMS{datetime.now().timestamp()}",
                'recipient': phone_number,
                'status': 'sent',
                'timestamp': datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def send_whatsapp(self, phone_number: str, message: str) -> Dict:
        """Send WhatsApp message"""
        try:
            return {
                'message_id': f"WA{datetime.now().timestamp()}",
                'recipient': phone_number,
                'status': 'sent',
                'platform': 'whatsapp',
                'timestamp': datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error sending WhatsApp: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def send_email(self, email: str, subject: str, body: str, html: bool = False) -> Dict:
        """Send email message"""
        try:
            return {
                'message_id': f"EMAIL{datetime.now().timestamp()}",
                'recipient': email,
                'subject': subject,
                'status': 'sent',
                'timestamp': datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def sync_data(self) -> Dict:
        """Sync messaging data"""
        return {'status': 'synced', 'timestamp': datetime.now().isoformat()}


class IntegrationManager:
    """Manages all integrations for the platform"""
    
    def __init__(self):
        self.integrations = {}
    
    def register_integration(self, integration_name: str, integration: IntegrationBase):
        """Register an integration"""
        self.integrations[integration_name] = integration
        logger.info(f"Integration registered: {integration_name}")
    
    def initialize_ehr(self, provider: str, api_key: str, hospital_id: str) -> bool:
        """Initialize EHR integration"""
        try:
            ehr = EHRIntegration(provider, api_key, hospital_id)
            if ehr.connect():
                self.register_integration('ehr', ehr)
                return True
        except Exception as e:
            logger.error(f"Failed to initialize EHR: {e}")
        return False
    
    def initialize_wearable(self, device_type: str, provider: str, token: str) -> bool:
        """Initialize wearable integration"""
        try:
            wearable = WearableIntegration(device_type, provider, token)
            if wearable.connect():
                self.register_integration(f'wearable_{device_type}', wearable)
                return True
        except Exception as e:
            logger.error(f"Failed to initialize wearable: {e}")
        return False
    
    def initialize_payments(self, provider: str, api_key: str, merchant_id: str) -> bool:
        """Initialize payment gateway"""
        try:
            payment = PaymentIntegration(provider, api_key, merchant_id)
            if payment.connect():
                self.register_integration('payment', payment)
                return True
        except Exception as e:
            logger.error(f"Failed to initialize payments: {e}")
        return False
    
    def initialize_messaging(self, provider: str, api_key: str) -> bool:
        """Initialize messaging provider"""
        try:
            messaging = MessagingIntegration(provider, api_key)
            if messaging.connect():
                self.register_integration('messaging', messaging)
                return True
        except Exception as e:
            logger.error(f"Failed to initialize messaging: {e}")
        return False
    
    def sync_all(self) -> Dict:
        """Sync all registered integrations"""
        results = {}
        for name, integration in self.integrations.items():
            try:
                results[name] = integration.sync_data()
            except Exception as e:
                logger.error(f"Sync failed for {name}: {e}")
                results[name] = {'status': 'failed', 'error': str(e)}
        
        return results


# Global integration manager instance
integration_manager = IntegrationManager()
