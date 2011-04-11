import simplejson as json

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

from elementtree import ElementTree
from decimal import *

from components.activities.models import *
from components.activities import *
from components.floors.models import *
from components.floors import *
from components.energy_goals import *
from components.makahiki_base import get_round_info
from pages.view_energy.forms import EnergyWallForm

from lib.restclient.restful_lib import *

@login_required
def index(request):
  user = request.user
  floor = user.get_profile().floor
  golow_activities = get_available_golow_activities(user)
  golow_posts = Post.objects.filter(floor=floor, style_class="user_post").order_by("-id")[:5]
  
  standings = []
  
  # wattdepot rest api call
  conn = Connection("http://server.wattdepot.org:8182/wattdepot/")
  ## conn = Connection("http://localhost:8182/wattdepot/")
  
  for f in Floor.objects.all():
    wdsource = "SIM_UH_" + f.dorm.name.upper() + "_FLOORS_" + f.slug
    floor_data_resp = conn.request_get("sources/" + wdsource + "/sensordata/latest")
    xmlString = floor_data_resp['body']
    dom = ElementTree.XML(xmlString)  
    for prop in dom.getiterator('Property'):
      if prop.findtext('Key') == 'powerConsumed' and f==floor:
        power = Decimal(prop.findtext('Value'))    # in W
      if prop.findtext('Key') == 'energyConsumedToDate':
        floor_energy = Decimal(prop.findtext('Value'))   # in kWh
        if f==floor:
          energy = floor_energy
    if f==floor:
      last_update = dom.findtext('Timestamp')
  
  rounds = get_round_info()
  scoreboard_rounds = []
  today = datetime.datetime.today()
  for key in rounds.keys():
    # Check if this round happened already or if it is in progress.
    # We don't care if the round happens in the future.
    if today >= datetime.datetime.strptime(rounds[key]["start"], "%Y-%m-%d"):
      # Slugify to create a div id.
      scoreboard_rounds.append(key)
  
  ## TODO. create the baseline table
  baseline = 24 
  energy = 20
  percent_reduce = 5;
  
  goals = FloorEnergyGoal.objects.filter(floor=floor);
  if goals.count() > 0:
    percent_reduce = goals[0].percent_reduction
  
  percent = 100 - percent_reduce  
  goal = baseline * percent / 100
  over = "over"
  diff = energy - goal
  if diff <= 0:
    over = "below"
    diff = 0 - diff
  
  bar_px = 150  
  if energy <= baseline:
    baseline_px = bar_px
    actual_px = bar_px * energy / baseline
  else:
    baseline_px = bar_px * baseline / energy
    actual_px = bar_px
  
  power_max = 1000    
  power = format(power, '.1f')        ## convert to kW if need
  energy = format(energy, '.1f')      ## convert to kWh if needed
  diff = format(diff, '.1f')
  
  helps = ["Current Lounge Power", "Overall kWh Score Board", "Daily Energy Goal Status"]
  helpfiles = ["view_energy/help1.html", "view_energy/help2.html", "view_energy/help3.html"]

  return render_to_response("energy/index.html",{
      "baseline": baseline,
      "goal":goal,
      "actual":energy,
      "percent":percent,
      "percent_reduce":percent_reduce,
      "actual_px":actual_px,
      "baseline_px":baseline_px,
      "over":over,
      "diff":diff,
      "power":power,
      "power_max":power_max,
      "last_update":last_update,
      "floor": floor,
      "scoreboard_rounds":scoreboard_rounds,
      "golow_activities":golow_activities,
      "posts":golow_posts,
      "wall_form": EnergyWallForm(),
      "help_info": {
        "prefix": "energy_index",
        "count": range(0, 3),
      }
    }
    ,context_instance=RequestContext(request))
    
@login_required
def post(request):
  if request.is_ajax() and request.method == "POST":
    form = EnergyWallForm(request.POST)
    if form.is_valid():
      post = Post(
          user=request.user, 
          floor=request.user.get_profile().floor, 
          text=form.cleaned_data["post"]
      )
      post.save()
      
      # Render the post and send it as a response.
      template = render_to_string("news/user_post.html", {"post": post}, 
          context_instance=RequestContext(request))
      return HttpResponse(json.dumps({
        "contents": template,
      }), mimetype="application/json")
    
    # At this point there is a form validation error.
    return HttpResponse(json.dumps({
        "message": "This should not be blank."
    }), mimetype="application/json")
  
  raise Http404    