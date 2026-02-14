# Simple static file server
FROM nginx:alpine
COPY generated /usr/share/nginx/html
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
