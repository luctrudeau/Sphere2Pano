#Sphere2Pano

Sphere2Pano is a simple tool to convert image taken from mirrored-spheres to panoramas.

##Dependencies:
* [Python 2.7.x](https://www.python.org/downloads/)
* [OpenCV](http://opencv.org/downloads.html)
* [Numpy](http://www.numpy.org/)

##Installation:
###MacOS (via brew):
Open a terminal and enter the following commands:
* First, install brew
```
ruby -e "$(curl -kfsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
* Next, add _homebrew/science_
```
brew tap homebrew/science
```
* Now, we can install OpenCV using brew:
```
brew install opencv
```
* Almost there, we just need to link OpenCV to python:
```
ln -s /usr/local/Cellar/opencv/2.4.10/lib/python2.7/site-packages/cv.py cv.py
ln -s /usr/local/Cellar/opencv/2.4.10/lib/python2.7/site-packages/cv2.so cv2.so
```

##Start:
```
python Server.py
``` 
