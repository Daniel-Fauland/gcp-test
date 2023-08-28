# Google Cloud Platform Tutorial

Various hands-on tutorials for different gcp services

## Cloud Functions

Cloud Functions tutorial can be found [here](./cloud_functions/README.md).

[Google Cloud Functions](https://cloud.google.com/functions/docs) is a serverless compute service offered by Google Cloud Platform (GCP) that enables developers to build, deploy, and run event-driven functions without the need to manage the underlying infrastructure.

**Capabilities:**

- Event-Driven Execution: Cloud Functions are triggered by various events, such as HTTP requests, Cloud Storage changes, Pub/Sub messages, and more.
- Scalability: Cloud Functions automatically scale based on the incoming workload, ensuring optimal resource utilization without manual intervention.
- Pay-as-You-Go Pricing: You are charged based on the number of invocations and the time your code runs, allowing for cost savings as you only pay for actual usage.
- Support for Multiple Languages: Cloud Functions supports multiple programming languages, including Node.js, Python, Go, and more, giving developers flexibility in choosing the language they're comfortable with.
- Easy Integration: Cloud Functions can be easily integrated with other Google Cloud services, allowing you to create complex workflows and applications.
- Managed Infrastructure: GCP handles the operational aspects such as provisioning, scaling, and maintenance, freeing developers from managing infrastructure.

**Pros:**

- Serverless Architecture: Developers can focus on writing code and building applications without worrying about server management, scaling, or infrastructure maintenance.
  Rapid Development: Cloud Functions enable quick development and deployment of small, single-purpose functions, which can speed up the development cycle.
- Auto-Scaling: Functions automatically scale up or down based on demand, ensuring optimal performance without manual intervention.
- Event-Driven: Cloud Functions are well-suited for event-driven scenarios like real-time data processing, webhooks, and automated tasks.
- Cost Efficiency: Pay-as-you-go pricing means you only pay for actual usage, making it cost-effective for sporadically used functions.
- Integration with GCP Services: Seamless integration with other Google Cloud services allows you to build comprehensive applications without worrying about compatibility.

**Cons:**

- Limited Execution Time: Cloud Functions have a maximum execution time limit (e.g., 9 minutes using v1 or 60 minutes using v2), which may restrict their use for tasks requiring longer processing times.
- Cold Start Latency: Functions may experience a delay known as "cold start" when they're invoked for the first time or after a period of inactivity. This can impact latency-sensitive applications.
- Stateless Nature: Cloud Functions are designed to be stateless, which can make handling stateful operations more complex.
- Limited Customization: While Cloud Functions abstract away infrastructure management, it also limits customization options for the underlying environment.
- Vendor Lock-In: Developing extensively on Cloud Functions might lead to vendor lock-in, where migrating to a different cloud provider could be challenging.

In summary, Google Cloud Functions offers a serverless and event-driven architecture that simplifies development and deployment of small functions. It's suitable for event-driven workloads and scenarios where rapid development and scalability are priorities. However, developers should be aware of its execution time limitations, cold start latency, and potential vendor lock-in.

## Cloud scheduler

Cloud scheduler is part of the cloud fcuntions tutorial which can be found [here](./cloud_functions/README.md).

Google Cloud Scheduler is a fully managed cron job service provided by Google Cloud Platform (GCP). It allows users to schedule and automate recurring tasks, such as calling HTTP/S endpoints or running Pub/Sub messages, using HTTP, HTTPS, or Pub/Sub as the target endpoint. It offers advanced features like job monitoring, retry mechanisms, time zone support, and task management through the console or API. With Cloud Scheduler, users can easily schedule and manage their tasks in the cloud, eliminating the need for manual intervention and improving operational efficiency.

## IAM & Admin

IAM tutorial can be found [here](./iam/README.md).

Google Cloud Identity and Access Management (IAM) is a service provided by Google Cloud Platform (GCP) that allows you to manage and control access to your cloud resources. It's a fundamental aspect of GCP's security and access control framework, enabling you to define who has what level of access to your resources and services within your Google Cloud projects.

IAM provides the following key features:

- Access Control: IAM allows you to grant and manage permissions for users, groups, and service accounts at a granular level. You can assign predefined roles (like Viewer, Editor, and Owner) or custom roles that you define to control what actions users can perform on specific resources.
- Resource Hierarchy: GCP resources are organized in a hierarchical structure, such as projects, folders, and resources within projects. IAM permissions can be granted at different levels of this hierarchy, ensuring that access is controlled at the appropriate level.
- Principle of Least Privilege: IAM follows the principle of least privilege, meaning that users and services are only granted the minimum necessary permissions to perform their tasks. This helps reduce the risk of accidental or intentional misuse of privileges.
- Service Accounts: IAM supports service accounts, which are identities used by applications and services to access GCP resources. Service accounts can be granted permissions just like human users.
- Audit and Monitoring: IAM provides audit logs that allow you to track who did what, when, and where in your GCP environment. This is crucial for security and compliance purposes.
- Identity Federation: You can integrate IAM with external identity providers, allowing users to log in using their existing credentials.

In summary, GCP IAM & Admin is a vital tool for securing your cloud environment, managing access to resources, and maintaining a strong security posture for your Google Cloud Platform projects. It helps you ensure that only authorized users and services can interact with your cloud resources, enhancing both security and operational efficiency.

## Google BigQuery Overview

BigQuery tutorial can be found [here](./bigquery/README.md).

Google BigQuery is a fully managed, serverless, and scalable data warehousing and analytics platform provided by Google Cloud Platform (GCP). It excels in handling large datasets and executing fast SQL-like queries through its distributed architecture.

**Capabilities:**

1. **Scalability:** BigQuery scales horizontally to handle massive datasets efficiently, making it suitable for petabyte-scale data.
2. **Serverless:** Fully managed by Google, eliminating the need for infrastructure provisioning, maintenance, and scaling tasks.
3. **Fast Query Performance:** Utilizes columnar storage and distributed processing for rapid query execution, especially for analytical tasks.
4. **SQL-Like Query Language:** Offers a familiar SQL-like query language for easy adoption by SQL users.
5. **Automatic Optimization:** Optimizes query execution through techniques like parallelism, data pruning, and caching.
6. **Real-Time Analysis:** Supports real-time analysis with features like streaming inserts and table decorators.
7. **Data Warehousing:** Serves as a central hub for consolidating and analyzing data from diverse sources.
8. **Integration with GCP Services:** Seamlessly integrates with other GCP services, including visualization and machine learning tools.

**Advantages over Traditional SQL Databases:**

1. **Scalability:** Handles larger datasets and complex queries effortlessly compared to traditional SQL databases.
2. **Performance:** Offers superior query performance due to distributed architecture and columnar storage.
3. **Serverless Model:** Eliminates manual infrastructure management, allowing focus on data analysis.
4. **Cost Efficiency:** Pay-as-you-go pricing based on processed data, cost-effective for sporadic workloads.
5. **Schema Flexibility:** Supports schema-on-read, accommodating semi-structured and nested data.
6. **Ease of Use:** Familiar SQL-like language caters to analysts and data scientists with varying expertise.
7. **Data Sharing:** Facilitates easy sharing of datasets and queries for collaboration within and outside organizations.

In summary, Google BigQuery excels in scalability, performance, serverless operation, and user-friendliness for analytical and data warehousing tasks. However, the choice between BigQuery and traditional SQL databases depends on specific use cases and infrastructure considerations.
