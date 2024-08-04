# Image Data Processing
This system is designed to process CSV files containing product information and image URLs.
It compresses the images asynchronously and generates a new CSV with updated image URLs.

## Database Schema
The System includes segregated components for a robust architechture.

Please checkout the in depth schema and overview of the system - [Database Schema Document](/Docs/Database.md).

## Low Level Design
The System includes multiple components like:
- Database (DB),
- Endpoints,
- Background Tasks and workers, etc.

Please checkout the complete LLD and overview of the system - [LLD Document](/Docs/LLD.md).

## API Endpoints
The Endpoints role and functions are discussed int the LLD Document's [API Endpoint Section](/Docs/LLD.md#21-api-endpoints).

Please see for the behaviour with sample requests, response, curl and PostMan Collection - [API Endpoints](/Docs/Endpoints.md).