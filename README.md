#Sphere2Pano

Sphere2Pano is a simple tool to convert image taken from mirrored-spheres to panoramas.

Here's a small video demonstrating the idea
<a href="http://www.youtube.com/watch?feature=player_embedded&v=U3dbtqcaSGI
" target="_blank"><img src="http://img.youtube.com/vi/U3dbtqcaSGI/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="640" height="360" border="10" /></a>

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
* Now, we can install OpenCV using brew
```
brew install opencv
```
* Almost there, open you python folder
```
cd /Library/Python/2.7/site-packages/
```
* Add the link to OpenCV
```
ln -s /usr/local/Cellar/opencv/2.4.10/lib/python2.7/site-packages/cv.py cv.py
ln -s /usr/local/Cellar/opencv/2.4.10/lib/python2.7/site-packages/cv2.so cv2.so
```

##Start:
```
python Server.py
``` 
