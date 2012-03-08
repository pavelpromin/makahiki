"""Defines all possible User badges."""

from apps.lib.brabeion import badges
from apps.lib.brabeion.base import Badge, BadgeAwarded


class DailyVisitorBadge(Badge):
    """Daily Visitor Badge (visit 3 days in a row)"""
    name = "Daily Visitor"
    description = ["Visited the site 3 days in a row.", ]
    hint = "Keep coming back!"
    slug = "dailyvisitor"
    levels = ["Awarded", ]
    events = ["dailyvisitor", ]
    multiple = False
    image = "images/badges/Threepeater.gif"

    def award(self, **state):
        """award the badge"""
        user = state["user"]
        visits = user.get_profile().daily_visit_count
        if visits >= 3:
            return BadgeAwarded()

badges.register(DailyVisitorBadge)


class FullyCommittedBadge(Badge):
    """Fully Committed Badge (5 commitments at a time)."""
    name = "Fully Committed"
    description = ["Participating in 5 commitments at the same time.", ]
    hint = "How committed are you?"
    slug = "fully_committed"
    levels = ["Awarded", ]
    events = ["fully_committed", ]
    multiple = False
    image = "images/badges/badge.gif"

    def award(self, **state):
        """award the badge"""
        user = state["user"]
        current_members = user.commitmentmember_set.filter(
            award_date__isnull=True
        )
        if current_members.count() == 5:
            return BadgeAwarded()

badges.register(FullyCommittedBadge)


class BugHunterBadge(Badge):
    """Bug Hunter Badge (filed a bug report)."""
    name = "Bug Hunter"
    description = ["Filed a bug report.", ]
    hint = "Found a bug?  Let us know!"
    slug = 'bug_hunter'
    levels = ['Awarded', ]
    events = ['bug_hunter', ]
    multiple = False
    image = "images/badges/badge.gif"

    def award(self, **state):
        """Awards the badge to a user.
           Note that since this badge is awarded directly, we just return the badge award object.
        """
        _ = state
        return BadgeAwarded()

badges.register(BugHunterBadge)
