# ECS Lambda Scheduler

Run ECS tasks
on Fargate
from CloudWatch Events.

### Why Do I Need This?

Amazon CloudWatch Events
only supports the EC2 launch type
when invoking ECS tasks.
This function enables
invoking tasks configured
to launch on ECS Fargate.

### How Does It Work?

This Lambda function reacts to
Cloudwatch Event Rules
by calling the ECS RunTask API
with the parameters provided
in the Event payload.

## Install

This function is deployed with
[Apex](https://apex.run).
Deployment is as simple as:

```shell
apex deploy
```

## Setup

1. Create an IAM role
for your Lambda function
with the following policy attached.

    **Note**: Make sure to replace `AWS_REGION`
    and
    `ACCOUNT_ID` with appropriate values.

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "logs:CreateLogStream"
                ],
                "Resource": [
                    "arn:aws:logs:AWS_REGION:ACCOUNT_ID:log-group:/aws/lambda/ecs-lambda-scheduler:*"
                ],
                "Effect": "Allow"
            },
            {
                "Action": [
                    "logs:PutLogEvents"
                ],
                "Resource": [
                    "arn:aws:logs:AWS_REGION:ACCOUNT_ID:log-group:/aws/lambda/ecs-lambda_scheduler:*:*"
                ],
                "Effect": "Allow"
            },
            {
                "Action": [
                    "ecs:RunTask",
                ],
                "Resource": "*",
                "Effect": "Allow"
            }
        ]
    }
    ```

2. Add the ARN
for the newly created role
to the `project.json` file.

    ```json
      "role": "MY_ARN"
    }
    ```

3. Deploy the function.

    ```shell
    apex deploy
    ```

4. Grant CloudWatch Events
the ability to invoke the function.

    **Note**: Make sure to replace `AWS_REGION`
    and
    `ACCOUNT_ID` with appropriate values.

    ```shell
    aws lambda add-permission \
      --function-name ecs-lambda-scheduler \
      --statement-id cloudwatch-events-policy \
      --action 'lambda:InvokeFunction' \
      --principal events.amazonaws.com \
      --source-arn 'arn:aws:events:AWS_REGION:ACCOUNT_ID:*'
    ```

5. Create a CloudWatch Event Rule
and pass the appropriate input format.

    Example:

    ```shell
    aws events put-rule \
      --name MY_RULE \
      --schedule-expression 'rate(5 minutes)'

    aws events put-targets \
      --rule MY_RULE \
      --targets '{"Id":"1","Arn":"MY_LAMBDA_ARN","Input":"{\"cluster\":\"prod\",\"count\":1,\"networkConfiguration\":{\"awsvpcConfiguration\":{\"assignPublicIp\":\"DISABLED\",\"securityGroups\":[\"sg-12345678\"],\"subnets\":[\"subnet-12345678\"]}},\"taskDefinition\":\"TASK_DEFINITION_ARN\"}"}'
    ```
