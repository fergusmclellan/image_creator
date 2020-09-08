FROM alpine

RUN apk add python3 && \
    apk add py3-pip && apk add cmd:pip3 && \
    apk add gcc python3-dev jpeg-dev zlib-dev musl-dev

# We copy just the requirements.txt first to leverage Docker cache
ADD https://raw.githubusercontent.com/fergusmclellan/image_creator/master/requirements.txt /app/
ADD https://raw.githubusercontent.com/fergusmclellan/image_creator/master/image_creation_app.py /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "image_creation_app.py" ]
