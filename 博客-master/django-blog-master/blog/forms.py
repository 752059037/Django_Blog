# 创建人;WanChun Ye
# 创建时间 : 19.2.21  19:24

from django import forms
from blog import models


class Boootstrip(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields.values():
            i.widget.attrs.update({'class': 'form-control'})

class ArticleForm(Boootstrip):
    class Meta:
        model = models.Article
        fields = "__all__"

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     for i in self.fields.values():
        #         i.widget.attrs.update({'class': 'form-control'})
