FROM ubuntu:latest
WORKDIR /app
COPY dist/app .
COPY artifacts artifacts
COPY static static
COPY templates templates
COPY uploaded uploaded
CMD ["./app"]
EXPOSE 5000