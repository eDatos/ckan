import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation

import json
import codecs
import requests



def get_all_groups():
    '''Return a list of all the groups
    '''
    groups = toolkit.get_action('group_list')(
        data_dict={'all_fields': True})

    return groups


def get_count_all_datasets():
    '''Returns the total number or datasets
    '''
    package_list = toolkit.get_action('package_search')(data_dict={})
    count = package_list.get('count')

    return count


CONFIG_FILE_PATH = "etc/config.json"
class IstacThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    # IConfigurer


    def __get_altered_header(self, header, json_config):
        """
        Método que modifica el header para hacer que contenga los botones dinámicos
        que se generan para esta aplicación en concreto.

        :param header: Código HTML del Header que se va a modificar
        :param json_config: Fichero de configuración cargado como un diccionario JSON
        """
        container_class = json_config['metadata']['htmlCodeClass']
        alteredHeader = header
        alteredHeader = "{% block header_wrapper %}" + alteredHeader + "{% endblock %}"

        # Añadimos los botones en la barra blanca
        code_container = """<div class=\"""" + container_class + """\" id=\"""" + container_class + """\"></div>"""
        code = """
        <div class=\"""" + container_class + """\" id=\"""" + container_class + """\">
            {% block header_account_container_content %}
                {% if c.userobj %}
                    {% block header_home_navigation_logueado %}
                        <a class="home-app pull-left" href="{{ h.url_for('home') }}">
                            <span class="title-icon">
                                <i class="fa fa-home" aria-hidden="true"></i>
                            </span>
                            {{ g.site_title  }}
                        </a>
                    {% endblock %}
                    <nav class="navigation">
                        <div class="nav-collapse collapse account avatar authed" data-module="me" data-me="{{ c.userobj.id }}">
                            <ul class="">
                                {% block header_account_logged %}
                                    {% if c.userobj.sysadmin %}
                                        <li>
                                            <a href="{{ h.url_for(controller='admin', action='index') }}"
                                                title="{{ _('Sysadmin settings') }}">
                                                <i class="fa fa-gavel" aria-hidden="true"></i>
                                                <span class="text">{{ _('Admin') }}</span>
                                            </a>
                                        </li>
                                    {% endif %}
                                    <li>
                                        <a href="{{ h.url_for(controller='user', action='read', id=c.userobj.name) }}" class="image"
                                            title="{{ _('View profile') }}">
                                            {{ h.gravatar((c.userobj.email_hash if c and c.userobj else ''), size=22) }}
                                            <span class="username">{{ c.userobj.display_name }}</span>
                                        </a>
                                    </li>
                                    {% set new_activities = h.new_activities() %}
                                    <li class="notifications {% if new_activities > 0 %}notifications-important{% endif %}">
                                        {% set notifications_tooltip = ngettext('Dashboard (%(num)d new item)', 'Dashboard (%(num)d new items)', new_activities) %}
                                        <a href="{{ h.url_for(controller='user', action='dashboard') }}"
                                            title="{{ notifications_tooltip }}">
                                            <i class="fa fa-tachometer" aria-hidden="true"></i>
                                            <span class="text">{{ _('Dashboard') }}</span>
                                            <span class="badge">{{ new_activities }}</span>
                                        </a>
                                    </li>
                                    {% block header_account_settings_link %}
                                        <li>
                                            <a href="{{ h.url_for(controller='user', action='edit', id=c.userobj.name) }}"
                                                title="{{ _('Edit settings') }}">
                                                <i class="fa fa-cog" aria-hidden="true"></i>
                                                <span class="text">{{ _('Settings') }}</span>
                                            </a>
                                        </li>
                                    {% endblock %}
                                    {% block header_site_navigation_tabs_3 %}
                                        {#{{ h.build_nav_main(('search', _('Datasets'))) }}#}
                                        <li>
                                            <a class="btn-datasets" href="{{ h.url_for('search') }}" title="{{ _('Datasets') }}">
                                                {{ _('Datasets') }}
                                            </a>
                                        </li>
                                    {% endblock %}
                                    {% block header_account_log_out_link %}
                                        <li>
                                            <a href="{{ h.url_for('/user/_logout') }}" title="{{ _('Log out') }}">
                                                <i class="fa fa-sign-out" aria-hidden="true"></i>
                                                <span class="text">{{ _('Log out') }}</span>
                                            </a>
                                        </li>
                                    {% endblock %}
                                {% endblock %}
                            </ul>
                        </div>
                    </nav>
                {% else %}
                    {% block header_home_navigation %}
                        <a class="home-app pull-left" href="{{ h.url_for('home') }}">
                            <span class="title-icon">
                                <i class="fa fa-home" aria-hidden="true"></i>
                            </span>
                            {{ g.site_title  }}
                        </a>
                    {% endblock %}
                    {% block header_site_navigation %}
                        <nav class="navigation">
                            <div class="nav-collapse collapse account avata account avatar">
                                <ul class="">
                                    {% block header_site_navigation_tabs_2 %}
                                        {#{{ h.build_nav_main(('search', _('Datasets'))) }}#}
                                        <li>
                                            <a class="btn-datasets" href="{{ h.url_for('search') }}" title="{{ _('Datasets') }}">
                                                {{ _('Datasets') }}
                                            </a>
                                        </li>
                                    {% endblock %}
                                    {% block header_account_log_out_link_2 %}
                                        <li>
                                            <a href="{{ h.url_for('/user/login') }}" title="{{ _('Log in') }}">
                                                <i class="fa fa-sign-in" aria-hidden="true"></i>
                                            </a>
                                        </li>   
                                    {% endblock %}
                                </ul>
                            </div>
                        </nav>
                    {% endblock %}
                {% endif %}
            {% endblock %}
        </div>
        """
        alteredHeader.replace(code_container, code)

        # Añadimos el botón hamburguesa
        code_container = """<div class="d-flex justify-content-end align-items-center">"""
        code = """
            <button data-target=".nav-collapse" data-toggle="collapse" class="btn btn-navbar" type="button">
                <span class="fa fa-bars"></span>
            </button>
            <div class="d-flex justify-content-end align-items-center">
        """
        alteredHeader.replace(code_container, code)

        return alteredHeader

    
    def __get_url(self, json_config, key):
        """
        Método genérico que devolverá la URL del header o footer según la clave que se pase

        :param json_config: Fichero de configuración cargado como un diccionario JSON
        :param key: Clave para buscar el header o footer
        """
        endpoint = json_config['metadata']['endpoint']
        url = "%s/properties/%s.json" % (endpoint, key)
        headers = {
            'Content-Type': 'text/html'
        }
        header_request = requests.get(url=url, headers=headers)
        json_header_request = json.loads(header_request)

        return json_header_request['value']


    def __get_header_url(self, json_config):
        """
        Método que devuelve la URL del header
        :param json_config: Fichero de configuración cargado como un diccionario JSON
        """
        header_key = json_config['metadata']['navbarPathKey']
        return "%s?appName=%s" % (self.__get_url(header_key), json_config['metadata']['appName'])


    def __get_footer_ulr(self, json_config):
        """
        Método que devuelve la URL del footer
        :param json_config: Fichero de configuración cargado como un diccionario JSON
        """
        footer_key = json_config['metadata']['footerPathKey']
        return "%s?appName=%s" % (self.__get_url(footer_key), json_config['metadata']['appName'])


    def __save_footer(self, footer):
        """
        Método que guarda el footer como template

        :param footer: Código del footer en formato string que se va a guardar
        """
        with codecs.open('templates/footer.html', 'w', encoding='utf8') as footer_file:
            footer_file.write(footer)


    def __save_header(self, header):
        """
        Método que guarda el header como template

        :param header: Código del header en formato string que se va a guardar
        """
        with codecs.open('templates/header.html', 'w', encoding='utf8') as header_file:
            header_file.write(header)


    def _load_header_footer(self):
        """
        Método que carga las templates para HEADER y FOOTER
        """
        with codecs.open(CONFIG_FILE_PATH, 'r', encoding='utf8') as config_file:
            json_config = json.loads(config_file.read())
            header = requests.get(url=self.__get_header_url(json_config)).content
            header = self.__get_altered_header(header=header, json_config=json_config)
            footer = requests.get(url=self.__get_footer_ulr(json_config)).content

            self.__save_header(header=header)
            self.__save_footer(footer=footer)


    def update_config(self, config_):
        self._load_header_footer()
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'istac_theme')


    def get_helpers(self):
        '''Register the get_all_groups function as a template helper function.
        '''
        return {
            'istac_theme_get_all_groups': get_all_groups,
            'istac_theme_get_count_all_datasets': get_count_all_datasets,
        }
