import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


HIGH_RISK_THRESHOLD = 80


def send_high_risk_notification(
    transaction_id,
    risk_score,
    triggered_rules,
    amount
):
    # Don't send notification for lower-risk transactions
    if risk_score < HIGH_RISK_THRESHOLD:
        return False

    # Get SNS topic from environment variable
    topic_arn = os.getenv("SNS_TOPIC_ARN")

    if not topic_arn:
        print("SNS_TOPIC_ARN is not configured.")
        return False

    try:
        sns = boto3.client(
            "sns",
            region_name=os.getenv("AWS_REGION", "ap-south-1")
        )

        message = (
            "HIGH-RISK FRAUD ALERT\n\n"
            f"Transaction ID: {transaction_id}\n"
            f"Amount: {amount}\n"
            f"Risk Score: {risk_score}\n"
            f"Triggered Rules: {', '.join(triggered_rules)}\n"
        )

        response = sns.publish(
            TopicArn=topic_arn,
            Subject="High-Risk Fraud Alert",
            Message=message
        )

        print("SNS notification sent!")
        print("Message ID:", response.get("MessageId"))

        return True

    except (BotoCoreError, ClientError) as error:
        print("SNS notification failed:", error)
        return False