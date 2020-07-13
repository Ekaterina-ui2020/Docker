“experiment.tar.gz” file contain the docker image that runs “matrixProfile.py” program. To use it you must have Docker install on your computer. The program takes user provided time series and query and creates Matrix profile using user define subsequence length m. The prosses is based on “Matrix Profile I: All Pairs Similarity Joins for Time Series: A Unifying View that Includes Motifs, Discords and Shapelets” by C.M. Yeh, Y. Zhu, L. Ulanova, N. Begum, Y. Ding, H. Dau, D. Silva, A. Mueen, E. Keogh.
Navigate to the directory with “experiment.tar.gz” file
$ docker load < experiment.tar
$ docker run -it  -v //c/Users/pass_on_your_computer:/result matrix_profile,
where pass_on_your_computer is the directory where binary files with timeseries and query
are located and the result of the python program will be store. Format above is for Windows host. 

If “experiment.tar.gz” file is unavailable, you may build the image using the follow “Dockerfile”:
FROM python:3.7-slim-buster
RUN python -m pip install --user numpy scipy
WORKDIR /result
COPY matrixProfile.py  /resuilt/matrixProfile.py
CMD ["python", "/resuilt/matrixProfile.py"]

To build the image run:
$ docker build . --rm -t matrix_profile
To run the container run:
$ docker run -it  -v //c/Users/pass_on_your_computer:/result matrix_profile
, where pass_on_your_computer is the directory where binary files with timeseries and query
are located and the result of the python program will be store. Format above is for Windows host.  

Or you may download image using
$docker run it  -v //c/Users/pass_on_your_computer:/result ekaterinamiller/matrix_profile
