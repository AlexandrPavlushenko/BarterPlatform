from django import template

register = template.Library()


@register.simple_tag
def get_user_proposal(ad, user):
    """Возвращает предложение обмена текущего пользователя для указанного объявления.

    Args:
        ad: Модель объявления, для которого проверяются предложения
        user: Авторизованный пользователь (модель User)

    Returns:
        Модель ExchangeProposal или None: Первое найденное предложение пользователя для этого объявления,
        либо None если пользователь не авторизован или не делал предложений.
    """
    if user.is_authenticated:
        return ad.exchange_proposals.filter(ad_sender=user).first()
    return None


@register.simple_tag
def incoming_proposals_count(ad, user):
    """Возвращает количество входящих предложений обмена для объявления.

    Подсчитывает предложения от других пользователей (исключая предложения текущего пользователя).

    Args:
        ad: Модель объявления, для которого проверяются предложения
        user: Авторизованный пользователь (модель User)

    Returns:
        int: Количество входящих предложений (0 если пользователь не авторизован)
    """
    if user.is_authenticated:
        return ad.exchange_proposals.exclude(ad_sender=user).count()
    return 0
