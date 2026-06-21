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


def _get_route_climate_info(db: Session, shipping_route: str):
    orders_on_route = db.query(models.ExportOrder).filter(
        models.ExportOrder.shipping_route == shipping_route
    ).all()
    if not orders_on_route:
        return None, None, None
    climate = db.query(models.DestinationClimate).filter(
        models.DestinationClimate.id == orders_on_route[0].climate_id
    ).first()
    if climate:
        return climate.climate_zone, climate.avg_high_temp_c, climate.avg_relative_humidity_pct
    return None, None, None


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
        route_data = {}

        for batch in batches:
            orders = db.query(models.ExportOrder).filter(
                models.ExportOrder.batch_id == batch.id
            ).all()
            total_orders += len(orders)

            for order in orders:
                route = order.shipping_route
                if route not in route_data:
                    route_data[route] = {"orders": 0, "complaints": 0, "bubbling": 0}
                route_data[route]["orders"] += 1

                complaints = db.query(models.CustomerComplaint).filter(
                    models.CustomerComplaint.order_id == order.id
                ).all()
                total_complaints += len(complaints)
                route_data[route]["complaints"] += len(complaints)
                for c in complaints:
                    if c.complaint_type == models.ComplaintType.BUBBLING:
                        bubbling_complaints += 1
                        route_data[route]["bubbling"] += 1

        complaint_rate = (total_complaints / total_orders * 100) if total_orders > 0 else 0.0
        bubbling_rate = (bubbling_complaints / total_orders * 100) if total_orders > 0 else 0.0

        high_risk_routes = [
            route for route, data in route_data.items()
            if data["complaints"] >= 1 and (data["complaints"] / data["orders"] * 100) >= 20.0
        ]
        high_risk_routes.sort(
            key=lambda r: route_data[r]["complaints"] / route_data[r]["orders"] if route_data[r]["orders"] > 0 else 0,
            reverse=True
        )

        route_details = []
        for route, data in route_data.items():
            rc_rate = (data["complaints"] / data["orders"] * 100) if data["orders"] > 0 else 0.0
            rb_rate = (data["bubbling"] / data["orders"] * 100) if data["orders"] > 0 else 0.0
            cz, avg_t, avg_h = _get_route_climate_info(db, route)
            route_details.append(schemas.RouteComplaintDetail(
                shipping_route=route,
                route_orders=data["orders"],
                route_complaints=data["complaints"],
                complaint_rate=round(rc_rate, 2),
                bubbling_complaints=data["bubbling"],
                bubbling_rate=round(rb_rate, 2),
                climate_zone=cz,
                avg_high_temp_c=avg_t,
                avg_relative_humidity_pct=avg_h
            ))
        route_details.sort(key=lambda x: x.complaint_rate, reverse=True)

        results.append(schemas.FormulaRisk(
            formula_id=formula.id,
            formula_code=formula.code,
            formula_name=formula.name,
            total_orders=total_orders,
            total_complaints=total_complaints,
            bubbling_complaints=bubbling_complaints,
            complaint_rate=round(complaint_rate, 2),
            bubbling_rate=round(bubbling_rate, 2),
            high_risk_routes=high_risk_routes[:5],
            route_details=route_details
        ))

    results.sort(key=lambda x: x.bubbling_rate, reverse=True)
    return results


def analyze_formula_route_risks(db: Session, min_orders: int = 1):
    results = []
    formulas = get_formulas(db, limit=1000)

    for formula in formulas:
        batches = db.query(models.VehicleBatch).filter(
            models.VehicleBatch.formula_id == formula.id
        ).all()

        route_data = {}
        for batch in batches:
            orders = db.query(models.ExportOrder).filter(
                models.ExportOrder.batch_id == batch.id
            ).all()
            for order in orders:
                route = order.shipping_route
                if route not in route_data:
                    route_data[route] = {"orders": 0, "complaints": 0, "bubbling": 0}
                route_data[route]["orders"] += 1

                complaints = db.query(models.CustomerComplaint).filter(
                    models.CustomerComplaint.order_id == order.id
                ).all()
                route_data[route]["complaints"] += len(complaints)
                for c in complaints:
                    if c.complaint_type == models.ComplaintType.BUBBLING:
                        route_data[route]["bubbling"] += 1

        for route, data in route_data.items():
            if data["orders"] < min_orders:
                continue
            rc_rate = (data["complaints"] / data["orders"] * 100) if data["orders"] > 0 else 0.0
            rb_rate = (data["bubbling"] / data["orders"] * 100) if data["orders"] > 0 else 0.0
            cz, avg_t, avg_h = _get_route_climate_info(db, route)
            results.append(schemas.FormulaRouteRisk(
                formula_id=formula.id,
                formula_code=formula.code,
                formula_name=formula.name,
                shipping_route=route,
                route_orders=data["orders"],
                route_complaints=data["complaints"],
                complaint_rate=round(rc_rate, 2),
                bubbling_complaints=data["bubbling"],
                bubbling_rate=round(rb_rate, 2),
                climate_zone=cz,
                avg_high_temp_c=avg_t,
                avg_relative_humidity_pct=avg_h
            ))

    results.sort(key=lambda x: x.complaint_rate, reverse=True)
    return results


def get_formula_route_trace(db: Session, formula_id: int, shipping_route: str):
    formula = get_formula(db, formula_id)
    if not formula:
        return None

    batches = db.query(models.VehicleBatch).filter(
        models.VehicleBatch.formula_id == formula_id
    ).all()

    route_orders = []
    route_complaints_total = 0
    route_bubbling_total = 0
    all_complaint_types = []

    for batch in batches:
        orders = db.query(models.ExportOrder).filter(
            models.ExportOrder.batch_id == batch.id,
            models.ExportOrder.shipping_route == shipping_route
        ).all()
        for order in orders:
            complaints = db.query(models.CustomerComplaint).filter(
                models.CustomerComplaint.order_id == order.id
            ).all()
            route_complaints_total += len(complaints)
            for c in complaints:
                if c.complaint_type == models.ComplaintType.BUBBLING:
                    route_bubbling_total += 1
                all_complaint_types.append(c.complaint_type.value)
            route_orders.append((order, batch, complaints))

    route_order_count = len(route_orders)
    rc_rate = (route_complaints_total / route_order_count * 100) if route_order_count > 0 else 0.0
    rb_rate = (route_bubbling_total / route_order_count * 100) if route_order_count > 0 else 0.0
    cz, avg_t, avg_h = _get_route_climate_info(db, shipping_route)

    batch_summaries = []
    for order, batch, complaints in route_orders:
        mark = db.query(models.BatchMark).filter(
            models.BatchMark.batch_id == batch.id
        ).order_by(models.BatchMark.marked_at.desc()).first()

        inspection = db.query(models.InspectionRecord).filter(
            models.InspectionRecord.batch_id == batch.id
        ).order_by(models.InspectionRecord.inspection_date.desc()).first()

        complaint_types = list(set(c.complaint_type.value for c in complaints))

        batch_summaries.append(schemas.BatchInspectionSummary(
            batch_id=batch.id,
            batch_code=batch.batch_code,
            model=batch.model,
            quantity=batch.quantity,
            production_date=batch.production_date,
            order_no=order.order_no,
            customer=order.customer,
            mark_status=mark.status.value if mark else None,
            mark_reason=mark.reason if mark else None,
            adhesion_grade=inspection.adhesion_grade if inspection else None,
            color_delta_e=inspection.color_delta_e if inspection else None,
            film_thickness_um=inspection.film_thickness_um if inspection else None,
            humidity_resistance_hours=inspection.humidity_resistance_hours if inspection else None,
            inspection_passed=inspection.passed if inspection else None,
            inspection_failed=inspection.failed if inspection else None,
            complaint_types=complaint_types
        ))

    return schemas.FormulaRouteRiskDetail(
        formula_id=formula.id,
        formula_code=formula.code,
        formula_name=formula.name,
        shipping_route=shipping_route,
        route_orders=route_order_count,
        route_complaints=route_complaints_total,
        complaint_rate=round(rc_rate, 2),
        bubbling_complaints=route_bubbling_total,
        bubbling_rate=round(rb_rate, 2),
        climate_zone=cz,
        avg_high_temp_c=avg_t,
        avg_relative_humidity_pct=avg_h,
        related_batches=batch_summaries
    )
