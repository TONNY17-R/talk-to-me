import React, { useState, useRef, useEffect, useContext } from 'react';
import { PaymentModal } from './PaymentModal';
import { ToastContext } from '../../contexts/ToastContext';
import './BookingModal.css';

export const BookingModal = ({ counsellor, onClose, onConfirm }) => {
  const [selectedDate, setSelectedDate] = useState('');
  const dateRef = useRef(null);
  const [selectedTime, setSelectedTime] = useState('');
  const [notes, setNotes] = useState('');
  const [bookingStep, setBookingStep] = useState('details'); // details, payment, confirmation
  const [paymentStatus, setPaymentStatus] = useState(null);
  const [bookingDetails, setBookingDetails] = useState(null);

  const getNextDays = () => {
    const days = [];
    for (let i = 0; i < 7; i++) {
      const date = new Date();
      date.setDate(date.getDate() + i);
      days.push(date.toISOString().split('T')[0]);
    }
    return days;
  };

  const parsePrice = (priceString) => {
    return parseInt(priceString.replace(/[^0-9]/g, '')) || 60;
  };

  const handleProceedToPayment = () => {
    if (selectedDate && selectedTime) {
      setBookingDetails({
        counsellor: counsellor.name,
        date: selectedDate,
        time: selectedTime,
        notes: notes,
        price: parsePrice(counsellor.price),
        duration: '60 min',
      });
      setBookingStep('payment');
    }
  };

  const handlePaymentSuccess = (paymentData) => {
    setPaymentStatus('success');
    setBookingStep('confirmation');
  };

  const { addToast } = useContext(ToastContext);

  const handleConfirmBooking = () => {
    onConfirm({
      date: selectedDate,
      time: selectedTime,
      notes: notes,
      paymentId: paymentStatus?.transactionId,
    });
    addToast('Booking confirmed! Check your receipt or email.', 'success');
  };

  const generateReceiptHTML = () => {
    const bookingDate = new Date(bookingDetails.date).toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric',
      year: 'numeric',
    });

    const receiptDate = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    });

    const receiptTime = new Date().toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });

    const whatsappUrl = 'https://wa.me/256747188470?text=' + encodeURIComponent('Hello Talk to Me Support, I need help with my booking');

    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Session Receipt</title>
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
          }
          .receipt {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          }
          .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #5B6CF8;
            padding-bottom: 20px;
          }
          .header h1 {
            color: #5B6CF8;
            margin: 0;
            font-size: 24px;
          }
          .header p {
            margin: 5px 0 0 0;
            color: #666;
            font-size: 14px;
          }
          .receipt-number {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-bottom: 20px;
          }
          .section {
            margin-bottom: 25px;
          }
          .section-title {
            font-weight: 700;
            color: #5B6CF8;
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 10px;
            border-bottom: 1px solid #eee;
            padding-bottom: 8px;
          }
          .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
          }
          .detail-row:last-child {
            border-bottom: none;
          }
          .detail-label {
            font-weight: 500;
            color: #666;
            flex: 1;
          }
          .detail-value {
            text-align: right;
            font-weight: 600;
            color: #333;
          }
          .price-section {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 6px;
            margin-top: 10px;
          }
          .total-row {
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: 700;
            color: #10B981;
            border-top: 2px solid #10B981;
            padding-top: 10px;
          }
          .footer {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
          }
          .status {
            text-align: center;
            color: #10B981;
            font-weight: 600;
            font-size: 16px;
            margin: 20px 0;
          }
        </style>
      </head>
      <body>
        <div class="receipt">
          <div class="header">
            <h1>💚 Talk to Me</h1>
            <p>Mental Health Support Platform</p>
          </div>

          <div class="receipt-number">
            Receipt #${paymentStatus?.transactionId || 'TXN-' + Date.now()}
          </div>

          <div class="status">✓ PAYMENT SUCCESSFUL</div>

          <div class="section">
            <div class="section-title">Booking Details</div>
            <div class="detail-row">
              <span class="detail-label">Counsellor:</span>
              <span class="detail-value">${bookingDetails.counsellor}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Session Date:</span>
              <span class="detail-value">${bookingDate}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Session Time:</span>
              <span class="detail-value">${bookingDetails.time}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Duration:</span>
              <span class="detail-value">${bookingDetails.duration}</span>
            </div>
          </div>

          <div class="section">
            <div class="section-title">Payment Information</div>
            <div class="detail-row">
              <span class="detail-label">Session Fee:</span>
              <span class="detail-value">UGX ${bookingDetails.price}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Processing Fee:</span>
              <span class="detail-value">UGX 0</span>
            </div>
            <div class="price-section">
              <div class="total-row">
                <span>Total Paid:</span>
                <span>UGX ${bookingDetails.price}</span>
              </div>
            </div>
          </div>

          <div class="section">
            <div class="section-title">Transaction Details</div>
            <div class="detail-row">
              <span class="detail-label">Transaction ID:</span>
              <span class="detail-value">${paymentStatus?.transactionId || 'Processing'}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Receipt Date:</span>
              <span class="detail-value">${receiptDate}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Receipt Time:</span>
              <span class="detail-value">${receiptTime}</span>
            </div>
          </div>

          <div class="footer">
            <p style="margin: 10px 0;">📧 A confirmation email has been sent to your registered email address</p>
            <p style="margin: 10px 0;">🔗 Join your session at the scheduled time via the platform</p>
            <p style="margin: 10px 0;">❓ For support, contact: support@talktome.ug</p>
            <p style="margin: 10px 0;">💬 WhatsApp Support: <a href="${whatsappUrl}" target="_blank" rel="noopener noreferrer">Message us on WhatsApp</a></p>
            <p style="margin: 20px 0 0 0; color: #bbb;">© 2026 Talk to Me. All rights reserved.</p>
          </div>
        </div>
      </body>
      </html>
    `;
  };

  const handleDownloadReceipt = () => {
    const receiptHTML = generateReceiptHTML();
    const blob = new Blob([receiptHTML], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Receipt-${paymentStatus?.transactionId || Date.now()}.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  useEffect(() => {
    if (bookingStep === 'details' && dateRef.current) {
      dateRef.current.focus();
    }
  }, [bookingStep]);

  if (bookingStep === 'details') {
    return (
      <div className="modal-overlay" onClick={onClose} role="dialog" aria-modal="true">
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <button className="close-button" onClick={onClose}>✕</button>

          <h2>Book Session with {counsellor.name}</h2>
          <p className="modal-subtitle">Step 1 of 3: Select Date & Time</p>

          <div className="booking-form">
            <div className="form-section">
              <label>Select Date:</label>
              <select
                ref={dateRef}
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="form-select"
              >
                <option value="">Choose a date...</option>
                {getNextDays().map((date) => (
                  <option key={date} value={date}>
                    {new Date(date).toLocaleDateString('en-US', {
                      weekday: 'long',
                      month: 'short',
                      day: 'numeric',
                    })}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-section">
              <label>Select Time:</label>
              <select
                value={selectedTime}
                onChange={(e) => setSelectedTime(e.target.value)}
                className="form-select"
              >
                <option value="">Choose a time...</option>
                {counsellor.availableSlots?.map((time) => (
                  <option key={time} value={time}>
                    {time}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-section">
              <label>Session Notes (Optional):</label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="What would you like to discuss? (optional)"
                className="form-textarea"
                rows="4"
              />
            </div>

            <div className="booking-summary">
              <h4>Booking Summary</h4>
              <div className="summary-item">
                <span>Counsellor:</span>
                <strong>{counsellor.name}</strong>
              </div>
              <div className="summary-item">
                <span>Specialization:</span>
                <strong>{counsellor.specialization}</strong>
              </div>
              <div className="summary-item">
                <span>Date:</span>
                <strong>
                  {selectedDate
                    ? new Date(selectedDate).toLocaleDateString('en-US', {
                        weekday: 'long',
                        month: 'short',
                        day: 'numeric',
                      })
                    : 'Not selected'}
                </strong>
              </div>
              <div className="summary-item">
                <span>Time:</span>
                <strong>{selectedTime || 'Not selected'}</strong>
              </div>
              <div className="summary-item">
                <span>Duration:</span>
                <strong>60 minutes</strong>
              </div>
              <div className="summary-item total-price">
                <span>Total Price:</span>
                <strong>{counsellor.price}</strong>
              </div>
            </div>

            <div className="modal-actions">
              <button className="cancel-button" onClick={onClose}>
                Cancel
              </button>
              <button
                className="confirm-button"
                onClick={handleProceedToPayment}
                disabled={!selectedDate || !selectedTime}
              >
                Proceed to Payment →
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (bookingStep === 'payment') {
    return (
      <PaymentModal
        bookingDetails={bookingDetails}
        onSuccess={handlePaymentSuccess}
        onClose={onClose}
      />
    );
  }

  if (bookingStep === 'confirmation') {
    return (
      <div className="modal-overlay" onClick={onClose} role="dialog" aria-modal="true">
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <div className="confirmation-container">
            <div className="success-icon">✓</div>
            <h2>Booking Confirmed!</h2>
            <p className="confirmation-message">
              Your session has been successfully booked and payment processed.
            </p>

            <div className="confirmation-details">
              <div className="detail-item">
                <span className="label">Counsellor:</span>
                <span className="value">{bookingDetails.counsellor}</span>
              </div>
              <div className="detail-item">
                <span className="label">Date:</span>
                <span className="value">
                  {new Date(bookingDetails.date).toLocaleDateString('en-US', {
                    weekday: 'long',
                    month: 'long',
                    day: 'numeric',
                  })}
                </span>
              </div>
              <div className="detail-item">
                <span className="label">Time:</span>
                <span className="value">{bookingDetails.time}</span>
              </div>
              <div className="detail-item">
                <span className="label">Duration:</span>
                <span className="value">60 minutes</span>
              </div>
              <div className="detail-item">
                <span className="label">Amount Paid:</span>
                <span className="value">UGX {bookingDetails.price}</span>
              </div>
              {paymentStatus?.transactionId && (
                <div className="detail-item">
                  <span className="label">Transaction ID:</span>
                  <span className="value">{paymentStatus.transactionId}</span>
                </div>
              )}
            </div>

            <div className="confirmation-actions">
              <button className="action-button primary" onClick={handleConfirmBooking}>
                Done
              </button>
              <button className="action-button secondary" onClick={handleDownloadReceipt}>
                📄 Download Receipt
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
};
