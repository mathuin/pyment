from tempfile import mkstemp
from shutil import move
from os import remove, close

def replace(file, pattern, subst):
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'w')
    old_file = open(file)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    new_file.close()
    close(fh)
    old_file.close()
    remove(file)
    move(abs_path, file)
fh, abs_path = mkstemp()
stockname = 'settings-stock.py'
settingsname = 'settings.py'

oldsitename = "^SITE_NAME = .*$"
newsitename = "SITE_NAME = 'Pyment'"

oldmetadesc = "^META_DESCRIPTION = .*$"
newmetadesc = "META_DESCRIPTION = 'Pyment is a small online supplier of high-quality fermented honey wine products.'"

olddbengine = "'ENGINE': .*$"
newdbengine = "'ENGINE: 'django.db.backends.sqlite3'"

oldsecretkey = "^SECRET_KEY = .*$"
newsecretkey = "SECRET_KEY = '&amp;b_htw&amp;h^-@cd&amp;666#-s49)=h@yijtb1oz+o@(a^!+-5610hcd'
"

# overwrite the stock file
old_settings = open(settingsname, 'r')
new_stock = open(stockname, 'w')
for line in old_file:
    line.replace("^SITE_NAME = .*$", "SITE_NAME = 'Pyment'").replace("^META_DESCRIPTION = .*$
