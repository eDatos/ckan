import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import os
from ckan.lib.plugins import DefaultTranslation


class IstacThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    # IConfigurer

    f = open("/servers/opendata/ckan/default/src/ckanext-istac_theme/ckanext/istac_theme/prueba.txt","w+")
    for i in range(10):
        f.write("This is line %d\r\n" % (i+1))
    f.close() 

    cwd = os.getcwd()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx " + cwd)    

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'istac_theme')
 
