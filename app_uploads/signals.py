# app_uploads/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UploadsDocs
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from django.core.files.storage import default_storage
from app_associados.drive_service import upload_file_to_drive

import os





@receiver(post_save, sender=UploadsDocs)
def processar_upload_e_enviar_drive(sender, instance, created, **kwargs):
    """
    Comprime o arquivo após upload e envia automaticamente
    uma cópia para o Google Drive do associado, preservando o nome original.
    """
    if not created:
        return

    path = instance.arquivo.path
    ext = path.lower().split('.')[-1]

    # 1️⃣ Compressão local
    try:
        if ext in ['jpg', 'jpeg', 'png']:
            imagem = Image.open(path).convert('RGB')
            imagem.save(path, optimize=True, quality=65)
        elif ext == 'pdf':
            reader = PdfReader(path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            with open(path, "wb") as f:
                writer.write(f)
    except Exception as e:
        print(f"⚠️ Erro ao comprimir arquivo: {e}")

    # 2️⃣ Envio automático para o Google Drive
    try:
        proprietario = getattr(instance, "proprietario_object", None)
        folder_id = getattr(proprietario, "drive_folder_id", None)

        if folder_id:
            # Usa o nome do upload (sem caminho local)
            nome_arquivo = instance.arquivo.name.split('/')[-1]

            # Envia para o Google Drive com o mesmo nome
            upload_file_to_drive(path, nome_arquivo, folder_id)
            print(f"✅ Arquivo '{nome_arquivo}' enviado para o Drive do associado ({folder_id})")
        else:
            print("⚠️ Nenhuma pasta Drive vinculada ao associado.")
    except Exception as e:
        print(f"❌ Erro ao enviar arquivo para o Drive: {e}")