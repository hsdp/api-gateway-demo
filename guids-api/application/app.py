#!/usr/bin/env python3
import os
from factories.application import create_application


app = create_application()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
else:
    application = app
