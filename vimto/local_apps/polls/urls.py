from django.conf.urls import url

from polls.views import *

urlpatterns = [
    url(r'^home$', view_home, name='urlnme_home'), 
    url(r'^contact', view_contact, name='urlnme_contact'),
    url(r'^button/add/$', view_buttons, name='urlnme_buttonA'),
    url(r'^button/result/$', view_buttons, name='urlnme_buttonR'),
    url(r'^Raw/$', view_listdatafolder, name='urlnme_raw'),
    url(r'^Ajax/$', view_ajax, name='urlnme_ajax'),
    url(r'^celery/$', view_celhome,{'ProcessFileName':"Tram19_Data_20160811-080443.4490.TDMS" } , name='urlnme_celeryhome'),
    url(r'^celery/do_task$', do_task, name='do_task'),
    url(r'^celery/poll_state$', poll_state, name='poll_state'),
    url(r'^player/$', view_player, name='urlnme_player'),
    url(r"^color/$", ColorList.as_view(), name="urlnme_color_list"),
    url(r"^color/like_color_(?P<color_id>\d+)/$", toggle_color_like, name="urlnme_toggle_color_like"),
    url(r"^passarray/$",view_passarray, name="urlnme_passdata"), 
    url(r'^', view_index, name='urlnme_index'),

]
