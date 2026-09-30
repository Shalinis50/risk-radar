def send_mock_notification(
    transaction_id,
    risk_score,
    triggered_rules,
    amount
):
    if risk_score < 80:
        print("No notification needed.")
        return False

    print("\n" + "=" * 50)
    print("🚨 HIGH-RISK FRAUD ALERT")
    print("=" * 50)
    print(f"Transaction ID: {transaction_id}")
    print(f"Amount: ₹{amount}")
    print(f"Risk Score: {risk_score}")
    print(f"Triggered Rules: {', '.join(triggered_rules)}")
    print("=" * 50)

    return True