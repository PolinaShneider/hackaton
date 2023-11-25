import pandas as pd

def create_list_of_tuples(timecodes, definitions):
    """ generates [(term, definition, timecode_start, timecode_end), ...] """
    term_definition_timecodestart_timecodeend = []

    for i, para in enumerate(timecodes.items()):
        term, term_timecodes = para
        definition = definitions[i]
        for term_timecode in term_timecodes:
            term_definition_timecodestart_timecodeend.append(
                (term, definition, term_timecode[0], term_timecode[1]))

    return term_definition_timecodestart_timecodeend


def make_list_of_tuples_unique(term_definition_timecodestart_timecodeend):
    overall_df = pd.DataFrame(term_definition_timecodestart_timecodeend,
                              columns=['Term', 'Definition', 'Time_start', 'Time_end'])
    overall_df = overall_df.drop_duplicates(subset=['Term'])
    
    return list(overall_df.to_records(index=False))


def prepare_list_of_tuples_to_docx(summary_list, list_of_tuples_unique):
    overall_list_of_tuples = [(None, summary[0], summary[1], summary[2]) for summary in summary_list] + \
                             list_of_tuples_unique
    overall_list_of_tuples = sorted(overall_list_of_tuples, key=lambda tup: float(tup[2]))
    
    return overall_list_of_tuples


def make_data_to_write_docx(overall_list_of_tuples):
    list_items_for_docx = []

    for item in overall_list_of_tuples:
        if not item[0]:
            # почему-то без норм предобработки
            summary = item[1].split('\n')[0].capitalize()
            start_summary = item[2]
            end_summary = item[3]
            
            summary_tuple = tuple([summary, start_summary, end_summary])
            
            list_items_for_docx.append(summary_tuple)
        else:
            list_items_for_docx.append(item)
            
    return list_items_for_docx

