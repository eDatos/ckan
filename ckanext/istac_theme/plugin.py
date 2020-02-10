import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation


def get_all_groups():
    '''Return a list of all the groups

    '''
    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'package_count desc', 'all_fields': True})

    return groups


def get_count_all_datasets():
    '''Returns the total number or datasets
    '''
    package_list = toolkit.get_action('package_list')(
        data_dict={
        })
    count = len(package_list)

    return count


class IstacThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'istac_theme')

    def get_helpers(self):
        '''Register the get_all_groups function as a template helper function.
        '''
        return {'istac_theme_get_all_groups': get_all_groups,
                'istac_theme_get_count_all_datasets': get_count_all_datasets,
                }
