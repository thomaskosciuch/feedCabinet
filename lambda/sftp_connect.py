
import pysftp
from os import environ

def sftp_connect() -> pysftp.Connection:

    hostname = environ['STFP_NBIN_HOST']
    username = environ["SFTP_NBIN_USER"]
    password = environ["SFTP_NBIN_PASSWORD"]
    
    username = 'ETFCM'
    hostname = 'sftp.corrnet.com'
    password = 'wijf&XjD!&jabf'

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

if __name__ == "__main__":
    sftp_connect()