import datetime
from typing import Self
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Enum,
    Numeric,
    Float,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.domain.entities.product import Product
from src.domain.entities.purchase import CustomerType, PaymentMethod, Purchase

Base = declarative_base()


def make_product_id_from_base(code, supplier, date):
    yyyymmdd = date.strftime("%Y%m%d")
    return f"{code}{supplier}{yyyymmdd}"


def make_product_id_from(product):
    return make_product_id_from_base(
        product.code, product.supplier, product.expiration_date
    )


def utc_now() -> datetime:
    return datetime.datetime.now(datetime.UTC)


class ProductModel(Base):
    __tablename__ = "product"

    id = Column(String(255), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    supplier = Column(String(100), nullable=False)
    inventory_quantity = Column(Integer, nullable=False)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    weight_in_kilograms = Column(Float, nullable=False)
    expiration_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), onupdate=utc_now)

    def __repr__(self):
        return f"<Product(id={self.id}, title={self.title}, code={self.code}, inventory_quantity={self.inventory_quantity})>"

    @classmethod
    def from_entity(cls, product: Product) -> Self:
        return cls(
            id=make_product_id_from(product),
            title=product.title,
            description=product.description,
            code=product.code,
            supplier=product.supplier,
            inventory_quantity=product.inventory_quantity,
            buy_price=product.buy_price,
            sell_price=product.sell_price,
            weight_in_kilograms=product.weight_in_kilograms,
            expiration_date=product.expiration_date,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

    def to_entity(self) -> Product:
        return Product(
            title=self.title,
            description=self.description,
            code=self.code,
            supplier=self.supplier,
            inventory_quantity=self.inventory_quantity,
            buy_price=self.buy_price,
            sell_price=self.sell_price,
            weight_in_kilograms=self.weight_in_kilograms,
            expiration_date=self.expiration_date,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class PurchaseModel(Base):
    __tablename__ = "purchase"

    id = Column(Integer, primary_key=True)
    product_id = Column(String(255), ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_date = Column(DateTime(timezone=True), default=utc_now)
    identification = Column(String(18), nullable=False)
    identification_type = Column(Enum(CustomerType), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    total_amount = Column(Numeric(10, 2))

    product = relationship("ProductModel", back_populates="purchases")

    def __repr__(self):
        return f"<Purchase(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, purchase_date={self.purchase_date}, identification={self.identification}, identification_type={self.identification_type}, payment_method={self.payment_method})>"

    @staticmethod
    def from_entity(entity: Purchase) -> Self:
        return PurchaseModel(
            product_id=entity.product_id,
            quantity=entity.quantity,
            purchase_date=entity.purchase_date,
            identification=entity.identification,
            identification_type=entity.identification_type,
            payment_method=entity.payment_method,
            total_amount=entity.total_amount,
        )

    def to_entity(self) -> Purchase:
        return Purchase(
            id=self.id,
            product_id=self.product_id,
            quantity=self.quantity,
            purchase_date=self.purchase_date,
            identification=self.identification,
            identification_type=self.identification_type,
            payment_method=self.payment_method,
            total_amount=self.total_amount,
        )
