FROM python:3.7
WORKDIR /usr/pai_python_sdk_cd

RUN curl https://gosspublic.alicdn.com/ossutil/install.sh | bash
RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install wheel
RUN python3 -m pip install twine

# Aone pipeline need the following command to successfully run the image
CMD ["sleep","infinity"]