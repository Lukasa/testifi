FROM pypy:2

ADD . /testifi

RUN pip install /testifi

EXPOSE 8080

CMD ["testifi"]
