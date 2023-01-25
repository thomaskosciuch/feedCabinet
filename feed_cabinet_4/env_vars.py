from aws_cdk import aws_ssm

def get_env_vars(self, NAME:str) -> dict:
    # access_key = aws_ssm.StringParameter.value_for_string_parameter(
    #     self, "synthetic_holding_aws_access_key_id")
    # secret_access_key = aws_ssm.StringParameter.value_for_string_parameter(
    #     self, "synthetic_holding_secret_access_key")
    sentry_dsn = aws_ssm.StringParameter.value_for_string_parameter(
        self, "LAMBDA_SENTRY_DSN")
    user = aws_ssm.StringParameter.value_for_string_parameter(
        self, "SFTP_NBIN_USER")
    host_url = aws_ssm.StringParameter.value_for_string_parameter(
        self, "SFTP_NBIN_HOST")
    password = aws_ssm.StringParameter.value_for_string_parameter(
        self, "SFTP_NBIN_PASSWORD")
    
    return {
        # "KEY_ID": access_key, 
        # "ACCESS_KEY": secret_access_key,
        "NAME": NAME,
        "SENTRY_DSN": sentry_dsn,
        "SFTP_NBIN_USER": user,
        "SFTP_NBIN_PASSWORD": password,
        "SFTP_NBIN_HOST": host_url
    }
