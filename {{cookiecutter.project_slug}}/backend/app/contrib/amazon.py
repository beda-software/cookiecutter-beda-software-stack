import boto3


def generate_aws_signed_url(aws_access_key_id,
                            aws_secret_access_key,
                            aws_bucket, object_name, expires_in, content_type=None,
                            http_method=None):
    session = boto3.Session(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
    s3client = session.client('s3')
    action = 'put_object' if http_method == 'PUT' else 'get_object'

    params = {'Bucket': aws_bucket,
              'Key': object_name
    }

    if content_type:
        params['ContentType'] = content_type

    return s3client.generate_presigned_url(action,
                                           Params=params,
                                           ExpiresIn=expires_in,
                                           HttpMethod=http_method)
