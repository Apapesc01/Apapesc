import os
from django.db import models
from django.conf import settings
from pathlib import Path

# Funções de upload para os arquivos PDF
def upload_to_declaracao_residencia(instance, filename):
    file_path = os.path.join('pdf', 'declaracao_residencia.pdf')
    full_path = Path(settings.MEDIA_ROOT) / file_path

    # Verifica se o arquivo existe antes de tentar removê-lo
    if full_path.exists():
        try:
            full_path.unlink()  # Remove o arquivo existente
        except PermissionError:
            print(f"Permissão negada ao tentar remover {full_path}")
        except Exception as e:
            print(f"Erro ao remover {full_path}: {e}")

    return file_path


# Modelos para armazenar os arquivos PDF
class DeclaracaoResidenciaModel(models.Model):
    pdf_base = models.FileField(
        upload_to=upload_to_declaracao_residencia,
        verbose_name="PDF Base para Declaração de Residência",
        help_text="Substituirá o arquivo base atual para a declaração de residência."
    )
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    def save(self, *args, **kwargs):
        # Substituir o arquivo existente se for necessário
        if self.pk:
            old_instance = DeclaracaoResidenciaModel.objects.get(pk=self.pk)
            if old_instance.pdf_base and old_instance.pdf_base != self.pdf_base:
                # Remove o arquivo anterior
                if os.path.isfile(old_instance.pdf_base.path):
                    os.remove(old_instance.pdf_base.path)

        super().save(*args, **kwargs)

    def __str__(self):
        return "Declaração de Residência"