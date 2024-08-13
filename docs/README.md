# Technical Decisions

## Introduction

The main purpose of this document is to describe the decisions regarding the tools and frameworks used to address the proposed technical test.

## Technology Stack

### Docker

The Docker containerization tool was used according to one of the test requirements. This tool allows developers to work with consistent development environments and also facilitates the deployment of the solution.

### Tornado

After some research on how to solve the problem, I found that the Tornado framework, along with Python's async module, was a well-known solution for this type of task. Tornado was chosen for its support of asynchronous programming and non-blocking I/O, which enhance performance by allowing the microservice to handle connections concurrently without blocking, thereby ensuring responsiveness. Additionally, this project provided my first opportunity to work with Tornado, and I used it to learn more about its capabilities.

### SQLite

The choice of SQLite was based on the context of the technical test, where there was a predefined number of city IDs to be queried. Additionally, its simplicity of use and integration into the project were considered suitable for the proposed solution of the test. However, in a production scenario, or even in development with more complex needs and larger volumes of data, replacing SQLite with a more robust database such as PostgreSQL or MySQL might be essential.

## Summary

In designing the solution for the proposed test, I focused on the principles of single responsibility and decoupling. The architecture was also crafted to facilitate unit testing. SQLite's simplicity was suitable for the technical test, while Tornado ensured responsiveness. For future scenarios with more complex requirements, exploring more robust databases or NoSQL options might be beneficial. Additionally, depending on the scenario, using a relational database might make it important to incorporate Django to simplify interaction with the database and avoid writing raw SQL code.

