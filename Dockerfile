FROM python:3
RUN mkdir /mailtoissue
WORKDIR /mailtoissue
ADD requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir ./accounts/
VOLUME /mailtoissue/accounts/
ADD checkMail.py ./

CMD python checkMail.py