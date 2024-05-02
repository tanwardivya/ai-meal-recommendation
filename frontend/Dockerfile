FROM node:20.11.0

WORKDIR /app

COPY package.json .

RUN npm config set legacy-peer-deps true

RUN npm install

COPY . .

EXPOSE 8080

CMD [ "npm", "run", "preview" ]