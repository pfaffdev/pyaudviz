# PyAudViz (Python Audio Visualizer)

This is a little GUI tool using Qt5 which creates an audio visualization video from an input audio.
You can also give it a background image and set a title text.

I have tested the program on macOS (10.14.6 Mojave), although it should also work on Linux and Windows. If you encounter problems or find bugs running it or have features suggestions, please [file an issue](https://github.com/pfaffdev/pyaudviz/issues/new).


## Dependencies

You need Python 3, PySide2, PIL (or Pillow), numpy and the program ffmpeg, which is used to read the audio and render the video.


## Installation

### Manual installation on Ubuntu

- Get all the python stuff: `sudo apt install python3 python3-pyqt4 python3-pil python3-numpy`
- If you have PySide2 installed, get pillow (at least version 3.3.0) from pip: `pip3 install pillow`
- Get ffmpeg/avconv: You can either use `avconv` from the standard repositories (package `libav-tools`) or get `ffmpeg` from the [website](http://ffmpeg.org/) or from a PPA (e.g. [https://launchpad.net/~jon-severinsson/+archive/ubuntu/ffmpeg](https://launchpad.net/~jon-severinsson/+archive/ubuntu/ffmpeg). The program does automatically detect if you don't have the ffmpeg binary and tries to use avconv instead.

Clone this repository and run PyAudViz with `python3 main.py`.


### Manual installation on Windows

- Download and install Python 3.4 from [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
- Download and install PyQt4 for Python 3.4 and Qt4 from [http://www.riverbankcomputing.co.uk/software/pyqt/download](http://www.riverbankcomputing.co.uk/software/pyqt/download)
- Download and install numpy from [http://www.scipy.org/scipylib/download.html](http://www.scipy.org/scipylib/download.html). There is an installer available, make sure to get the one for Python 3.4
- Download and install Pillow from [https://pypi.python.org/pypi/Pillow/3.3.0](https://pypi.python.org/pypi/Pillow/3.3.0)
- Download and install ffmpeg from [https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html). You can use the static builds.
- Add ffmpeg to your system PATH environment variable.

Clone this repository and run PyAudViz from the command line with `C:\Python34\python.exe main.py`.


### Manual installation on macOS

- Install [Homebrew](http://brew.sh/)
- Use the following commands to install the needed dependencies:

**NOTE:** If you already have `ffmpeg`, `sip` or `pyqt` installed, you will probably need to replace `install` with `reinstall`.

```
brew install python3
brew install -- ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-libass --with-libquvi --with-libvorbis --with-libvpx --with-opus --with-x265
brew install qt
brew install -- sip --with-python3
brew install -- pyqt --with-python3
pip3 install --upgrade pip
pip3 install pillow
pip3 install numpy
```

Clone this repository and run PyAudViz with `python3 main.py`.


## License

PyAudViz is licensed under the MIT license.
