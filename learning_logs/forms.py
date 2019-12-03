from django import forms

from learning_logs.models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        label = { 'text': '' }