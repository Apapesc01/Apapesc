# app_uploads/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import UploadsDocs
from app_associados.drive_service import upload_file_to_drive
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import os


@receiver(post_save, sender=UploadsDocs)
def processar_upload_e_enviar_drive(sender, instance, created, **kwargs):
    """
    Comprime o arquivo e envia automaticamente para o Google Drive,
    garantindo que o nome final (renomeado pelo model) seja usado.
    """
    if not created:
        return

    def _processar():
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
                nome_arquivo = os.path.basename(instance.arquivo.name)
                upload_file_to_drive(path, nome_arquivo, folder_id)
                print(f"✅ '{nome_arquivo}' enviado para o Drive do associado ({folder_id})")
            else:
                print("⚠️ Associado sem pasta Drive vinculada.")
        except Exception as e:
            print(f"❌ Erro ao enviar para o Drive: {e}")

    # Executa somente após o commit final (quando o rename já ocorreu)
    transaction.on_commit(_processar)
