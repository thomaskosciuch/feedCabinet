
import pysftp
from paramiko import SFTPClient, Transport
from os import environ

hostname = environ['STFP_NBIN_HOST']
username = environ["SFTP_NBIN_USER"]
password = environ["SFTP_NBIN_PASSWORD"]

class SftpS3File():
    """
    Used to distinguish between S3 and SFTP files
    """

    def __str__(self):
        return f'sftp:{self.sftp_name}, s3:{self.s3_name}'

    def __init__(self, sftp_name:str, s3_name:str):
        self.sftp_name: str = sftp_name
        self.s3_name: str = s3_name

def sftp_connect() -> pysftp.Connection:
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    conn_params = {
                'host': hostname,
                'port': 22,
                'username': username,
                'cnopts': cnopts, 
                'password': password
            }
    conn = pysftp.Connection(**conn_params)
    return conn

def sftp_paramiko_connect() -> SFTPClient:
    transport = Transport((hostname, 22))
    transport.connect(None,username,password)
    return SFTPClient.from_transport(transport)

def get_sftp_files(connection: pysftp.Connection, folder_name, name_converter) -> list[SftpS3File]:
    filenames:list[SftpS3File] = []
    for filename in connection.listdir(folder_name):
        s3_name = name_converter(filename)
        if s3_name: filenames += [SftpS3File(filename, s3_name)]
    return filenames

if __name__ == "__main__":
    sftp_connect()