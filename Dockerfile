FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt
#CMD streamlit run src/Home.py --server.maxUploadSize 2000 --server.maxMessageSize 1000
CMD sh run.sh