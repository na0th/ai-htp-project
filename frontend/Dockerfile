# FROM node:18.16

# # 필요한 파일을 이미지로 복사
# COPY package.json .

# WORKDIR .

# ADD . .
# RUN npm install

# EXPOSE 8080
# CMD ["npm", "run", "serve"]

FROM node:18.16

# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# build app for production with minification
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]