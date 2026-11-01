FROM node:20-slim

WORKDIR /app/backend

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 4500

# CMD ["node", "src/index.js"]
CMD ["npm", "run", "dev"]