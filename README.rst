
=============
ckanext-istac_theme
=============

Extensión que contiene la capa de estilos del portal de datos abiertos del ISTAC

------------
Requirements
------------

Extensión creada para la versión 2.7.2 de CKAN

-----------
Installation
------------


Para instalar la extensión ckanext-istac_theme:

1. Activar el entorno Python del CKAN estando como el usuario ckan::

     . default/bin/activate

2. Instalar la extensión ckanext-istac_theme en el entorno virtual de Python::

     pip install ckanext-istac_theme

3. Añadir la extensión en la lista de plugins de CKAN  en el fichero de configuración
   ``/servers/opendata/ckan/default/development.ini`` en la propiedad ``ckan.plugins`` añadir ``istac_theme``

4. Reiniciar el servidor Apache estando como root::

     systemctl restart httpd


------------------------
Development Installation
------------------------

Para instalar la extensión ckanext-istac_theme en Desarrollo hacer lo siguiente 
estando dentro del entorno virtual de Python::

    git clone https://git.arte-consultores.com/istac/ckan-istac.git
    cd ckanext-istac_theme
    python setup.py develop
    pip install -r dev-requirements.txt

