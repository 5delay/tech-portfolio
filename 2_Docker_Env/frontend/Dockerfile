FROM node:18.16

WORKDIR /app/frontend

COPY package*.json ./
RUN npm install --force

COPY . .

ENV HOST=0.0.0.0
ENV PORT=3800

EXPOSE 3800

CMD ["npm", "start"]