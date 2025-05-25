from django import template

register = template.Library()

@register.simple_tag
def get_user_proposal(ad, user):
    if user.is_authenticated:
        return ad.exchange_proposals.filter(ad_sender=user).first()
    return None

@register.simple_tag
def incoming_proposals_count(ad, user):
    if user.is_authenticated:
        return ad.exchange_proposals.exclude(ad_sender=user).count()
    return 0