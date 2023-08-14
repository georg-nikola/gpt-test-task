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
    try:
        s3.Object(bucket_name, 'metrics.json').put(Body=json.dumps(metrics))
    except s3.meta.client.exceptions.NoSuchBucket as e:
        return {
            'statusCode': 500,
            'body': f"Error: The bucket '{bucket_name}' does not exist."
        }
    except s3.meta.client.exceptions.AccessDenied as e:
        return {
            'statusCode': 403,
            'body': f"Error: Access denied when writing to '{bucket_name}'."
        }
    except Exception as e:
        # Catch any other exception (this is a general exception, so be cautious about using it)
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

    return {
        'statusCode': 200,
        'body': json.dumps(metrics)
    }

