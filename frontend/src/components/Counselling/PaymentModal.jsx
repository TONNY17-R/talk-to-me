import React, { useState, useRef, useEffect } from 'react';
import './PaymentModal.css';

export const PaymentModal = ({ bookingDetails, onSuccess, onClose }) => {
  const [paymentStep, setPaymentStep] = useState('method'); // method, prompt, processing, confirmation
  const [selectedMethod, setSelectedMethod] = useState(null);
  const firstMethodRef = useRef(null);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [cardDetails, setCardDetails] = useState({ number: '', mmyy: '', cvc: '' });
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [promptData, setPromptData] = useState(null);
  const [processingMessage, setProcessingMessage] = useState('');
  const [transactionId, setTransactionId] = useState('');

  const paymentMethods = [
    {
      id: 'mtn',
      name: 'MTN Mobile Money',
      icon: '📱',
      description: 'Pay via MTN Mobile Money (Uganda)',
      color: '#FFD000',
      ussd: '*165*',
    },
    {
      id: 'airtel',
      name: 'Airtel Money',
      icon: '📱',
      description: 'Pay via Airtel Money (Uganda)',
      color: '#FF0000',
      ussd: '*185#',
    },
    {
      id: 'equity',
      name: 'Equity Bank Mobile',
      icon: '🏦',
      description: 'Pay via Equity Bank',
      color: '#1E90FF',
      ussd: '*247#',
    },
    {
      id: 'card',
      name: 'Credit/Debit Card',
      icon: '💳',
      description: 'Visa, Mastercard, or Local Cards',
      color: '#F59E0B',
    },
  ];

  const generatePrompt = (method, phone) => {
    const selectedPaymentMethod = paymentMethods.find((m) => m.id === method);

    if (method === 'mtn' || method === 'airtel') {
      return {
        type: 'mobile-money',
        title: `${selectedPaymentMethod.name} Payment Prompt`,
        message: `A payment prompt will be sent to ${phone}`,
        prompt: `You will receive a USSD prompt (${selectedPaymentMethod.ussd}) on your phone`,
        instructions: [
          `1. You will receive a pop-up on ${phone}`,
          `2. Follow the prompt to enter your PIN`,
          `3. Confirm payment of UGX ${bookingDetails.price}`,
          `4. Wait for confirmation message`,
        ],
        waitingMessage: 'Waiting for payment confirmation from your phone...',
      };
    } else if (method === 'equity') {
      return {
        type: 'bank-transfer',
        title: 'Equity Bank Payment',
        message: `A payment request has been sent to ${phone}`,
        prompt: 'You will receive an SMS request on your registered phone',
        instructions: [
          `1. Open your Equity Bank app`,
          `2. Go to "Send Money" section`,
          `3. Enter amount: UGX ${bookingDetails.price}`,
          `4. Confirm transaction with your PIN`,
        ],
        waitingMessage: 'Waiting for payment confirmation...',
      };
    } else if (method === 'card') {
      return {
        type: 'card',
        title: 'Card Payment',
        message: 'Processing your card payment',
        prompt: 'Your card will be charged',
        instructions: [
          `Card ending in ${cardDetails.number.slice(-4)}`,
          `Amount: UGX ${bookingDetails.price}`,
          `Processing payment...`,
        ],
        waitingMessage: 'Processing your payment...',
      };
    }
  };

  const handleProcessPayment = async () => {
    if (!selectedMethod || (!phoneNumber && selectedMethod !== 'card')) {
      setError('Please fill in all required fields');
      return;
    }

    // Show payment prompt
    const prompt = generatePrompt(selectedMethod, phoneNumber || '****');
    setPromptData(prompt);
    setPaymentStep('prompt');
  };

  const handleConfirmPayment = async () => {
    setProcessing(true);
    setError(null);

    // Simulate payment steps
    const processingSteps = [
      'Initiating payment...',
      `Sending request to ${selectedMethod === 'mtn' ? 'MTN' : selectedMethod === 'airtel' ? 'Airtel' : selectedMethod === 'equity' ? 'Equity Bank' : 'Card Processor'}...`,
      promptData.waitingMessage,
      'Verifying payment...',
      'Payment confirmed! ✓',
    ];

    try {
      for (let i = 0; i < processingSteps.length; i++) {
        await new Promise((resolve) => setTimeout(resolve, 800));
        setProcessingMessage(processingSteps[i]);
      }

      const newTransactionId = `TXN-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
      setTransactionId(newTransactionId);

      const paymentData = {
        method: selectedMethod,
        amount: bookingDetails.price,
        phoneNumber: phoneNumber,
        timestamp: new Date(),
        transactionId: newTransactionId,
        status: 'success',
      };

      await new Promise((resolve) => setTimeout(resolve, 500));
      setPaymentStep('confirmation');
      onSuccess(paymentData);
    } catch (err) {
      setError('Payment processing failed. Please try again.');
      setProcessing(false);
    }
  };

  useEffect(() => {
    if (paymentStep === 'method' && firstMethodRef.current) {
      firstMethodRef.current.focus();
    }
  }, [paymentStep]);

  if (paymentStep === 'method') {
    return (
      <div className="modal-overlay" onClick={onClose} role="dialog" aria-modal="true">
        <div className="modal-content payment-modal" onClick={(e) => e.stopPropagation()}>
          <button className="close-button" onClick={onClose}>✕</button>

          <h2>Select Payment Method</h2>
          <p className="modal-subtitle">Step 2 of 3: Choose how to pay</p>
          <p className="payment-amount">
            Total Amount: <strong>UGX {bookingDetails.price}</strong>
          </p>

          <div className="payment-methods">
            {paymentMethods.map((method, idx) => (
              <div
                key={method.id}
                ref={idx === 0 ? firstMethodRef : null}
                tabIndex={0}
                className={`payment-method-card ${selectedMethod === method.id ? 'selected' : ''}`}
                style={{
                  borderColor: selectedMethod === method.id ? method.color : '#e5e7eb',
                }}
                onClick={() => {
                  setSelectedMethod(method.id);
                  setError(null);
                }}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    setSelectedMethod(method.id);
                    setError(null);
                  }
                }}
              >
                <div className="method-icon" style={{ color: method.color }}>
                  {method.icon}
                </div>
                <div className="method-info">
                  <h4>{method.name}</h4>
                  <p>{method.description}</p>
                </div>
                <div className="method-radio">
                  <input
                    type="radio"
                    name="payment-method"
                    value={method.id}
                    checked={selectedMethod === method.id}
                    disabled
                  />
                </div>
              </div>
            ))}
          </div>

          {selectedMethod && (
            <div className="payment-input-section">
              {(selectedMethod === 'mtn' || selectedMethod === 'airtel' || selectedMethod === 'equity') && (
                <div className="form-section">
                  <label>
                    {selectedMethod === 'mtn'
                      ? 'MTN Phone Number'
                      : selectedMethod === 'airtel'
                      ? 'Airtel Phone Number'
                      : 'Phone Number'}
                  </label>
                  <input
                    type="tel"
                    placeholder="e.g., 0701234567 or +256701234567"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    className="form-input"
                  />
                  <p className="input-help">
                    ✓ You'll receive a payment prompt on this number to confirm payment
                  </p>
                </div>
              )}

              {selectedMethod === 'card' && (
                <div>
                  <div className="form-section">
                    <label>Card Number</label>
                    <input
                      type="text"
                      placeholder="1234 5678 9012 3456"
                      value={cardDetails.number}
                      onChange={(e) => setCardDetails({ ...cardDetails, number: e.target.value })}
                      className="form-input"
                    />
                  </div>
                  <div className="card-row">
                    <div className="form-section">
                      <label>Expiry (MM/YY)</label>
                      <input
                        type="text"
                        placeholder="12/25"
                        value={cardDetails.mmyy}
                        onChange={(e) => setCardDetails({ ...cardDetails, mmyy: e.target.value })}
                        className="form-input"
                      />
                    </div>
                    <div className="form-section">
                      <label>CVC</label>
                      <input
                        type="text"
                        placeholder="123"
                        value={cardDetails.cvc}
                        onChange={(e) => setCardDetails({ ...cardDetails, cvc: e.target.value })}
                        className="form-input"
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {error && <div className="error-message">⚠️ {error}</div>}

          <div className="modal-actions">
            <button className="cancel-button" onClick={onClose}>
              Cancel
            </button>
            <button
              className="confirm-button"
              onClick={handleProcessPayment}
              disabled={!selectedMethod || (!phoneNumber && selectedMethod !== 'card')}
            >
              Continue to Payment 🔒
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (paymentStep === 'prompt') {
    return (
      <div className="modal-overlay" onClick={onClose} role="dialog" aria-modal="true">
        <div className="modal-content payment-modal" onClick={(e) => e.stopPropagation()}>
          <h2>{promptData.title}</h2>
          <p className="modal-subtitle">Step 2 of 3: Complete payment</p>

          <div className="prompt-container">
            <div className="prompt-icon">📱</div>
            <div className="prompt-message">
              <h3>{promptData.message}</h3>
              <p className="prompt-ussd">{promptData.prompt}</p>
            </div>
          </div>

          <div className="instructions-section">
            <h4>Instructions:</h4>
            <div className="instructions-list">
              {promptData.instructions.map((instruction, idx) => (
                <div key={idx} className="instruction-item">
                  {instruction}
                </div>
              ))}
            </div>
          </div>

          <div className="payment-summary">
            <div className="summary-item">
              <span>Amount to Pay:</span>
              <strong>UGX {bookingDetails.price}</strong>
            </div>
            <div className="summary-item">
              <span>Payment Method:</span>
              <strong>
                {paymentMethods.find((m) => m.id === selectedMethod).name}
              </strong>
            </div>
          </div>

          <div className="modal-actions">
            <button className="cancel-button" onClick={() => setPaymentStep('method')}>
              ← Back
            </button>
            <button
              className="confirm-button"
              onClick={handleConfirmPayment}
              disabled={processing}
            >
              {processing ? 'Processing...' : '✓ Payment Received'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (paymentStep === 'confirmation') {
    return (
      <div className="modal-overlay" onClick={onClose} role="dialog" aria-modal="true">
        <div className="modal-content payment-modal" onClick={(e) => e.stopPropagation()}>
          <div className="processing-container">
            {processing ? (
              <>
                <div className="processing-spinner"></div>
                <h3>{processingMessage}</h3>
              </>
            ) : (
              <>
                <div className="success-checkmark">✓</div>
                <h2>Payment Successful!</h2>
                <p>Your payment has been processed successfully.</p>
                <div className="transaction-info">
                  <div className="info-item">
                    <span>Transaction ID:</span>
                    <strong>{transactionId}</strong>
                  </div>
                  <div className="info-item">
                    <span>Amount:</span>
                    <strong>UGX {bookingDetails.price}</strong>
                  </div>
                  <div className="info-item">
                    <span>Method:</span>
                    <strong>
                      {paymentMethods.find((m) => m.id === selectedMethod).name}
                    </strong>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    );
  }
};
