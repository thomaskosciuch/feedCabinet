import boto3

def get_s3_files(bucket_name):

    s3 = boto3.client('s3')
    kwargs = {
        'Prefix':'ftp/raw',
        'Bucket': bucket_name
    }
    
    continuation_token = None
    file_names = []
    while True:
        if continuation_token:
            kwargs['ContinuationToken'] = continuation_token
        files = s3.list_objects_v2(**kwargs)
        for obj in files["Contents"]:
            file_names.append(obj['Key'])
        continuation_token = files.get("NextContinuationToken", None)
        if not continuation_token:
            break        
    return file_names

if __name__ == '__main__':
    file_names = get_s3_files('qnext.custodian.nbin')
    print(file_names)