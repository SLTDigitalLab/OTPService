FROM python:3.11-alpine
RUN mkdir build
WORKDIR /build
COPY . .
RUN pip install -r requirements.txt 
# --no-cache-dir
EXPOSE 8000
WORKDIR /build/app
CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000
# CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000