FROM python
RUN mkdir /app
WORKDIR /app
ADD . /app/
EXPOSE 5020
ENV DB=netplanner
ENV DB_PORT=5432
ENV DB_HOST=localhost
ENV DB_PASS=sinadbpass1132
ENV DB_USER=netplanner
ENV MAIL_USERNAME=netplanner@sinacomsys.com
ENV MAIL_PASSWORD=@NetPl@nner2020@
ENV BROKER_DEFAULT_USER=sina
ENV BROKER_DEFAULT_PASSWORD=sina
ENV BROKER_HOST=localhost
ENV BROKER_PORT=5672
ENV SECRET_KEY=9cb762ea2b00298a069fd05ee2662f9b031b71a4cdde32bb971943e3e384f06d
ENV ALGORITHM=HS256
RUN cd /app/
RUN pip3 install -r req.txt