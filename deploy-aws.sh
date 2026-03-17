#!/bin/bash
# Deploy to AWS - Production Deployment Script

echo "🚀 Deploying Vira Assistant to AWS..."

# Configuration
AWS_REGION="us-west-2"
ECR_REPOSITORY="vira-assistant"
ECS_CLUSTER="vira-cluster"
ECS_SERVICE="vira-service"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Build Docker image
echo "🏗️  Building Docker image..."
docker build -f Dockerfile.prod -t $ECR_REPOSITORY .

# Login to ECR
echo "🔐 Logging into Amazon ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Tag and push to ECR
echo "📦 Pushing to ECR..."
docker tag $ECR_REPOSITORY:latest $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest

# Create ECS task definition
echo "⚙️  Creating ECS task definition..."
cat > task-definition.json << EOF
{
    "family": "vira-assistant",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "256",
    "memory": "512",
    "executionRoleArn": "arn:aws:iam::$ACCOUNT_ID:role/ecsTaskExecutionRole",
    "taskRoleArn": "arn:aws:iam::$ACCOUNT_ID:role/ecsTaskRole",
    "containerDefinitions": [
        {
            "name": "vira-assistant",
            "image": "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest",
            "portMappings": [
                {
                    "containerPort": 5000,
                    "protocol": "tcp"
                }
            ],
            "environment": [
                {
                    "name": "FLASK_ENV",
                    "value": "production"
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/vira-assistant",
                    "awslogs-region": "$AWS_REGION",
                    "awslogs-stream-prefix": "ecs"
                }
            }
        }
    ]
}
EOF

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Update ECS service
echo "🚀 Deploying to ECS..."
aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service $ECS_SERVICE \
    --task-definition vira-assistant \
    --force-new-deployment

# Get load balancer URL
echo "🌐 Getting application URL..."
LOAD_BALANCER_ARN=$(aws ecs describe-services --cluster $ECS_CLUSTER --services $ECS_SERVICE --query 'services[0].loadBalancers[0].targetGroupArn' --output text)
LOAD_BALANCER_NAME=$(echo $LOAD_BALANCER_ARN | cut -d'/' -f2 | cut -d'/' -f1)

echo "✅ Deployment complete!"
echo "📱 Your Vira Assistant is being deployed to ECS"
echo "🔗 Check the AWS Console for the Load Balancer URL"

# Clean up
rm task-definition.json
