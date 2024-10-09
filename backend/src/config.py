import configparser
import os


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini"))


# this is used to set the environment to run the application
# by default it is set for "dev" - development
ENV = os.getenv("APP_ENV", "dev")

# Process ECG_REST_LEADS
ecg_rest_leads_str = config.get(ENV, 'ECG_REST_LEADS')
ecg_rest_leads = {
    k.strip(): int(v) for k, v in (item.split(':') for item in ecg_rest_leads_str.split(','))}

# Process ECG_SHAPE
ecg_shape = tuple(map(int, config.get(ENV, 'ECG_SHAPE').split(',')))