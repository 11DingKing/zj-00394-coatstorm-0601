from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
import enum


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


class RiskCategory(str, enum.Enum):
    FORMULA = "formula"
    SPRAY_LINE = "spray_line"
    CLIMATE = "climate"


class ReinspectionStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CoatingFormulaBase(BaseModel):
    code: str
    name: str
    primer: str
    topcoat: str
    clearcoat: Optional[str] = None
    hardener_ratio: str
    supplier: Optional[str] = None


class CoatingFormulaCreate(CoatingFormulaBase):
    pass


class CoatingFormula(CoatingFormulaBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SprayLineBase(BaseModel):
    code: str
    name: str
    location: Optional[str] = None
    description: Optional[str] = None


class SprayLineCreate(SprayLineBase):
    pass


class SprayLine(SprayLineBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class DestinationClimateBase(BaseModel):
    port_code: str
    port_name: str
    country: str
    region: Optional[str] = None
    avg_high_temp_c: float
    avg_low_temp_c: float
    avg_relative_humidity_pct: float
    monsoon_season: Optional[str] = None
    climate_zone: Optional[str] = None


class DestinationClimateCreate(DestinationClimateBase):
    pass


class DestinationClimate(DestinationClimateBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class VehicleBatchBase(BaseModel):
    batch_code: str
    model: str
    quantity: int
    formula_id: int
    spray_line_id: int
    cure_temperature_c: float
    cure_duration_min: float
    air_dry_duration_hours: float
    production_date: datetime


class VehicleBatchCreate(VehicleBatchBase):
    pass


class VehicleBatch(VehicleBatchBase):
    id: int
    created_at: datetime
    formula: Optional[CoatingFormula] = None
    spray_line: Optional[SprayLine] = None

    model_config = ConfigDict(from_attributes=True)


class ExportOrderBase(BaseModel):
    order_no: str
    batch_id: int
    climate_id: int
    packaging_method: PackagingMethod
    shipping_route: str
    shipment_date: datetime
    estimated_arrival: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    customer: str


class ExportOrderCreate(ExportOrderBase):
    pass


class ExportOrder(ExportOrderBase):
    id: int
    created_at: datetime
    batch: Optional[VehicleBatch] = None
    climate: Optional[DestinationClimate] = None

    model_config = ConfigDict(from_attributes=True)


class InspectionRecordBase(BaseModel):
    batch_id: int
    inspector: str
    inspection_date: datetime
    sample_size: int
    adhesion_grade: str
    color_delta_e: float
    film_thickness_um: float
    humidity_resistance_hours: float
    passed: int
    failed: int
    notes: Optional[str] = None


class InspectionRecordCreate(InspectionRecordBase):
    pass


class InspectionRecord(InspectionRecordBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BatchMarkBase(BaseModel):
    batch_id: int
    status: BatchMarkStatus
    marked_by: str
    reason: str


class BatchMarkCreate(BatchMarkBase):
    pass


class BatchMark(BatchMarkBase):
    id: int
    marked_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerComplaintBase(BaseModel):
    order_id: int
    complaint_type: ComplaintType
    vehicle_count: int
    severity: str
    reported_at: datetime
    description: str
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None


class CustomerComplaintCreate(CustomerComplaintBase):
    pass


class CustomerComplaint(CustomerComplaintBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReferenceSameCombo(BaseModel):
    batches: List[VehicleBatch] = []
    orders: List[ExportOrder] = []


class TraceResult(BaseModel):
    order: ExportOrder
    batch: VehicleBatch
    formula: CoatingFormula
    spray_line: SprayLine
    climate: DestinationClimate
    inspections: List[InspectionRecord]
    marks: List[BatchMark]
    complaints: List[CustomerComplaint]
    direct_same_batch_orders: List[ExportOrder]
    reference_same_combo: ReferenceSameCombo


class RouteComplaintDetail(BaseModel):
    shipping_route: str
    route_orders: int
    route_complaints: int
    complaint_rate: float
    bubbling_complaints: int
    bubbling_rate: float
    climate_zone: Optional[str] = None
    avg_high_temp_c: Optional[float] = None
    avg_relative_humidity_pct: Optional[float] = None


class FormulaRisk(BaseModel):
    formula_id: int
    formula_code: str
    formula_name: str
    total_orders: int
    total_complaints: int
    bubbling_complaints: int
    complaint_rate: float
    bubbling_rate: float
    high_risk_routes: List[str]
    route_details: List[RouteComplaintDetail] = []


class FormulaRouteRisk(BaseModel):
    formula_id: int
    formula_code: str
    formula_name: str
    shipping_route: str
    route_orders: int
    route_complaints: int
    complaint_rate: float
    bubbling_complaints: int
    bubbling_rate: float
    climate_zone: Optional[str] = None
    avg_high_temp_c: Optional[float] = None
    avg_relative_humidity_pct: Optional[float] = None


class BatchInspectionSummary(BaseModel):
    batch_id: int
    batch_code: str
    model: str
    quantity: int
    production_date: datetime
    order_no: str
    customer: str
    mark_status: Optional[str] = None
    mark_reason: Optional[str] = None
    adhesion_grade: Optional[str] = None
    color_delta_e: Optional[float] = None
    film_thickness_um: Optional[float] = None
    humidity_resistance_hours: Optional[float] = None
    inspection_passed: Optional[int] = None
    inspection_failed: Optional[int] = None
    complaint_types: List[str] = []


class FormulaRouteRiskDetail(BaseModel):
    formula_id: int
    formula_code: str
    formula_name: str
    shipping_route: str
    route_orders: int
    route_complaints: int
    complaint_rate: float
    bubbling_complaints: int
    bubbling_rate: float
    climate_zone: Optional[str] = None
    avg_high_temp_c: Optional[float] = None
    avg_relative_humidity_pct: Optional[float] = None
    related_batches: List[BatchInspectionSummary]


class ReinspectionOrderBase(BaseModel):
    order_id: int
    risk_categories: str
    formula_risk_score: float = 0.0
    spray_line_risk_score: float = 0.0
    climate_risk_score: float = 0.0
    complaint_risk_score: float = 0.0
    total_risk_score: float
    risk_detail: Optional[str] = None


class ReinspectionOrderCreate(ReinspectionOrderBase):
    pass


class ReinspectionOrderUpdate(BaseModel):
    status: Optional[ReinspectionStatus] = None
    assigned_inspector: Optional[str] = None
    reinspection_result: Optional[str] = None


class ReinspectionOrder(ReinspectionOrderBase):
    id: int
    status: ReinspectionStatus
    assigned_inspector: Optional[str] = None
    reinspection_result: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReferenceSummary(BaseModel):
    same_combo_batch_count: int = 0
    same_combo_order_count: int = 0
    same_combo_complaint_count: int = 0
    same_combo_bubbling_count: int = 0
    same_combo_marked_batches: List[str] = []


class ReinspectionOrderDetail(ReinspectionOrder):
    order: Optional[ExportOrder] = None
    batch: Optional[VehicleBatch] = None
    formula: Optional[CoatingFormula] = None
    spray_line: Optional[SprayLine] = None
    climate: Optional[DestinationClimate] = None
    inspections: List[InspectionRecord] = []
    marks: List[BatchMark] = []
    complaints: List[CustomerComplaint] = []
    reference_summary: Optional[ReferenceSummary] = None


class PreDepartureWarningItem(BaseModel):
    order_id: int
    order_no: str
    customer: str
    shipping_route: str
    shipment_date: datetime
    batch_code: str
    formula_code: str
    formula_name: str
    spray_line_code: str
    spray_line_name: str
    port_name: str
    climate_zone: Optional[str] = None
    avg_high_temp_c: Optional[float] = None
    avg_relative_humidity_pct: Optional[float] = None
    formula_risk_score: float
    spray_line_risk_score: float
    climate_risk_score: float
    complaint_risk_score: float
    total_risk_score: float
    risk_categories: List[str]
    risk_detail: str


class ReinspectionDashboardStats(BaseModel):
    total_warnings: int
    pending_count: int
    in_progress_count: int
    completed_count: int
    cancelled_count: int
    formula_risk_count: int
    spray_line_risk_count: int
    climate_risk_count: int
    avg_total_risk_score: float
    high_risk_orders: List[ReinspectionOrder]
