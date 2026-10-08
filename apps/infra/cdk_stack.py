from aws_cdk import (
    Stack,
    aws_budgets as budgets,
    aws_sns as sns,
    aws_iam as iam,
    CfnOutput
)
from constructs import Construct

class HolocronFinOpsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Topic for Cost Alerts
        budget_alarm_topic = sns.Topic(self, "HolocronBudgetAlertTopic",
            display_name="Holocron Career AI Cost Alerts"
        )

        # 2. Strict Budget definition (FinOps)
        # Assuming maximum of .00 / month for dev/RAG environment
        budget = budgets.CfnBudget(self, "HolocronDevBudget",
            budget=budgets.CfnBudget.BudgetDataProperty(
                budget_type="COST",
                time_unit="MONTHLY",
                budget_limit=budgets.CfnBudget.SpendProperty(
                    amount=10.00,
                    unit="USD"
                )
            ),
            notifications_with_subscribers=[
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        notification_type="ACTUAL",
                        comparison_operator="GREATER_THAN",
                        threshold=80.0,
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            subscription_type="SNS",
                            address=budget_alarm_topic.topic_arn
                        )
                    ]
                )
            ]
        )

        # Grant Budget service permission to publish to SNS
        budget_alarm_topic.grant_publish(
            iam.ServicePrincipal("budgets.amazonaws.com")
        )

        CfnOutput(self, "BudgetTopicArn", value=budget_alarm_topic.topic_arn)
