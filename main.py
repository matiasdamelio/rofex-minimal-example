import configparser
import quickfix as fix
import time
from application import Application

user_config_filename = './conf/config.ini'
fix_config_filename = './conf/rofex.cfg'

config = configparser.ConfigParser(interpolation=None)
config.read(user_config_filename)

params = {
    'TargetCompID'    : config['ACCOUNT']['TargetCompID'],
    'SenderCompID'    : config['ACCOUNT']['SenderCompID'],
    'Password'        : config['ACCOUNT']['Password'],
    'Account'         : config['ACCOUNT']['Account']
}

settings       = fix.SessionSettings(fix_config_filename)
application    = Application(params['TargetCompID'], params['SenderCompID'], params['Password'], params['Account'])
storefactory   = fix.FileStoreFactory(settings)
logfactory     = fix.FileLogFactory(settings)
initiator      = fix.SocketInitiator(application, storefactory, settings, logfactory)

initiator.start()

while True:
    time.sleep(1)