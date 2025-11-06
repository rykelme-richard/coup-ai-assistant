"""
Gerador de vídeo a partir de roteiro e áudio gerados
"""
import os
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from config import VIDEO_OUTPUT_DIR, VIDEO_FORMAT, VIDEO_FPS

class VideoGenerator:
    def __init__(self):
        os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)
    
    def create_video_from_script(self, script, audio_path, output_filename="video_final.mp4", 
                                  background_color=(0, 0, 0), text_color='white'):
        """
        Cria vídeo a partir de roteiro e áudio
        
        Args:
            script: Roteiro com timestamps
            audio_path: Caminho do arquivo de áudio
            output_filename: Nome do arquivo de saída
            background_color: Cor de fundo (RGB)
            text_color: Cor do texto
        """
        try:
            # Carrega áudio
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Parse do script
            segments = self._parse_script_segments(script)
            
            # Cria clips de texto
            clips = []
            for segment in segments:
                if segment['narration']:
                    # Cria texto clip
                    txt_clip = TextClip(
                        segment['text'],
                        fontsize=50,
                        color=text_color,
                        font='Arial-Bold',
                        size=(1080, 1920),  # Formato vertical TikTok
                        method='caption'
                    ).set_duration(segment['duration']).set_position('center')
                    
                    clips.append(txt_clip)
            
            # Combina clips
            if clips:
                video = CompositeVideoClip(
                    clips,
                    size=(1080, 1920)
                ).set_duration(duration)
                
                # Adiciona áudio
                video = video.set_audio(audio)
                
                # Salva
                output_path = os.path.join(VIDEO_OUTPUT_DIR, output_filename)
                video.write_videofile(
                    output_path,
                    fps=VIDEO_FPS,
                    codec='libx264',
                    audio_codec='aac'
                )
                
                print(f"Vídeo gerado: {output_path}")
                return output_path
            else:
                print("Nenhum segmento encontrado no roteiro")
                return None
                
        except Exception as e:
            print(f"Erro ao gerar vídeo: {e}")
            print("Nota: Para usar este módulo, você precisa ter ffmpeg instalado")
            return None
    
    def _parse_script_segments(self, script):
        """Parse do roteiro em segmentos com duração"""
        segments = []
        lines = script.split('\n')
        
        prev_end = 0
        for line in lines:
            line = line.strip()
            if not line or not line.startswith('[') or 'TIMESTAMP' not in line:
                continue
            
            # Extrai timestamp
            timestamp_part = line[line.find('[TIMESTAMP:'):line.find(']')+1]
            timestamp = timestamp_part.replace('[TIMESTAMP:', '').replace(']', '').strip()
            
            # Parse timestamp (ex: "0-3s" ou "3-10s")
            if '-' in timestamp and 's' in timestamp:
                start_str, end_str = timestamp.split('-')
                start = float(start_str.replace('s', ''))
                end = float(end_str.replace('s', ''))
                duration = end - start
            else:
                start = prev_end
                duration = 3  # Default 3 segundos
                end = start + duration
            
            # Extrai texto
            if ' - ' in line:
                parts = line.split(' - ')
                text = parts[-1].strip().strip('"').strip("'")
            else:
                text = ""
            
            segments.append({
                'start': start,
                'end': end,
                'duration': duration,
                'text': text
            })
            
            prev_end = end
        
        return segments
    
    def create_simple_video(self, text, audio_path, output_filename="video_simples.mp4"):
        """
        Cria vídeo simples com texto estático e áudio
        """
        try:
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Cria texto clip
            txt_clip = TextClip(
                text,
                fontsize=60,
                color='white',
                font='Arial-Bold',
                size=(1080, 1920),
                method='caption',
                align='center'
            ).set_duration(duration).set_position('center')
            
            # Cria vídeo com fundo preto
            video = CompositeVideoClip(
                [txt_clip],
                size=(1080, 1920),
                bg_color=(0, 0, 0)
            ).set_duration(duration).set_audio(audio)
            
            output_path = os.path.join(VIDEO_OUTPUT_DIR, output_filename)
            video.write_videofile(
                output_path,
                fps=VIDEO_FPS,
                codec='libx264',
                audio_codec='aac'
            )
            
            print(f"Vídeo simples gerado: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Erro ao gerar vídeo simples: {e}")
            return None
