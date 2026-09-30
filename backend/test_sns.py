from notifications import send_high_risk_notification


result = send_high_risk_notification(
    transaction_id="TXN-TEST-001",
    risk_score=85,
    triggered_rules=[
        "unusual_amount",
        "transaction_velocity"
    ],
    amount=75000
)

print("Notification result:", result)