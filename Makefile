.PHONY: prod stage docker local  # Mark targets as "phony" so they always run

local:
	ENVIRONMENT=local poetry run uvicorn app.main:app --host 0.0.0.0 --reload

prod:
	ENVIRONMENT=prod poetry run uvicorn app.main:app --host 0.0.0.0

stage:
	ENVIRONMENT=stage poetry run uvicorn app.main:app --host 0.0.0.0

docker:
	ENVIRONMENT=docker poetry run uvicorn app.main:app --host 0.0.0.0
