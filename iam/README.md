# IAM (Identity Access Management)

This section will cover a few tutorials regarding IAM.

Contents:

- [Overview between different IAM entities](#overview-between-different-iam-entities)
- [Create service account](#create-service-account)
- [Grant permissions/roles to an existing service account](#grant-permissionsroles-to-an-existing-service-account)
- [View roles granted to an existing service account](#view-roles-granted-to-an-existing-service-account)

## Overview between different IAM entities

- Permissions:
  Permissions are individual actions that define what a user, service account, or group is allowed to do with a specific resource. Examples include read, write, delete, and create. Permissions are combined to define the level of access that a user or service account has for a particular resource.
- Roles:
  Roles are collections of permissions. They define a set of actions that can be performed on resources. Google Cloud provides both predefined roles (such as Viewer, Editor, and Owner) and custom roles that you can create. Roles make it easier to manage access by grouping related permissions together.
- Service Accounts:
  Service accounts are special identities used by applications and services to authenticate and interact with Google Cloud resources. They can be assigned roles that determine what actions the service account can perform. Service accounts are commonly used to enable applications to access GCP resources securely without using personal user credentials.
- Users:
  Users are individual people who have Google Cloud accounts and can interact with GCP resources. Users can be assigned roles that grant them specific permissions on resources. These roles determine what the user is allowed to do within the GCP environment.
- Groups:
  Groups are collections of users. Instead of managing permissions and roles for each user individually, you can assign roles to groups. This simplifies access management, especially in large organizations, by granting access to multiple users through a single group assignment.

In summary, permissions define specific actions, roles group together permissions, service accounts are used by applications to access resources securely, users are individual people with GCP accounts, and groups make it easier to manage access for multiple users collectively. These concepts in Google Cloud IAM work together to provide a robust access control framework that ensures security, compliance, and effective resource management.

## Create service account

In order to create a service account follow these steps:

1. Go to IAM & ADMIN in GCP
2. Go to _roles_ an check if a role with your desired permissions does already exist
3. If no such role does exist create a new role and add all permissions needed
4. Go to _Service Accounts_ and create a new service account.
5. Choose a name (e.g. _cloud-scheduler_) and give a description what this service account is being used for
6. Grant this service account access to project by adding one or multiple roles (e.g. _Cloud Functions Invoker_)
7. Optional: You can grant users or groups the permission to deploy services using this service account

## Grant permissions/roles to an existing service account

The easiest way to grant permissions to a service account is assigning it a role via gcloud.
General code snippet:

```shell
gcloud <gcp-service> add-iam-policy-binding <resource-name> \
  --member="serviceAccount:<service-acc-name>@<project-id>.iam.gserviceaccount.com" \
  --role="roles/<gcp-resource>.<type>"
```

Example code snippet:

```shell
gcloud functions add-iam-policy-binding func-pubsub-subscriber \
  --member="serviceAccount:cloud-function-a@propane-nomad-396712.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.invoker"
```

## View roles granted to an existing service account

In order to check all given roles to a service account the fastet way is to use gcloud:

General code snippet:

```shell
gcloud projects get-iam-policy <project-id> \
--flatten="bindings[].members" \
--format="table(bindings.role)" \
--filter="bindings.members:serviceAccount:<service-account>@<project-id>.iam.gserviceaccount.com"
```

Example code snippet:

```shell
gcloud projects get-iam-policy propane-nomad-396712 \
--flatten="bindings[].members" \
--format="table(bindings.role)" \
--filter="bindings.members:serviceAccount:sa-func-b@propane-nomad-396712.iam.gserviceaccount.com"
```
