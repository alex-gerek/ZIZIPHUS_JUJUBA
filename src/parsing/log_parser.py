"""
Log Parser for UVB-76 Raw Logs.
Extracts timestamps, callsigns, 5-digit headers, codewords, and digit groups.
Handles tab-separated single-line entries, multi-line blocks, phonetic transliteration,
multiple code blocks per radiogram, and listener annotations.
"""

import re
import pathlib
from typing import List, Dict, Any, Tuple, Optional

MONTH_MAP = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

DATE_LINE_REGEX = re.compile(
    r'^\.?\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})(?:\s+([\d:, \t]+))?(.*)$'
)

KNOWN_CALLSIGNS = [
    'MDZhB', 'МДЖБ', 'ZhUOZ', 'ЖУОЗ', 'ANVF', 'АНВФ',
    'UZB-76', 'УЗБ-76', 'ВЛХН', 'VLHN', 'ЦХЖБ', 'CXZhB',
    '701st', '701-й', 'LNR4', 'ЛНР4', 'K5TZh', 'К5ТЖ',
    '?????', '---'
]

def clean_word(token: str) -> str:
    """Normalize code word token."""
    cleaned = re.sub(r'[^А-Яа-яA-Za-z0-9\?\-]', '', token).strip().upper()
    return cleaned

def extract_code_blocks(text: str) -> List[Dict[str, Any]]:
    """
    Parse codewords and associated 4+4 digit groups from text.
    Handles:
    - Standard 8-digit blocks (e.g. 'ЗИЗИФУС 77248209' or 'ЗИЗИФУС 7724 8209')
    - Multi-block radiograms (e.g. 'ГАШЕНИЕ 4895 4813 ЗИЗИФУС 9836 1935')
    - Uncertainties (e.g. 'VERTOLIST(?) 2103 2643')
    """
    # Replace tabs, commas, semicolons
    normalized = text.replace('\t', ' ').replace(',', ' ').replace(';', ' ')
    tokens = normalized.split()
    
    # Expand 8-digit tokens to two 4-digit tokens
    expanded = []
    for tok in tokens:
        if re.fullmatch(r'\d{8}', tok):
            expanded.extend([tok[:4], tok[4:]])
        else:
            expanded.append(tok)
            
    blocks = []
    current_words = []
    i = 0
    while i < len(expanded):
        tok = expanded[i]
        
        # Check for pair of 4-digit numbers: tok and expanded[i+1]
        if i + 1 < len(expanded) and re.fullmatch(r'\d{4}', tok) and re.fullmatch(r'\d{4}', expanded[i+1]):
            w = ' '.join(current_words)
            uncertain = 1 if '?' in w or '?' in tok or '?' in expanded[i+1] else 0
            if w:
                blocks.append({
                    'code_word': w,
                    'digit_group_1': tok,
                    'digit_group_2': expanded[i+1],
                    'digit_combination': tok + expanded[i+1],
                    'uncertainty_flag': uncertain
                })
            current_words = []
            i += 2
        elif re.fullmatch(r'\d{4}', tok):
            # Stray 4-digit number
            current_words.append(tok)
            i += 1
        elif re.fullmatch(r'\d{5}', tok):
            # 5-digit header token, skip if encountered here
            i += 1
        else:
            cleaned = clean_word(tok)
            if cleaned and cleaned not in ['MHZ', 'KHZ', 'J3E', 'USB', 'LOGGED', 'BY', 'RECORDED', 'TRANSCRIPTED']:
                current_words.append(cleaned)
            i += 1
            
    return blocks

class UVBLogParser:
    def __init__(self):
        pass

    def parse_file(self, filepath: pathlib.Path) -> List[Dict[str, Any]]:
        """Parses a raw log file into a list of message candidates."""
        content = filepath.read_text(encoding='utf-8', errors='replace')
        lines = content.splitlines()
        
        raw_entries = []
        cur = None
        
        for idx, line in enumerate(lines, 1):
            s = line.strip()
            # Check if line matches a date header
            m = DATE_LINE_REGEX.match(s)
            if m and ('MHz' not in s and 'kHz' not in s):
                if cur:
                    raw_entries.append(cur)
                mon_str, day_str, yr_str, time_str, extra = m.groups()
                month = MONTH_MAP.get(mon_str, 1)
                day = int(day_str)
                year = int(yr_str)
                date_iso = f"{year:04d}-{month:02d}-{day:02d}"
                cur = {
                    'source_file': filepath.name,
                    'source_line': idx,
                    'date': date_iso,
                    'year': year,
                    'month': month,
                    'day': day,
                    'time_as_logged': (time_str or '').strip(),
                    'extra_header_text': (extra or '').strip(),
                    'raw_lines': [line]
                }
            elif cur:
                cur['raw_lines'].append(line)
                
        if cur:
            raw_entries.append(cur)
            
        parsed_records = []
        for entry in raw_entries:
            record = self._process_entry(entry)
            parsed_records.append(record)
            
        return parsed_records

    def _process_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Processes raw lines of an entry to extract metadata and code blocks."""
        raw_lines = entry['raw_lines']
        full_text = '\n'.join(raw_lines)
        
        callsign = ''
        header_number = ''
        cyrillic_lines = []
        latin_lines = []
        logger_notes = []
        
        # Check extra_header_text for callsign/header
        extra = entry.get('extra_header_text', '')
        if extra:
            for cs in KNOWN_CALLSIGNS:
                if cs.lower() in extra.lower():
                    callsign = extra
                    break
            m_hdr = re.search(r'\b\d{5}\b', extra)
            if m_hdr:
                header_number = m_hdr.group(0)
                
        for line in raw_lines[1:]:
            s = line.strip()
            if not s:
                continue
            
            # Check for logger annotations
            if any(k in s.lower() for k in ['logged by', 'recorded by', 'transcripted by', 'transcript by', 'transcription:']):
                logger_notes.append(s)
                continue
                
            # Skip technical transmission metadata
            if any(k in s for k in ['MHz', 'kHz', 'J3E (USB)', 'J3E']):
                continue
                
            # Check callsign
            is_callsign_line = any(cs.lower() in s.lower() for cs in KNOWN_CALLSIGNS)
            if is_callsign_line and not callsign:
                callsign = s
                # Header number might be on the callsign line
                m_hdr = re.search(r'\b\d{5}\b', s)
                if m_hdr:
                    header_number = m_hdr.group(0)
                continue
                
            # Check standalone 5-digit header
            if re.fullmatch(r'\d{5}', s) and not header_number:
                header_number = s
                continue
                
            # Check cyrillic vs latin content
            if re.search(r'[А-Яа-я]', s):
                cyrillic_lines.append(s)
            elif re.search(r'[A-Za-z]{3,}', s):
                latin_lines.append(s)
            elif re.search(r'\d{4}', s):
                # Number-only line (part of block)
                if cyrillic_lines:
                    cyrillic_lines.append(s)
                elif latin_lines:
                    latin_lines.append(s)
                    
        # Extract blocks: Cyrillic preferred, fallback to Latin
        blocks = []
        if cyrillic_lines:
            blocks = extract_code_blocks(' '.join(cyrillic_lines))
        if not blocks and latin_lines:
            blocks = extract_code_blocks(' '.join(latin_lines))
            
        # Also check if line 1 or any tabbed line contained both latin and cyrillic blocks
        if not blocks:
            blocks = extract_code_blocks(full_text)
            
        full_word_sequence = ' | '.join(
            f"{b['code_word']} {b['digit_group_1']} {b['digit_group_2']}"
            for b in blocks
        )
        
        # Assess quality flag
        quality = 'NORMAL'
        if not blocks:
            if any(k in full_text.lower() for k in ['breakdown', 'diesel', 'moans', 'problems with marker', 'marker off', 'carrier']):
                quality = 'NON_VOICE_ANOMALY'
            else:
                quality = 'INCOMPLETE_OR_UNPARSED'
        elif any(b['uncertainty_flag'] for b in blocks):
            quality = 'UNCERTAIN_TRANSCRIPTION'
        elif ',' in entry['time_as_logged']:
            quality = 'RETRANSMISSION_MULTI_TIME'
            
        return {
            'source_file': entry['source_file'],
            'source_line': entry['source_line'],
            'date': entry['date'],
            'year': entry['year'],
            'month': entry['month'],
            'day': entry['day'],
            'time_as_logged': entry['time_as_logged'],
            'timezone': 'unknown',
            'callsign': callsign,
            'header_number': header_number,
            'full_text': full_text,
            'full_word_sequence': full_word_sequence,
            'block_count': len(blocks),
            'blocks': blocks,
            'quality_flag': quality,
            'logger_notes': ' | '.join(logger_notes)
        }
