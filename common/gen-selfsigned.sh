#!/bin/bash
#
# Generate an independent, self-signed keypair that isn't related to a certificate authority.

# Arguments:
# - NAME
# - LIFETIME in days
generate_selfsigned()
{
  local NAME=$1
  local LIFETIME=$2

  info "Generating a self-signed keypair for: <${NAME}>"

  openssl req -x509 -newkey rsa:2048 -days ${LIFETIME} -nodes -batch \
    -keyout /certificates/${NAME}-key.pem \
    -out /certificates/${NAME}-cert.pem

  success "Self-signed keypair generated for: <${NAME}>"
}
