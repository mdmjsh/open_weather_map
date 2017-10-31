FROM python:3-onbuild
COPY weatherdata . /
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "python", "./weatherdata/openweather.py" ]
