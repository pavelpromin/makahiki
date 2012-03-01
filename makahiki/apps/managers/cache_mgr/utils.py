"""Provides utility methods for invalidating various caches."""

from django.core.cache import cache
from django.utils.hashcompat import md5_constructor
from django.utils.http import urlquote


def invalidate_template_cache(fragment_name, *variables):
    """Invalidates the cache associated with a template.
    Credit: `djangosnippets.org/snippets/1593/ <http://djangosnippets.org/snippets/1593/>`_"""

    args = md5_constructor(u':'.join([urlquote(var) for var in variables]))
    cache_key = 'template.cache.%s.%s' % (fragment_name, args.hexdigest())
    cache.delete(cache_key)


def invalidate_info_bar_cache(user):
    """Invalidates the user and team caches of the info bar."""
    invalidate_template_cache("infobar", user.username)
    team = user.get_profile().team
    if team:
        invalidate_template_cache("infobar", team.name)


def invalidate_team_avatar_cache(task, user):
    """Invalidates task completed avatar list cache."""
    if task and user and user.get_profile() and user.get_profile().team:
        invalidate_template_cache("team_avatar", task.id, user.get_profile().team.id)


def invalidate_commitments_cache(user):
    """Invalidates the cache of the commitments list for the user."""
    invalidate_template_cache("commitments", user.username)
