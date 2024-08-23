

import sys
import os

# Add the project directory to the sys.path
project_home = u'/qar/www'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

from qarweb import create_app

app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)

application = app