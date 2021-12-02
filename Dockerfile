FROM public.ecr.aws/lambda/python:3.9

# Copy function code
COPY /pipeline/* ${LAMBDA_TASK_ROOT}/
COPY README.md ${LAMBDA_TASK_ROOT}

COPY pyproject.toml poetry.lock ./
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

WORKDIR /pipeline
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]

