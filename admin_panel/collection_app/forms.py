from django.forms import ModelForm, DateInput
from apis.nft_management.models import Collection, Category


class CollectionForm(ModelForm):
    """
    CollectionForm class

    This From used to make form of Collection

    Parameters
    ----------
    ModelForm : django.forms

    """
    class Meta:
        model = Collection
        fields = '__all__'


class CategoryForm(ModelForm):
    """
    CategoryForm class

    This From used to make form of Category

    Parameters
    ----------
    ModelForm : django.forms

    """
    class Meta:
        model = Category
        fields = '__all__'