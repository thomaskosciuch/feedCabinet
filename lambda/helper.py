def sftp_to_s3_filename(name:str) -> str or None:
    if not '.csv' in name.lower():
        return None
    if 'ETFCMVAL' in name:
        return f'ftp/val/{name}'
    if 'ETFCMADR' in name:
        return f'ftp/adr/{name}'
    if 'ETFCMAP' in name:
        return f'ftp/map/{name}'
    if 'ETFCMBK' in name:
        return f'ftp/mbk/{name}'
    if 'ETFCMPMT' in name:
        return f'ftp/pmt/{name}'
    if 'ETFCMTRD' in name:
        return f'ftp/trd/{name}'
    if 'ETFCMPOS' in name:
        return f'ftp/pos/{name}'
    if 'ETFCMTRD' in name:
        return f'ftp/unknown/{name}'
    return None
