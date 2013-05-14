'''
URLs definition for the SGG Designer.
Created on Feb 4, 2013

@author: Cam Moore
'''

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^newcol/(?P<col_slug>[\w\d\-]+)/(?P<level_slug>[\w\d\-]+)/(?P<column>[\d]+)/' +
        '(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.instantiate_column',
        name='instantiate_column'),
    url(r'^newaction/(?P<action_slug>[\w\d\-]+)/(?P<level_slug>[\w\d\-]+)' +
        '/(?P<column>[\d]+)/(?P<row>[\d]+)/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.instantiate_action',
        name='instantiate_action'),
    url(r'^paletteaction/(?P<action_slug>[\w\d\-]+)/(?P<level_slug>[\w\d\-]+)' +
        '/(?P<new_column>[\d]+)/(?P<new_row>[\d]+)/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.move_palette_action',
        name='move_palette_action'),
    url(r'^moveaction/(?P<action_slug>[\w\d\-]+)/(?P<level_slug>[\w\d\-]+)' +
        '/(?P<old_column>[\d]+)/(?P<old_row>[\d]+)/(?P<new_column>[\d]+)/(?P<new_row>[\d]+)/' +
        '(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.move_action',
        name='move_action'),
    url(r'^delete_action/(?P<action_slug>[\w\d\-]+)/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.delete_action',
        name='delete_designer_action'),
    url(r'^delete_column/(?P<col_slug>[\w\d\-]+)/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.delete_column',
        name='delete_designer_column'),
    url(r'^clear_from_grid/(?P<action_slug>[\w\d\-]+)/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.clear_from_grid',
        name='clear_from_grid'),
    url(r'^revert_to_grid/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.revert_to_grid',
        name='revert_to_grid'),
    url(r'^publish_to_grid/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.publish_to_grid',
        name='publish_to_grid'),
    url(r'^load_example_grid/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.load_example_grid',
        name='load_example_grid'),
    url(r'^run_lint/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.run_lint',
        name='unlock_lint'),
    url(r'^get_diff/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.get_diff',
        name='designer_diff'),
    url(r'^delete_level/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.delete_level',
        name='delete_designer_level'),
    url(r'^add_level/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.add_level',
        name='add_designer_level'),
    url(r'^set_event_date/(?P<draft_slug>[\w\d-]+)/$',
        'apps.widgets.smartgrid_design.views.set_event_date',
        name='set_designer_event_date'),
    url(r'^new_draft/$',
        'apps.widgets.smartgrid_design.views.new_draft',
        name='new_draft'),
    url(r'^copy_designer_action/(?P<action_slug>[\w\d-]+)/(?P<draft_slug>[\w\d\-]+)/$',
        'apps.widgets.smartgrid_design.views.copy_action',
        name='copy_designer_action'),
    url(r'^copy_library_action/(?P<action_slug>[\w\d-]+)/(?P<draft_slug>[\w\d\-]+)/$',
        'apps.widgets.smartgrid_library.views.copy_action',
        name='copy_designer_action'),
)
