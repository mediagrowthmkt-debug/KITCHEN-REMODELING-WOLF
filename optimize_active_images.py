#!/usr/bin/env python3
"""
Script para otimizar apenas as imagens usadas no index.html
Converte para WebP com alta compressão
"""

import os
from pathlib import Path
from PIL import Image

# Diretório base
BASE_DIR = Path("/Users/bruno/Documents/LPS/CLIENTES/WOLF/KITCHEN REMODELING")

# Lista de imagens usadas no index.html
ACTIVE_IMAGES = [
    "0 - Brand Logo/brand-logo-wolfcarpenters.png",
    "MORE MATERIALS/hero/Snapinst.app_471409545_605857828504025_7462411292612250991_n_1080.jpg",
    "MORE MATERIALS/hero/WhatsApp Image 2025-03-13 at 15.42.50 (2).jpeg",
    "MORE MATERIALS/hero/zLBcsu7Q.jpeg",
    "2 - Before and After Transformation/after-new-kitchen.jpg",
    "2 - Before and After Transformation/before-old-kitchen.jpg",
    "3 - Portfolio - Another Kitchen Renovation/portfolio-blue-white-kitchen-1.jpg",
    "3 - Portfolio - Another Kitchen Renovation/portfolio-blue-white-kitchen-2.jpg",
    "3 - Portfolio - Another Kitchen Renovation/portfolio-overview-island.jpg",
    "3 - Portfolio - Another Kitchen Renovation/portfolio-sink-and-window.jpg",
    "3 - Portfolio - Another Kitchen Renovation/portfolio-sink-closeup.jpg",
    "4 - Project Highlights - Custom Kitchens/custom-black-kitchen-1.jpg",
    "4 - Project Highlights - Custom Kitchens/custom-black-kitchen-2.jpg",
    "4 - Project Highlights - Custom Kitchens/custom-black-kitchen-3.jpg",
    "4 - Project Highlights - Custom Kitchens/custom-black-kitchen-wide.jpg",
    "MORE MATERIALS/imagens/51918b8d-cfde-40ef-b321-30fb9e4ec24a (1).jpg",
    "MORE MATERIALS/imagens/6fdb1cc0-8d4f-4176-99ac-480f12c5bea5 (1).jpg",
    "MORE MATERIALS/imagens/d7e2b09a-8129-4be1-96e0-e53b78ba04bd (1).jpg",
    "MORE MATERIALS/imagens/xhGYIZvA.jpeg",
    "6 - Meet the Team - Wolf Carpenters/team-full-group.jpg",
]

def get_file_size_mb(filepath):
    """Retorna o tamanho do arquivo em MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def optimize_image(image_path):
    """Converte e otimiza imagem para WebP"""
    try:
        if not image_path.exists():
            print(f"✗ Arquivo não encontrado: {image_path}")
            return False
            
        # Abrir imagem
        img = Image.open(image_path)
        
        # Converter para RGB se necessário
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Redimensionar se muito grande (mantém proporção)
        max_dimension = 1920
        original_size_pixels = img.size
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            print(f"  📐 Redimensionado: {original_size_pixels} -> {new_size}")
        
        # Criar nome do arquivo WebP
        webp_path = image_path.with_suffix('.webp')
        
        # Se já é WebP, otimizar no lugar
        if image_path.suffix.lower() == '.webp':
            temp_path = image_path.with_stem(image_path.stem + '_temp')
            original_size = get_file_size_mb(image_path)
            img.save(temp_path, 'WEBP', quality=75, method=6)
            new_size = get_file_size_mb(temp_path)
            
            os.remove(image_path)
            temp_path.rename(image_path)
            webp_path = image_path
        else:
            # Converter para WebP
            original_size = get_file_size_mb(image_path)
            img.save(webp_path, 'WEBP', quality=75, method=6)
            new_size = get_file_size_mb(webp_path)
            
            # Remover arquivo original
            os.remove(image_path)
        
        reduction = ((original_size - new_size) / original_size * 100) if original_size > 0 else 0
        print(f"✓ {image_path.name}")
        print(f"  💾 {original_size:.2f}MB -> {new_size:.2f}MB (↓ {reduction:.1f}%)")
        
        return webp_path.relative_to(BASE_DIR)
        
    except Exception as e:
        print(f"✗ Erro ao otimizar {image_path.name}: {e}")
        return False

def update_html_references(conversions):
    """Atualiza as referências no index.html para os novos arquivos WebP"""
    html_file = BASE_DIR / "index.html"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir cada referência
        for old_path, new_path in conversions.items():
            if old_path != str(new_path):  # Só se mudou a extensão
                content = content.replace(old_path, str(new_path))
        
        # Salvar arquivo atualizado
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✓ HTML atualizado com {len(conversions)} referências")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao atualizar HTML: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 70)
    print("🖼️  OTIMIZAÇÃO DE IMAGENS ATIVAS - KITCHEN REMODELING")
    print("=" * 70)
    print(f"\n📋 Total de imagens a processar: {len(ACTIVE_IMAGES)}\n")
    
    conversions = {}
    success_count = 0
    total_original_size = 0
    total_new_size = 0
    
    for i, img_rel_path in enumerate(ACTIVE_IMAGES, 1):
        print(f"\n[{i}/{len(ACTIVE_IMAGES)}] Processando...")
        img_path = BASE_DIR / img_rel_path
        
        if img_path.exists():
            original_size = get_file_size_mb(img_path)
            total_original_size += original_size
            
            result = optimize_image(img_path)
            
            if result:
                conversions[img_rel_path] = result
                # Calcular novo tamanho
                new_path = BASE_DIR / result
                if new_path.exists():
                    new_size = get_file_size_mb(new_path)
                    total_new_size += new_size
                success_count += 1
        else:
            print(f"✗ Arquivo não encontrado: {img_rel_path}")
    
    print("\n" + "=" * 70)
    print("📊 RESUMO DA OTIMIZAÇÃO")
    print("=" * 70)
    print(f"✓ Imagens processadas: {success_count}/{len(ACTIVE_IMAGES)}")
    print(f"💾 Tamanho original total: {total_original_size:.2f}MB")
    print(f"💾 Tamanho otimizado total: {total_new_size:.2f}MB")
    
    if total_original_size > 0:
        total_reduction = ((total_original_size - total_new_size) / total_original_size * 100)
        saved_mb = total_original_size - total_new_size
        print(f"📉 Redução total: {saved_mb:.2f}MB ({total_reduction:.1f}%)")
    
    # Atualizar HTML
    if conversions:
        print("\n" + "=" * 70)
        print("📝 ATUALIZANDO REFERÊNCIAS NO HTML")
        print("=" * 70)
        update_html_references(conversions)
    
    print("\n" + "=" * 70)
    print("✅ OTIMIZAÇÃO CONCLUÍDA!")
    print("=" * 70)

if __name__ == "__main__":
    main()
