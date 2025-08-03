# Notas de Instalação

# Em Localhost
Criar/rodar scripts/container para grupos:
docker-compose exec web python manage.py create_groups

Criar/rodar scripts/container para tipos doc:
docker-compose exec web python manage.py create_tipo_docs

sudo docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
# --------------------------

# Em Produção
Criar/rodar scripts/container para grupos:
sudo docker compose -f docker-compose.prod.yml exec web python manage.py create_groups

Criar/rodar scripts/container para tipos doc:
sudo docker compose -f docker-compose.prod.yml exec web python manage.py create_tipo_docs

sudo docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
# --------------------------------


# -------------------------------------


