FROM python:3
WORKDIR /usr/src/app
COPY auditor.py .
CMD ["python", "auditor.py"]