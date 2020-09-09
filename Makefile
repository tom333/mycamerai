
.PHONY: tests clean quality

tests: build-devbox # Execution des tests
	$(call execute_cmd) run pytest -c pyproject.toml -s --log-cli-level=10  --junitxml=./junit_report.xml

quality: build-devbox # Execution des outils de qualité
	$(call execute_cmd) run black -l 200 --target-version py37 mycamerai
	$(call execute_cmd) run isort --recursive ./mycamerai -vvv
	$(call execute_cmd) run flake8 mycamerai --ignore=E501

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
	podman build -t mycamerai-devbox -f Dockerfile.dev .

poetry: build-devbox
	$(call execute_cmd) $(POETRY_ARGS)

distclean: build-buildozer
	podman run --interactive --tty --rm -v buildozer_home:/home/user/.buildozer  --volume ${CURDIR}:/home/user/hostcwd mycamerai-buildozer distclean

build-buildozer: # Construction de l'image de dev
	podman build -t mycamerai-buildozer -f Dockerfile .

deploy: build-buildozer
	podman run -it \
					--privileged \
					--volume /dev/bus/usb:/dev/bus/usb \
					--volume buildozer_home:/root/.buildozer \
					--volume gradle_cache:/root/.gradle \
					--volume /home/moi/.android:/root/.android \
					--volume ${CURDIR}:/home/user/hostcwd \
					mycamerai-buildozer android debug deploy run logcat

build-ide: # Construction de l'image contenant vscode
	podman build -t mycamerai-ide -f Dockerfile.ide .

run-ide: build-ide # Lancement de Vscode
	podman run -it -p 127.0.0.1:8080:8080 -v "${CURDIR}:/home/coder/project" mycamerai-ide --auth none &
	xdg-open "http://localhost:8080/?folder=vscode-remote%3A%2F%2Flocalhost%3A8080%2Fhome%2Fcoder%2Fproject" &


define execute_cmd
	podman run -i -v ${CURDIR}:/opt/mycamerai --env-file .env mycamerai-devbox $(1)
endef