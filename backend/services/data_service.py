"""
Service pour télécharger et parser des datasets (CSV, Excel)
Utilisé pour extraire des données quantitatives depuis des URLs
"""

import httpx
import csv
import io
import math
from typing import List, Dict, Optional
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class DataService:
    """Service pour télécharger et parser des datasets"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls']
        self.max_file_size = 10 * 1024 * 1024  # 10 MB max
        self.min_rows = 5  # Minimum 5 lignes (ajusté pour statistiques concises)
        self.min_data_density = 0.3  # Minimum 30% de données non-nulles
        
        # Modèle d'embeddings pour la recherche sémantique
        print("🤖 Chargement du modèle d'embeddings...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Modèle d'embeddings chargé")
    
    @staticmethod
    def clean_nan_values(obj):
        """
        Nettoie récursivement tous les NaN, Infinity et autres valeurs non-JSON d'un objet
        
        Args:
            obj: L'objet à nettoyer (dict, list, ou valeur simple)
        
        Returns:
            L'objet nettoyé avec tous les NaN remplacés par None
        """
        if isinstance(obj, dict):
            return {k: DataService.clean_nan_values(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [DataService.clean_nan_values(item) for item in obj]
        elif isinstance(obj, float):
            # Vérifier NaN, Infinity
            if math.isnan(obj) or math.isinf(obj):
                return None
            return obj
        else:
            return obj
    
    def validate_dataset_quality(self, dataset: Dict) -> bool:
        """
        Valide qu'un dataset a suffisamment de lignes et de données non-vides
        
        Args:
            dataset: Le dataset à valider
        
        Returns:
            True si le dataset est valide, False sinon
        """
        try:
            total_rows = dataset.get('total_rows', 0)
            rows = dataset.get('rows', [])
            
            # Vérifier nombre minimum de lignes
            if total_rows < self.min_rows:
                print(f"⚠️ Dataset rejeté: seulement {total_rows} lignes (min {self.min_rows})")
                return False
            
            # Calculer la densité de données (% de valeurs non-nulles)
            if not rows:
                return False
            
            total_cells = 0
            non_null_cells = 0
            
            for row in rows:
                for value in row.values():
                    total_cells += 1
                    if value is not None and value != '' and value != '-':
                        non_null_cells += 1
            
            if total_cells == 0:
                return False
            
            data_density = non_null_cells / total_cells
            
            if data_density < self.min_data_density:
                print(f"⚠️ Dataset rejeté: seulement {data_density*100:.1f}% de données (min {self.min_data_density*100}%)")
                return False
            
            print(f"✅ Dataset validé: {total_rows} lignes, {data_density*100:.1f}% de densité")
            return True
            
        except Exception as e:
            print(f"❌ Erreur validation dataset: {e}")
            return False
    
    def extract_keywords_from_dataset(self, dataset: Dict) -> str:
        """
        Extrait les mots-clés d'un dataset (colonnes + quelques valeurs) pour validation
        
        Args:
            dataset: Le dataset parsé
        
        Returns:
            String contenant colonnes et valeurs pour analyse
        """
        try:
            columns = dataset.get('columns', [])
            preview = dataset.get('preview', [])
            
            # Texte searchable: colonnes + premières valeurs
            keywords_text = f"Colonnes: {', '.join([str(c) for c in columns[:10]])}. "
            
            # Ajouter quelques valeurs
            if preview:
                for i, row in enumerate(preview[:2]):
                    keywords_text += f"Ligne {i+1}: {', '.join([f'{k}={v}' for k, v in list(row.items())[:5]])}. "
            
            return keywords_text
            
        except Exception as e:
            return ""
    
    async def search_all_apis(self, query: str) -> List[Dict]:
        """
        Recherche de datasets via toutes les APIs disponibles
        
        Args:
            query: Termes de recherche
        
        Returns:
            Liste de datasets avec metadata
        """
        all_datasets = []
        
        # 1. data.gouv.fr
        datagouv_results = await self.search_datagouv_api(query)
        all_datasets.extend(datagouv_results)
        
        # 2. INSEE (séries temporelles)
        insee_results = await self.search_insee_api(query)
        all_datasets.extend(insee_results)
        
        # Dédupliquer par URL
        seen_urls = set()
        unique_datasets = []
        for ds in all_datasets:
            if ds['url'] not in seen_urls:
                seen_urls.add(ds['url'])
                unique_datasets.append(ds)
        
        print(f"📊 Total datasets uniques: {len(unique_datasets)}")
        return unique_datasets[:5]  # Limiter à 5 meilleurs
    
    def _calculate_semantic_score(self, item: Dict, query_embedding: np.ndarray) -> float:
        """
        Calcule un score de pertinence sémantique pour un dataset
        
        Args:
            item: Dataset data.gouv.fr
            query_embedding: Embedding de la requête utilisateur
        
        Returns:
            Score de pertinence (0-100, plus élevé = plus pertinent)
        """
        # Construire le texte du dataset
        title = item.get("title") or ""
        description = item.get("description") or ""
        dataset_text = f"{title}. {description[:300]}"  # Limiter la description
        
        # Encoder le dataset
        dataset_embedding = self.embedding_model.encode([dataset_text])
        
        # Similarité cosinus (0 à 1)
        semantic_similarity = cosine_similarity(query_embedding.reshape(1, -1), dataset_embedding)[0][0]
        
        # Score de base : similarité sémantique (0-70 points)
        score = semantic_similarity * 70
        
        # Bonus 1 : Nombre de ressources CSV/Excel (+5 max)
        resources = item.get("resources", [])
        csv_resources = [r for r in resources if (r.get("format") or "").lower() in ['csv', 'xlsx', 'xls']]
        score += min(len(csv_resources) * 2, 5)
        
        # Bonus 2 : Popularité (+10 max)
        metrics = item.get("metrics") or {}
        followers = metrics.get("followers", 0) if isinstance(metrics, dict) else 0
        score += min(followers / 10, 10)
        
        # Bonus 3 : Qualité de la description (+5 max)
        desc_length = len(description)
        if desc_length > 200:
            score += 5
        elif desc_length > 100:
            score += 3
        elif desc_length > 50:
            score += 1
        
        # Bonus 4 : Organisation reconnue (+10)
        org = item.get("organization") or {}
        org_name = (org.get("name", "") if isinstance(org, dict) else "").lower()
        recognized_orgs = ['insee', 'ministère', 'gouvernement', 'ademe', 'état']
        if any(org in org_name for org in recognized_orgs):
            score += 10
        
        return score
    
    async def _fetch_dataset_preview(self, url: str, format_type: str) -> Optional[Dict]:
        """
        Télécharge un aperçu des 5 premières lignes d'un dataset avec le nombre total de lignes
        
        Args:
            url: URL du dataset
            format_type: Type de fichier (csv, xlsx, xls)
        
        Returns:
            Dict avec 'preview' (5 premières lignes) et 'total_rows' ou None si échec
        """
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url, follow_redirects=True)
                
                if response.status_code != 200:
                    return None
                
                content = response.content
                
                if format_type == 'csv':
                    # Parser CSV complet pour compter les lignes
                    text = content.decode('utf-8', errors='ignore')
                    lines = text.split('\n')
                    # Compter lignes non-vides (exclure header)
                    total_rows = len([line for line in lines[1:] if line.strip()]) if len(lines) > 1 else 0
                    
                    # Aperçu des 5 premières lignes
                    preview_lines = lines[:6]  # Header + 5 lignes
                    reader = csv.DictReader(preview_lines)
                    preview = [dict(row) for row in list(reader)[:5]]
                    
                    return {
                        'preview': self.clean_nan_values(preview),
                        'total_rows': total_rows
                    }
                
                elif format_type in ['xlsx', 'xls']:
                    # Parser Excel complet pour compter
                    df_full = pd.read_excel(io.BytesIO(content))
                    total_rows = len(df_full)
                    
                    # Aperçu des 5 premières lignes
                    preview = df_full.head(5).to_dict('records')
                    
                    return {
                        'preview': self.clean_nan_values(preview),
                        'total_rows': total_rows
                    }
                
                return None
                
        except Exception as e:
            print(f"   ⚠️ Impossible de charger l'aperçu: {e}")
            return None
    
    async def search_datagouv_api(self, query: str) -> List[Dict]:
        """
        Recherche directe de datasets sur data.gouv.fr via leur API avec scoring sémantique
        
        Args:
            query: Termes de recherche
        
        Returns:
            Liste des 5 datasets les plus pertinents avec metadata
        """
        try:
            # Extraire les mots-clés pertinents pour l'API
            stop_words = ['analyse', 'marché', 'étude', 'du', 'de', 'des', 'le', 'la', 'les', 'un', 'une', 'en', 'sur', 'données', 'data']
            keywords = [word for word in query.lower().split() if word not in stop_words and len(word) > 2]
            search_query = ' '.join(keywords) if keywords else query
            
            print(f"🇫🇷 Recherche data.gouv.fr API: {query}")
            print(f"   → Mots-clés pour API: {search_query}")
            
            # Encoder la query complète pour la similarité sémantique
            print(f"   🧠 Encoding sémantique de la requête...")
            query_embedding = self.embedding_model.encode([query])[0]
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                # API de recherche data.gouv.fr - récupérer plus de résultats pour mieux scorer
                response = await client.get(
                    "https://www.data.gouv.fr/api/1/datasets/",
                    params={
                        "q": search_query,
                        "page_size": 50,  # Augmenté pour avoir plus de choix
                        "sort": "-followers"  # Trier par popularité comme base
                    }
                )
                
                if response.status_code != 200:
                    print(f"❌ Erreur API data.gouv.fr: {response.status_code}")
                    return []
                
                data = response.json()
                print(f"   → {data.get('total', 0)} résultats totaux, analyse sémantique de {len(data.get('data', []))} datasets")
                
                # Scorer et trier les datasets avec embeddings
                scored_items = []
                for item in data.get("data", []):
                    score = self._calculate_semantic_score(item, query_embedding)
                    scored_items.append((score, item))
                
                # Trier par score décroissant
                scored_items.sort(key=lambda x: x[0], reverse=True)
                
                # Extraire les 5 meilleurs avec leurs ressources + aperçu
                datasets = []
                for score, item in scored_items[:5]:  # Top 5
                    title = item.get("title", "Dataset")
                    description = item.get("description", "")[:200]
                    org = item.get("organization") or {}
                    organization = org.get("name", "Inconnu") if isinstance(org, dict) else "Inconnu"
                    resources = item.get("resources", [])
                    
                    print(f"   ✓ [Score: {score:.1f}] {title[:60]}")
                    
                    # Chercher des ressources CSV/Excel
                    for resource in resources:
                        url = resource.get("url", "")
                        format_type = (resource.get("format") or "").lower()
                        resource_title = resource.get("title", "Données")
                        
                        if format_type in ['csv', 'xlsx', 'xls'] or any(ext in url.lower() for ext in ['.csv', '.xlsx', '.xls']):
                            # Télécharger un aperçu du dataset
                            print(f"      📥 Chargement aperçu...")
                            preview_data = await self._fetch_dataset_preview(url, format_type)
                            
                            dataset_entry = {
                                "title": f"{title} - {resource_title}",
                                "url": url,
                                "type": format_type or self._detect_format_from_url(url),
                                "description": description,
                                "organization": organization,
                                "source": "data.gouv.fr",
                                "relevance_score": float(round(score, 2)),
                                "preview": preview_data.get('preview') if preview_data else None,
                                "preview_columns": list(preview_data['preview'][0].keys()) if preview_data and preview_data.get('preview') and len(preview_data['preview']) > 0 else [],
                                "total_rows": preview_data.get('total_rows', 0) if preview_data else 0
                            }
                            
                            datasets.append(dataset_entry)
                            break  # Prendre la première ressource CSV/Excel seulement
                
                print(f"✅ Trouvé {len(datasets)} datasets pertinents sur data.gouv.fr")
                return datasets
                
        except Exception as e:
            print(f"❌ Erreur recherche data.gouv.fr: {e}")
            return []
    
    def _detect_format_from_url(self, url: str) -> str:
        """Détecte le format depuis l'URL"""
        url_lower = url.lower()
        if '.csv' in url_lower:
            return 'csv'
        elif '.xlsx' in url_lower:
            return 'xlsx'
        elif '.xls' in url_lower:
            return 'xls'
        return 'unknown'
    
    async def search_insee_api(self, query: str) -> List[Dict]:
        """
        Recherche de séries temporelles INSEE via leur API
        
        Args:
            query: Termes de recherche
        
        Returns:
            Liste de datasets INSEE
        """
        try:
            print(f"🇫🇷 Recherche INSEE API: {query}")
            
            # Pour l'instant, retourner vide car l'API INSEE nécessite setup complexe
            # Les datasets INSEE seront trouvés via data.gouv.fr qui référence l'INSEE
            print("📊 INSEE: utiliser data.gouv.fr comme proxy")
            return []
                
        except Exception as e:
            print(f"❌ Erreur recherche INSEE: {e}")
            return []
    
    async def search_insee_api(self, query: str) -> List[Dict]:
        """
        Recherche de séries temporelles INSEE via leur API
        
        Args:
            query: Termes de recherche
        
        Returns:
            Liste de datasets INSEE
        """
        try:
            print(f"🇫🇷 Recherche INSEE API: {query}")
            
            # API INSEE nécessite une clé API, mais on peut chercher dans les séries publiées
            # Pour l'instant, retourner une liste vide (nécessite authentification)
            # TODO: Implémenter avec clé API INSEE si disponible
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Recherche dans les données locales INSEE (fichiers Excel disponibles)
                # Utiliser l'index des publications INSEE
                response = await client.get(
                    "https://www.insee.fr/fr/statistiques/recherche",
                    params={
                        "q": query,
                        "debut": 0
                    },
                    follow_redirects=True
                )
                
                if response.status_code != 200:
                    print(f"⚠️ INSEE API non disponible")
                    return []
                
                # Pour l'instant, retourner vide car l'API INSEE nécessite setup complexe
                # Les datasets INSEE seront trouvés via data.gouv.fr qui référence l'INSEE
                print("📊 INSEE: utiliser data.gouv.fr comme proxy")
                return []
                
        except Exception as e:
            print(f"❌ Erreur recherche INSEE: {e}")
            return []
    
    def is_dataset_url(self, url: str) -> bool:
        """Vérifie si une URL pointe vers un dataset supporté (CSV ou Excel uniquement)"""
        url_lower = url.lower()
        
        # Exclure PDF et XML
        if any(url_lower.endswith(ext) for ext in ['.pdf', '.xml']):
            return False
        
        # Accepter uniquement CSV et Excel
        return any(url_lower.endswith(fmt) for fmt in self.supported_formats)
    
    async def scrape_dataset_links(self, page_url: str) -> List[str]:
        """
        Scrape une page HTML pour extraire les liens vers des datasets (CSV, Excel)
        
        Args:
            page_url: URL de la page à scraper
        
        Returns:
            Liste des URLs de datasets trouvées
        """
        try:
            # Ignorer les PDF et XML
            if page_url.lower().endswith(('.pdf', '.xml')):
                print(f"⏭️ Fichier non HTML ignoré: {page_url}")
                return []
            
            print(f"🔍 Scraping de la page: {page_url}")
            
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                response = await client.get(page_url)
                
                if response.status_code != 200:
                    print(f"❌ Erreur HTTP {response.status_code}")
                    return []
                
                # Parser le HTML
                soup = BeautifulSoup(response.text, 'lxml')
                
                dataset_urls = []
                
                # SPÉCIFIQUE data.gouv.fr : Chercher les ressources
                if 'data.gouv.fr' in page_url:
                    print("  🇫🇷 Détection data.gouv.fr - Recherche spécifique")
                    # Chercher les liens de ressources
                    for resource in soup.find_all(['a', 'div'], class_=lambda x: x and 'resource' in str(x).lower()):
                        if resource.get('href'):
                            href = resource['href']
                            absolute_url = urljoin(page_url, href)
                            if self.is_dataset_url(absolute_url):
                                dataset_urls.append(absolute_url)
                                print(f"  ✅ Ressource data.gouv.fr: {absolute_url}")
                    
                    # Chercher dans data-href et onclick
                    for elem in soup.find_all(attrs={'data-href': True}):
                        href = elem['data-href']
                        absolute_url = urljoin(page_url, href)
                        if self.is_dataset_url(absolute_url):
                            dataset_urls.append(absolute_url)
                            print(f"  ✅ Data-href data.gouv.fr: {absolute_url}")
                
                # Recherche générique pour tous les sites
                
                # Chercher tous les liens <a>
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    
                    # Construire l'URL absolue
                    absolute_url = urljoin(page_url, href)
                    
                    # Vérifier si c'est un lien vers un dataset
                    if self.is_dataset_url(absolute_url):
                        # Vérifier que ce n'est pas un lien interne de navigation
                        if not any(skip in absolute_url.lower() for skip in ['login', 'signup', 'auth', 'account']):
                            dataset_urls.append(absolute_url)
                            print(f"  ✅ Dataset trouvé: {absolute_url}")
                
                # Chercher dans download links et export buttons
                for elem in soup.find_all(['a', 'button'], class_=lambda x: x and any(
                    term in str(x).lower() for term in ['download', 'export', 'télécharger', 'data']
                )):
                    if elem.get('href'):
                        absolute_url = urljoin(page_url, elem['href'])
                        if self.is_dataset_url(absolute_url):
                            dataset_urls.append(absolute_url)
                            print(f"  ✅ Dataset trouvé (bouton): {absolute_url}")
                    elif elem.get('data-url'):
                        absolute_url = urljoin(page_url, elem['data-url'])
                        if self.is_dataset_url(absolute_url):
                            dataset_urls.append(absolute_url)
                            print(f"  ✅ Dataset trouvé (data-url): {absolute_url}")
                
                # Dédupliquer
                dataset_urls = list(set(dataset_urls))
                
                print(f"📊 Total datasets extraits: {len(dataset_urls)}")
                return dataset_urls
                
        except Exception as e:
            print(f"❌ Erreur lors du scraping de {page_url}: {e}")
            return []
    
    async def download_and_parse(self, url: str) -> Optional[Dict]:
        """
        Télécharge et parse un dataset depuis une URL
        
        Args:
            url: URL du dataset
        
        Returns:
            Dict avec structure:
            {
                "format": "csv" | "excel",
                "rows": [{"col1": "val1", "col2": "val2"}, ...],
                "preview": [liste des 5 premières lignes],
                "columns": ["col1", "col2", ...],
                "total_rows": int
            }
        """
        
        if not self.is_dataset_url(url):
            print(f"⚠️ URL non supportée: {url}")
            return None
        
        try:
            print(f"📥 Téléchargement du dataset: {url}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, follow_redirects=True)
                
                if response.status_code != 200:
                    print(f"❌ Erreur HTTP {response.status_code} pour {url}")
                    return None
                
                # Vérifier la taille
                content_length = len(response.content)
                if content_length > self.max_file_size:
                    print(f"⚠️ Fichier trop volumineux: {content_length / 1024 / 1024:.2f} MB")
                    return None
                
                # Parser selon le format
                if url.lower().endswith('.csv'):
                    return await self._parse_csv(response.content, url)
                elif url.lower().endswith(('.xlsx', '.xls')):
                    return await self._parse_excel(response.content, url)
                
        except httpx.TimeoutException:
            print(f"⏱️ Timeout lors du téléchargement de {url}")
            return None
        except Exception as e:
            print(f"❌ Erreur lors du parsing de {url}: {e}")
            return None
    
    async def _parse_csv(self, content: bytes, url: str) -> Dict:
        """Parse un fichier CSV"""
        try:
            # Essayer différents encodages
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    text_content = content.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                print(f"❌ Impossible de décoder le CSV avec les encodages communs")
                return None
            
            # Détecter le délimiteur
            sniffer = csv.Sniffer()
            sample = text_content[:1024]
            try:
                dialect = sniffer.sniff(sample)
                delimiter = dialect.delimiter
            except:
                delimiter = ','  # Par défaut
            
            # Parser le CSV
            reader = csv.DictReader(io.StringIO(text_content), delimiter=delimiter)
            rows = list(reader)
            
            if not rows:
                print(f"⚠️ CSV vide: {url}")
                return None
            
            # Remplacer les chaînes vides et 'nan' par None
            for row in rows:
                for key in row:
                    if row[key] == '' or row[key] == 'nan' or row[key] == 'NaN':
                        row[key] = None
            
            columns = list(rows[0].keys())
            preview = rows[:5]  # 5 premières lignes
            
            print(f"✅ CSV parsé: {len(rows)} lignes, {len(columns)} colonnes")
            
            # Construire le résultat
            result = {
                "format": "csv",
                "url": url,
                "rows": rows,
                "preview": preview,
                "columns": columns,
                "total_rows": len(rows)
            }
            
            # NETTOYAGE FINAL : éliminer récursivement tous les NaN restants
            result = self.clean_nan_values(result)
            
            # VALIDATION : vérifier qualité du dataset
            if not self.validate_dataset_quality(result):
                return None
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur parsing CSV: {e}")
            return None
    
    async def _parse_excel(self, content: bytes, url: str) -> Dict:
        """Parse un fichier Excel"""
        try:
            # Utiliser pandas pour parser Excel
            df = pd.read_excel(io.BytesIO(content), engine='openpyxl')
            
            if df.empty:
                print(f"⚠️ Excel vide: {url}")
                return None
            
            # Remplacer TOUS les NaN/inf par None (crucial pour JSON)
            df = df.replace([float('inf'), float('-inf')], None)
            df = df.fillna(value=None)
            
            # Convertir en dictionnaire
            rows = df.to_dict('records')
            columns = [str(col) for col in df.columns.tolist()]  # Forcer en string
            preview = rows[:5]  # 5 premières lignes
            
            print(f"✅ Excel parsé: {len(rows)} lignes, {len(columns)} colonnes")
            
            # Construire le résultat
            result = {
                "format": "excel",
                "url": url,
                "rows": rows,
                "preview": preview,
                "columns": columns,
                "total_rows": len(rows)
            }
            
            # NETTOYAGE FINAL : éliminer récursivement tous les NaN restants
            result = self.clean_nan_values(result)
            
            # VALIDATION : vérifier qualité du dataset
            if not self.validate_dataset_quality(result):
                return None
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur parsing Excel: {e}")
            return None
    
    def format_preview_for_display(self, dataset: Dict) -> str:
        """Formate les 5 premières lignes pour affichage"""
        if not dataset or not dataset.get("preview"):
            return "Aucune donnée disponible"
        
        preview = dataset["preview"]
        columns = dataset["columns"]
        
        # Créer un tableau texte
        output = f"📊 Dataset ({dataset['total_rows']} lignes, {len(columns)} colonnes)\n\n"
        output += "Colonnes: " + ", ".join(columns) + "\n\n"
        output += "Aperçu (5 premières lignes):\n"
        
        for i, row in enumerate(preview, 1):
            output += f"Ligne {i}: " + " | ".join([f"{k}={v}" for k, v in row.items()]) + "\n"
        
        return output
