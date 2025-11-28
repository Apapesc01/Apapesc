FROM nginx:alpine

RUN apk update && \
    apk add --no-cache certbot certbot-nginx openssl

COPY nginx.conf /etc/nginx/nginx.conf
