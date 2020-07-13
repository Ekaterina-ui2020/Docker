FROM python:3.7-slim-buster
RUN python -m pip install --user numpy scipy
WORKDIR /result
COPY matrixProfile.py  /resuilt/matrixProfile.py
CMD ["python", "/resuilt/matrixProfile.py"]
