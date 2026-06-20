from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base


class PackagingMethod(str, enum.Enum):
    WOODEN_CRATE = "wooden_crate"
    CARTON = "carton"
    CONTAINER_BULK = "container_bulk"
    PALLET_WRAP = "pallet_wrap"


class BatchMarkStatus(str, enum.Enum):
    OBSERVE = "observe"
    RECALL = "recall"
    REPAINT = "repaint"
    RELEASE = "release"


class ComplaintType(str, enum.Enum):
    BUBBLING = "bubbling"
    PEELING = "peeling"
    DISCOLORATION = "discoloration"
    CRACKING = "cracking"
    OTHER = "other"


class CoatingFormula(Base):
    __tablename__ = "coating_formulas"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    primer = Column(String(200), nullable=False)
    topcoat = Column(String(200), nullable=False)
    clearcoat = Column(String(200))
    hardener_ratio = Column(String(50), nullable=False)
    supplier = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    batches = relationship("VehicleBatch", back_populates="formula")


class SprayLine(Base):
    __tablename__ = "spray_lines"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    location = Column(String(200))
    description = Column(Text)

    batches = relationship("VehicleBatch", back_populates="spray_line")


class DestinationClimate(Base):
    __tablename__ = "destination_climates"

    id = Column(Integer, primary_key=True, index=True)
    port_code = Column(String(50), unique=True, index=True, nullable=False)
    port_name = Column(String(200), nullable=False)
    country = Column(String(100), nullable=False)
    region = Column(String(100))
    avg_high_temp_c = Column(Float, nullable=False)
    avg_low_temp_c = Column(Float, nullable=False)
    avg_relative_humidity_pct = Column(Float, nullable=False)
    monsoon_season = Column(String(100))
    climate_zone = Column(String(100))

    orders = relationship("ExportOrder", back_populates="climate")


class VehicleBatch(Base):
    __tablename__ = "vehicle_batches"

    id = Column(Integer, primary_key=True, index=True)
    batch_code = Column(String(50), unique=True, index=True, nullable=False)
    model = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    formula_id = Column(Integer, ForeignKey("coating_formulas.id"), nullable=False)
    spray_line_id = Column(Integer, ForeignKey("spray_lines.id"), nullable=False)
    cure_temperature_c = Column(Float, nullable=False)
    cure_duration_min = Column(Float, nullable=False)
    air_dry_duration_hours = Column(Float, nullable=False)
    production_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    formula = relationship("CoatingFormula", back_populates="batches")
    spray_line = relationship("SprayLine", back_populates="batches")
    orders = relationship("ExportOrder", back_populates="batch")
    inspections = relationship("InspectionRecord", back_populates="batch")
    marks = relationship("BatchMark", back_populates="batch")


class ExportOrder(Base):
    __tablename__ = "export_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, index=True, nullable=False)
    batch_id = Column(Integer, ForeignKey("vehicle_batches.id"), nullable=False)
    climate_id = Column(Integer, ForeignKey("destination_climates.id"), nullable=False)
    packaging_method = Column(Enum(PackagingMethod), nullable=False)
    shipping_route = Column(String(200), nullable=False)
    shipment_date = Column(DateTime(timezone=True), nullable=False)
    estimated_arrival = Column(DateTime(timezone=True))
    actual_arrival = Column(DateTime(timezone=True))
    customer = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    batch = relationship("VehicleBatch", back_populates="orders")
    climate = relationship("DestinationClimate", back_populates="orders")
    complaints = relationship("CustomerComplaint", back_populates="order")


class InspectionRecord(Base):
    __tablename__ = "inspection_records"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("vehicle_batches.id"), nullable=False)
    inspector = Column(String(100), nullable=False)
    inspection_date = Column(DateTime(timezone=True), nullable=False)
    sample_size = Column(Integer, nullable=False)
    adhesion_grade = Column(String(20), nullable=False)
    color_delta_e = Column(Float, nullable=False)
    film_thickness_um = Column(Float, nullable=False)
    humidity_resistance_hours = Column(Float, nullable=False)
    passed = Column(Integer, nullable=False)
    failed = Column(Integer, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    batch = relationship("VehicleBatch", back_populates="inspections")


class BatchMark(Base):
    __tablename__ = "batch_marks"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("vehicle_batches.id"), nullable=False)
    status = Column(Enum(BatchMarkStatus), nullable=False)
    marked_by = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    marked_at = Column(DateTime(timezone=True), server_default=func.now())

    batch = relationship("VehicleBatch", back_populates="marks")


class CustomerComplaint(Base):
    __tablename__ = "customer_complaints"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("export_orders.id"), nullable=False)
    complaint_type = Column(Enum(ComplaintType), nullable=False)
    vehicle_count = Column(Integer, nullable=False)
    severity = Column(String(50), nullable=False)
    reported_at = Column(DateTime(timezone=True), nullable=False)
    description = Column(Text, nullable=False)
    resolution = Column(Text)
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("ExportOrder", back_populates="complaints")
