# HomomorphicFiltering

## Prerequisites

To install OpenCV from the Ubuntu 18.04 repositories, follow these steps:

Refresh the packages index and install the OpenCV package by typing:

```sudo apt update```

```sudo apt install python3-opencv```

The command above will install all packages necessary to run OpenCV.

To verify the installation, import the cv2 module and print the OpenCV version:

```python3 -c "import cv2; print(cv2.__version__)"```


To run:

### OS

The current project is created and build under Ubuntu linux.

---

The following modules are needed for the project to run:

* python3
* OpenCv
* Tkinter

NOTE:
If you run the executable which is located in `dist/hf` in the project folder, the modules are not necessary to be installed

***

### OpenCv

Refresh the packages index and install the OpenCV package by typing:

>sudo apt update
>
>sudo apt install python3-opencv

The command above will install all packages necessary to run OpenCV.

To verify the installation:

> python3 -c "import cv2; print(cv2.\_\_version\_\_)"

***

<h3>Tkinter</h3>

To install Tkinter type:

>sudo apt-get install python3-tk

To verify the installation:

>python3 -c "import tkinter; print(tkinter.TkVersion)"

***
### Other

For the other project dependencies run the following command from inside the project folder:

>sudo pip install -r requirements.txt

# Run the project

The project comes both as a `.py` script and bundled as an executable.

## Ubuntu

For running the script type the following from within the project folder:

> python3 hf.py path/to/image

To use the executable file:
* Change the access permissions of the file
> sudo chmod a+x dist/hf

* Then run the file as normal from within the project folder:

> ./dist/hf

When you run the script or the executable, a popup will appear where you will choose an image.
The window will load with the sliders to make any changes needed.
When satisfied with your output press `Esc` and a another dialogue box will appear to chose where to save the result.