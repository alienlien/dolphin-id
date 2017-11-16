Install python3.6 on CentOS:
Ref: https://www.softwarecollections.org/en/scls/rhscl/rh-python36/
$ sudo yum install centos-release-scl
$ sudo yum install scl-utils-build
$ sudo yum install yum-utils
$ sudo yum-config-manager --enable centos-sclo-rh-testing
$ sudo yum install rh-python36
$ scl enable rh-python36 bash

Install pip on CentOS:
$ sudo yum -y install python-pip

Install opencv on CentOS:
Ref: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_fedora/py_setup_in_fedora.html
1) Install Dependency
$ sudo yum install epel-release -y
$ sudo yum update -y
$ sudo yum install cmake
$ sudo yum install python-devel numpy
$ sudo yum install gcc gcc-c++
$ sudo yum install gtk2-devel
$ sudo yum install libdc1394-devel
$ sudo yum install libv4l-devel
$ sudo yum install gstreamer-plugins-base-devel

2) Install FFMPEG
Ref: https://www.vultr.com/docs/how-to-install-ffmpeg-on-centos
$ sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
$ sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
$ sudo yum install ffmpeg ffmpeg-devel -y

3) Other dependencies
$ sudo yum install libpng-devel libjpeg-turbo-devel jasper-devel openexr-devel libtiff-devel libwebp-devel
$ sudo yum install tbb-devel eigen3-devel

4) Clone opencv source code
$ git clone https://github.com/opencv/opencv.git

5) Make
$ mkdir build
$ cd ./build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \ 
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_TBB=ON \
    -D WITH_EIGEN=ON ..
$ make
$ sudo make install
$ sudo ldconfig

# Installation
## Python environment
Ubuntu: Install python-logilab-common also.
$ git clone https://git.ai.csie.ndhu.edu.tw/alienlien/dolphin-id.git
$ sudo apt install python-logilab-common
$ pip3 install pipenv
$ pipenv install
$ pipenv shell -c

## Install darkflow
$ git clone https://github.com/thtrieu/darkflow
$ pip install -e .

## Get the model
TODO: Find the place/procedure to get/set model.
- ./model/dolphin_classifier.h5
- ./ckpt

## Test
1. Start the server
$ python3 ./server.py
2. Run regression test
$ cd ./regression_test/
$ ./run.sh

Install gdrive tool
- Download the binary from web page or use homebrew.
$ brew install gdrive
- Ref: https://github.com/prasmussen/gdrive

Use the gdrive tool for the first time
1) Authentication needed.
2) Go to the following url as shown in the command line.
3) Enter verification code as shown in the browser.

Get weight 
- https://drive.google.com/drive/folders/0B1tW_VtY7onidEwyQ2FtQVplWEU
- tiny-yolo-voc.weights

Training Dataset:
- Dolphin images and bounding boxes.
- https://drive.google.com/drive/folders/0B3a2oBXXOsEqbXlodDZuUV9RVVk

Bounding box tool:
- VGG VIA: http://www.robots.ox.ac.uk/~vgg/software/via/

Dataset backup:
- Classifier: classifier_src.tar.gz
- Detector: detector_src.tar.gz.a{a..j}, and join file.
$ cat detector_src.tar.gz.a{a..j} > detector_src.tar.gz

Classifier:

Prepare data
1) Merge the data according to the IDs.
2) Split the data into training and validation folders.
$ data.py
$ split.py

Train:
- $ ./train_classifier.sh

Detector:

Prepare data
$ python3 ./prepare_detector.py

Make sure that the yolo weight is in the bin folder.
- ./bin/yolo-voc.weights

Train the detector:
$ ./train_detector.sh

# Prepare Model
- Classifier: ./model/dolphin_classifier.h5
- Detector: ./ckpt
