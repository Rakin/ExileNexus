import requests
import json
from datetime import datetime, timedelta

try:
    from googleapiclient.discovery import build
except ImportError:
    build = None

class PoeMetaScanner:
    def __init__(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {}

        self.api_key = self.config.get('youtube_api_key', "")
        self.league = self.config.get('league', 'Keepers')
        self.youtube = None

        if self.api_key and self.api_key != "SUA_CHAVE_AQUI" and build:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
            except:
                self.youtube = None

    def get_youtube_trends(self):
        if not self.youtube:
            return "⚠️ YouTube API Key ausente"

        # Janela rigorosa de 24 horas para capturar o início do Hype
        time_threshold = (datetime.utcnow() - timedelta(hours=24)).isoformat() + 'Z'
        
        try:
            # Busca agressiva por termos de "Hype"
            search_query = f"Path of Exile (3.27 OR {self.league}) (broken OR OP OR build OR guide)"
            
            request = self.youtube.search().list(
                q=search_query,
                part="snippet",
                type="video",
                publishedAfter=time_threshold,
                order="relevance",
                maxResults=2
            )
            response = request.execute()
            items = response.get('items', [])

            if not items:
                return "⏱️ [24H] Sem vídeos explosivos nas últimas horas. Monitorando..."

            cards = []
            for item in items:
                s = item['snippet']
                video_id = item['id']['videoId']
                title = s['title'].replace("&#39;", "'").replace("&amp;", "&")[:50]
                channel = s['channelTitle'].upper()
                
                # Cálculo de tempo preciso (Horas e Minutos)
                pub_time = datetime.strptime(s['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                diff = datetime.utcnow() - pub_time
                total_seconds = int(diff.total_seconds())
                
                if total_seconds < 3600:
                    time_desc = f"{total_seconds // 60} min atrás"
                else:
                    time_desc = f"{total_seconds // 3600} horas atrás"

                card = (
                    f"  ┌──────────────────────────────────────────────────────────┐\n"
                    f"  │ 📺 CANAL: {channel[:44]:<44} │\n"
                    f"  │ 📝 {title:<52} │\n"
                    f"  │ ⏱️ POSTADO: {time_desc:<13} | 🔗 https://youtu.be/{video_id:<14} │\n"
                    f"  └──────────────────────────────────────────────────────────┘"
                )
                cards.append(card)
            
            return "🚀 HYPE DETECTADO (ÚLTIMAS 24H):\n" + "\n".join(cards)

        except Exception as e:
            if "quotaExceeded" in str(e): return "⚠️ Cota YouTube excedida."
            return f"⚠️ Erro YouTube: {str(e)[:20]}"

    def get_quick_summary(self):
        return self.get_youtube_trends()

    def _search_hype_fallback(self):
        """Busca de 48h se as últimas 24h estiverem paradas."""
        time_threshold = (datetime.utcnow() - timedelta(days=2)).isoformat() + 'Z'
        request = self.youtube.search().list(
            q=f"PoE 3.27 {self.league} builds",
            part="snippet",
                type="video",
            publishedAfter=time_threshold,
            order="viewCount",
            maxResults=2
        )
        res = request.execute()
        items = res.get('items', [])
        return "📡 SEM HYPE NAS 24H. ÚLTIMOS VÍDEOS:\n" + "\n".join([f"   ▶ [{i['snippet']['channelTitle'][:10]}] {i['snippet']['title'][:30]}..." for i in items])

    def get_quick_summary(self):
        """Método chamado pelo main.py para o cabeçalho."""
        return self.get_youtube_trends()

    def run_report(self):
        """Relatório detalhado para o log inicial."""
        print(f"\n--- TENDÊNCIAS DO YOUTUBE (ÚLTIMAS 24H) ---")
        summary = self.get_youtube_trends()
        print(summary)