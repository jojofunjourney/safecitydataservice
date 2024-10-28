.PHONY: prod stage docker local  # Mark targets as "phony" so they always run

local:
	ENVIRONMENT=local poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# prod:
# 	ENVIRONMENT=prod poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080

# stage:
# 	ENVIRONMENT=stage poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080

# docker:
# 	ENVIRONMENT=docker poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080
