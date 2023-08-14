import boto3

def create_s3_bucket(bucket_name):
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucket_name)

def create_disks_and_snapshots():
    ec2 = boto3.resource('ec2')
    # Create unattached disk
    ec2.create_volume(Size=1, AvailabilityZone='us-west-1a')
    
    # Create non-encrypted disks
    for _ in range(2):
        ec2.create_volume(Size=1, AvailabilityZone='us-west-1a', Encrypted=False)
    
    # Create encrypted snapshots
    for _ in range(3):
        volume = ec2.create_volume(Size=1, AvailabilityZone='us-west-1a', Encrypted=False)
        snapshot = volume.create_snapshot(Description="Encrypted Snapshot")
        # If you want to cleanup and not maintain the volumes, delete them after creating snapshots
        volume.delete()

def create_lambda_role():
    iam = boto3.client('iam')
    trust_relationship = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    response = iam.create_role(RoleName='LambdaMetricsRole', AssumeRolePolicyDocument=json.dumps(trust_relationship))
    role_arn = response['Role']['Arn']
    
    # Attach necessary permissions to the role
    policies = ["arn:aws:iam::aws:policy/AmazonS3FullAccess", "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"]
    for policy in policies:
        iam.attach_role_policy(RoleName='LambdaMetricsRole', PolicyArn=policy)
    
    return role_arn

if __name__ == "__main__":
    bucket_name = "aws-metrics-bucket"
    create_s3_bucket(bucket_name)
    create_disks_and_snapshots()
    create_lambda_role()
