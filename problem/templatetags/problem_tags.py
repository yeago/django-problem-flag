from django import template

from django.core.urlresolvers import reverse

from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def problem_form_url(object):
	return reverse("problem_flag_form",args=[ContentType.objects.get_for_model(object.__class__).pk,object.pk])
