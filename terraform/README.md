# Terraform

This section will cover a few hands-on tutorials using Terraform.

## Prerequisites

To get started make sure you have [terraform](https://www.terraform.io) installed on your local machine.
You can check your installation by running the following command in terminal:

```shell
terraform -v
```

Then create a new [service account](../iam/README.md#create-service-account) on GCP which has the global _Editor_ role so that terraform is able to create and manage resources. Now download the [credentials json](../iam/README.md#create-credentials-json-file) file of that service account so that terraform can be executed on your local machine.

## 1. Create VM instance

In this example you will create a virtual machine instance on GCP using terraform. VM Instances are part of the _Compute Engine_ resource which gives you the possibility to create and manage virtualized hardware resources.

1. Start by creating a terraform script (usually called _main.tf_). The very first thing to do in every terraform script is setting the provider and project.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   provider "<cloud-provider>" {
   credentials = file("path/to/your/credentials.json")
   project     = "<project-id>"
   region      = "<your-region>"
   }
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   provider "google" {
   credentials = file("credentials.json")
   project     = "propane-nomad-396712"
   region      = "europe-west3"
   }
   ```

   </details>

2. Then you can add your resources that should be created. In this case it will be a vm instance.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   resource "<provider>_<product>-<resource>" "<tf-resource-name>" {
   name         = "<name>"
   machine_type = "<machine-type>"
   zone         = "<your-zone>"

   boot_disk {
       initialize_params {
       image = "<image>"
       }
   }

   network_interface {
       network = "default"
       access_config {}
   }
   }
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   resource "google_compute_instance" "vm_instance" {
   name                      = "my-vm"
   machine_type              = "e2-small"
   zone                      = "europe-west3-c"
   allow_stopping_for_update = true

   boot_disk {
       initialize_params {
       image = "debian-cloud/debian-11"
       }
   }

   network_interface {
       network = "default"
       access_config {}
   }
   }
   ```

   </details>

   If you set the _allow_stopping_for_update_ flag to _true_ you will allow the vm to automatically stop in order to install updates. If you need uninterrupted uptime on your vm you can set this flag to _false_ but it's recommended to have this feature on.
   The image specifies the operating system used by the VM. You can get a list of all available images via gcloud:

   ```shell
   gcloud compute images list
   ```

   The network part lets you specify the network interface used as well as any kind access configuration. The access_config must be scpecified even if it's empty to ensure the VM is actually reachable via the internet.

3. Once the terraform script is completed open a terminal and navigate to the directory of the _main.tf_ file. Now initialize terraform.

   ```shell
   terraform init
   ```

4. You can check which resources will be created, modified or deleted including all parametes (even those not specified in the script) before deploying it to the cloud.

   ```shell
   terraform plan
   ```

5. If everything looks fine deploy the defined resources on the cloud and confirm by typing _yes_ in the terminal.

   ```shell
   terraform apply
   ```

   **Note:** A VM costs money just by running even if there is no traffic/data on it. Therefore if it's not in use you can stop the VM to prevent being charged. You don't need to delete & redeploy the vm every time.

6. After creating resources terraform will create a "terraform.tfstate" file which will basically function as a documentation for terraform which resources are in which specific state. Such a file is important if you plan to update resources that already exist as any kind of change will fail if you don't have the tfstate for your resources.

## 2. Create (sub)network and update VM instance

This section shows how you can update the VM instance deployed earlier by creating your own (sub)network instead of using the default one. The default network creates a subnetwork for each region gcp offers which is not necessary.

1. Create a new resource which will use the network category. There you can turn off the default behaviour of automatically creating subnetworks.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   resource "<provider>_<product>_network" "<tf-network-name>" {
   name                    = "<network-name>"
   auto_create_subnetworks = false
   }
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   resource "google_compute_network" "terraform_network" {
   name                    = "terraform-network"
   auto_create_subnetworks = false
   }
   ```

   </details>

2. Then create your own subnetwork and assign it to your network.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   resource "<provider>_<product>_subnetwork" "<tf-subnetwork-name>" {
   name          = "<subnetwork-name>"
   ip_cidr_range = "X.X.X.X/X"
   region        = "<your-region>"
   network       = <provider>_<product>_network.<tf-network-name>.id
   }
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   resource "google_compute_subnetwork" "terraform_subnet" {
   name          = "terraform-subnetwork"
   ip_cidr_range = "10.20.0.0/16"
   region        = "europe-west3"
   network       = google_compute_network.terraform_network.id
   }
   ```

   </details>

3. Use the new network instead of the default network for the VM instance.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   resource "<provider>_<product>_<resource>" "<tf-resource-name>" {
   # ...

   network_interface {
      network    = <provider>_<product>_network.<tf-network-name>.self_link
      subnetwork = <provider>_<product>_subnetwork.<tf-subnetwork-name>.self_link
      access_config {}
   }
   }
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   resource "google_compute_instance" "vm_instance" {
   # ...

   network_interface {
      network    = google_compute_network.terraform_network.self_link
      subnetwork = google_compute_subnetwork.terraform_subnet.self_link
      access_config {}
   }
   }
   ```

   </details>

4. If you don't have the _terraform.tfstate_ file the update will fail. Therefore you need to get the state of your resource for each resource you plan to change indivudally.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   terraform import <provider>_<product>_<resource>.<name> <id>
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   terraform import google_compute_instance.vm_instance projects/propane-nomad-396712/zones/europe-west3-c/instances/my-vm
   ```

   </details>

5. Update the VM instance.

   ```shell
   terraform init  # Only needed if not initialized yet
   ```

   ```shell
   terraform plan
   ```

   ```shell
   terraform apply
   ```

6. The VM instance should be updated after a few seconds and now have the newly created (sub)network assigned to it. You can check the networks list with gcloud for example.

   ```shell
   gcloud compute networks list
   ```

   **Note:** Some changes like network are _non-destructive_ which means that the resource can be updated in-place. However other changes like hardware configuration or os image are _destructive_ changes and will delete and redeploy the resource rather than updating it.

## 3. Using input variables

In Terraform, input variables allow you to parameterize your configuration and define values that can be used throughout your code. Input variables enable you to make your configuration more flexible and reusable by allowing you to pass values dynamically when running Terraform commands. You can define and use variables by following these steps.

1. Create a new .tf file (e.g. _variables.tf_)
2. Define your variables. You can set default values so that you don't need to specify them later on in your terminal.
   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   variable "<variable-name>" {
   default = "<default-value>"
   }
   variable "<variable-name2>" {}
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   variable "project" {
   default = "propane-nomad-396712"
   }
   variable "credentials_file" {
   default = "../credentials.json"
   }
   variable "region" {
   default = "europe-west3"
   }

   variable "machine_type" {}
   ```

   </details>

3. Now use the variables in your main.tf file.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   provider "<provider-name>" {
   credentials = file(var.<variable-name>)
   project     = var.<variable-name2>
   region      = "<your-region>"
   }
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   provider "google" {
   credentials = file(var.credentials_file)
   project     = var.project
   region      = var.region
   }

   resource "google_compute_instance" "vm_instance" {
   name                      = "my-vm"
   machine_type              = var.machine_type
   }
   ```

   </details>

4. You can either pass all variable values via the cli or via a _terraform.tfvars_ file. You don't need to spefiy the variables that have a default value but you can override these defaults in the cli or tfvars file if you want to. The _terraform.tfvars_ file will be auto-detected so you don't need to pass any arguments to the cli.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   terraform plan -var <variable-name>="<variable-value>" -var <variable-name2>="<variable-value2>"
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   terraform plan -var machine="e2-small" -var project="propane-nomad-396712"
   ```

   </details>

5. Deploy the resources. Make sure you also include the arguments when executing terraform apply if you don't have a _terraform.tfvars_ file.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   terraform apply -var <variable-name>="<variable-value>" -var <variable-name2>="<variable-value2>"
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   terraform apply -var machine="e2-small" -var project="propane-nomad-396712"
   ```

   </details>

## Recreate and delete resources using taint and destroy

- Terraform taint is a command in Terraform, an infrastructure as code tool, that marks a resource as tainted. Tainting a resource means that Terraform considers it to be potentially corrupted or incorrect. When a resource is tainted, it will be destroyed and recreated on the next apply, even if no changes were made to its configuration. This can be useful in cases where a resource is in an unexpected state and needs to be rebuilt. It will only be executed **after** you **apply** your build.

   <details>
   <summary>Show general code snippet:</summary>

  ```shell
  terraform taint <provider>_<product>_<resource>.<name>
  ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

  ```shell
  terraform taint google_compute_instance.vm_instance
  ```

   </details>

- Destroy on the other hand lets you delete delete resources created by terraform completely. However it can only destroy resources that were created by terraform in the first place and nothing else. It will automatically destroy resources in the correct order (like subnetwork before network) to prevent any errors in the cloud. You can either destroy all resources at once or a specific resource.

  ```shell
  terraform destroy
  ```

   <details>
   <summary>Show general code snippet:</summary>

  ```shell
  terraform destroy -target=<provider>_<product>_<resource>.<name>
  ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

  ```shell
  terraform destroy -target=google_compute_instance.vm_instance
  ```

   </details>

  **Note**: Even if you only want to destroy a specific resource terraform will always delete all dependencies as well.
