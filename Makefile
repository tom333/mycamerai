
.PHONY: tests clean quality

tests: build-devbox # Execution des tests
	$(call execute_cmd) run pytest -c pyproject.toml -s --log-cli-level=10  --junitxml=./junit_report.xml

quality: build-devbox # Execution des outils de qualité
	$(call execute_cmd) run black -l 200 --target-version py37 photo
	$(call execute_cmd) run isort --recursive ./photo -vvv
	$(call execute_cmd) run flake8 photo --ignore=E501

clean: # Ménage des fichiers générés
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -f junit_report.xml
	rm -Rf .coverage
	rm -Rf dist
	rm -Rf *.egg-info
	rm -Rf .pytest_cache

# If the first argument is "poetry"...
ifeq (poetry,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "poetry"
  POETRY_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(POETRY_ARGS):dummy;@:)
endif

build-devbox: # Construction de l'image de dev
	docker build -t mycamerai-devbox -f Dockerfile.dev .

poetry: build-devbox
	$(call execute_cmd) $(POETRY_ARGS)

distclean: build-buildozer
	docker run --interactive --tty --rm -u 1000 -v buildozer_home:/home/user/.buildozer  --volume ${CURDIR}:/home/user/hostcwd mycamerai-buildozer distclean

build-buildozer: # Construction de l'image de dev
	docker build -t mycamerai-buildozer -f Dockerfile .

deploy: build-buildozer
	docker run -t --volume ~/.buildozer:/home/user/.buildozer --volume ${CURDIR}:/home/user/hostcwd mycamerai-buildozer android debug deploy run logcat

init-buildozer: build-buildozer
#	docker volume create buildozer_home
#	docker run --interactive --tty --rm --volume ${CURDIR}:/home/user/hostcwd mycamerai-buildozer android update
#	docker run --interactive --tty --rm -u 1000 -v buildozer_home:/home/user/.buildozer --entrypoint "sudo" mycamerai-buildozer chown -R 1000 /home/user/.buildozer
#	docker run --interactive --tty --rm -u 1000 -v buildozer_home:/home/user/.buildozer  --volume ${CURDIR}:/home/user/hostcwd mycamerai-buildozer android update
#	docker run --interactive --tty --rm --mount type=volume,source=buildozer_home,target=/home/user/.buildozer  --volume ${CURDIR}:/home/user/hostcwd mycamerai-buildozer android update
#  --volume "$HOME/.buildozer":/home/user/.buildozer \

build-ide: # Construction de l'image contenant vscode
	docker build -t mycamerai-ide -f Dockerfile.ide .

run-ide: build-ide # Lancement de Vscode
	docker run -it -p 127.0.0.1:8080:8080 -v "${CURDIR}:/home/coder/project" mycamerai-ide --auth none &
	xdg-open "http://localhost:8080/?folder=vscode-remote%3A%2F%2Flocalhost%3A8080%2Fhome%2Fcoder%2Fproject" &


define execute_cmd
	docker run -i -v ${CURDIR}:/opt/mycamerai --env-file .env mycamerai-devbox $(1)
endef