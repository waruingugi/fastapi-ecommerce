from enum import Enum


class BusinessTypes(str, Enum):
    RETAILER = "RETAILER"
    INDIVIDUAL = "INDIVIDUAL"
    DISTRIBUTOR = "DISTRIBUTOR"
    MANUFACTURER = "MANUFACTURER"
    SHOP = "SHOP"


class BusinessVerificationStates(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
