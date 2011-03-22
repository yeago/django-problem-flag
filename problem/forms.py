from django import forms

from django.contrib.contenttypes.models import ContentType

from misc.problem.models import ProblemFlag

class ProblemFlagNotesForm(forms.ModelForm):
	def __init__(self,content_object,*args,**kwargs):
		self._content_object = content_object
		super(ProblemFlagNotesForm,self).__init__(*args,**kwargs)

	def save(self):
		record = super(ProblemFlagNotesForm,self).save(commit=False)
		record.content_type = ContentType.objects.get_for_model(self._content_object.__class__)
		record.object_id = self._content_object.pk
		record.save()
		return record

	class Meta:
		fields = ('notes',)
		model = ProblemFlag

