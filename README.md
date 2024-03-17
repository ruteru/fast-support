# Fast-Support

Fast-Support is a Python package designed to provide support for FastAPI applications when deploying on Firebase Functions. It includes utilities to handle incoming requests, route them to the appropriate FastAPI endpoints, and generate responses compatible with Firebase Functions.

## Installation

You can install Fast-Support via pip:

```bash
pip install fast-support
```


## Usage

```python
from fastapi import FastAPI
from firebase_functions import https_fn, options
from fast_support import router
import hello_world

my_name = FastAPI()

my_name.include_router(hello_world.app)

@https_fn.on_request(cors=options.CorsOptions(cors_origins=['*'], cors_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']))
def myfunction(req: https_fn.Request) -> https_fn.Response:
    router(req, app=my_name, debug=True)
```


## Features
- Routing incoming requests to FastAPI endpoints
- Handling query parameters and request body
- Debug mode for logging request details


## Contributing
Contributions are welcome! Please feel free to submit issues or pull requests.