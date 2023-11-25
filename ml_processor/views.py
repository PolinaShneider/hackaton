# file: views.py

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from code.main import initialize_models, process_audio, generate_document

whisper_model, llm_model, tokenizer = initialize_models()

@method_decorator(csrf_exempt, name='dispatch')
class MLProcessorView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        path_to_mp3_file = data.get('path_to_mp3_file')

        if not path_to_mp3_file:
            return JsonResponse({'error': 'No file path provided'}, status=400)

        summary_list, timecodes, definitions = process_audio(whisper_model, llm_model, tokenizer, path_to_mp3_file)
        lecture_save_path = "MODULES_RUN_LECTURE.docx"
        generate_document(summary_list, timecodes, definitions, lecture_save_path)

        return JsonResponse({'result': 'Processing successful', 'doc_path': lecture_save_path})
