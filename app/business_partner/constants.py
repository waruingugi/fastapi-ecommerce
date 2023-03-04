from enum import Enum


class BusinessPartnerTypes(str, Enum):
    RETAILER = "RETAILER"
    INDIVIDUAL = "INDIVIDUAL"
    DISTRIBUTOR = "DISTRIBUTOR"
    MANUFACTURER = "MANUFACTURER"
    SHOP = "SHOP"


class BusinessPartnerVerificationStates(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
