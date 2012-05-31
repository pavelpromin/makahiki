"""Invocation:  python manage.py setup_test_data <command>

Sets up test data given the specified <command>.  Possible commands are:

  * create_users <number users for each team>
  * delete_users
  * rounds
  * event_dates
  * resource_usages
  * resource_baselines
  * resource_goalsettings
  * all

If 'all', the number of users per team is set to 5."""

import datetime
from django.contrib.auth.models import User

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.managers.challenge_mgr.models import RoundSettings
from apps.managers.resource_mgr.models import EnergyUsage, WaterUsage
from apps.managers.team_mgr.models import Team
from apps.widgets.resource_goal.models import EnergyGoalSetting, EnergyBaselineHourly, \
    EnergyBaselineDaily, WaterGoalSetting, WaterBaselineDaily, WaterGoal, EnergyGoal
from apps.widgets.smartgrid.models import Event


class Command(MakahikiBaseCommand):
    """command"""
    help = "Setup the test data. Supported commands are : \n" \
           "  create_users <number_of_users for each team>\n" \
           "  delete_users \n" \
           "  rounds \n" \
           "  event_dates \n" \
           "  resource_usages \n" \
           "  resource_baselines \n" \
           "  resource_goalsettings \n" \
           "  all \n"

    def handle(self, *args, **options):
        """set up the test data"""

        if len(args) == 0:
            self.stdout.write(self.help)
            return

        operation = args[0]
        if operation == 'create_users':

            if len(args) == 1:
                self.stdout.write("Please specify the number of test users for each team.\n")
                return

            count = int(args[1])
            self.create_users(count)

        elif operation == 'delete_users':
            self.delete_users()
        elif operation == 'rounds':
            self.setup_rounds()
        elif operation == 'event_dates':
            self.setup_event_dates()
        elif operation == 'resource_usages':
            self.setup_resource_usages()
        elif operation == 'resource_baselines':
            self.setup_resource_baselines()
        elif operation == 'resource_goalsettings':
            self.setup_resource_goalsettings()
        elif operation == 'all':
            self.delete_users()
            self.create_users(5)
            self.setup_rounds()
            self.setup_event_dates()
            self.setup_resource_usages()
            self.setup_resource_baselines()
            self.setup_resource_goalsettings()
        else:
            self.stdout.write("Invalid command. see help for supported commands.\n")

    def create_users(self, count):
        """Create the specified number of test users for each team."""
        total_count = 0
        for team in Team.objects.all():
            for i in range(0, count):
                username = "testuser-%s-%d" % (team.slug, i)
                user = User.objects.create_user(username,
                                                username + "@test.com",
                                                password="testuser")
                profile = user.get_profile()
                profile.setup_complete = True
                profile.setup_profile = True
                profile.team = team
                profile.save()
                profile.add_points(25, datetime.datetime.today(), 'test points for raffle')
                total_count += 1

        self.stdout.write("%d test users created.\n" % total_count)

    def delete_users(self):
        """delete the test users name start with 'testuser-'."""
        users = User.objects.filter(username__startswith="testuser-")
        total_count = 0
        for user in users:
            user.delete()
            total_count += 1
        self.stdout.write("%d test users deleted.\n" % total_count)

    def setup_rounds(self):
        """set up test rounds, any existing rounds will be deleted."""

        for r in RoundSettings.objects.all():
            r.delete()

        start = datetime.datetime.today()
        end1 = start + datetime.timedelta(days=7)
        end2 = end1 + datetime.timedelta(days=7)
        overall_end = end2 + datetime.timedelta(days=7)

        RoundSettings(name="Round 1", start=start, end=end1).save()
        RoundSettings(name="Round 2", start=end1, end=end2).save()
        RoundSettings(name="Overall", start=end2, end=overall_end).save()

        self.stdout.write("set up 3 rounds, starting from today.\n")

    def setup_event_dates(self):
        """adjust event dates to start from the beginning of the competition"""
        for event in Event.objects.filter(event_date__lte=datetime.datetime.today()):
            event_day_delta = event.event_date.date() - datetime.date(2011, 10, 17)
            event.event_date = datetime.datetime.today() + event_day_delta

            pub_day_delta = event.pub_date - datetime.date(2011, 10, 17)
            event.pub_date = datetime.date.today() + pub_day_delta

            event.save()
        self.stdout.write("event dates adjusted to round date.\n")

    def setup_resource_usages(self):
        """remove any resource usage before the competition"""
        today = datetime.datetime.today()
        for usage in EnergyUsage.objects.filter(date__lte=today):
            usage.delete()
        for usage in WaterUsage.objects.filter(date__lte=today):
            usage.delete()

        # add initialize data for energy and water
        for team in Team.objects.all():
            WaterUsage(team=team, date=today.date(), time=datetime.time(15), usage=1).save()
            EnergyUsage(team=team, date=today.date(), time=datetime.time(15), usage=1).save()

        self.stdout.write("created initial resource usages for all teams.\n")

    def setup_resource_baselines(self):
        """set up the resource baseline data, all existing data will be delete."""

        # energy hourly
        for baseline in EnergyBaselineHourly.objects.all():
            baseline.delete()
        for team in Team.objects.all():
            for day in range(0, 7):
                for hour in range(1, 25):
                    EnergyBaselineHourly(team=team, day=day, hour=hour, usage=1000 * hour).save()

        # energy daily
        for baseline in EnergyBaselineDaily.objects.all():
            baseline.delete()
        for team in Team.objects.all():
            for day in range(0, 7):
                EnergyBaselineDaily(team=team, day=day, usage=1000 * 24).save()

        # water daily
        for baseline in WaterBaselineDaily.objects.all():
            baseline.delete()
        for team in Team.objects.all():
            for day in range(0, 7):
                WaterBaselineDaily(team=team, day=day, usage=1000 * 24).save()

        self.stdout.write("created test baselines for all teams.\n")

    def setup_resource_goalsettings(self):
        """set up the resource goal data. all existing data will be delete."""

        #EnergyGoal
        for goal in EnergyGoal.objects.all():
            goal.delete()
        for goal_setting in EnergyGoalSetting.objects.all():
            goal_setting.delete()

        for team in Team.objects.all():
            EnergyGoalSetting(team=team,
                              goal_percent_reduction=5,
                              warning_percent_reduction=3,
                              manual_entry=False,
                              manual_entry_time=datetime.time(15),
                              goal_points=20).save()

        # WaterGoal
        for goal in WaterGoal.objects.all():
            goal.delete()
        for goal_setting in WaterGoalSetting.objects.all():
            goal_setting.delete()

        for team in Team.objects.all():
            WaterGoalSetting(team=team,
                              goal_percent_reduction=5,
                              warning_percent_reduction=3,
                              manual_entry=True,
                              manual_entry_time=datetime.time(15),
                              goal_points=20).save()

        self.stdout.write("created test goal settings for all teams.\n")