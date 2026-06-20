from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
import models
import schemas
from typing import List, Optional
from datetime import datetime


def get_formula(db: Session, formula_id: int):
    return db.query(models.CoatingFormula).filter(models.CoatingFormula.id == formula_id).first()


def get_formula_by_code(db: Session, code: str):
    return db.query(models.CoatingFormula).filter(models.CoatingFormula.code == code).first()


def get_formulas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CoatingFormula).offset(skip).limit(limit).all()


def create_formula(db: Session, formula: schemas.CoatingFormulaCreate):
    db_formula = models.CoatingFormula(**formula.model_dump())
    db.add(db_formula)
    db.commit()
    db.refresh(db_formula)
    return db_formula


def get_spray_line(db: Session, line_id: int):
    return db.query(models.SprayLine).filter(models.SprayLine.id == line_id).first()


def get_spray_line_by_code(db: Session, code: str):
    return db.query(models.SprayLine).filter(models.SprayLine.code == code).first()


def get_spray_lines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SprayLine).offset(skip).limit(limit).all()


def create_spray_line(db: Session, line: schemas.SprayLineCreate):
    db_line = models.SprayLine(**line.model_dump())
    db.add(db_line)
    db.commit()
    db.refresh(db_line)
    return db_line


def get_climate(db: Session, climate_id: int):
    return db.query(models.DestinationClimate).filter(models.DestinationClimate.id == climate_id).first()


def get_climate_by_port(db: Session, port_code: str):
    return db.query(models.DestinationClimate).filter(models.DestinationClimate.port_code == port_code).first()


def get_climates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DestinationClimate).offset(skip).limit(limit).all()


def create_climate(db: Session, climate: schemas.DestinationClimateCreate):
    db_climate = models.DestinationClimate(**climate.model_dump())
    db.add(db_climate)
    db.commit()
    db.refresh(db_climate)
    return db_climate


def get_batch(db: Session, batch_id: int):
    return db.query(models.VehicleBatch).filter(models.VehicleBatch.id == batch_id).first()


def get_batch_by_code(db: Session, batch_code: str):
    return db.query(models.VehicleBatch).filter(models.VehicleBatch.batch_code == batch_code).first()


def get_batches(db: Session, skip: int = 0, limit: int = 100, formula_id: Optional[int] = None,
                spray_line_id: Optional[int] = None):
    query = db.query(models.VehicleBatch)
    if formula_id:
        query = query.filter(models.VehicleBatch.formula_id == formula_id)
    if spray_line_id:
        query = query.filter(models.VehicleBatch.spray_line_id == spray_line_id)
    return query.offset(skip).limit(limit).all()


def create_batch(db: Session, batch: schemas.VehicleBatchCreate):
    db_batch = models.VehicleBatch(**batch.model_dump())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch


def get_order(db: Session, order_id: int):
    return db.query(models.ExportOrder).filter(models.ExportOrder.id == order_id).first()


def get_order_by_no(db: Session, order_no: str):
    return db.query(models.ExportOrder).filter(models.ExportOrder.order_no == order_no).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100, batch_id: Optional[int] = None,
               climate_id: Optional[int] = None):
    query = db.query(models.ExportOrder)
    if batch_id:
        query = query.filter(models.ExportOrder.batch_id == batch_id)
    if climate_id:
        query = query.filter(models.ExportOrder.climate_id == climate_id)
    return query.offset(skip).limit(limit).all()


def create_order(db: Session, order: schemas.ExportOrderCreate):
    db_order = models.ExportOrder(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_inspection(db: Session, inspection_id: int):
    return db.query(models.InspectionRecord).filter(models.InspectionRecord.id == inspection_id).first()


def get_inspections_by_batch(db: Session, batch_id: int):
    return db.query(models.InspectionRecord).filter(models.InspectionRecord.batch_id == batch_id).all()


def get_inspections(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InspectionRecord).offset(skip).limit(limit).all()


def create_inspection(db: Session, inspection: schemas.InspectionRecordCreate):
    db_inspection = models.InspectionRecord(**inspection.model_dump())
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection


def get_batch_mark(db: Session, mark_id: int):
    return db.query(models.BatchMark).filter(models.BatchMark.id == mark_id).first()


def get_marks_by_batch(db: Session, batch_id: int):
    return db.query(models.BatchMark).filter(models.BatchMark.batch_id == batch_id).all()


def get_batch_marks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BatchMark).offset(skip).limit(limit).all()


def create_batch_mark(db: Session, mark: schemas.BatchMarkCreate):
    db_mark = models.BatchMark(**mark.model_dump())
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark


def get_complaint(db: Session, complaint_id: int):
    return db.query(models.CustomerComplaint).filter(models.CustomerComplaint.id == complaint_id).first()


def get_complaints_by_order(db: Session, order_id: int):
    return db.query(models.CustomerComplaint).filter(models.CustomerComplaint.order_id == order_id).all()


def get_complaints(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CustomerComplaint).offset(skip).limit(limit).all()


def create_complaint(db: Session, complaint: schemas.CustomerComplaintCreate):
    db_complaint = models.CustomerComplaint(**complaint.model_dump())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def trace_by_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if not order:
        return None

    batch = get_batch(db, order.batch_id)
    formula = get_formula(db, batch.formula_id)
    spray_line = get_spray_line(db, batch.spray_line_id)
    climate = get_climate(db, order.climate_id)
    inspections = get_inspections_by_batch(db, batch.id)
    marks = get_marks_by_batch(db, batch.id)

    related_batches = db.query(models.VehicleBatch).filter(
        or_(
            models.VehicleBatch.formula_id == batch.formula_id,
            models.VehicleBatch.spray_line_id == batch.spray_line_id
        )
    ).filter(models.VehicleBatch.id != batch.id).limit(20).all()

    related_orders = []
    for rb in related_batches:
        orders = db.query(models.ExportOrder).filter(models.ExportOrder.batch_id == rb.id).all()
        related_orders.extend(orders)

    return schemas.TraceResult(
        order=schemas.ExportOrder.model_validate(order),
        batch=schemas.VehicleBatch.model_validate(batch),
        formula=schemas.CoatingFormula.model_validate(formula),
        spray_line=schemas.SprayLine.model_validate(spray_line),
        climate=schemas.DestinationClimate.model_validate(climate),
        inspections=[schemas.InspectionRecord.model_validate(i) for i in inspections],
        marks=[schemas.BatchMark.model_validate(m) for m in marks],
        related_batches=[schemas.VehicleBatch.model_validate(rb) for rb in related_batches],
        related_orders=[schemas.ExportOrder.model_validate(ro) for ro in related_orders]
    )


def trace_by_batch(db: Session, batch_id: int):
    batch = get_batch(db, batch_id)
    if not batch:
        return None

    orders = get_orders(db, batch_id=batch.id)
    if orders:
        return trace_by_order(db, orders[0].id)
    return None


def analyze_formula_risks(db: Session):
    results = []

    formulas = get_formulas(db, limit=1000)

    for formula in formulas:
        batches = db.query(models.VehicleBatch).filter(
            models.VehicleBatch.formula_id == formula.id
        ).all()

        total_orders = 0
        total_complaints = 0
        bubbling_complaints = 0
        route_complaints = {}

        for batch in batches:
            orders = db.query(models.ExportOrder).filter(
                models.ExportOrder.batch_id == batch.id
            ).all()
            total_orders += len(orders)

            for order in orders:
                complaints = db.query(models.CustomerComplaint).filter(
                    models.CustomerComplaint.order_id == order.id
                ).all()
                total_complaints += len(complaints)
                for c in complaints:
                    if c.complaint_type == models.ComplaintType.BUBBLING:
                        bubbling_complaints += 1
                    if order.shipping_route not in route_complaints:
                        route_complaints[order.shipping_route] = route_complaints.get(order.shipping_route, 0) + 1

        complaint_rate = (total_complaints / total_orders * 100) if total_orders > 0 else 0.0
        bubbling_rate = (bubbling_complaints / total_orders * 100) if total_orders > 0 else 0.0

        high_risk_routes = [
            route for route, count in route_complaints.items() if count >= 2
        ]
        high_risk_routes.sort(key=lambda r: route_complaints.get(r, 0), reverse=True)

        results.append(schemas.FormulaRisk(
            formula_id=formula.id,
            formula_code=formula.code,
            formula_name=formula.name,
            total_orders=total_orders,
            total_complaints=total_complaints,
            bubbling_complaints=bubbling_complaints,
            complaint_rate=round(complaint_rate, 2),
            bubbling_rate=round(bubbling_rate, 2),
            high_risk_routes=high_risk_routes[:5]
        ))

    results.sort(key=lambda x: x.bubbling_rate, reverse=True)
    return results
