from os.path import basename
from django import template

register = template.Library()

@register.filter
def filename(value):
	try:
		return basename(value.url)
	except AttributeError:
		return '[No URL Value]'
