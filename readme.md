# Another word game  

## Installation
The master branch is based on Python 3.10 and PySide6.  
Create a virtual environment and install `PySide6` with `pip`.  
Before the first run, `widget/ui_{MainWindow,TopFrame}.py` has to be built:  
```
user@widget $ pyside6-uic MainWindow.ui > ui_MainWindow.py  
user@widget $ pyside6-uic TopFrame.ui > ui_TopFrame.py  
```

## Installation (Windows)
For easier set up on Windows, download `msys2_compat` branch instead.  
It is modified to be based on Python 3.9 and PySide2 which are available on msys2 as official packages.  
You don't need to build the files like on the master branch.  
The files are already included in the repository, because pyside2-uic is missing from the official package.  
