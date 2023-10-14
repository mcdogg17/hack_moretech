FROM python:latest

WORKDIR /jup
COPY . .

EXPOSE 88:88

RUN pip install --upgrade pip
RUN pip install --no-cache-dir jupyter -U && pip install --no-cache-dir jupyterlab
RUN pip install -r requirements.txt
