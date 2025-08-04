# core/base_imports.py
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.conf import settings
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseRedirect,
    FileResponse,
    Http404,
)
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import io
from decimal import Decimal
from django import forms
import os
from django.db.models import Sum
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
from django.utils import timezone
from django.apps import apps
from django.db.models import Max
from django.contrib import messages
from django.views.decorators.http import require_POST
from app_accounts.models import CustomUser
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.contenttypes.models import ContentType

from googleapiclient.http import MediaFileUpload

from django.contrib.auth import get_user_model

from django.views.decorators.csrf import csrf_exempt

from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View
    )
from urllib.parse import urlencode
from datetime import datetime
from pdfrw import PdfReader, PdfWriter, PageMerge
from pdfrw.buildxobj import pagexobj
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageBreak
from io import BytesIO
from reportlab.lib.colors import lightgrey, grey
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import Color
