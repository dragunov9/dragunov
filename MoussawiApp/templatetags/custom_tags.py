from django import template

register = template.Library()

@register.filter
def is_following(user_profile, other_profile):
    return other_profile in user_profile.following.all()