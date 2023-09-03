variable "project" {
  type        = string
  description = "The project ID"
  default     = "propane-nomad-396712"
}
variable "credentials_file" {
  type        = string
  description = "The path to the credentials file used for authentication"
  default     = "../credentials.json"
}
variable "region" {
  default = "europe-west3"
}

variable "vm_instance" {
  type        = tuple([string, string, bool])
  description = "Define machine_type, zone and allow_stopping_for_update"
  default     = ["e2-small", "europe-west3-c", true]
}

variable "vm_disk" {
  type = object({
    image = string
    size  = number
  })
  description = "Define paramters for the vm boot disk"
  default = {
    image = "debian-cloud/debian-11"
    size  = "10" # 10 GB boot disk
  }
  validation {
    condition     = length(var.vm_disk.image) > 3
    error_message = "Not a valid boot image."
  }
}


variable "example1" {
  type        = string
  description = "String variable"
  default     = "abc"
}

variable "example2" {
  type        = number
  description = "Number variable"
  default     = 123 # Same as "123"
}

variable "example3" {
  type        = any
  description = "Can hold any value"
  default     = "123" # or "abc" or true
}

variable "example4" {
  type        = list(any)
  description = "List variable that can hold any value"
  default     = [1, 2, "abc", true]
}

variable "example5" {
  type        = list(string)
  description = "List variable that can only hold string values"
  default     = [1, 2, "abc", true] # Everything will be converted to string
}

variable "example6" {
  type        = set(string)
  description = "Set variable"
  default     = [1, 2, 2, true] # set does not have order and does not care about repetition --> ["1", "2", "true"]
}

variable "example7" {
  type        = tuple([string, number, bool])
  description = "Tuple variable"
  default     = ["2.5", 3, "true"] # Will be converted to --> [2.5, 3, true]
}

variable "example8" {
  type        = map(string)
  description = "Map variable (can only hold the same data types)"
  default = {
    var1 = "value1"
    var2 = "value2"
    var3 = "value3"
  }
}

variable "example9" {
  type = object({
    var4 = string
    var5 = bool
    var6 = number
    var7 = object({
      var7_1 = string
      var7_2 = any
    })
  })
  description = "Object variable (can hold all data types and can be nested)"
  default = {
    var4 = "value4"
    var5 = true
    var6 = 2.5
    var7 = {
      var7_1 = "abc"
      var7_2 = true
    }
  }
}




