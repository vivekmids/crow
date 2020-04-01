FROM node:12-buster AS build
RUN npm install -g gatsby-cli
WORKDIR /app
ADD . ./
RUN npm install
RUN gatsby build

FROM gatsbyjs/gatsby
COPY --from=build /app/public /pub
