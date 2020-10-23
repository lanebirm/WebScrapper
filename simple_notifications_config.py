#
#  ______________________
# / Simple Notifications \
# \ By Davide Nastri     /
#  ----------------------
#     \ ^__^
#      \(oo)\_______
#       (__)\       )\/\
#         ||-----w |
#         ||      ||
#
# This script sends notification using
# Email, Pushbullet or Pushover
#
# Email has been tested using smtp.gmail.com and port 587
#
# Please fill in your data and make sure this configuration file is not readable by other users


# Email notification parameters
EMAIL_SENDER = 'lanebirmbetnotify@gmail.com'
EMAIL_PASSWORD = 'lanebirm78574'
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_SERVER_PORT = '587'
EMAIL_DEBUG_LEVEL = '0'

# Push notification parameters (Pushover)
PUSHOVER_APP_TOKEN = 'a4w1u48o3n5b7a3ajyoeu6dvfvenrc'
USER_KEY = 'ueziccgxnan7nrdcs4portymnqc1cz'

# Push notification parameters (Pushbullet)
PUSHBULLET_APP_TOKEN = 'YOUR_APP_TOKEN'
