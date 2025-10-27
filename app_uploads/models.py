# app_uploads/models.py
import os
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from unidecode import unidecode 
from django.conf import settings
from django.core.exceptions import ValidationError
import shutil

# app_uploads/models.py
from django.utils.text import slugify
from unidecode import unidecode
from django.utils import timezone
import os

def upload_to_path(instance, filename):
    ext = filename.split('.')[-1]

    # Tipo do documento
    tipo_nome = instance.tipo.nome if instance.tipo else instance.tipo_custom or 'documento'
    tipo_nome = slugify(unidecode(tipo_nome))

    # Nome do proprietário
    prop = instance.proprietario_object
    nome_prop = "sem_nome"

    if hasattr(prop, 'user') and hasattr(prop.user, 'get_full_name'):
        nome_prop = prop.user.get_full_name()
    elif hasattr(prop, 'nome_fantasia'):
        nome_prop = prop.nome_fantasia
    elif hasattr(prop, 'nome_reparticao'):
        nome_prop = prop.nome_reparticao

    nome_prop = slugify(unidecode(nome_prop))

    # Timestamp para unicidade
    datahora = timezone.now().strftime('%Y%m%d_%H%M%S')

    # Caminho e nome final
    filename_final = f"{tipo_nome}_{nome_prop}_{datahora}.{ext}"
    return os.path.join('uploads_associados', nome_prop, filename_final)


# app_uploads
class TipoDocumentoUp(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(null=True, blank=True)

    def clean(self):
        # Confere se já existe um "nome" igual (case-insensitive), ignorando ele mesmo
        if TipoDocumentoUp.objects.filter(nome__iexact=self.nome).exclude(pk=self.pk).exists():
            raise ValidationError({'nome': 'Este nome de documento já está cadastrado.'})    

    def __str__(self):
        return self.nome

def validate_file_extension(value):
    valid_mime = ['application/pdf', 'image/jpeg', 'image/png']
    if value.file.content_type not in valid_mime:
        raise ValidationError("Tipo de arquivo não permitido.")
    
class UploadsDocs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    tipo = models.ForeignKey(TipoDocumentoUp, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_custom = models.CharField("Classificação Livre", max_length=100, blank=True)

    arquivo = models.FileField(
        upload_to=upload_to_path,
        validators=[validate_file_extension]
    )
    data_envio = models.DateTimeField(auto_now_add=True)
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # 🔗 Proprietário genérico (associado / associacao / reparticao)
    proprietario_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    proprietario_object_id = models.PositiveIntegerField()
    proprietario_object = GenericForeignKey('proprietario_content_type', 'proprietario_object_id')
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
                    

    def __str__(self):
        return f"{self.tipo or self.tipo_custom} - {self.proprietario_object}"

    class Meta:
        verbose_name = "Documento Enviado"
        verbose_name_plural = "Uploads de Documentos"
        ordering = ['-data_envio']
        
                        
    @property
    def ext(self):
        return os.path.splitext(self.arquivo.name)[-1].lower().replace('.', '')
