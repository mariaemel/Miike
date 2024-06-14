from django import template

# from miike.main.models import Like

register = template.Library()

@register.simple_tag(takes_context=True)
def is_liked(context, post_id):
    request = context['request']
    try:
        likes = Like.objects.get(post_id=post_id, liked_by=request.user.id).like
    except Exception as e:
        likes = False
    return likes

@register.simple_tag()
def count_likes(post_id):
    return Like.objects.filter(post_id=post_id, like=True).count()

@register.simple_tag(takes_context=True)
def  likes_id(context, post_id):
    request = context['request']
    return Like.objects.get(post_id=post_id, liked_by=request.user.id).id