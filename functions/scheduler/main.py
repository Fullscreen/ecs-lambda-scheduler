import boto3, logging

# This function invokes ECS tasks with the Fargate launch type
# on behalf of CloudWatch Events Rules.
#
# It expects an event object that conforms to the ECS run-task schema
# https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html
#
# Example:
# {
#   "cluster": "string",
#   "count": number,
#   "networkConfiguration": {
#     "awsvpcConfiguration": {
#       "assignPublicIp": "string",
#       "securityGroups": [ "string" ],
#       "subnets": [ "string" ]
#     }
#   },
#   "taskDefinition": "string"
# }

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
  logger.info("Received event {}".format(event))

  required = ("networkConfiguration", "taskDefinition")
  if not all (k in event for k in required):
     raise ValueError("The Lambda event is missing required keys {}".format(required))

  client = boto3.client("ecs")
  result = client.run_task(
      cluster=event.get("cluster", ""),
      taskDefinition=event.get("taskDefinition", ""),
      overrides=event.get("overrides", {}),
      count=1,
      launchType="FARGATE",
      networkConfiguration=event.get("networkConfiguration", "")
  )
