from sentry_sdk import add_breadcrumb, capture_message, set_tag
from sftp_connect import SftpS3File, get_sftp_files, sftp_connect, sftp_paramiko_connect
import boto3
import pysftp
import time

from helper import sftp_to_s3_filename
from s3_connect import get_s3_files
from sentry import init_sentry



def handler(event, context):
    folder_name = "/users/ETFCM/RPT" #event['folder_name']
    bucket_name = "qnext.custodian.nbin" #event['bucket_name']
    
    init_sentry()
    sftp: pysftp.Connection = sftp_connect()
    sftp_files: list[SftpS3File] = get_sftp_files(sftp, folder_name, sftp_to_s3_filename)  
    s3_files: list[str] = get_s3_files(bucket_name)
    difference = [x for x in sftp_files if f'{x.s3_name}' not in s3_files]
    add_breadcrumb(message = 'data count', data = {
        'sftp':str(len(sftp_files)),
        's3': str(len(s3_files)),
        'diff': str(len(difference))}
    )

    success = []
    failed = []
    sftp_paramiko = sftp_paramiko_connect()
    
    try:
        for file in difference:
            t = time.time()
            try:
                with sftp_paramiko.open(f'{folder_name}/{file.sftp_name}', "r") as io_file:
                    io_file.prefetch()
                    s3 = boto3.client('s3')
                    s3.put_object(Body=io_file, Bucket=bucket_name, Key=f'{file.s3_name}')
                success += [str(file)]
            except:
                failed += (str(file))
            print(f'{file.s3_name}: {time.time() - t}s')
        sftp_paramiko.close()
    except:
        sftp_paramiko.close()
        raise

    set_tag('transfered', len(success))
    add_breadcrumb(message = 'files', data = {'failed': failed, 'success': success})
    capture_message('Feed The Cabinet Report', level='info')

if __name__ == "__main__":

    event = {
        "folder_name": "/users/ETFCM/RPT",
        "bucket_name": "qnext.custodian.nbin"
    }

    handler(event, None)