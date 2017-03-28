import os
import datetime
import json
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from celery.result import AsyncResult
from celeryproj import tasks as celerytasks
from vimtofileprocess.initalprocess import vimtoprocessor as fileproc
from polls.utils import random_floats
from polls.models import Color
from polls.forms import PersonForm
from polls.StationHandler import STATIONS

sectionlng = [-1.8992970113788488, -1.8990261082683446, -1.8987478290830495,  -1.8986492579017522, -1.8985298996005895,
              -1.8983890836273076, -1.8983287339244725, -1.8983052645955922, -1.8982730780874135, -1.8982489382062795,
              -1.898223457220638,  -1.8981932823692205,  -1.8981617664132955,  -1.8981382970844152, -1.8981134866510274,
              -1.8980786179338338, -1.8980477725301625, -1.8979994927678945, -1.897910979870403, -1.8978171025548818,
              -1.8977453534637334, -1.897700426462734, -1.8976454411779287, -1.8975850914750936, -1.8974851791892888,
              -1.8973624681268575, -1.8972873662744405, -1.8971532558236959, -1.8970841889415624, -1.8969514195953252]
sectionlat = [52.47864501918298, 52.478630316614954, 52.47860499551409, 52.47859764422404, 52.47858947612251,
              52.47858294164019, 52.47858865931228, 52.47859519379372, 52.47860540391909, 52.478614797232304,
              52.47863235863859, 52.478657679723696, 52.478702604193664, 52.47874916223232, 52.4788055218974,
              52.47889210327125, 52.47895132156562, 52.47899747093974, 52.479048521075995, 52.47909671235026,
              52.47914980437096, 52.47920371312644, 52.47929029371671, 52.47937483214751, 52.479484691025064,
              52.479605576313055, 52.47968562179398, 52.47979752186503, 52.479855513760704, 52.48002228099191]


def view_index(request):
    context = {
                'title': 'Save Variables',
                'message': " Hello, world. You're at the polls index.",
                'year': datetime.datetime.now().year,
                'sectionlng': sectionlng,
                'sectionlat': sectionlat,
        }
    return render(request, 'inline-viewbox-zoomed.html', context)


def view_home(request):
    context = {
                'title': 'View Home',
                'message': " . You're at the home view.",
                'year': datetime.datetime.now().year,
        }
    return render(request, 'home.html', context)


def view_contact(request):
    context = {
                'title': 'Contact Details',
                'message': " Hello, world. You're at the contacts page.",
                'year': datetime.datetime.now().year,
        }
    return render(request, 'contact.html', context)


@csrf_exempt
def view_buttons(request):
    """Renders the Buttons UI page."""

    assert isinstance(request, HttpRequest)
    # if post request came
    if request.method == 'POST':
        # getting values from post
        RangeA = request.POST.get('RangeA')
        RangeB = request.POST.get('RangeB')
        RangeC = int(RangeA) + int(RangeB)
        # adding the values in a context variable
        context = {
            'title': 'Call Results',
            'message': 'Your Results page.',
            'year': datetime.datetime.now().year,
            'RangeA': RangeA,
            'RangeB': RangeB,
            'RangeC': RangeC
        }
        return render(request, 'buttonsresults.html', context)
    else:
        # if post request is not true
        # returning the form template
        # adding the values in a context variable
        context = {
                'title': 'Save Variables',
                'message': 'Save Python Functions page.',
                'year': datetime.datetime.now().year,
        }
        return render(request, 'buttonssubmit.html', context)


def view_listdatafolder(request):
    vimtoprocess = fileproc('init')
    path = os.path.join(settings.VIMTO_FILE_RAW)
    rawdatafilesTDMS = []
    rawdatafilesTDMSValid = []
    dirs = os.listdir(path)

    FileSections = ["1-2:20160811-0804", "2-3:20160811-0804", "3-4:20160811-0804",
                    "4-5:20160811-0804", "5-6:20160811-0804", "6-7:20160811-0804"]

    if settings.DEBUGDATAFILES is True:
        print('listdatafolder:PATH:', path)
        print('listdatafolder:url:', settings.MEDIA_URL)
        print('listdatafolder:list', dirs)
    filetime = datetime.datetime.today()
    mintime = filetime + datetime.timedelta(-9999)
    maxtime = filetime + datetime.timedelta(9999)
    for file in dirs:
        # print('listdatafolder:',file)
        if file.endswith("tdms"):
            filetime = fileproc.getFileDateTime(fileproc, file)
            if (filetime > mintime):
                mintime = filetime
            if (filetime < maxtime):
                maxtime = filetime
            rawdatafilesTDMS.append("%s" % str(filetime))
            if vimtoprocess.didMove(file):
                rawdatafilesTDMSValid.append(True)
            else:
                rawdatafilesTDMSValid.append(False)
    del dirs
    del file
    # '04/01/2016''20161006'
    context = {
            'title': 'RAW DATA',
            'year': datetime.datetime.now().year,
            'rawdatafilesTDMS': rawdatafilesTDMS,
            'rawdatafilesTDMSValid': rawdatafilesTDMSValid,
            'mintime': mintime,
            'maxtime': maxtime,
            'sections': FileSections,
    }

    return render(request, 'rawdatafolder.html', context)


def view_ajax(request):
    context = {
                'title': 'ajax test',
                'message': " update page without reloading",
                'year': datetime.datetime.now().year,
        }
    return render(request, 'ajaxtest.html', context)


@csrf_exempt
def view_player(request):
    """Renders the Player UI page."""

    selected_station = STATIONS[0]
    assert isinstance(request, HttpRequest)
    # if post request came
    if request.method == 'POST':
        # getting values from post
        playerstate = 1
        # Generate 1000 random  numbers which are between 1 and 9999.
        data = random_floats(0.5, 2.8, 50000)
        # adding the values in a context variable
        context = {
            'selected_station': selected_station,
            'STATIONS': STATIONS,
            'title': 'Call Results',
            'message': 'Your Results page.',
            'year': datetime.datetime.now().year,
            'playerstate': playerstate,
            'data': data,
        }
        return render(request, 'playertest.html', context)
    else:
        # if post request is not true
        # returing the form template
        # adding the values in a context variable
        context = {
                'selected_station': selected_station,
                'STATIONS': STATIONS,
                'title': 'Save Variables',
                'message': 'Save Python Functions page.',
                'year': datetime.datetime.now().year,
        }
        return render(request, 'playertest.html', context)


@csrf_exempt
def view_celhome_1(request):

    # if post request is not true
    # returning the form template
    # adding the values in a context variable
    context = {
            'title': 'Save Variables',
            'message': 'Save Python Functions page.',
            'year': datetime.datetime.now().year,
    }
    return render(request, 'celhome.html', context)


@csrf_exempt
def do_task_1(request):

    assert isinstance(request, HttpRequest)
    # if post request came
    if request.method == 'POST':
        # getting values from post
        RangeA = request.POST.get('RangeA')
        RangeB = request.POST.get('RangeB')
        strbit = celerytasks.test_rabbit_running()
        RangeC = celerytasks.longtime_add(RangeA, RangeB) + " :at: " + strbit
        # adding the values in a context variable
        context = {
            'title': 'Call Results',
            'message': 'Your CELERY RESULTS page.',
            'year': datetime.datetime.now().year,
            'RangeA': RangeA,
            'RangeB': RangeB,
            'RangeC': RangeC
        }
        return render(request, 'buttonsresults.html', context)


@csrf_exempt
def view_celhome(request, ProcessFileName):

    context = {
        'title': 'Save Variables',
        'message': 'Save Python Functions page.',
        'year': datetime.datetime.now().year,
        'ProcessFileName': ProcessFileName
    }

    if 'task_id' in request.session.keys() and request.session['task_id']:
        task_id = request.session['task_id']
        context['task_id'] = task_id
        print('task_id:', task_id)

    print('view_celhome:', view_celhome)
    return render(request, 'celhome.html',  context)


@csrf_exempt
def do_task(request):
    """ A view the call the task and write the task id to the session """
    data = 'Fail'
    if request.is_ajax():
        job = celerytasks.create_models()
        request.session['task_id'] = job.id
        data = job.id
        print('data:', data)
    else:
        data = 'This is not an ajax request!'
        print('data:', data)
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')


MIN_SEARCH_CHARS = 2
"""
The minimum number of characters required in a search. If there are less,
the form submission is ignored. This value is used by the below view and
the template.
"""


class ColorList(ListView):
    """
    Displays all colors in a table with only two columns: the name of the
    color, and a "like/unlike" button.
    """
    model = Color
    context_object_name = "colors"

    def dispatch(self, request, *args, **kwargs):
        print("ColorList.Dispatch")
        self.request = request     # So get_context_data can access it.
        return super(ColorList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        print("ColorList.get_queryset")
        return super(ColorList, self).get_queryset()

    def get_context_data(self, **kwargs):
        print("ColorList.get_context_data")
        context = super(ColorList, self).get_context_data(**kwargs)

        global MIN_SEARCH_CHARS

        search_text = ""   # Assume no search
        if(self.request.method == "GET"):
            search_text = self.request.GET.get("search_text", "").strip().lower()
            if(len(search_text) < MIN_SEARCH_CHARS):
                search_text = ""   # Ignore search

        if(search_text != ""):
            color_search_results = Color.objects.filter(name__contains=search_text)
        else:
            color_search_results = []

        context["search_text"] = search_text
        context["color_search_results"] = color_search_results

        # For display under the search form
        context["MIN_SEARCH_CHARS"] = MIN_SEARCH_CHARS

        context["title"] = 'Call Results'
        context["message"] = 'Your CELERY RESULTS page.'
        context["year"] = datetime.datetime.now().year
        return context


def toggle_color_like(request, color_id):
    """Toggle "like" for a single color, then refresh the color-list page."""
    color = None
    try:
        # There's only one object with this id, but this returns a list
        # of length one. Get the first (index 0)
        color = Color.objects.filter(id=color_id)[0]
    except Color.DoesNotExist as e:
        raise ValueError("Unknown color.id=" + str(color_id) + ". error: " + str(e))

    color.is_favorited = not color.is_favorited
    color.save()  # Commit the change to the database

    return redirect("urlnme_color_list")  # See urls.pycolor


def view_passarray(request):
    context = {
                'title': 'Pass Array Details',
                'message': " Hello, world. You're at the contacts page.",
                'year': datetime.datetime.now().year,
        }
    return render(request, 'passdata.html', context)


def changeZoom(request):
    pass


def view_Accordian(request):
    context = {
                'title': 'Family Details',
                'message': " Hello, Accordian page.",
                'year': datetime.datetime.now().year,
        }
    return render(request, 'Accordian.html', context)
