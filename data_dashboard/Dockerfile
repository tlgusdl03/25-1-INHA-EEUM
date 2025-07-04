# Build stage
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

ARG VITE_KAKAO_MAP_API_KEY
ARG VITE_API1_BASE_URL
ARG VITE_API2_BASE_URL

RUN echo "VITE_KAKAO_MAP_API_KEY=$VITE_KAKAO_MAP_API_KEY" >> .env.production \
 && echo "VITE_API1_BASE_URL=$VITE_API1_BASE_URL" >> .env.production \
 && echo "VITE_API2_BASE_URL=$VITE_API2_BASE_URL" >> .env.production

RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html 
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

