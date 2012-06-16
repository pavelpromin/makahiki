"""Admin definition for Smart Grid Game widget."""
from django.db import models
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.smartgrid.models import ActionMember, Activity, Category, Event, \
                                     Commitment, ConfirmationCode, TextPromptQuestion, \
                                     QuestionChoice, Level
from django.contrib import admin
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.util import ErrorList
from django.forms import TextInput, Textarea
from django.core.urlresolvers import reverse


class TextQuestionInlineFormSet(BaseInlineFormSet):
    """Custom formset model to override validation."""

    def clean(self):
        """Validates the form data and checks if the activity confirmation type is text."""

        # Form that represents the activity.
        activity = self.instance
        if not activity.pk:
            # If the activity is not saved, we don't care if this validates.
            return

        # Count the number of questions.
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass

        if activity.confirm_type == "text" and count == 0:
            # Why did I do this?
            # activity.delete()
            raise forms.ValidationError(
                "At least one question is required if the activity's confirmation type is text.")

        elif activity.confirm_type != "text" and count > 0:
            # activity.delete()
            raise forms.ValidationError("Questions are not required for this confirmation type.")


class QuestionChoiceInline(admin.TabularInline):
    """Question Choice admin."""
    model = QuestionChoice
    fieldset = (
        (None, {
            'fields': ('question', 'choice'),
            'classes': ['wide', ],
            })
        )
    extra = 4


class TextQuestionInline(admin.TabularInline):
    """Text Question admin."""
    model = TextPromptQuestion
    fieldset = (
        (None, {
            'fields': ('question', 'answer'),
            })
        )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 70})},
        }

    extra = 1
    formset = TextQuestionInlineFormSet


class ActivityAdminForm(forms.ModelForm):
    """Activity Admin Form."""
    class Meta:
        """Meta"""
        model = Activity

    def clean(self):
        """
          Validates the admin form data based on a set of constraints.

            1.  Events must have an event date.
            2.  If the verification type is "image" or "code", then a confirm prompt is required.
            3.  If the verification type is "text", then additional questions are required
                (Handled in the formset class below).
            4.  Publication date must be before expiration date.
            5.  If the verification type is "code", then the number of codes is required.
            6.  Either points or a point range needs to be specified.
        """

        # Data that has passed validation.
        cleaned_data = self.cleaned_data

        #2 Check the verification type.
        confirm_type = cleaned_data.get("confirm_type")
        prompt = cleaned_data.get("confirm_prompt")
        if confirm_type != "text" and len(prompt) == 0:
            self._errors["confirm_prompt"] = ErrorList(
                [u"This confirmation type requires a confirmation prompt."])
            del cleaned_data["confirm_type"]
            del cleaned_data["confirm_prompt"]

        #4 Publication date must be before the expiration date.
        if "pub_date" in cleaned_data and "expire_date" in cleaned_data:
            pub_date = cleaned_data.get("pub_date")
            expire_date = cleaned_data.get("expire_date")

            if expire_date and pub_date >= expire_date:
                self._errors["expire_date"] = ErrorList(
                    [u"The expiration date must be after the pub date."])
                del cleaned_data["expire_date"]

        #6 Either points or a point range needs to be specified.
        points = cleaned_data.get("point_value")
        point_range_start = cleaned_data.get("point_range_start")
        point_range_end = cleaned_data.get("point_range_end")
        if not points and not (point_range_start or point_range_end):
            self._errors["point_value"] = ErrorList(
                [u"Either a point value or a range needs to be specified."])
            del cleaned_data["point_value"]
        elif points and (point_range_start or point_range_end):
            self._errors["point_value"] = ErrorList(
                [u"Please specify either a point_value or a range."])
            del cleaned_data["point_value"]
        elif not points:
            point_range_start = cleaned_data.get("point_range_start")
            point_range_end = cleaned_data.get("point_range_end")
            if not point_range_start:
                self._errors["point_range_start"] = ErrorList(
                    [u"Please specify a start value for the point range."])
                del cleaned_data["point_range_start"]
            elif not point_range_end:
                self._errors["point_range_end"] = ErrorList(
                    [u"Please specify a end value for the point range."])
                del cleaned_data["point_range_end"]
            elif point_range_start >= point_range_end:
                self._errors["point_range_start"] = ErrorList(
                    [u"The start value must be less than the end value."])
                del cleaned_data["point_range_start"]
                del cleaned_data["point_range_end"]

        return cleaned_data

    def save(self, *args, **kwargs):
        _ = args
        _ = kwargs
        activity = super(ActivityAdminForm, self).save(*args, **kwargs)

        activity.save()

        # If the activity's confirmation type is text, make sure to save the questions.
        if self.cleaned_data.get("confirm_type") == "text":
            self.save_m2m()

        return activity


class EventAdminForm(forms.ModelForm):
    """Event Admin Form."""
    num_codes = forms.IntegerField(required=False,
        label="Number of codes",
        help_text="Number of confirmation codes to generate",
        initial=0
    )

    def __init__(self, *args, **kwargs):
        """
        Override to change number of codes help text if we are editing an activity and add in a
        list of RSVPs.
        """
        super(EventAdminForm, self).__init__(*args, **kwargs)

        # Instance points to an instance of the model.
        # Check if it is created and if it has a code confirmation type.
        if self.instance and self.instance.type:
            url = reverse("activity_view_codes", args=(self.instance.type, self.instance.slug,))
            self.fields["num_codes"].help_text = "Number of additional codes to generate " \
                "<a href=\"%s\" target=\"_blank\">View codes</a>" % url

            url = reverse("activity_view_rsvps", args=(self.instance.type, self.instance.slug,))
            self.fields["event_max_seat"].help_text += \
                " <a href='%s' target='_blank'>View RSVPs</a>" % url

    class Meta:
        """Meta"""
        model = Event

    def clean(self):
        """
          Validates the admin form data based on a set of constraints.

            1.  Events must have an event date.
            2.  If the verification type is "image" or "code", then a confirm prompt is required.
            3.  If the verification type is "text", then additional questions are required
                (Handled in the formset class below).
            4.  Publication date must be before expiration date.
            5.  If the verification type is "code", then the number of codes is required.
            6.  Either points or a point range needs to be specified.
        """

        # Data that has passed validation.
        cleaned_data = self.cleaned_data

        #1 Check that an event has an event date.
        is_event = cleaned_data.get("type") == "event"
        event_date = cleaned_data.get("event_date")
        has_date = "event_date" in cleaned_data   # Check if this is in the data dict.
        if is_event and has_date and not event_date:
            self._errors["event_date"] = ErrorList([u"Events require an event date."])
            del cleaned_data["event_date"]

        #4 Publication date must be before the expiration date.
        if "pub_date" in cleaned_data and "expire_date" in cleaned_data:
            pub_date = cleaned_data.get("pub_date")
            expire_date = cleaned_data.get("expire_date")

            if expire_date and pub_date >= expire_date:
                self._errors["expire_date"] = ErrorList(
                    [u"The expiration date must be after the pub date."])
                del cleaned_data["expire_date"]

        #5 Number of codes is required if the verification type is "code"
        has_codes = "num_codes" in cleaned_data
        num_codes = cleaned_data.get("num_codes")
        if has_codes and not num_codes:
            self._errors["num_codes"] = ErrorList(
                [u"The number of codes is required for this confirmation type."])
            del cleaned_data["num_codes"]

        return cleaned_data

    def save(self, *args, **kwargs):
        _ = args
        _ = kwargs
        activity = super(EventAdminForm, self).save(*args, **kwargs)

        activity.save()

        # Generate confirmation codes if needed.
        if self.cleaned_data.get("num_codes") > 0:
            ConfirmationCode.generate_codes_for_activity(activity,
                self.cleaned_data.get("num_codes"))

        return activity


class LevelAdmin(admin.ModelAdmin):
    """Level Admin"""
    list_display = ["name", "priority"]

admin.site.register(Level, LevelAdmin)
challenge_mgr.register_game_admin_model("smartgrid", Level)


class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""
    list_display = ["name", "priority"]
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)
challenge_mgr.register_game_admin_model("smartgrid", Category)


class ActivityAdmin(admin.ModelAdmin):
    """Activity Admin"""
    fieldsets = (
        ("Basic Information",
         {'fields': (('name', 'type'),
                     ('slug', 'related_resource'),
                     ('title', 'duration'),
                     'image',
                     'description',
                     ('video_id', 'video_source'),
                     'embedded_widget',
                     ('pub_date', 'expire_date'),
                     ('unlock_condition', 'unlock_condition_text'),
                     )}),
        ("Points",
         {"fields": (("point_value", "social_bonus"), ("point_range_start", "point_range_end"), )}),
        ("Ordering", {"fields": (("level", "category", "priority"), )}),
        ("Confirmation Type", {'fields': ('confirm_type', 'confirm_prompt')}),
    )
    prepopulated_fields = {"slug": ("name",)}
    form = ActivityAdminForm
    inlines = [TextQuestionInline]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})},
        }

    list_display = ["title", "level", "category", "priority", "point_value"]

    actions = ["delete_selected", "increment_priority", "decrement_priority"]

    def delete_selected(self, request, queryset):
        """override the delete selected."""
        _ = request
        for obj in queryset:
            obj.delete()

    delete_selected.short_description = "Delete the selected objects."

    def increment_priority(self, request, queryset):
        """increment priority."""
        _ = request
        for obj in queryset:
            obj.priority += 1
            obj.save()

    increment_priority.short_description = "Increment selected objects' priority by 1."

    def decrement_priority(self, request, queryset):
        """decrement priority."""
        _ = request
        for obj in queryset:
            obj.priority -= 1
            obj.save()

    decrement_priority.short_description = "Decrement selected objects' priority by 1."

admin.site.register(Activity, ActivityAdmin)
challenge_mgr.register_game_admin_model("smartgrid", Activity)


class EventAdmin(admin.ModelAdmin):
    """Event Admin"""
    fieldsets = (
        ("Basic Information",
         {'fields': (('name', 'type'),
                     ('slug', 'related_resource'),
                     ('title', 'duration'),
                     'image',
                     'description',
                     ('pub_date', 'expire_date'),
                     ('event_date', 'event_location', 'event_max_seat'),
                     ('unlock_condition', 'unlock_condition_text'),
                     )}),
        ("Points", {"fields": (("point_value", "social_bonus"),)}),
        ("Ordering", {"fields": (("level", "category", "priority"), )}),
        ("Confirmation Code", {'fields': ('num_codes',)}),
        )
    prepopulated_fields = {"slug": ("name",)}
    form = EventAdminForm

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})},
        }

    list_display = ["title", "level", "category", "priority", "type",
                    "event_date", "point_value", ]

    actions = ["delete_selected", "increment_priority", "decrement_priority"]

    def delete_selected(self, request, queryset):
        """override the delete selected."""
        _ = request
        for obj in queryset:
            obj.delete()

    delete_selected.short_description = "Delete the selected objects."

    def increment_priority(self, request, queryset):
        """increment priority."""
        _ = request
        for obj in queryset:
            obj.priority += 1
            obj.save()

    increment_priority.short_description = "Increment selected objects' priority by 1."

    def decrement_priority(self, request, queryset):
        """decrement priority."""
        _ = request
        for obj in queryset:
            obj.priority -= 1
            obj.save()

    decrement_priority.short_description = "Decrement selected objects' priority by 1."

admin.site.register(Event, EventAdmin)
challenge_mgr.register_game_admin_model("smartgrid", Event)


class CommitmentAdmin(admin.ModelAdmin):
    """Commitment Admin."""
    fieldsets = (
        ("Basic Information", {
            'fields': ('name',
                       ('slug', 'related_resource'),
                       ('title', 'duration'),
                       'image',
                       'description',
                       'unlock_condition', 'unlock_condition_text',
                       ),
            }),
        ("Points", {"fields": (("point_value", 'social_bonus'), )}),
        ("Ordering", {"fields": (("level", "category", "priority"), )}),
        )
    prepopulated_fields = {"slug": ("name",)}

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})},
        }

    list_display = ["title", "level", "category", "priority", "point_value"]

    actions = ["delete_selected", "increment_priority", "decrement_priority"]

    def delete_selected(self, request, queryset):
        """override the delete selected."""
        _ = request
        for obj in queryset:
            obj.delete()

    delete_selected.short_description = "Delete the selected objects."

    def increment_priority(self, request, queryset):
        """increment the priority."""
        _ = request
        for obj in queryset:
            obj.priority += 1
            obj.save()

    increment_priority.short_description = "Increment selected objects' priority by 1."

    def decrement_priority(self, request, queryset):
        """decrement the priority."""
        _ = request
        for obj in queryset:
            obj.priority -= 1
            obj.save()

    decrement_priority.short_description = "Decrement selected objects' priority by 1."

admin.site.register(Commitment, CommitmentAdmin)
challenge_mgr.register_game_admin_model("smartgrid", Commitment)


class ActionMemberAdminForm(forms.ModelForm):
    """Activity Member admin."""
    def __init__(self, *args, **kwargs):
        """Override to dynamically change the form if the activity specifies a point range.."""

        super(ActionMemberAdminForm, self).__init__(*args, **kwargs)
        # Instance points to an instance of the model.
        member = self.instance
        if member and member.action and not member.action.point_value:
            action = member.action
            message = "Specify the number of points to award.  This value must be between %d and %d"
            message = message % (action.point_range_start, action.point_range_end)
            self.fields["points_awarded"].help_text = message

    class Meta:
        """Meta"""
        model = ActionMember

    def clean(self):
        """Custom validator that checks values for variable point activities."""

        # Data that has passed validation.
        cleaned_data = self.cleaned_data
        status = cleaned_data.get("approval_status")

        action = self.instance.action
        if status == "approved" and not action.point_value:
            # Check if the point value is filled in.
            if "points_awarded" not in cleaned_data:
                self._errors["points_awarded"] = ErrorList(
                    [u"This action requires that you specify the number of points to award."])

            # Check if the point value is valid.
            elif cleaned_data["points_awarded"] < action.point_range_start or \
                 cleaned_data["points_awarded"] > action.point_range_end:
                message = "The points to award must be between %d and %d" % (
                    action.point_range_start, action.point_range_end)
                self._errors["points_awarded"] = ErrorList([message])
                del cleaned_data["points_awarded"]
        elif status == "approved" and "points_awarded" in cleaned_data:
            self._errors["points_awarded"] = ErrorList(
                [u"This field is only required for activities with variable point values."])
            del cleaned_data["points_awarded"]

        return cleaned_data


class ActionMemberAdmin(admin.ModelAdmin):
    """ActionMember Admin."""
    radio_fields = {"approval_status": admin.HORIZONTAL}
    fields = (
        "user", "action", "question", "admin_link", "full_response", "image",
        "admin_comment", "approval_status",)
    readonly_fields = (
        "question", "admin_link", "full_response", "social_email", "social_email2",)
    list_display = (
        "action", "submission_date", "approval_status", "short_question", "short_response")
    list_filter = ["approval_status", "action__type"]
    actions = ["delete_selected"]
    date_hierarchy = "submission_date"
    ordering = ["submission_date"]

    form = ActionMemberAdminForm

    def short_question(self, obj):
        """return the short question."""
        return "%s" % (obj.question)

    short_question.short_description = 'Question'

    def short_response(self, obj):
        """return the short response"""
        return "%s %s" % (obj.response, obj.image)

    short_response.short_description = 'Response'

    def full_response(self, obj):
        """return the full response."""
        return "%s" % (obj.response).replace("\n", "<br/>")

    full_response.short_description = 'Response'
    full_response.allow_tags = True

    def changelist_view(self, request, extra_context=None):
        """
        Set the default filter of the admin view to pending.
        Based on iridescent's answer to
        http://stackoverflow.com/questions/851636/default-filter-in-django-admin
        """
        if 'HTTP_REFERER' in request.META and 'PATH_INFO' in request.META:
            test = request.META['HTTP_REFERER'].split(request.META['PATH_INFO'])
            if test[-1] and not test[-1].startswith('?'):
                if not 'approval_status__exact' in request.GET:
                    q = request.GET.copy()
                    q['approval_status__exact'] = 'pending'
                    request.GET = q
                    request.META['QUERY_STRING'] = request.GET.urlencode()

        return super(ActionMemberAdmin, self).changelist_view(request,
            extra_context=extra_context)

    def delete_selected(self, request, queryset):
        """override the delete selected."""
        _ = request
        for obj in queryset:
            obj.delete()

    delete_selected.short_description = "Delete the selected objects."

    def get_form(self, request, obj=None, **kwargs):
        """Override to remove the points_awarded field if the action
        does not have variable points."""
        if obj and not obj.action.point_value:
            self.fields = ("user", "action", "question", "admin_link", "response", "image",
                           "admin_comment", "approval_status", "points_awarded", "social_email")
        else:
            self.fields = ("user", "action", "question", "admin_link", "response", "image",
                           "admin_comment", "approval_status")

        return super(ActionMemberAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(ActionMember, ActionMemberAdmin)
challenge_mgr.register_game_admin_model("smartgrid", ActionMember)
