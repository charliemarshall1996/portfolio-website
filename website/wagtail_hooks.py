from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from django_celery_beat.models import (
    IntervalSchedule,
    PeriodicTask,
    CrontabSchedule,
    ClockedSchedule,
    SolarSchedule
)


class CrontabScheduleSnippet(SnippetViewSet):
    model = CrontabSchedule
    list_display = ("minute", "hour", "day_of_week",
                    "day_of_month", "month_of_year")
    panels = [
        FieldPanel("minute"),
        FieldPanel("hour"),
        FieldPanel("day_of_week"),
        FieldPanel("day_of_month"),
        FieldPanel("month_of_year"),
    ]


class IntervalScheduleSnippet(SnippetViewSet):
    model = IntervalSchedule
    list_display = ("every", "period")
    panels = [
        FieldPanel("every"),
        FieldPanel("period"),
    ]


class ClockedScheduleSnippet(SnippetViewSet):
    model = ClockedSchedule
    list_display = ("clocked_time",)
    panels = [
        FieldPanel("clocked_time"),
    ]


class SolarScheduleSnippet(SnippetViewSet):
    model = SolarSchedule
    list_display = ("event", "latitude", "longitude")
    panels = [
        FieldPanel("event"),
        FieldPanel("latitude"),
        FieldPanel("longitude"),
    ]


class PeriodicTaskSnippet(SnippetViewSet):
    model = PeriodicTask
    list_display = (
        "name",
        "task",
        "enabled",
        "last_run_at",
        "total_run_count",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("task"),
        FieldPanel("interval"),
        FieldPanel("crontab"),
        FieldPanel("clocked"),
        FieldPanel("solar"),
        FieldPanel("args"),
        FieldPanel("kwargs"),
        FieldPanel("enabled"),
    ]


class SchedulingSnippetGroup(SnippetViewSetGroup):
    items = (CrontabScheduleSnippet, IntervalScheduleSnippet,
             ClockedScheduleSnippet, SolarScheduleSnippet, PeriodicTaskSnippet)
    menu_icon = "calendar-check"
    menu_label = "Scheduling"
    menu_name = "scheduling"


class PeriodicTaskSnippet(SnippetViewSet):
    model = PeriodicTask
    list_display = (
        "name",
        "task",
        "enabled",
        "last_run_at",
        "total_run_count",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("task"),
        FieldPanel("interval"),
        FieldPanel("args"),
        FieldPanel("kwargs"),
        FieldPanel("enabled"),
    ]


class WebsiteSchedulingSnippetGroup(SnippetViewSetGroup):
    items = (PeriodicTaskSnippet, IntervalScheduleSnippet)
    menu_icon = "calendar-check"
    menu_label = "Website Analysis Scheduling"
    menu_name = "website-analysis-scheduling"


register_snippet(WebsiteSchedulingSnippetGroup)
