from django.conf import settings

def projectMedia(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'PROJECT_NAME': settings.PROJECT_NAME, 'PROJECT_NAME_SHORT': settings.PROJECT_NAME_SHORT}