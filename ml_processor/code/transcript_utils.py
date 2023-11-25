def whisper_transcribe_file(model, path_to_mp3_file):
    transcription = model.transcribe(path_to_mp3_file, language="ru", verbose=False)

    return transcription

def extract_timecodes_and_context(transcript, terms):
    segments = transcript['segments']
    timecodes = dict()
    context = dict()

    for term in terms:
        timecodes[term] = [(segment["start"], segment["end"]) for segment in segments if term in segment['text'].strip().lower()]
        context[term] = [segment["text"] for segment in segments if term in segment['text'].strip().lower()]

    return timecodes, context

