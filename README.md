# OTPService: One-Time Password & Messaging Service

OTPService is a service that provides secure one-time password (OTP) generation and delivery functionalities. It also offers messaging capabilities through SMS and Email channels.

## Features

### OTP Generation

- Configurable OTP length and validity period.

### Delivery Channels  

- Secure and reliable OTP delivery via SMS and Email.
- Customizable message templates for OTP and additional informational messages.

### Scalability

- esigned to handle high volumes of OTP requests efficiently.
- Integrates seamlessly with your existing applications.

### Security

- OTPs are generated and stored securely using industry-standard practices.
- Communication channels utilize secure protocols for data transmission.

### Customization

- Configure branding elements within message templates.
- Integrate with your user management system for user authentication.

## Benefits

- Enhance user registration and login security with robust OTP generation.
- Provide a convenient and familiar way for users to receive OTPs via SMS and Email.
- Improve scalability for high-demand OTP services.
- Ensure secure communication with industry-standard security protocols.

## Setup Guide using Docker Compose

This guide outlines setting up OTPService using Docker Compose. It requires Docker and Docker Compose to be installed on your system.

### Prerequisites

- Docker Engine (<https://docs.docker.com/engine/install/>)
- Docker Compose (<https://docs.docker.com/compose/install/>)
- SNMP Account (For emails)
- SMPP Account (For SMS)

### Clone project from GitHub

```bash
git clone https://github.com/SLTDigitalLab/OTPService.git
cd OTPService
```

### Setup `.env` file

Rename the .env.sample file to .env

```env
SMPP_HOST=<string>
SMPP_PORT=<number>
SMPP_SYS_ID=<string>
SMPP_PASSWORD=<string>

SNMP_SSL= <boolean>
SNMP_HOST=<string>
SNMP_PORT=<boolean>
SNMP_SENDER_EMAIL=<string>
SNMP_PASSWORD=<string>
```

### Start the services

```bash
docker compose up --build -d
```

Navigate to localhost:8000/api/docs to access the documentation.
