provider "aws" {
    region = "us-west-2"
}

resource "aws_s3_bucket" "my_bucket" {
    bucket = "my-unique-bucket-name"
    acl    = "private"
}

resource "aws_iam_role" "s3_access_role" {
    name = "s3_access_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "ec2.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_policy" "s3_access_policy" {
    name        = "s3_access_policy"
    description = "Policy to allow S3 access"
    policy      = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = [
                    "s3:ListBucket",
                    "s3:GetObject",
                    "s3:PutObject"
                ]
                Effect   = "Allow"
                Resource = [
                    aws_s3_bucket.my_bucket.arn,
                    "${aws_s3_bucket.my_bucket.arn}/*"
                ]
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "s3_access_policy_attachment" {
    role       = aws_iam_role.s3_access_role.name
    policy_arn = aws_iam_policy.s3_access_policy.arn
}
