from defining_utils import get_answer

summary_prompt = ''' 
    <s>system 
    Ты — русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им извлекать нужную информацию из текста.</s> 
    <s>user 
    Текст: {} 
    Вопрос: о чем рассказывается в данной части лекции? Какие темы рассмотрены? Ответь одним предложением.</s> 
    <s>bot 
    Вот ответ на ваш вопрос:'''

def create_5mins_batches(segments, batch_time_s=300):
    batch_and_start = []
    
    cur_time = 0 
    cur_start = 0
    cur_batch = ""
    
    for segment in segments:
        seg_text = segment['text']
        seg_start = segment['start']
        seg_fin = segment['end']
        
        seg_time = seg_fin - seg_start
        if cur_time + seg_time <= batch_time_s:
            cur_batch += seg_text
            cur_time += seg_time
        
        else:
            batch_and_start.append(tuple([cur_batch.strip(), cur_start, cur_start + cur_time]))
            cur_start += cur_time 
            cur_time = 0
            cur_batch = ""
            
    if cur_batch != "":
        batch_and_start.append(tuple([cur_batch.strip(), cur_start, cur_start + cur_time]))
            
    return batch_and_start
            
    
def make_summary(model, tokenizer, transcript_segments, DEVICE):
    summary_list = []
    
    batches = create_5mins_batches(transcript_segments)

    for batch in batches:
        batch_text, batch_start, batch_end = batch[0], batch[1], batch[2]
        batch_prompt = summary_prompt.format(batch_text)
        batch_summary = get_answer(model, tokenizer, batch_prompt, DEVICE)

        # пост-обработка
        batch_summary = batch_summary.split('\n')[0].capitalize()

        summary_list.append([batch_summary, batch_start, batch_end])
        
    return summary_list