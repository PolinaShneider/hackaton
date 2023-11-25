rag_prompt = '''<s>system
Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им.</s>
<s>user
Текст: {}
Вопрос: что такое {}?</s>
<s>bot
Вот ответ на ваш вопрос:'''


def get_answer(model, tokenizer, prompt, DEVICE):
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    outputs = model.generate(input_ids=inputs["input_ids"].to(DEVICE),
                            top_p=0.5,
                            temperature=0.3,
                            attention_mask=inputs["attention_mask"],
                            max_new_tokens=128,
                            pad_token_id=tokenizer.eos_token_id,
                            do_sample=True)

    output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    parsed_answer = output.split("Вот ответ на ваш вопрос:")[1].strip()

    if "bot:" in parsed_answer:
        parsed_answer = parsed_answer.split("bot:")[0].strip()


    if not parsed_answer.endswith('.'):
        parsed_answer_sentences = parsed_answer.split('.')
        parsed_answer = '.'.join(parsed_answer_sentences[:-1]) + '.'


    parsed_answer = parsed_answer.replace('</s>', '')
    parsed_answer = parsed_answer.replace('bot', '')

    return parsed_answer


def get_rag_context(term_fragments, CONTEXT_WORDS_THRESH=50):
    context = ""

    for fragment in term_fragments:
        if len(context.split(' ')) + len(fragment.split(' ')) < CONTEXT_WORDS_THRESH:
            context += fragment

    context = context.strip()

    return context


def get_rag_prompts(terms_and_context_dict):
    rag_prompts = []

    for term_to_define, term_fragments in terms_and_context_dict.items():
        term_context = get_rag_context(term_fragments)
        prompt = rag_prompt.format(term_context, term_to_define)

        rag_prompts.append(prompt)

    return rag_prompts

def generate_all_definitions(model, tokenizer, context, DEVICE):
    definitions = []

    prompts_list = get_rag_prompts(context)
    
    for prompt in prompts_list:
        definitions.append(get_answer(model, tokenizer, prompt, DEVICE))
        
    return definitions
