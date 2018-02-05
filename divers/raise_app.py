#

import platform
import subprocess
import os

def raise_app():
    if platform.system() == 'Darwin':
        #os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        subprocess.call([
            '/usr/bin/osascript', '-e',
            'tell app "System Events" to set frontmost of every process whose unix id is {} to true'.format(os.getpid())
        ])