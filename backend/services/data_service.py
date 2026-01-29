"""
Service pour télécharger et parser des datasets (CSV, Excel)
Utilisé pour extraire des données quantitatives depuis des URLs
"""

import httpx
import csv
import io
from typing import List, Dict, Optional
import pandas as pd


class DataService:
    """Service pour télécharger et parser des datasets"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls']
        self.max_file_size = 10 * 1024 * 1024  # 10 MB max
    
    def is_dataset_url(self, url: str) -> bool:
        """Vérifie si une URL pointe vers un dataset supporté"""
        url_lower = url.lower()
        return any(url_lower.endswith(fmt) for fmt in self.supported_formats)
    
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
            
            columns = list(rows[0].keys())
            preview = rows[:5]  # 5 premières lignes
            
            print(f"✅ CSV parsé: {len(rows)} lignes, {len(columns)} colonnes")
            
            return {
                "format": "csv",
                "url": url,
                "rows": rows,
                "preview": preview,
                "columns": columns,
                "total_rows": len(rows)
            }
            
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
            
            # Convertir en dictionnaire
            rows = df.to_dict('records')
            columns = df.columns.tolist()
            preview = rows[:5]  # 5 premières lignes
            
            print(f"✅ Excel parsé: {len(rows)} lignes, {len(columns)} colonnes")
            
            return {
                "format": "excel",
                "url": url,
                "rows": rows,
                "preview": preview,
                "columns": columns,
                "total_rows": len(rows)
            }
            
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
