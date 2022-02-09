# flask_postgresql_template

The purpose of this repository is to make a standard FLASK aplication template to create standard get request able to connect with a postgreSQL database, LOG management and error managenment with EMAIL (Configurated for GMAIL ).

Afther you get a working environment. You can use it and build new webservices.

## prerequisites

Has anaconda installed on windows. And configured you system variables ($path) of anaconda on windows:
* C:\ProgramData\Anaconda3
* C:\ProgramData\Anaconda3\Scripts
* C:\ProgramData\Anaconda3\Library\bin

## Instalation protocol

1. Clone the github repository.
```
$ git clone https://github.com/R-Rijnbeek/flask_postgresql_template.git
```

2. Enter the project folder.
```
$ cd flask_postgresql_template
```

3. Build the virtual environment on the repository by running:
```
$ build.bat
```

4. To activate the environmet and run the webservice:
```
$ activate ./env
$ python entrypoint.py
```
or use your interpreter using the right virtual environment.

Afther that, you can test it writing on your webbrowser: http://127.0.0.1:8080/hello_world?NAME=John getting as output:

```
{"DATA":{"message":"Hello World John"},"SUCCES":true}
```

## Notes to know:

1. The dependencies to use all features of this repository are writed on the environmet.yml file
2. Future feature: Make the EMAIL content optional
3. This repository is tested with windows 10 and anaconda version 4.11.0.
4. This is a standard template. You can use it for your purpose to make it easier to build you flask webservice aplication and install or create new features on your local repository.
