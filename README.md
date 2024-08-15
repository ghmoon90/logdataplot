
# Introduction 

This is python code building gui for depicting plot of log data imdiately at event place without any 3rd party SW. 
It is developed by chat GPT, and using tkinter, pandas, and matplotlib. 
The input file can be csv data, or excel data format. 


# environment 
▲ OS : windows 
▲ python based, dependency with pandas, matplotlib

# install 

## manual install 

1.download python installer from https://www.python.org/ftp/python </br>

2.install the python
▲ you need to add path the python path to environment path. </br></br>

3. update the pip by 
put this command to command line.
``` python
python -m pip install --upgrade pip
```

4. install packages (dependency : matplotlib, pandas, tkinter)
   put this command to command line. </br>
``` python
 pip install matplotlib pandas 
```
or 
``` python
 pip install -r requirements.txt
```

## install by vbs file
1. run install.bat or pkgset.vbs
2. it will download python 3.7.9-amd64, update pip, install required package automatically.

# user instruction 
1. run logplot.py by click button 
2. load files by click button.
3. select a file from file select dropdown list
4. select the data from the column select listbox, and click add button.
5. to depict a graph on new window, click plot graph button.
6. you can show or hide the grid by click grid checkbox.
7. by remove the data from column, you can erase the data from selection, and hide the data on next graph. 
