"""Exploratory event-study for a selected, incomplete UVB-76 log archive.
No claim of causal links. Standard-library-only, reproducible.
"""
import csv, collections, datetime as dt, json, pathlib, statistics
ROOT=pathlib.Path(__file__).parent
ROWS=list(csv.DictReader((ROOT/'UVB76_full_messages_deduplicated.csv').open(encoding='utf-8-sig')))
COUNTS=collections.Counter(dt.date.fromisoformat(r['date']) for r in ROWS)
EVENTS=[('Kyiv government change','2014-02-22'),('Crimean administrative buildings seized','2014-02-27'),('Crimea referendum','2014-03-16'),('Annexation treaty signed','2014-03-18')]
WINDOWS=(7,30)

def preceding(day, window):
    return sum(COUNTS.get(day-dt.timedelta(days=i),0) for i in range(1,window+1))

def same_year_reference(day,window):
    # Uniform calendar-date reference, no access to later years.
    first=dt.date(day.year,1,1); last=dt.date(day.year,12,31)
    eligible=[first+dt.timedelta(days=i) for i in range((last-first).days+1) if first+dt.timedelta(days=i)>=first+dt.timedelta(days=window)]
    values=[preceding(x,window) for x in eligible]
    observed=preceding(day,window)
    return dict(observed=observed,baseline_mean=round(statistics.mean(values),2),baseline_median=statistics.median(values),percentile=round(100*sum(v<=observed for v in values)/len(values),1),p_upper=round(sum(v>=observed for v in values)/len(values),4),reference_dates=len(values))

output=[]
for name,s in EVENTS:
    day=dt.date.fromisoformat(s)
    for w in WINDOWS:
        output.append({'event':name,'date':s,'window_days':w,**same_year_reference(day,w)})
with (ROOT/'UVB76_event_study_2014.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=output[0].keys());writer.writeheader();writer.writerows(output)
# Word + 8-digit groups; build connected components from shared numbers
pairs=[]
for r in ROWS:
    for part in r['full_word_sequence'].split(' | '):
        bits=part.strip().split()
        if len(bits)>=3 and len(bits[-2])==4 and len(bits[-1])==4 and bits[-2].isdigit() and bits[-1].isdigit():
            pairs.append({'date':r['date'],'time':r['time_as_logged'],'word':' '.join(bits[:-2]),'digits':bits[-2]+bits[-1],'source':r['source_file'],'source_line':r['source_line']})
bydigits=collections.defaultdict(list)
for p in pairs:bydigits[p['digits']].append(p)
shared=[]
for digits,entries in bydigits.items():
    words=sorted(set(x['word'] for x in entries))
    if len(words)>1:
        shared.append({'digits':digits,'distinct_words':len(words),'occurrences':len(entries),'words':' | '.join(words),'dates':' | '.join(sorted(set(x['date'] for x in entries)))})
shared.sort(key=lambda x:(-x['distinct_words'],-x['occurrences'],x['digits']))
with (ROOT/'UVB76_crossword_number_links.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=shared[0].keys());writer.writeheader();writer.writerows(shared)
summary={'messages':len(ROWS),'parsed_blocks':len(pairs),'cross_word_number_groups':len(shared),'year_counts':dict(sorted(collections.Counter(x['date'][:4] for x in ROWS).items())),'event_study':output,'warnings':['Selected, incomplete, nonrandom archive; no inference about full station activity.','Historical events are illustrative and partly clustered, so event tests are not independent.','Same-year reference dates are a descriptive baseline, not a validated causal or predictive significance test.','Source transcription, UTC/local timestamps, and 2014 historical-event timestamps need independent verification.']}
(ROOT/'UVB76_model_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('first links',shared[:4])
