import os
import sys
import uvicorn

def run_app(environment):
    # Set the environment variable for the app
    os.environ["ENVIRONMENT"] = environment
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8080))
    reload = False

    if environment == "local":
        port = 8000
        reload = True
    elif environment == "stage":
        port = int(os.environ.get("PORT", 8080))
        reload = False
    elif environment == "prod":
        port = int(os.environ.get("PORT", 8080))
        reload = False
    elif environment == "docker":
        port = int(os.environ.get("PORT", 8080))
        reload = False
    else:
        print(f"Invalid environment: {environment}")
        sys.exit(1)

    print(f"Starting app in {environment} mode on port {port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)

# Wrapper functions for each environment
def dev():
    run_app("local")

def stage():
    run_app("stage")

def prod():
    run_app("prod")

def docker():
    run_app("docker")

if __name__ == "__main__":
    # Determine the environment from the command line or default to 'local'
    environment = sys.argv[1] if len(sys.argv) > 1 else "local"
    run_app(environment)
