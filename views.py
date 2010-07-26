from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.http import Http404
from django.template import RequestContext
from django.conf import settings

from django.views.generic.list_detail import object_list
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail

from misc.problem import forms as pforms
from misc.problem import models as pmodels

def list(request,include_resolved=False,content_type=None,object_pk=None,perm_required='problem',login_required=True):
	if (login_required and not request.user.is_authenticated()) or \
		(perm_required and not request.user.has_perm(perm_required)):
		raise Http404

	queryset = pmodels.ProblemFlag.objects.all()
	if not include_resolved:
		queryset = queryset.exclude(resolved=True)

	if content_type:
		queryset = queryset.filter(content_type=content_type)
	
	if object_pk:
		queryset = queryset.filter(object_pk=object_pk)

	return object_list(request,queryset=queryset)

def flag(request,content_type,object_pk,login_required=True):
	if login_required and not request.user.is_authenticated():
		raise Http404

	model_class = get_object_or_404(ContentType,pk=content_type)
	content_object = get_object_or_404(model_class,pk=object_pk)
	problem, created = pmodels.ProblemFlag.objects.get_or_create(content_type=content_type,object_pk=object_pk)
	if created and request.user.is_authenticated():
		problem.user = user
		problem.save()

	request.user.message_set.create(message="Problem flag added")

	recipients = getattr(settings,'PROBLEM_MANAGERS',None) or settings.MANAGERS
	recipients = [i[1] for i in recipients]

	send_mail("%s flagged with problem by %s" % (content_object,request.user),\
			"%s" % (content_object.get_absolute_url()),settings.DEFAULT_FROM_EMAIL,recipients)
	
	return redirect(request.GET.get('return_url',content_object.get_absolute_url()))

def delete(request,content_type,object_pk,perm_required='delete_problem',login_required=True):
	if (login_required and not request.user.is_authenticated()) or (perm_required and not \
			request.user.has_perm(perm_required)):
		raise Http404

	model_class = get_object_or_404(ContentType,pk=content_type)
	content_object = get_object_or_404(model_class,pk=object_pk)

	problem = get_object_or_404(pmodels.ProblemFlag,content_type=content_type,object_pk=object_pk)
	problem.delete()
	request.user.message_set.create(message="Problem flag deleted")
	return redirect(request.GET.get('return_url',content_object.get_absolute_url()))

def subscribe(request,content_type,object_pk):
	if not request.user.is_authenticated():
		raise Http404
	# no perm, login always required
	model_class = get_object_or_404(ContentType,pk=content_type)
	content_object = get_object_or_404(model_class,pk=object_pk)
	problem = get_object_or_404(pmodels.ProblemFlag,content_type=content_type,object_pk=object_pk)
	request.user.message_set.create(message="Subscription added")
	pmodels.ProblemSubscription.objects.get_or_create(user=request.user,problem=problem)
	return redirect(request.GET.get('return_url',content_object.get_absolute_url()))


def resolve(request,content_type,object_pk,perm_required='change_problem',login_required=True):
	if (login_required and not request.user.is_authenticated()) or \
			(perm_required and not request.user.has_perm(perm_required)):
		raise Http404

	model_class = get_object_or_404(ContentType,pk=content_type)
	content_object = get_object_or_404(model_class,pk=object_pk)
	problem = get_object_or_404(pmodels.ProblemFlag,content_type=content_type,object_pk=object_pk)
	problem.resolved = True
	problem.save()
	request.user.message_set.create(message="Problem resolved")
	return redirect(request.GET.get('return_url',content_object.get_absolute_url()))

def form(request,content_type,object_pk,form_class=pforms.ProblemFlagNotesForm,login_required=True):
	if login_required and not request.user.is_authenticated():
		raise Http404

	content_type = get_object_or_404(ContentType,pk=content_type)
	content_object = get_object_or_404(content_type.model_class(),pk=object_pk)
	form = form_class(content_object)
	if request.POST:
		form = form_class(content_object,request.POST)
		if form.is_valid():
			flag = form.save()
			request.user.message_set.create(message="Problem flag added")

			recipients = getattr(settings,'PROBLEM_MANAGERS',None) or settings.MANAGERS
			recipients = [i[1] for i in recipients]
			
			send_mail("%s flagged with problem by %s" % (content_object,request.user),\
					"Item url  -- http://tappedout.net%s\r\n\r\nNotes -- %s"\
					% (content_object.get_absolute_url(),flag.notes),settings.DEFAULT_FROM_EMAIL,recipients)
			
			return redirect(content_object.get_absolute_url())

	return render_to_response('problem/form.html', {'form': form, 'object': content_object }, context_instance=RequestContext(request))
