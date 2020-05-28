FROM python:alpine

RUN pip install flask python-dateutil Werkzeug
COPY . /
RUN chmod +x entrypoint.sh
EXPOSE 5000

ENTRYPOINT [ "./entrypoint.sh" ]
