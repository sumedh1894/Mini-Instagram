from django import forms

class ImageUpload(forms.Form):
    image_field = forms.FileField(
        label='Click to browse computer',
        help_text='Only jpeg, png and gif allowed: ')

    #require should be set to false to upload image without a caption
    caption = forms.CharField(max_length=100,label='Enter a Caption',required=False)