"""
ZIZIPHUS JUJUBA: Live Radio Monitoring & Signal Interceptor Module.
Manages live WebSDR/KiwiSDR streams, real-time message logging into SQLite,
and signal intelligence telemetry for UVB-76 (4625.0 kHz USB).
"""

import datetime
import sqlite3
from typing import Dict, Any, List, Optional

# Curated online SDR receivers tuned to 4625 kHz USB
SDR_RECEIVERS = [
    {
        "id": "twente_nl",
        "name": "University of Twente WebSDR (Enschede, NL)",
        "location": "Enschede, Netherlands",
        "distance": "~2,100 km from Kerro / Povarovo",
        "frequency": "4625.0 kHz",
        "modulation": "USB",
        "bandwidth": "2.4 kHz",
        "stream_url": "http://websdr.ewi.utwente.nl:8901/?tune=4625usb",
        "audio_stream": "http://websdr.ewi.utwente.nl:8901/~~stream?tune=4625usb",
        "embed_url": "http://websdr.ewi.utwente.nl:8901/?tune=4625usb",
        "status": "ONLINE",
        "type": "WebSDR"
    },
    {
        "id": "kiwi_finland",
        "name": "Northern Europe KiwiSDR (Finland)",
        "location": "Mäntsälä / Kuusamo, Finland",
        "distance": "~450 km (Excellent Ground & Skywave)",
        "frequency": "4625.0 kHz",
        "modulation": "USB",
        "bandwidth": "2.7 kHz",
        "stream_url": "http://oh3btr.dyndns.org:8073/?f=4625.00usb",
        "audio_stream": "",
        "embed_url": "http://oh3btr.dyndns.org:8073/?f=4625.00usb",
        "status": "ONLINE",
        "type": "KiwiSDR"
    },
    {
        "id": "kiwi_poland",
        "name": "Central European KiwiSDR (Poland)",
        "location": "Warsaw / Bialystok, Poland",
        "distance": "~950 km",
        "frequency": "4625.0 kHz",
        "modulation": "USB",
        "bandwidth": "2.4 kHz",
        "stream_url": "http://sp5pbe.dyndns.org:8073/?f=4625.00usb",
        "audio_stream": "",
        "embed_url": "http://sp5pbe.dyndns.org:8073/?f=4625.00usb",
        "status": "ONLINE",
        "type": "KiwiSDR"
    },
    {
        "id": "community_relay",
        "name": "24/7 Community Shortwave Relay (4625 kHz)",
        "location": "Distributed WebSDR Network",
        "distance": "Relay stream",
        "frequency": "4625.0 kHz",
        "modulation": "USB",
        "bandwidth": "3.0 kHz",
        "stream_url": "https://stream.priyom.org/live",
        "audio_stream": "https://stream.priyom.org/live.mp3",
        "embed_url": "https://priyom.org/military-stations/russia/the-buzzer",
        "status": "ACTIVE",
        "type": "Icecast Relay"
    },
    {
        "id": "synth_local",
        "name": "Authentic Hardware Synthesizer (Local Lab Audio Engine)",
        "location": "Local DSP / Web Audio API Engine",
        "distance": "0 km (Real-time synthesis)",
        "frequency": "4625.0 kHz",
        "modulation": "USB / AM BFO",
        "bandwidth": "460 Hz Tone + Static",
        "stream_url": "#synth",
        "audio_stream": "internal://webaudio_buzzer",
        "embed_url": "",
        "status": "STANDBY / OPERATIONAL",
        "type": "Local Synthesizer"
    }
]

# Station technical specifications
STATION_SPECS = {
    "callsign_history": [
        {"period": "1976 – 2010", "callsign": "УЗБ-76 (UZB-76)", "role": "Historical identifier"},
        {"period": "2010 – 2015", "callsign": "МДЖБ (MDZhB)", "role": "Main period (including 2014 crisis)"},
        {"period": "2015 – 2019", "callsign": "ЖУОЗ (ZhUOZ)", "role": "Western Military District"},
        {"period": "2019 – 2020", "callsign": "АНВФ (ANVF)", "role": "Modern rotation"},
        {"period": "2020 – present", "callsign": "НЖТИ / ВЖЦХ (NZhTI / VZhTsKh)", "role": "Current operational callsigns"}
    ],
    "transmitter": {
        "primary_frequency": "4625.0 kHz",
        "mode": "USB (Upper Sideband) with suppressed/reduced carrier and AM carrier leak",
        "power_est": "10 – 20 kW",
        "cadence": "21 to 34 bursts per minute (1.0 - 1.2 sec per burst, ~460 Hz tone)",
        "primary_site": "Naro-Fominsk / Kerro Massif (60.274°N, 30.297°E), Leningrad Oblast",
        "backup_site": "Povarovo (historical, 56.083°N, 37.100°E), Moscow Oblast"
    }
}


class LiveRadioManager:
    """Manages real-time intercept logging and SDR endpoints."""

    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn

    def get_receivers(self) -> List[Dict[str, Any]]:
        return SDR_RECEIVERS

    def get_station_specs(self) -> Dict[str, Any]:
        return STATION_SPECS

    def log_interception(
        self,
        callsign: str,
        codeword: str,
        digit_combination: str,
        header_number: Optional[str] = None,
        operator_callsign: str = "LAB_OPERATOR",
        signal_quality: str = "5/5",
        notes: str = "",
        custom_datetime: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record a live radio interception directly into the SQLite database.
        Creates records in Messages and CodeBlocks tables.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        if custom_datetime:
            try:
                dt = datetime.datetime.fromisoformat(custom_datetime)
            except Exception:
                dt = now
        else:
            dt = now

        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S")
        year = dt.year
        month = dt.month
        day = dt.day

        callsign = (callsign or "МДЖБ").strip().upper()
        codeword = (codeword or "").strip().upper()
        digits = (digit_combination or "").strip()
        header = (header_number or "").strip()

        # Build full text snippet
        full_text_parts = [callsign]
        if header:
            full_text_parts.append(header)
        if codeword:
            full_text_parts.append(codeword)
        if digits:
            full_text_parts.append(digits)
        full_text = " ".join(full_text_parts)

        # Parse digits into 4+4 groups
        clean_digits = "".join(c for c in digits if c.isdigit())
        g1 = clean_digits[:4] if len(clean_digits) >= 4 else ""
        g2 = clean_digits[4:8] if len(clean_digits) >= 8 else ""
        eight_digit = f"{g1} {g2}".strip() if g1 and g2 else clean_digits

        cur = self.conn.cursor()

        # Insert into Messages
        cur.execute("""
            INSERT INTO Messages (
                source_id, source_file, source_line,
                date, year, month, day, time_as_logged, timezone,
                callsign, header_number, full_text, full_word_sequence,
                block_count, quality_flag, is_duplicate
            ) VALUES (1, 'LIVE_MONITORING', 1, ?, ?, ?, ?, ?, 'UTC', ?, ?, ?, ?, 1, ?, 0)
        """, (
            date_str,
            year,
            month,
            day,
            time_str,
            callsign,
            header,
            full_text,
            codeword,
            f"LIVE ({signal_quality})"
        ))
        message_id = cur.lastrowid

        # Insert into CodeBlocks if codeword or digits present
        codeblock_id = None
        if codeword or eight_digit:
            cur.execute("""
                INSERT INTO CodeBlocks (
                    message_id, block_index, code_word,
                    digit_group_1, digit_group_2, digit_combination,
                    uncertainty_flag, notes
                ) VALUES (?, 1, ?, ?, ?, ?, 0, ?)
            """, (
                message_id,
                codeword,
                g1,
                g2,
                eight_digit,
                notes
            ))
            codeblock_id = cur.lastrowid

        # Insert into AuditLog
        cur.execute("""
            INSERT INTO AuditLog (
                source_file, source_line, date, time,
                audit_type, action_taken, rationale, raw_snippet
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "LIVE_MONITORING",
            1,
            date_str,
            time_str,
            "LIVE_INTERCEPTION",
            "INSERTED_PRIMARY",
            f"Logged live by {operator_callsign}. Quality: {signal_quality}. Notes: {notes}",
            full_text
        ))

        self.conn.commit()

        # Check for historical matches of this codeword or digit group
        historical_matches = []
        if eight_digit:
            m_rows = cur.execute("""
                SELECT m.date, m.time_as_logged, m.callsign, cb.code_word, cb.digit_combination
                FROM CodeBlocks cb
                JOIN Messages m ON cb.message_id = m.id
                WHERE cb.digit_combination = ? AND m.id != ?
                ORDER BY m.date DESC
            """, (eight_digit, message_id)).fetchall()
            for r in m_rows:
                historical_matches.append({
                    "type": "NUMBER_MATCH",
                    "date": r[0],
                    "time": r[1],
                    "callsign": r[2],
                    "codeword": r[3],
                    "digits": r[4]
                })

        if codeword:
            w_rows = cur.execute("""
                SELECT m.date, m.time_as_logged, m.callsign, cb.code_word, cb.digit_combination
                FROM CodeBlocks cb
                JOIN Messages m ON cb.message_id = m.id
                WHERE cb.code_word = ? AND m.id != ?
                ORDER BY m.date DESC
                LIMIT 5
            """, (codeword, message_id)).fetchall()
            for r in w_rows:
                historical_matches.append({
                    "type": "WORD_MATCH",
                    "date": r[0],
                    "time": r[1],
                    "callsign": r[2],
                    "codeword": r[3],
                    "digits": r[4]
                })

        return {
            "status": "SUCCESS",
            "message_id": message_id,
            "codeblock_id": codeblock_id,
            "logged_at": f"{date_str} {time_str} UTC",
            "full_text": full_text,
            "historical_matches_found": len(historical_matches),
            "historical_matches": historical_matches
        }

    def get_recent_interceptions(self, limit: int = 25) -> List[Dict[str, Any]]:
        """Retrieve all operator live interceptions."""
        cur = self.conn.cursor()
        rows = cur.execute("""
            SELECT m.id, m.date, m.time_as_logged, m.callsign, m.header_number,
                   m.full_word_sequence, m.quality_flag, m.full_text,
                   cb.digit_combination
            FROM Messages m
            LEFT JOIN CodeBlocks cb ON cb.message_id = m.id
            WHERE m.source_file = 'LIVE_MONITORING'
            ORDER BY m.id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        results = []
        for r in rows:
            results.append({
                "id": r[0],
                "date": r[1],
                "time": r[2],
                "callsign": r[3],
                "header_number": r[4],
                "codeword": r[5],
                "quality_flag": r[6],
                "full_text": r[7],
                "digit_combination": r[8]
            })
        return results
