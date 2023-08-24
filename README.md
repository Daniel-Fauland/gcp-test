# Google Cloud Platform Tutorial

Various hands-on tutorials for differnt gcp services

## Cloud functions

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

Google Cloud Scheduler is a fully managed cron job service provided by Google Cloud Platform (GCP). It allows users to schedule and automate recurring tasks, such as calling HTTP/S endpoints or running Pub/Sub messages, using HTTP, HTTPS, or Pub/Sub as the target endpoint. It offers advanced features like job monitoring, retry mechanisms, time zone support, and task management through the console or API. With Cloud Scheduler, users can easily schedule and manage their tasks in the cloud, eliminating the need for manual intervention and improving operational efficiency.
