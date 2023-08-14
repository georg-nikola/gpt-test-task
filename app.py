import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    s3 = boto3.resource('s3')
    
    unattached_volumes = list(ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}]))
    non_encrypted_volumes = list(ec2.volumes.filter(Filters=[{'Name': 'encrypted', 'Values': ['false']}]))
    non_encrypted_snapshots = list(ec2.snapshots.filter(Filters=[{'Name': 'encrypted', 'Values': ['false']}]))
    
    metrics = {
        'unattached_volumes_count': len(unattached_volumes),
        'unattached_volumes_size': sum([vol.size for vol in unattached_volumes]),
        'non_encrypted_volumes_count': len(non_encrypted_volumes),
        'non_encrypted_snapshots_count': len(non_encrypted_snapshots)
    }

    # Save metrics to S3
    bucket_name = "aws-metrics-bucket"
    s3.Object(bucket_name, 'metrics.json').put(Body=json.dumps(metrics))

    return {
        'statusCode': 200,
        'body': json.dumps(metrics)
    }

