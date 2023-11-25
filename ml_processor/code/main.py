# # file: ml_processing.py
# import whisper
# from peft import AutoPeftModelForCausalLM
# from transformers import AutoTokenizer
# import torch
#
# from transcript_utils import whisper_transcribe_file, extract_timecodes_and_context
# from prepare_for_docx import make_data_to_write_docx, make_list_of_tuples_unique, prepare_list_of_tuples_to_docx, create_list_of_tuples
# from defining_utils import generate_all_definitions
# from ner_utils import get_terms_candidates, filter_terms_by_frequency
# from summarization_utils import make_summary
# from write_docx import create_docx_from_list
#
# def initialize_models():
#     # Initialize Whisper
#     whisper_model = whisper.load_model("small")
#     whisper_model.to('cuda' if torch.cuda.is_available() else 'cpu')
#
#     # Initialize LLM
#     base_model_name = "Open-Orca/Mistral-7B-OpenOrca"
#     tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True, use_fast=False)
#     tokenizer.pad_token = tokenizer.eos_token
#
#     adapt_model_name = "IlyaGusev/saiga_mistral_7b_lora"
#     llm_model = AutoPeftModelForCausalLM.from_pretrained(
#         adapt_model_name,
#         device_map={"": 'cuda' if torch.cuda.is_available() else 'cpu'},
#         torch_dtype=torch.bfloat16)
#
#     return whisper_model, llm_model, tokenizer
#
# def process_audio(whisper_model, llm_model, tokenizer, path_to_mp3_file):
#     transcript = whisper_transcribe_file(whisper_model, path_to_mp3_file)
#     lecture_text = transcript['text']
#
#     terms = get_terms_candidates(lecture_text, strong=True)
#     cleared_terms = filter_terms_by_frequency(terms)
#     final_terms_unique = cleared_terms.keys()
#
#     timecodes, context = extract_timecodes_and_context(transcript, final_terms_unique)
#     definitions = generate_all_definitions(llm_model, tokenizer, context, 'cuda' if torch.cuda.is_available() else 'cpu')
#     summary_list = make_summary(llm_model, tokenizer, transcript['segments'], 'cuda' if torch.cuda.is_available() else 'cpu')
#
#     return summary_list, timecodes, definitions
#
# def generate_document(summary_list, timecodes, definitions, lecture_save_path):
#     data_for_docx = prepare_data_for_docx(summary_list, timecodes, definitions)
#     doc = create_docx_from_list(data_for_docx)
#     doc.save(lecture_save_path)
#
#
# def prepare_data_for_docx(transcript, summary_list, timecodes, definitions):
#     term_definition_timecodestart_timecodeend = create_list_of_tuples(timecodes, definitions)
#     list_of_tuples_unique = make_list_of_tuples_unique(term_definition_timecodestart_timecodeend)
#     overall_list_of_tuples = prepare_list_of_tuples_to_docx(summary_list, list_of_tuples_unique)
#     data_for_docx = make_data_to_write_docx(overall_list_of_tuples)
#     return data_for_docx
#
# def generate_document(doc_data, lecture_save_path):
#     doc = create_docx_from_list(doc_data)
#     doc.save(lecture_save_path)

import whisper
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer, AutoModel
import torch

from transcript_utils import whisper_transcribe_file, extract_timecodes_and_context
from defining_utils import generate_all_definitions
from ner_utils import get_terms_candidates, filter_terms_by_frequency, finalize_terms
from prepare_for_docx import create_list_of_tuples, make_list_of_tuples_unique, prepare_list_of_tuples_to_docx, make_data_to_write_docx
from summarization_utils import make_summary
from write_docx import create_docx_from_list

if __name__ == "__main__":
    # init whisper
    model_size = "small"

    # define device
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    # load model
    whisper_model = whisper.load_model(model_size)
    whisper_model.to(DEVICE)
    print("WHISPER IS INITIALIZED")

    # llama model names
    adapt_model_name = "IlyaGusev/saiga_mistral_7b_lora"
    base_model_name = "Open-Orca/Mistral-7B-OpenOrca"

    # llm tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_name,
        trust_remote_code=True,
        use_fast=False)

    # adjustments
    tokenizer.pad_token = tokenizer.eos_token
    device_map = {"": DEVICE}

    # llm model
    model = AutoPeftModelForCausalLM.from_pretrained(
        adapt_model_name,
        device_map=device_map,
        torch_dtype=torch.bfloat16)

    print("SAIGA IS INITIALIZED")

    ## PATH TO FILE
    path_to_mp3_file = "audio4.mp3"

    ## GET TRANSCRIPT AND TEXT
    transcript = whisper_transcribe_file(whisper_model, path_to_mp3_file)
    lecture_text = transcript['text']

    print("TRANSCRIPT IS DONE")

    ## NER (ADD!!!)
    terms = get_terms_candidates(lecture_text, strong=True)
    cleared_terms = filter_terms_by_frequency(terms)
    final_terms_unique = cleared_terms.keys()

    print("TERMS ARE DONE")

    ## GET TIMECODES AND CONTEXTS OF TERMS (DICTS)
    timecodes, context = extract_timecodes_and_context(transcript, final_terms_unique)

    ## GENERATE DEFINITIONS BY CONTEXT
    definitions = generate_all_definitions(model, tokenizer, context, DEVICE)
    print("DEFS:", definitions)

    ## GENERATE SUMMARIES
    summary_list = make_summary(model, tokenizer, transcript['segments'], DEVICE)
    print("SUMMARY:", summary_list)

    ## prepare for .docx (Sonya's strange code)
    term_definition_timecodestart_timecodeend = create_list_of_tuples(timecodes, definitions)
    list_of_tuples_unique = make_list_of_tuples_unique(term_definition_timecodestart_timecodeend)
    overall_list_of_tuples = prepare_list_of_tuples_to_docx(summary_list, list_of_tuples_unique)
    data_for_docx = make_data_to_write_docx(overall_list_of_tuples)

    print("DATA FOR DOCX IS DONE", summary_list)

    ## docx object
    doc = create_docx_from_list(data_for_docx)

    ## SAVE IT AS YOU WISH
    lecture_save_path = "MODULES_RUN_LECTURE.docx"
    doc.save(lecture_save_path)
    print("DOSX IS SAVED. SUCCESS!!")
