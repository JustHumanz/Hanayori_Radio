FROM python:alpine

RUN pip install flask apscheduler python-dateutil
COPY . /
RUN chmod +x entrypoint.sh
EXPOSE 5000

ENTRYPOINT [ "./entrypoint.sh" ]
