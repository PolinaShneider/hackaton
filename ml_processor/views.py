# ml_processor/views.py
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class MLProcessorView(View):
    def post(self, request, *args, **kwargs):
        # Your logic for handling the post request
        # Perhaps you're calling a Python script here
        return JsonResponse({'result': 'Processing successful'})
