FROM golang:1.23.2-alpine AS base

RUN go install github.com/go-delve/delve/cmd/dlv@latest

WORKDIR /build
COPY go.mod .
COPY go.sum .
RUN go mod download

COPY cmd cmd
COPY internal internal

FROM base AS builder

WORKDIR cmd/petstore-code
RUN go build -o /build/petstore-code .

FROM base AS debug
WORKDIR cmd/petstore-code
RUN go build -gcflags="all=-N -l" -o /build/petstore-code .

ENV DEBUG_PORT=2345
EXPOSE $DEBUG_PORT
ENTRYPOINT /go/bin/dlv --listen=:$DEBUG_PORT --headless=true --api-version=2 --accept-multiclient exec /build/petstore-code

FROM alpine AS run
COPY --from=builder /build/petstore-code /
USER 1000
CMD ["/petstore-code"]

