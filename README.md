# Proyecto de grado GITSIGHT PRO

## Autores
- Alejandro Ahogado Prieto (a.ahogado@uniandes.edu.co)
- Juan Sebastián Hoyos Muñoz (js.hoyosm@uniandes.edu.co)

## Descripción

Este repositorio contiene el código desarrollado como parte de la tesis GITSIGHT PRO. El objetivo de este proyecto es proveer las herramientas necesarias para la creación de un análisis de repositorios públicos de GitHub, de forma que se puedan encontrar ciertas tendencias en la efectividad y eficiencia de los desarrolladores, tras haber recolectado, transformado y presentado la información.

## Requisitos 

- Asegúrese de tener instalado python 3.9 (este se testeó específicamente con Python 3.9.2rc1 y 3.9.2) ya que algunas de las librerías utilizadas pueden presentar incompatibilidades con otras versiones. De igual manera, es necesario tener instalado y configurado postgreSQL 16 en las variables del entorno (apuntador al bin de PosgreSQL 16 y al bin del ODBC). 

- Es necesario que se cree manualmente la base de datos llamada datamining_db, con el esquema public (solo la primera vez) asignada al usuario postgres. Solo es necesario que esté creada, los esquemas adicionales y modelos se cargarán automáticamente al iniciar la aplicación.
  Ejemplo:
    - CREATE DATABASE datamining_db;
    - \c datamining_db;
    - CREATE SCHEMA PUBLIC; (es posible que el esquema public se cree automáticamente)

- Clone el repositorio en su ordenador, en este caso haciendo uso de git bash ejecute (git clone https://github.com/SELF-Software-Evolution-Lab/gitsigth.git)

- Una vez realizado lo anterior, ejecute el archivo "requirements.txt" encontrado en la raíz del proyecto.
  Ejemplo:
     - pip install -r requirements.txt

- Finalmente, ejecute el archivo "start_server.sh" encontrado en la raíz del proyecto. (En bash ejecute ./start_server.sh)*
  - Si quiere finalizar el proceso en git bash use ctrl+c

- Una vez se finalice el proceso de descarga de datos, ejecute el archivo de tableau para ver el dashboard correspondiente. 

*Es importante tener en cuenta que siempre que se inicie la aplicación desde cero al ejecutar este archivo, se limpiará la base de datos, por lo que en la consola se le pedirá indicar la clave asignada a la base de datos. Cuando no se detiene por completo la aplicación y se realizan nuevos análisis, este procedimiento se realiza automáticamente.

Dependiendo de su sistema operativo y configuración es posible que deba brindar ciertos permisos para poder ejecutar la aplicación.

### Recomendación
- Le recomendamos hacer uso de git bash para facilitar el uso de la aplicación. Lo puede encontrar en https://git-scm.com/downloads
- Si desea instalar la versión de python mencionada, la puede encontrar aquí https://www.python.org/downloads/release/python-392/

## Usuario administrador
En caso de que sea el nuevo administrador de la aplicación, en esta se implementó la autenticación con GitHub, por lo que esta debe estar registrada en OAuth Apps para poder usarla. 

Si quiere registrarla desde cero, diríjase a su cuenta de GitHub, en la sección de settings, developer settings, encontrará OAuth Apps. En este caso se configuró con la siguiente información:
- Name: DataMining
- Homepage URL: http://localhost:8000
- Authorization callback URL: http://localhost:8000/callback

Una vez realice el procedimiento anterior, se le generará un Client ID y Client Secret el cuál deberá reemplazar en el archivo views.py (GITHUB_CLIENT_ID y GITHUB_CLIENT_SECRET). Esta configuración se maneja de esta manera ya que actualmente el proyecto es privado, sin embargo, si desea aumentar la seguridad puede manejar los secretos en tu ambiente y realizar la respectiva configuración o hacer uso de AWS secrets o algo por el estilo.
