import re

stockname = 'settings-stock.py'
settingsname = 'settings.py'

oldnew = {
    "^SITE_NAME = .*$": "SITE_NAME = 'Pyment'",
    "^META_DESCRIPTION = .*$": "META_DESCRIPTION = 'Pyment is a small online supplier of high-quality fermented honey wine products.'",
    "^BREWER_NAME = .*$": "BREWER_NAME = 'Your Name'",
    "^BREWER_EMAIL = .*$": "BREWER_EMAIL = 'your_email@example.com'",
    "^BREWER_LOCATION = .*$": "BREWER_LOCATION = 'Anywhere, USA'",
    "'NAME': .*$": "'NAME': os.path.join(PROJECT_ROOT, 'pyment.sqlite3'),",
    "^SECRET_KEY = .*$": "SECRET_KEY = '&amp;b_htw&amp;h^-@cd&amp;666#-s49)=h@yijtb1oz+o@(a^!+-5610hcd'",
}

# brute force!
old_settings = open(settingsname, 'r')
new_stock = open(stockname, 'w')
for line in old_settings:
    for old, new in oldnew.iteritems():
        line = re.sub(old, new, line)
    new_stock.write(line)
old_settings.close()
new_stock.close()
