from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

import models
import crud


HIGH_RISK_COMPLAINT_RATE_THRESHOLD = 20.0
COMPLAINT_RATE_ROUND_DECIMALS = 2


@dataclass
class OrderTraceChain:
    order: models.ExportOrder
    batch: models.VehicleBatch
    formula: models.CoatingFormula
    spray_line: models.SprayLine
    climate: models.DestinationClimate
    inspections: List[models.InspectionRecord] = field(default_factory=list)
    marks: List[models.BatchMark] = field(default_factory=list)
    complaints: List[models.CustomerComplaint] = field(default_factory=list)


@dataclass
class ComplaintStats:
    total_orders: int = 0
    total_complaints: int = 0
    bubbling_complaints: int = 0

    @property
    def complaint_rate(self) -> float:
        return _calc_rate(self.total_complaints, self.total_orders)

    @property
    def bubbling_rate(self) -> float:
        return _calc_rate(self.bubbling_complaints, self.total_orders)


@dataclass
class SameComboRef:
    batches: List[models.VehicleBatch] = field(default_factory=list)
    orders: List[models.ExportOrder] = field(default_factory=list)
    order_count: int = 0
    complaint_count: int = 0
    bubbling_count: int = 0
    marked_batch_codes: List[str] = field(default_factory=list)


def _calc_rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator * 100, COMPLAINT_RATE_ROUND_DECIMALS)


def is_high_risk_complaint_rate(complaint_rate: float, min_complaints: int = 1) -> bool:
    return min_complaints >= 1 and complaint_rate >= HIGH_RISK_COMPLAINT_RATE_THRESHOLD


def build_order_trace_chain(db: Session, order_id: int) -> Optional[OrderTraceChain]:
    order = crud.get_order(db, order_id)
    if not order:
        return None

    batch = crud.get_batch(db, order.batch_id)
    if not batch:
        return None

    formula = crud.get_formula(db, batch.formula_id)
    spray_line = crud.get_spray_line(db, batch.spray_line_id)
    climate = crud.get_climate(db, order.climate_id)
    inspections = crud.get_inspections_by_batch(db, batch.id)
    marks = crud.get_marks_by_batch(db, batch.id)
    complaints = crud.get_complaints_by_order(db, order.id)

    return OrderTraceChain(
        order=order,
        batch=batch,
        formula=formula,
        spray_line=spray_line,
        climate=climate,
        inspections=inspections,
        marks=marks,
        complaints=complaints,
    )


def get_orders_by_batch(db: Session, batch_id: int, exclude_order_id: Optional[int] = None) -> List[models.ExportOrder]:
    query = db.query(models.ExportOrder).filter(models.ExportOrder.batch_id == batch_id)
    if exclude_order_id is not None:
        query = query.filter(models.ExportOrder.id != exclude_order_id)
    return query.all()


def get_batches_by_formula_spray_line(
    db: Session,
    formula_id: int,
    spray_line_id: int,
    exclude_batch_id: Optional[int] = None,
    limit: Optional[int] = None,
) -> List[models.VehicleBatch]:
    query = db.query(models.VehicleBatch).filter(
        and_(
            models.VehicleBatch.formula_id == formula_id,
            models.VehicleBatch.spray_line_id == spray_line_id,
        )
    )
    if exclude_batch_id is not None:
        query = query.filter(models.VehicleBatch.id != exclude_batch_id)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def get_orders_by_batches(db: Session, batch_ids: List[int]) -> List[models.ExportOrder]:
    if not batch_ids:
        return []
    return db.query(models.ExportOrder).filter(models.ExportOrder.batch_id.in_(batch_ids)).all()


def get_same_combo_reference(
    db: Session,
    formula_id: int,
    spray_line_id: int,
    exclude_batch_id: Optional[int] = None,
    batch_limit: Optional[int] = None,
) -> SameComboRef:
    batches = get_batches_by_formula_spray_line(
        db, formula_id, spray_line_id, exclude_batch_id=exclude_batch_id, limit=batch_limit
    )
    batch_ids = [b.id for b in batches]
    orders = get_orders_by_batches(db, batch_ids)

    order_count = len(orders)
    complaint_count = 0
    bubbling_count = 0
    for o in orders:
        order_complaints = crud.get_complaints_by_order(db, o.id)
        complaint_count += len(order_complaints)
        for c in order_complaints:
            if c.complaint_type == models.ComplaintType.BUBBLING:
                bubbling_count += 1

    marked_batch_codes = []
    for b in batches:
        b_marks = crud.get_marks_by_batch(db, b.id)
        if b_marks:
            marked_batch_codes.append(b.batch_code)

    return SameComboRef(
        batches=batches,
        orders=orders,
        order_count=order_count,
        complaint_count=complaint_count,
        bubbling_count=bubbling_count,
        marked_batch_codes=marked_batch_codes,
    )


def get_latest_batch_mark(db: Session, batch_id: int) -> Optional[models.BatchMark]:
    return (
        db.query(models.BatchMark)
        .filter(models.BatchMark.batch_id == batch_id)
        .order_by(models.BatchMark.marked_at.desc())
        .first()
    )


def get_latest_inspection(db: Session, batch_id: int) -> Optional[models.InspectionRecord]:
    return (
        db.query(models.InspectionRecord)
        .filter(models.InspectionRecord.batch_id == batch_id)
        .order_by(models.InspectionRecord.inspection_date.desc())
        .first()
    )


def get_route_climate_info(db: Session, shipping_route: str) -> Tuple[Optional[str], Optional[float], Optional[float]]:
    orders_on_route = (
        db.query(models.ExportOrder).filter(models.ExportOrder.shipping_route == shipping_route).all()
    )
    if not orders_on_route:
        return None, None, None
    climate = crud.get_climate(db, orders_on_route[0].climate_id)
    if climate:
        return climate.climate_zone, climate.avg_high_temp_c, climate.avg_relative_humidity_pct
    return None, None, None


def _aggregate_complaints_for_orders(db: Session, orders: List[models.ExportOrder]) -> ComplaintStats:
    stats = ComplaintStats(total_orders=len(orders))
    for order in orders:
        order_complaints = crud.get_complaints_by_order(db, order.id)
        stats.total_complaints += len(order_complaints)
        for c in order_complaints:
            if c.complaint_type == models.ComplaintType.BUBBLING:
                stats.bubbling_complaints += 1
    return stats


def aggregate_by_formula(db: Session, formula_id: int) -> ComplaintStats:
    batches = db.query(models.VehicleBatch).filter(models.VehicleBatch.formula_id == formula_id).all()
    batch_ids = [b.id for b in batches]
    orders = get_orders_by_batches(db, batch_ids)
    return _aggregate_complaints_for_orders(db, orders)


def aggregate_by_spray_line(db: Session, spray_line_id: int) -> Tuple[ComplaintStats, int, int]:
    batches = db.query(models.VehicleBatch).filter(models.VehicleBatch.spray_line_id == spray_line_id).all()
    batch_ids = [b.id for b in batches]
    orders = get_orders_by_batches(db, batch_ids)
    stats = _aggregate_complaints_for_orders(db, orders)

    total_inspections = 0
    failed_inspections = 0
    for b in batches:
        inspections = crud.get_inspections_by_batch(db, b.id)
        total_inspections += len(inspections)
        for insp in inspections:
            if insp.failed > 0:
                failed_inspections += 1

    return stats, total_inspections, failed_inspections


def aggregate_by_climate(db: Session, climate_id: int) -> ComplaintStats:
    orders = db.query(models.ExportOrder).filter(models.ExportOrder.climate_id == climate_id).all()
    return _aggregate_complaints_for_orders(db, orders)


def aggregate_by_formula_routes(db: Session, formula_id: int) -> Dict[str, ComplaintStats]:
    batches = db.query(models.VehicleBatch).filter(models.VehicleBatch.formula_id == formula_id).all()
    batch_ids = [b.id for b in batches]
    orders = get_orders_by_batches(db, batch_ids)

    route_stats: Dict[str, ComplaintStats] = {}
    for order in orders:
        route = order.shipping_route
        if route not in route_stats:
            route_stats[route] = ComplaintStats()
        route_stats[route].total_orders += 1
        order_complaints = crud.get_complaints_by_order(db, order.id)
        route_stats[route].total_complaints += len(order_complaints)
        for c in order_complaints:
            if c.complaint_type == models.ComplaintType.BUBBLING:
                route_stats[route].bubbling_complaints += 1
    return route_stats


def aggregate_all_formulas_routes(db: Session) -> Dict[Tuple[int, str], ComplaintStats]:
    all_stats: Dict[Tuple[int, str], ComplaintStats] = {}
    formulas = crud.get_formulas(db, limit=1000)

    for formula in formulas:
        batches = db.query(models.VehicleBatch).filter(models.VehicleBatch.formula_id == formula.id).all()
        batch_ids = [b.id for b in batches]
        orders = get_orders_by_batches(db, batch_ids)

        for order in orders:
            key = (formula.id, order.shipping_route)
            if key not in all_stats:
                all_stats[key] = ComplaintStats()
            all_stats[key].total_orders += 1
            order_complaints = crud.get_complaints_by_order(db, order.id)
            all_stats[key].total_complaints += len(order_complaints)
            for c in order_complaints:
                if c.complaint_type == models.ComplaintType.BUBBLING:
                    all_stats[key].bubbling_complaints += 1

    return all_stats


def count_recent_complaints_by_formula(db: Session, formula_id: int, days: int = 90) -> int:
    recent_cutoff = datetime.now() - timedelta(days=days)
    return (
        db.query(models.CustomerComplaint)
        .join(models.ExportOrder)
        .join(models.VehicleBatch)
        .filter(
            models.VehicleBatch.formula_id == formula_id,
            models.CustomerComplaint.reported_at >= recent_cutoff,
        )
        .count()
    )


def count_recent_complaints_by_spray_line(db: Session, spray_line_id: int, days: int = 90) -> int:
    recent_cutoff = datetime.now() - timedelta(days=days)
    return (
        db.query(models.CustomerComplaint)
        .join(models.ExportOrder)
        .join(models.VehicleBatch)
        .filter(
            models.VehicleBatch.spray_line_id == spray_line_id,
            models.CustomerComplaint.reported_at >= recent_cutoff,
        )
        .count()
    )


def count_recent_complaints_by_climate(db: Session, climate_id: int, days: int = 60) -> int:
    recent_cutoff = datetime.now() - timedelta(days=days)
    return (
        db.query(models.CustomerComplaint)
        .join(models.ExportOrder)
        .filter(
            models.ExportOrder.climate_id == climate_id,
            models.CustomerComplaint.reported_at >= recent_cutoff,
        )
        .count()
    )


def count_recent_failed_batches_by_spray_line(db: Session, spray_line_id: int, days: int = 90) -> int:
    recent_cutoff = datetime.now() - timedelta(days=days)
    recent_batches = (
        db.query(models.VehicleBatch)
        .filter(
            models.VehicleBatch.spray_line_id == spray_line_id,
            models.VehicleBatch.production_date >= recent_cutoff,
        )
        .all()
    )
    failed_count = 0
    for batch in recent_batches:
        insp = get_latest_inspection(db, batch.id)
        if insp and insp.failed > 0:
            failed_count += 1
    return failed_count
