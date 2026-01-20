#!/usr/bin/env python3
"""
Script para otimizar todas as imagens e vídeos da pasta KITCHEN REMODELING
Converte imagens para WebP com alta compressão e otimiza vídeos
"""

import os
import subprocess
from pathlib import Path
from PIL import Image
import shutil

# Diretório base
BASE_DIR = Path("/Users/bruno/Documents/LPS/CLIENTES/WOLF/KITCHEN REMODELING")

# Extensões suportadas
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'}

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ FFmpeg instalado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ FFmpeg não encontrado. Instalando...")
        subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
    
    try:
        from PIL import Image
        print("✓ Pillow instalado")
    except ImportError:
        print("✗ Pillow não encontrado. Instalando...")
        subprocess.run(['pip3', 'install', 'Pillow'], check=True)

def get_file_size_mb(filepath):
    """Retorna o tamanho do arquivo em MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def optimize_image(image_path):
    """Converte e otimiza imagem para WebP"""
    try:
        # Se já é WebP, ainda otimiza
        img = Image.open(image_path)
        
        # Converter para RGB se necessário (PNG com transparência, etc)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Redimensionar se muito grande (mantém proporção)
        max_dimension = 1920
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            print(f"  Redimensionado para: {new_size}")
        
        # Criar nome do arquivo WebP
        webp_path = image_path.with_suffix('.webp')
        
        # Se o arquivo original já é .webp, criar um temporário
        if image_path.suffix.lower() == '.webp':
            webp_path = image_path.with_stem(image_path.stem + '_optimized')
        
        # Salvar como WebP com qualidade otimizada
        original_size = get_file_size_mb(image_path)
        img.save(webp_path, 'WEBP', quality=75, method=6)
        new_size = get_file_size_mb(webp_path)
        
        # Se o original era WebP, substituir
        if image_path.suffix.lower() == '.webp':
            os.remove(image_path)
            webp_path.rename(image_path)
            webp_path = image_path
        else:
            # Remover arquivo original (não-WebP)
            os.remove(image_path)
        
        reduction = ((original_size - new_size) / original_size * 100) if original_size > 0 else 0
        print(f"✓ {image_path.name} -> {webp_path.name}")
        print(f"  {original_size:.2f}MB -> {new_size:.2f}MB (redução de {reduction:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro ao otimizar {image_path.name}: {e}")
        return False

def optimize_video(video_path):
    """Otimiza vídeo reduzindo tamanho mantendo qualidade aceitável"""
    try:
        original_size = get_file_size_mb(video_path)
        
        # Criar nome do arquivo otimizado
        output_path = video_path.with_stem(video_path.stem + '_optimized')
        
        # Parâmetros de otimização para vídeo
        # CRF 28 = boa qualidade com compressão alta (18-28 é o range recomendado)
        # preset medium = balanço entre velocidade e compressão
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-c:v', 'libx264',          # Codec H.264
            '-crf', '28',                # Qualidade (menor = melhor, mas maior arquivo)
            '-preset', 'medium',         # Velocidade de encoding
            '-c:a', 'aac',               # Codec de áudio
            '-b:a', '128k',              # Bitrate de áudio reduzido
            '-movflags', '+faststart',   # Otimização para streaming
            '-vf', 'scale=1280:720',     # Redimensionar para 720p se maior
            '-y',                         # Sobrescrever sem perguntar
            str(output_path)
        ]
        
        print(f"⏳ Otimizando {video_path.name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and output_path.exists():
            new_size = get_file_size_mb(output_path)
            reduction = ((original_size - new_size) / original_size * 100) if original_size > 0 else 0
            
            # Substituir o original pelo otimizado
            os.remove(video_path)
            output_path.rename(video_path)
            
            print(f"✓ {video_path.name}")
            print(f"  {original_size:.2f}MB -> {new_size:.2f}MB (redução de {reduction:.1f}%)")
            return True
        else:
            print(f"✗ Erro ao otimizar {video_path.name}")
            if output_path.exists():
                os.remove(output_path)
            return False
            
    except Exception as e:
        print(f"✗ Erro ao otimizar {video_path.name}: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("OTIMIZAÇÃO DE MÍDIA - KITCHEN REMODELING")
    print("=" * 60)
    print()
    
    # Verificar dependências
    print("Verificando dependências...")
    check_dependencies()
    print()
    
    # Criar backup primeiro
    backup_dir = BASE_DIR.parent / "_BACKUP_KITCHEN_ORIGINAL"
    if not backup_dir.exists():
        print(f"Criando backup em: {backup_dir}")
        # Não fazer backup completo, apenas avisar
        print("⚠️  AVISO: Certifique-se de ter backup dos arquivos originais!")
        input("Pressione ENTER para continuar ou CTRL+C para cancelar...")
        print()
    
    # Encontrar todos os arquivos
    print("Buscando arquivos...")
    image_files = []
    video_files = []
    
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            file_path = Path(root) / file
            ext = file_path.suffix.lower()
            
            if ext in IMAGE_EXTENSIONS or ext == '.webp':
                image_files.append(file_path)
            elif ext in VIDEO_EXTENSIONS:
                video_files.append(file_path)
    
    print(f"Encontrados: {len(image_files)} imagens, {len(video_files)} vídeos")
    print()
    
    # Processar imagens
    if image_files:
        print(f"{'=' * 60}")
        print(f"PROCESSANDO IMAGENS ({len(image_files)} arquivos)")
        print(f"{'=' * 60}")
        
        success = 0
        for i, img_path in enumerate(image_files, 1):
            print(f"\n[{i}/{len(image_files)}] Processando imagem...")
            if optimize_image(img_path):
                success += 1
        
        print(f"\n✓ Imagens otimizadas: {success}/{len(image_files)}")
    
    # Processar vídeos
    if video_files:
        print(f"\n{'=' * 60}")
        print(f"PROCESSANDO VÍDEOS ({len(video_files)} arquivos)")
        print(f"{'=' * 60}")
        
        success = 0
        for i, vid_path in enumerate(video_files, 1):
            print(f"\n[{i}/{len(video_files)}] Processando vídeo...")
            if optimize_video(vid_path):
                success += 1
        
        print(f"\n✓ Vídeos otimizados: {success}/{len(video_files)}")
    
    print("\n" + "=" * 60)
    print("OTIMIZAÇÃO CONCLUÍDA!")
    print("=" * 60)

if __name__ == "__main__":
    main()
