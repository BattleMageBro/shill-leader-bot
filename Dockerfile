FROM python:3.9
# set work directory
RUN mkdir -p /bot/
WORKDIR /bot/
# copy project
COPY . /bot/
# install dependencies
RUN pip install -r requirements.txt
# run app
CMD ["python", "executor.py"]