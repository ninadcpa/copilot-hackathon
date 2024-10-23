This document provides a step-by-step guide to set up the necessary AWS resources for the hackathon. The resources include an API Gateway, Lambda function, DynamoDB table, S3 bucket, and IAM roles and policies.

## Prerequisites

- AWS CLI installed and configured
- AWS account with necessary permissions

## Steps

### 1. Create API Gateway

Create an API Gateway named `hackathon-aws-creds` with a Lambda function integration.

### 2. Create Lambda Function

Create a Lambda function named `hackathon_sts_token` and integrate it with the API Gateway.

### 3. Create DynamoDB Table

Create a DynamoDB table named `hackathon-user-table` with the following specifications:
- Provisioned capacity: 2
- Columns: `userid` (Primary Key), `policies`

### 4. Create S3 Bucket

Create an S3 bucket named `hackathon-bucket-1` with a restricted S3 bucket policy.

### 5. Create IAM Role

Create an IAM role named `hackathon-sts-system-role` with the following permissions:
- Permission to create IAM roles with names starting with `hackathon-*`
- Permission to create and attach IAM policies starting with `hackathon*`
- `sts:AssumeRole` on IAM roles starting with `hackathon*`
- Read/Write access on the DynamoDB table `hackathon-user-table`

### 6. Attach IAM Role to Lambda Function

Attach the IAM role `hackathon-sts-system-role` to the Lambda function `hackathon_sts_token`.

## Detailed Commands

### Create API Gateway


