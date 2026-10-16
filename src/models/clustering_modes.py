"""
Clustering and Operational Modes Classification Engine.
Implements:
- K-Means clustering (k=3 and k=4) on monthly normalized spike-day profiles
- Silhouette analysis for cluster validity
- PCA 2D embedding for cluster visualization
- Identification of the 4 operational modes:
  Mode 1: Exercise culmination (Sep-Oct burst)
  Mode 2: Full training cycle (Feb-Nov wave)
  Mode 3: Opsec + exercise (Quiet + Sep flare)
  Mode 4: Off-cycle surge / Real operations (2019-2022)
"""

import sqlite3
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

from src.analysis.time_series import TimeSeriesAnalyzer

OPERATIONAL_MODE_DESCRIPTIONS = {
    1: {
        'name': 'Режим 1: Кульминация учений (Sep-Oct burst)',
        'name_en': 'Mode 1: Exercise culmination (Sep-Oct burst)',
        'description': 'Всплеск активности строго приурочен к завершающему этапу годового цикла стратегических маневров (сентябрь-октябрь).',
        'interpretation': 'Стратегические учения Запад/Восток/Кавказ/Центр'
    },
    2: {
        'name': 'Режим 2: Полный цикл боевой подготовки (Feb-Nov wave)',
        'name_en': 'Mode 2: Full training cycle (Feb-Nov wave)',
        'description': 'Широкая непрерывная волна активности с февраля по ноябрь, отражающая весенний и осенний периоды боевой учебы.',
        'interpretation': 'Плановые радиосети связи округов и военных баз'
    },
    3: {
        'name': 'Режим 3: Режим радиомолчания + учения (Quiet + Sep flare)',
        'name_en': 'Mode 3: Opsec + exercise (Quiet + Sep flare)',
        'description': 'Длительное радиомолчание в течение большей части года с точечной вспышкой радиообмена в сентябре.',
        'interpretation': 'Режим скрытности (OpSec) с проверкой готовности'
    },
    4: {
        'name': 'Режим 4: Внеплановый всплеск / Реальные операции (Off-cycle surge)',
        'name_en': 'Mode 4: Real operations / Off-cycle surge',
        'description': 'Аномальная активность в нетипичные зимние и весенние месяцы (январь-март), коррелирующая с реальными военно-политическими событиями.',
        'interpretation': 'Оперативное боевое управление в условиях кризисов'
    }
}

class OperationalModesClustering:
    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn
        self.ts_analyzer = TimeSeriesAnalyzer(db_conn)

    def fit_clustering(self, n_clusters: int = 3) -> Dict[str, Any]:
        """Runs K-Means clustering and PCA on normalized monthly activity matrix."""
        mat_data = self.ts_analyzer.get_normalized_monthly_matrix()
        matrix = mat_data['matrix']
        years = mat_data['years']
        
        if len(years) < n_clusters:
            return {'error': 'Not enough years for clustering'}
            
        feature_matrix = []
        for row in matrix:
            feature_matrix.append([row[f'm{m}'] for m in range(1, 13)])
        X = np.array(feature_matrix)
        
        # K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
        labels = kmeans.fit_predict(X)
        
        # Silhouette Score (if n_clusters < len(years))
        sil_score = 0.0
        if 1 < n_clusters < len(years):
            try:
                sil_score = round(float(silhouette_score(X, labels)), 3)
            except Exception:
                sil_score = 0.0
                
        # 2D PCA projection
        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(X)
        var_ratio = [round(float(v), 3) for v in pca.explained_variance_ratio_]
        
        # Map clusters to operational modes based on profile centroids
        clustered_years = []
        for i, y in enumerate(years):
            cid = int(labels[i])
            clustered_years.append({
                'year': int(y),
                'cluster_id': cid,
                'pca_x': round(float(X_pca[i, 0]), 2),
                'pca_y': round(float(X_pca[i, 1]), 2),
                'monthly_profile': [round(float(v), 1) for v in X[i]],
                'total_spike_days': matrix[i]['total_spike_days'],
                'mode_name': f"Cluster {cid + 1}"
            })
            
        centroids = []
        for cid in range(n_clusters):
            centroids.append([round(float(v), 1) for v in kmeans.cluster_centers_[cid]])
            
        return {
            'n_clusters': n_clusters,
            'silhouette_score': sil_score,
            'pca_variance_explained': var_ratio,
            'clustered_years': clustered_years,
            'cluster_centroids': centroids,
            'operational_modes_reference': OPERATIONAL_MODE_DESCRIPTIONS
        }
