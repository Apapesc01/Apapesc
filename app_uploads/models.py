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


def upload_to_path(instance, filename):
    from django.contrib.contenttypes.models import ContentType

    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"  # Nome único só pra não quebrar
    datahora = timezone.now().strftime('%Y%m%d_%H%M%S')

    tipo_nome = instance.tipo.nome if hasattr(instance, 'tipo') and instance.tipo else getattr(instance, 'tipo_custom', None) or 'documento'
    tipo_nome = slugify(unidecode(tipo_nome))

    nome_prop = "sem_nome"
    try:
        ct = instance.proprietario_content_type
        model_class = ct.model_class()
        prop = model_class.objects.get(pk=instance.proprietario_object_id)

        if hasattr(prop, 'get_full_name'):
            nome_prop = prop.get_full_name()
        elif hasattr(prop, 'nome_fantasia'):
            nome_prop = prop.nome_fantasia
        elif hasattr(prop, 'nome_reparticao'):
            nome_prop = prop.nome_reparticao
    except:
        pass

    nome_prop = slugify(unidecode(nome_prop))

    new_filename = f"{tipo_nome}_{nome_prop}_{datahora}.{ext}"
    return os.path.join('uploads_associados', 'temp', filename)


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
        is_new = self._state.adding
        super().save(*args, **kwargs)  # Salva primeiro

        if is_new and self.arquivo and self.proprietario_object:
            try:
                ext = self.arquivo.name.split('.')[-1]
                datahora = timezone.now().strftime('%Y%m%d_%H%M%S')

                # Tipo do documento
                tipo_nome = self.tipo.nome if self.tipo else self.tipo_custom or 'documento'
                tipo_nome = slugify(unidecode(tipo_nome))

                # Nome do proprietário
                prop = self.proprietario_object
                nome_prop = "sem_nome"

                if hasattr(prop, 'user') and hasattr(prop.user, 'get_full_name'):
                    nome_prop = prop.user.get_full_name()
                elif hasattr(prop, 'nome_fantasia'):
                    nome_prop = prop.nome_fantasia
                elif hasattr(prop, 'nome_reparticao'):
                    nome_prop = prop.nome_reparticao

                nome_prop = slugify(unidecode(nome_prop))

                # Novo caminho
                new_filename = f"{tipo_nome}_{nome_prop}_{datahora}.{ext}"
                new_dir = os.path.join('uploads_associados', nome_prop)
                new_path = os.path.join(new_dir, new_filename)
                full_old_path = self.arquivo.path
                full_new_path = os.path.join(settings.MEDIA_ROOT, new_path)

                # Cria diretório se necessário
                os.makedirs(os.path.dirname(full_new_path), exist_ok=True)

                # Move o arquivo
                shutil.move(full_old_path, full_new_path)

                # Atualiza o path do model
                self.arquivo.name = new_path
                super().save(update_fields=['arquivo'])

            except Exception as e:
                print(f"❌ Erro ao renomear e mover arquivo: {e}")
                

    def __str__(self):
        return f"{self.tipo or self.tipo_custom} - {self.proprietario_object}"

    class Meta:
        verbose_name = "Documento Enviado"
        verbose_name_plural = "Uploads de Documentos"
        ordering = ['-data_envio']
        
                        
    @property
    def ext(self):
        return os.path.splitext(self.arquivo.name)[-1].lower().replace('.', '')
