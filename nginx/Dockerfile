FROM nginx:latest

# Удаляем стандартный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# Копируем свой конфиг
COPY nginx.conf /etc/nginx/conf.d/