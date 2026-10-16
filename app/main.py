"""
ZIZIPHUS JUJUBA: Signal Intelligence & Pattern Analysis Lab.
FastAPI Application Backend.
Serves interactive analytical endpoints, network graph data, statistical models,
audit logs, and historical event studies.
"""

import pathlib
import json
import sqlite3
from typing import Optional, List
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from src.database.db_manager import DatabaseManager
from src.analysis.frequency_analysis import FrequencyAnalyzer
from src.analysis.repetition_analysis import RepetitionAnalyzer
from src.analysis.time_series import TimeSeriesAnalyzer
from src.models.clustering_modes import OperationalModesClustering
from src.models.graph_intelligence import GraphIntelligenceEngine
from src.models.event_study import HistoricalEventStudy
from src.models.hypothesis_tests import HypothesisTestingEngine
from src.analysis.traffic_behavior import TrafficBehaviorEngine
from src.analysis.structural_analysis import StructuralDynamicsEngine
from src.analysis.anomaly_detector import AnomalyDetector
from src.models.network_evolution import NetworkEvolutionEngine
from src.models.event_study_advanced import AdvancedEventStudyEngine
from src.analysis.findings_registry import FindingsRegistryEngine

import sys

def get_base_dir() -> pathlib.Path:
    if getattr(sys, 'frozen', False):
        exe_dir = pathlib.Path(sys.executable).parent.resolve()
        if (exe_dir / "data/database/ziziphus_jujuba.db").exists():
            return exe_dir
        if (exe_dir / "_internal/data/database/ziziphus_jujuba.db").exists():
            return exe_dir / "_internal"
        if hasattr(sys, '_MEIPASS'):
            meipass = pathlib.Path(sys._MEIPASS).resolve()
            if (meipass / "data/database/ziziphus_jujuba.db").exists():
                return meipass
        return exe_dir
    return pathlib.Path(__file__).resolve().parent.parent

BASE_DIR = get_base_dir()
DB_PATH = BASE_DIR / "data/database/ziziphus_jujuba.db"
EXPORTS_DIR = BASE_DIR / "exports"

app = FastAPI(
    title="ZIZIPHUS JUJUBA: Signal Intelligence Lab",
    description="Operational pattern analysis of UVB-76 archives",
    version="2.0.0"
)

# Static and templates
static_dir = BASE_DIR / "app/static"
templates_dir = BASE_DIR / "app/templates"
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

def get_db():
    mgr = DatabaseManager(DB_PATH)
    return mgr.get_connection()

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    """Main lab interface."""
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/api/overview")
async def get_overview():
    """Summary metrics of the laboratory."""
    with get_db() as conn:
        total_msgs = conn.execute("SELECT COUNT(*) FROM Messages WHERE is_duplicate = 0").fetchone()[0]
        total_raw = conn.execute("SELECT COUNT(*) FROM Messages").fetchone()[0]
        total_blocks = conn.execute("SELECT COUNT(*) FROM CodeBlocks cb JOIN Messages m ON cb.message_id = m.id WHERE m.is_duplicate = 0").fetchone()[0]
        unique_words = conn.execute("SELECT COUNT(DISTINCT code_word) FROM CodeBlocks cb JOIN Messages m ON cb.message_id = m.id WHERE m.is_duplicate = 0").fetchone()[0]
        unique_numbers = conn.execute("SELECT COUNT(DISTINCT digit_combination) FROM CodeBlocks cb JOIN Messages m ON cb.message_id = m.id WHERE m.is_duplicate = 0").fetchone()[0]
        audit_entries = conn.execute("SELECT COUNT(*) FROM AuditLog").fetchone()[0]
        events_count = conn.execute("SELECT COUNT(*) FROM HistoricalEvents").fetchone()[0]
        
        years_data = conn.execute("""
            SELECT year, COUNT(*) as cnt
            FROM Messages
            WHERE is_duplicate = 0
            GROUP BY year
            ORDER BY year ASC
        """).fetchall()
        
    return {
        'status': 'OPERATIONAL',
        'station': 'UVB-76 (The Buzzer / 4625 kHz)',
        'metrics': {
            'primary_messages': total_msgs,
            'total_raw_archive_entries': total_raw,
            'flagged_duplicates': total_raw - total_msgs,
            'parsed_code_blocks': total_blocks,
            'unique_codewords': unique_words,
            'unique_8digit_combinations': unique_numbers,
            'audit_log_items': audit_entries,
            'historical_events_registered': events_count
        },
        'years_distribution': {r['year']: r['cnt'] for r in years_data}
    }

@app.get("/api/targets/ziziphus_cluster")
async def get_target_cluster():
    """Detailed primary data for ZIZIPHUS, PASKOIT, GASHENIE, NIZKIJ."""
    with get_db() as conn:
        analyzer = RepetitionAnalyzer(conn)
        data = analyzer.inspect_specific_targets()
    return data

@app.get("/api/graph/subgraph")
async def get_graph_subgraph(
    targets: Optional[str] = Query("ЗИЗИФУС,ПАСКОИТ,ГАШЕНИЕ,НИЗКИЙ"),
    depth: int = Query(1, ge=1, le=2)
):
    """Network subgraph around target words."""
    words = [w.strip() for w in targets.split(',') if w.strip()]
    with get_db() as conn:
        engine = GraphIntelligenceEngine(conn)
        subgraph = engine.get_target_subgraph(target_words=words, depth=depth)
    return subgraph

@app.get("/api/graph/metrics")
async def get_graph_metrics():
    """Centrality, connected components and topology metrics."""
    with get_db() as conn:
        engine = GraphIntelligenceEngine(conn)
        metrics = engine.get_network_metrics()
    return metrics

@app.get("/api/graph/search")
async def search_graph(q: str = Query(..., min_length=2)):
    """Search for any codeword or number group in network."""
    with get_db() as conn:
        engine = GraphIntelligenceEngine(conn)
        res = engine.search_node(q)
    return res

@app.get("/api/frequency/words")
async def get_word_freq(top_n: int = Query(50, ge=5, le=200)):
    with get_db() as conn:
        fa = FrequencyAnalyzer(conn)
        return fa.get_word_frequencies(top_n=top_n)

@app.get("/api/frequency/digits")
async def get_digit_freq(top_n: int = Query(50, ge=5, le=200)):
    with get_db() as conn:
        fa = FrequencyAnalyzer(conn)
        return fa.get_digit_frequencies(top_n=top_n)

@app.get("/api/frequency/callsigns")
async def get_callsigns():
    with get_db() as conn:
        fa = FrequencyAnalyzer(conn)
        return fa.get_callsign_frequencies()

@app.get("/api/repetition/repeated_numbers")
async def get_repeated_numbers(min_occ: int = Query(2, ge=2)):
    with get_db() as conn:
        ra = RepetitionAnalyzer(conn)
        return ra.get_repeated_numbers(min_occurrences=min_occ)

@app.get("/api/temporal/monthly_matrix")
async def get_monthly_matrix():
    with get_db() as conn:
        ts = TimeSeriesAnalyzer(conn)
        return ts.get_normalized_monthly_matrix()

@app.get("/api/temporal/diurnal")
async def get_diurnal():
    with get_db() as conn:
        ts = TimeSeriesAnalyzer(conn)
        return ts.get_diurnal_distribution()

@app.get("/api/temporal/coverage")
async def get_coverage():
    with get_db() as conn:
        ts = TimeSeriesAnalyzer(conn)
        return ts.get_archive_coverage_audit()

@app.get("/api/clustering/modes")
async def get_clustering(k: int = Query(3, ge=2, le=5)):
    with get_db() as conn:
        cl = OperationalModesClustering(conn)
        return cl.fit_clustering(n_clusters=k)

@app.get("/api/events/study")
async def get_event_study():
    """Historical timeline event study."""
    with get_db() as conn:
        es = HistoricalEventStudy(conn)
        return es.evaluate_all_historical_events()

@app.get("/api/events/custom")
async def evaluate_custom_event(
    date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    name: str = Query("Пользовательское событие")
):
    with get_db() as conn:
        es = HistoricalEventStudy(conn)
        return es.evaluate_custom_event(date_str=date, event_name=name)

@app.get("/api/hypothesis/permutation")
async def run_permutation(
    window: int = Query(7, ge=1, le=30),
    n_trials: int = Query(2000, ge=500, le=5000)
):
    with get_db() as conn:
        # Load event dates
        rows = conn.execute("SELECT start_date FROM HistoricalEvents").fetchall()
        event_dates = [r['start_date'] for r in rows]
        ht = HypothesisTestingEngine(conn)
        return ht.run_permutation_test(event_dates, window_days=window, n_permutations=n_trials)

@app.get("/api/audit/logs")
async def get_audit_logs(limit: int = Query(100, ge=10, le=500)):
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, source_file, source_line, date, time, audit_type, action_taken, rationale, raw_snippet
            FROM AuditLog
            ORDER BY id ASC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]

@app.get("/api/messages/browse")
async def browse_messages(
    year: Optional[int] = None,
    callsign: Optional[str] = None,
    word: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100)
):
    """Browse primary or audited messages with filtering."""
    offset = (page - 1) * page_size
    filters = ["m.is_duplicate = 0"]
    params = []
    if year:
        filters.append("m.year = ?")
        params.append(year)
    if callsign:
        filters.append("m.callsign LIKE ?")
        params.append(f"%{callsign}%")
    if word:
        filters.append("m.full_word_sequence LIKE ?")
        params.append(f"%{word}%")
        
    where = "WHERE " + " AND ".join(filters)
    
    with get_db() as conn:
        total = conn.execute(f"SELECT COUNT(*) FROM Messages m {where}", params).fetchone()[0]
        q = f"""
            SELECT m.id, m.date, m.time_as_logged, m.callsign, m.header_number,
                   m.full_word_sequence, m.quality_flag, m.source_file, m.source_line
            FROM Messages m
            {where}
            ORDER BY m.date ASC, m.time_as_logged ASC
            LIMIT ? OFFSET ?
        """
        rows = conn.execute(q, params + [page_size, offset]).fetchall()
        
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size,
        'items': [dict(r) for r in rows]
    }

@app.get("/api/export/download/{filename}")
async def download_export(filename: str):
    """Serve exported CSV or DB files."""
    allowed = [
        'UVB76_full_messages.csv',
        'UVB76_full_messages_deduplicated.csv',
        'UVB76_duplicates_audit.csv',
        'UVB76_repeated_numbers.csv',
        'UVB76_repeated_numbers_deduplicated.csv',
        'UVB76_crossword_number_links.csv',
        'ziziphus_jujuba.db',
        'COMPREHENSIVE_RESEARCH_REPORT.md'
    ]
    if filename not in allowed:
        raise HTTPException(status_code=404, detail="File not found")
        
    if filename.endswith('.db'):
        path = DB_PATH
    else:
        path = EXPORTS_DIR / filename
        
    if not path.exists():
        raise HTTPException(status_code=404, detail="File does not exist")
        
    return FileResponse(path, filename=filename, media_type="application/octet-stream")
        

# ==========================================
# PHASE 2: COMPREHENSIVE TRAFFIC BEHAVIOR & STRUCTURAL ENDPOINTS
# ==========================================

@app.get("/api/traffic/volume")
async def get_traffic_volume():
    """Volume dynamics: yearly, monthly, daily, and day of week."""
    with get_db() as conn:
        engine = TrafficBehaviorEngine(conn)
        return engine.get_volume_dynamics()


@app.get("/api/traffic/diurnal")
async def get_traffic_diurnal():
    """Diurnal hourly distribution UTC vs MSK."""
    with get_db() as conn:
        engine = TrafficBehaviorEngine(conn)
        return engine.get_diurnal_distribution()


@app.get("/api/traffic/inter_arrival")
async def get_inter_arrival():
    """Inter-arrival intervals Delta t, burstiness, and Poisson testing."""
    with get_db() as conn:
        engine = TrafficBehaviorEngine(conn)
        return engine.get_inter_arrival_analysis()


@app.get("/api/traffic/cycles")
async def get_traffic_cycles():
    """Autocorrelation and periodic activity cycles."""
    with get_db() as conn:
        engine = TrafficBehaviorEngine(conn)
        return engine.get_periodicity_and_autocorrelation()


@app.get("/api/structural/callsigns")
async def get_callsign_evolution():
    """Chronological callsign transition matrix."""
    with get_db() as conn:
        engine = StructuralDynamicsEngine(conn)
        return engine.get_callsign_evolution()


@app.get("/api/structural/blocks")
async def get_message_blocks():
    """Message length and code block counts."""
    with get_db() as conn:
        engine = StructuralDynamicsEngine(conn)
        return engine.get_message_length_and_block_counts()


@app.get("/api/structural/vocabulary")
async def get_vocabulary_dynamics():
    """Heaps' law fit, vocabulary arrival and turnover."""
    with get_db() as conn:
        engine = StructuralDynamicsEngine(conn)
        return engine.get_vocabulary_turnover()


@app.get("/api/structural/cooccurrence")
async def get_word_cooccurrence():
    """Word co-occurrence within multi-block messages."""
    with get_db() as conn:
        engine = StructuralDynamicsEngine(conn)
        return engine.get_word_cooccurrence()


@app.get("/api/anomalies/daily")
async def get_daily_anomalies(threshold: float = Query(3.0, ge=1.5, le=6.0)):
    """Statistical anomaly detection via Modified Z-score (MAD)."""
    with get_db() as conn:
        detector = AnomalyDetector(conn)
        return detector.detect_daily_anomalies(threshold_mad=threshold)


@app.get("/api/anomalies/feb2022")
async def get_feb2022_audit():
    """In-depth forensic audit of February 2022 data."""
    with get_db() as conn:
        detector = AnomalyDetector(conn)
        return detector.audit_february_2022()


@app.get("/api/anomalies/gaps")
async def get_archive_gaps():
    """Archive coverage and data hiatus audit."""
    with get_db() as conn:
        detector = AnomalyDetector(conn)
        return detector.audit_archive_coverage_and_gaps()


@app.get("/api/network/epochs")
async def get_network_epochs():
    """Topological metrics across 4 chronological epochs."""
    with get_db() as conn:
        engine = NetworkEvolutionEngine(conn)
        return engine.get_epoch_metrics()


@app.get("/api/network/epoch_vis/{epoch_id}")
async def get_epoch_visualization(epoch_id: str):
    """Network subgraph for Vis.js rendering of an epoch."""
    with get_db() as conn:
        engine = NetworkEvolutionEngine(conn)
        return engine.get_epoch_subgraph_vis(epoch_id)


@app.get("/api/events/rigorous")
async def get_rigorous_events(window: int = Query(14, ge=3, le=45)):
    """Event study with Benjamini-Hochberg FDR and gap exclusion."""
    with get_db() as conn:
        engine = AdvancedEventStudyEngine(conn)
        return engine.run_rigorous_event_study(window_days=window)


@app.get("/api/findings/registry")
async def get_findings_registry():
    """Categorized registry of confirmed facts, refuted hypotheses, and limitations."""
    engine = FindingsRegistryEngine()
    return engine.get_findings_summary()
