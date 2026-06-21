from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
import models
import schemas
from typing import List, Optional
from datetime import datetime, timedelta
import json


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
    complaints = get_complaints_by_order(db, order.id)

    direct_same_batch_orders = db.query(models.ExportOrder).filter(
        models.ExportOrder.batch_id == batch.id,
        models.ExportOrder.id != order.id
    ).all()

    same_combo_batches = db.query(models.VehicleBatch).filter(
        and_(
            models.VehicleBatch.formula_id == batch.formula_id,
            models.VehicleBatch.spray_line_id == batch.spray_line_id
        ),
        models.VehicleBatch.id != batch.id
    ).limit(20).all()

    same_combo_orders = []
    for scb in same_combo_batches:
        sc_orders = db.query(models.ExportOrder).filter(
            models.ExportOrder.batch_id == scb.id
        ).all()
        same_combo_orders.extend(sc_orders)

    return schemas.TraceResult(
        order=schemas.ExportOrder.model_validate(order),
        batch=schemas.VehicleBatch.model_validate(batch),
        formula=schemas.CoatingFormula.model_validate(formula),
        spray_line=schemas.SprayLine.model_validate(spray_line),
        climate=schemas.DestinationClimate.model_validate(climate),
        inspections=[schemas.InspectionRecord.model_validate(i) for i in inspections],
        marks=[schemas.BatchMark.model_validate(m) for m in marks],
        complaints=[schemas.CustomerComplaint.model_validate(c) for c in complaints],
        direct_same_batch_orders=[schemas.ExportOrder.model_validate(o) for o in direct_same_batch_orders],
        reference_same_combo=schemas.ReferenceSameCombo(
            batches=[schemas.VehicleBatch.model_validate(b) for b in same_combo_batches],
            orders=[schemas.ExportOrder.model_validate(o) for o in same_combo_orders]
        )
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


def get_reinspection(db: Session, reinspection_id: int):
    return db.query(models.ReinspectionOrder).filter(models.ReinspectionOrder.id == reinspection_id).first()


def get_reinspections(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    risk_category: Optional[str] = None,
):
    query = db.query(models.ReinspectionOrder)
    if status:
        query = query.filter(models.ReinspectionOrder.status == status)
    if risk_category:
        query = query.filter(models.ReinspectionOrder.risk_categories.contains(risk_category))
    return query.order_by(models.ReinspectionOrder.total_risk_score.desc()).offset(skip).limit(limit).all()


def create_reinspection(db: Session, reinspection: schemas.ReinspectionOrderCreate):
    db_reinspection = models.ReinspectionOrder(**reinspection.model_dump())
    db.add(db_reinspection)
    db.commit()
    db.refresh(db_reinspection)
    return db_reinspection


def update_reinspection(db: Session, reinspection_id: int, update_data: schemas.ReinspectionOrderUpdate):
    db_reinspection = get_reinspection(db, reinspection_id)
    if not db_reinspection:
        return None
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_reinspection, key, value)
    if update_data.status == models.ReinspectionStatus.COMPLETED:
        db_reinspection.completed_at = datetime.now()
    db.commit()
    db.refresh(db_reinspection)
    return db_reinspection


def get_reinspection_detail(db: Session, reinspection_id: int):
    db_reinspection = get_reinspection(db, reinspection_id)
    if not db_reinspection:
        return None

    order = get_order(db, db_reinspection.order_id)
    batch = get_batch(db, order.batch_id) if order else None
    formula = get_formula(db, batch.formula_id) if batch else None
    spray_line = get_spray_line(db, batch.spray_line_id) if batch else None
    climate = get_climate(db, order.climate_id) if order else None
    inspections = get_inspections_by_batch(db, batch.id) if batch else []
    marks = get_marks_by_batch(db, batch.id) if batch else []
    complaints = get_complaints_by_order(db, order.id) if order else []

    reference_summary = None
    if batch and formula and spray_line:
        same_combo_batches = db.query(models.VehicleBatch).filter(
            and_(
                models.VehicleBatch.formula_id == batch.formula_id,
                models.VehicleBatch.spray_line_id == batch.spray_line_id
            ),
            models.VehicleBatch.id != batch.id
        ).all()

        same_combo_order_count = 0
        same_combo_complaint_count = 0
        same_combo_bubbling_count = 0
        same_combo_marked_codes = []

        for scb in same_combo_batches:
            sc_orders = db.query(models.ExportOrder).filter(
                models.ExportOrder.batch_id == scb.id
            ).all()
            same_combo_order_count += len(sc_orders)
            for sco in sc_orders:
                sc_complaints = db.query(models.CustomerComplaint).filter(
                    models.CustomerComplaint.order_id == sco.id
                ).all()
                same_combo_complaint_count += len(sc_complaints)
                for scc in sc_complaints:
                    if scc.complaint_type == models.ComplaintType.BUBBLING:
                        same_combo_bubbling_count += 1

            sc_marks = db.query(models.BatchMark).filter(
                models.BatchMark.batch_id == scb.id
            ).all()
            if sc_marks:
                same_combo_marked_codes.append(scb.batch_code)

        reference_summary = schemas.ReferenceSummary(
            same_combo_batch_count=len(same_combo_batches),
            same_combo_order_count=same_combo_order_count,
            same_combo_complaint_count=same_combo_complaint_count,
            same_combo_bubbling_count=same_combo_bubbling_count,
            same_combo_marked_batches=same_combo_marked_codes
        )

    return schemas.ReinspectionOrderDetail(
        id=db_reinspection.id,
        order_id=db_reinspection.order_id,
        risk_categories=db_reinspection.risk_categories,
        formula_risk_score=db_reinspection.formula_risk_score,
        spray_line_risk_score=db_reinspection.spray_line_risk_score,
        climate_risk_score=db_reinspection.climate_risk_score,
        complaint_risk_score=db_reinspection.complaint_risk_score,
        total_risk_score=db_reinspection.total_risk_score,
        risk_detail=db_reinspection.risk_detail,
        status=db_reinspection.status,
        assigned_inspector=db_reinspection.assigned_inspector,
        reinspection_result=db_reinspection.reinspection_result,
        completed_at=db_reinspection.completed_at,
        created_at=db_reinspection.created_at,
        order=schemas.ExportOrder.model_validate(order) if order else None,
        batch=schemas.VehicleBatch.model_validate(batch) if batch else None,
        formula=schemas.CoatingFormula.model_validate(formula) if formula else None,
        spray_line=schemas.SprayLine.model_validate(spray_line) if spray_line else None,
        climate=schemas.DestinationClimate.model_validate(climate) if climate else None,
        inspections=[schemas.InspectionRecord.model_validate(i) for i in inspections],
        marks=[schemas.BatchMark.model_validate(m) for m in marks],
        complaints=[schemas.CustomerComplaint.model_validate(c) for c in complaints],
        reference_summary=reference_summary
    )


def _calc_formula_risk_score(db: Session, formula_id: int) -> tuple:
    formula = get_formula(db, formula_id)
    if not formula:
        return 0.0, []

    batches = db.query(models.VehicleBatch).filter(
        models.VehicleBatch.formula_id == formula_id
    ).all()

    total_orders = 0
    total_complaints = 0
    bubbling_complaints = 0
    reasons = []

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

    score = 0.0
    complaint_rate = (total_complaints / total_orders * 100) if total_orders > 0 else 0.0
    bubbling_rate = (bubbling_complaints / total_orders * 100) if total_orders > 0 else 0.0

    if complaint_rate >= 30:
        score += 40.0
        reasons.append(f"配方投诉率{complaint_rate:.1f}%过高(>=30%)")
    elif complaint_rate >= 15:
        score += 25.0
        reasons.append(f"配方投诉率{complaint_rate:.1f}%偏高(>=15%)")
    elif complaint_rate >= 5:
        score += 10.0
        reasons.append(f"配方投诉率{complaint_rate:.1f}%(>=5%)")

    if bubbling_rate >= 20:
        score += 35.0
        reasons.append(f"起泡率{bubbling_rate:.1f}%严重(>=20%)")
    elif bubbling_rate >= 10:
        score += 20.0
        reasons.append(f"起泡率{bubbling_rate:.1f}%偏高(>=10%)")
    elif bubbling_rate >= 3:
        score += 8.0
        reasons.append(f"起泡率{bubbling_rate:.1f}%(>=3%)")

    recent_cutoff = datetime.now() - timedelta(days=90)
    recent_complaints = db.query(models.CustomerComplaint).join(models.ExportOrder).join(
        models.VehicleBatch
    ).filter(
        models.VehicleBatch.formula_id == formula_id,
        models.CustomerComplaint.reported_at >= recent_cutoff
    ).count()
    if recent_complaints >= 3:
        score += 25.0
        reasons.append(f"近90天投诉{recent_complaints}起(>=3)")
    elif recent_complaints >= 1:
        score += 10.0
        reasons.append(f"近90天投诉{recent_complaints}起")

    return min(score, 100.0), reasons


def _calc_spray_line_risk_score(db: Session, spray_line_id: int) -> tuple:
    spray_line = get_spray_line(db, spray_line_id)
    if not spray_line:
        return 0.0, []

    batches = db.query(models.VehicleBatch).filter(
        models.VehicleBatch.spray_line_id == spray_line_id
    ).all()

    total_orders = 0
    total_complaints = 0
    reasons = []
    failed_inspection_count = 0
    total_inspection_count = 0

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

        inspections = db.query(models.InspectionRecord).filter(
            models.InspectionRecord.batch_id == batch.id
        ).all()
        total_inspection_count += len(inspections)
        for insp in inspections:
            if insp.failed > 0:
                failed_inspection_count += 1

    score = 0.0
    complaint_rate = (total_complaints / total_orders * 100) if total_orders > 0 else 0.0

    if complaint_rate >= 25:
        score += 35.0
        reasons.append(f"喷涂线投诉率{complaint_rate:.1f}%过高(>=25%)")
    elif complaint_rate >= 10:
        score += 20.0
        reasons.append(f"喷涂线投诉率{complaint_rate:.1f}%偏高(>=10%)")
    elif complaint_rate >= 3:
        score += 8.0
        reasons.append(f"喷涂线投诉率{complaint_rate:.1f}%(>=3%)")

    fail_rate = (failed_inspection_count / total_inspection_count * 100) if total_inspection_count > 0 else 0.0
    if fail_rate >= 50:
        score += 35.0
        reasons.append(f"质检不合格批次率{fail_rate:.1f}%过高(>=50%)")
    elif fail_rate >= 25:
        score += 20.0
        reasons.append(f"质检不合格批次率{fail_rate:.1f}%偏高(>=25%)")
    elif fail_rate > 0:
        score += 8.0
        reasons.append(f"存在质检不合格批次")

    recent_cutoff = datetime.now() - timedelta(days=90)
    recent_batches = db.query(models.VehicleBatch).filter(
        models.VehicleBatch.spray_line_id == spray_line_id,
        models.VehicleBatch.production_date >= recent_cutoff
    ).all()
    recent_failed = 0
    for batch in recent_batches:
        insp = db.query(models.InspectionRecord).filter(
            models.InspectionRecord.batch_id == batch.id
        ).order_by(models.InspectionRecord.inspection_date.desc()).first()
        if insp and insp.failed > 0:
            recent_failed += 1
    if recent_failed >= 2:
        score += 30.0
        reasons.append(f"近90天{recent_failed}批次质检有不合格(>=2)")
    elif recent_failed >= 1:
        score += 12.0
        reasons.append(f"近90天{recent_failed}批次质检有不合格")

    return min(score, 100.0), reasons


def _calc_climate_risk_score(db: Session, climate_id: int) -> tuple:
    climate = get_climate(db, climate_id)
    if not climate:
        return 0.0, []

    score = 0.0
    reasons = []

    if climate.avg_high_temp_c >= 35:
        score += 20.0
        reasons.append(f"目的港平均高温{climate.avg_high_temp_c}°C极高(>=35°C)")
    elif climate.avg_high_temp_c >= 30:
        score += 12.0
        reasons.append(f"目的港平均高温{climate.avg_high_temp_c}°C偏高(>=30°C)")

    if climate.avg_relative_humidity_pct >= 85:
        score += 20.0
        reasons.append(f"平均湿度{climate.avg_relative_humidity_pct}%极高(>=85%)")
    elif climate.avg_relative_humidity_pct >= 75:
        score += 10.0
        reasons.append(f"平均湿度{climate.avg_relative_humidity_pct}%偏高(>=75%)")

    tropical_zones = ["热带雨林气候", "热带季风气候", "热带草原气候"]
    if climate.climate_zone in tropical_zones:
        score += 15.0
        reasons.append(f"气候区为{climate.climate_zone}(热带)")

    orders_on_route = db.query(models.ExportOrder).filter(
        models.ExportOrder.climate_id == climate_id
    ).all()
    route_complaints = 0
    for order in orders_on_route:
        complaints = db.query(models.CustomerComplaint).filter(
            models.CustomerComplaint.order_id == order.id
        ).all()
        route_complaints += len(complaints)

    route_complaint_rate = (route_complaints / len(orders_on_route) * 100) if orders_on_route else 0.0
    if route_complaint_rate >= 30:
        score += 25.0
        reasons.append(f"该目的港投诉率{route_complaint_rate:.1f}%过高(>=30%)")
    elif route_complaint_rate >= 10:
        score += 15.0
        reasons.append(f"该目的港投诉率{route_complaint_rate:.1f}%偏高(>=10%)")
    elif route_complaint_rate > 0:
        score += 5.0
        reasons.append(f"该目的港存在投诉")

    return min(score, 100.0), reasons


def _calc_complaint_risk_score(db: Session, order_id: int, formula_id: int, spray_line_id: int, climate_id: int) -> tuple:
    score = 0.0
    reasons = []

    recent_cutoff = datetime.now() - timedelta(days=60)
    recent_formula_complaints = db.query(models.CustomerComplaint).join(models.ExportOrder).join(
        models.VehicleBatch
    ).filter(
        models.VehicleBatch.formula_id == formula_id,
        models.CustomerComplaint.reported_at >= recent_cutoff
    ).all()

    if len(recent_formula_complaints) >= 3:
        score += 25.0
        reasons.append(f"同配方近60天投诉{len(recent_formula_complaints)}起(>=3)")
    elif len(recent_formula_complaints) >= 1:
        score += 10.0
        reasons.append(f"同配方近60天投诉{len(recent_formula_complaints)}起")

    recent_line_complaints = db.query(models.CustomerComplaint).join(models.ExportOrder).join(
        models.VehicleBatch
    ).filter(
        models.VehicleBatch.spray_line_id == spray_line_id,
        models.CustomerComplaint.reported_at >= recent_cutoff
    ).all()

    if len(recent_line_complaints) >= 3:
        score += 25.0
        reasons.append(f"同喷涂线近60天投诉{len(recent_line_complaints)}起(>=3)")
    elif len(recent_line_complaints) >= 1:
        score += 10.0
        reasons.append(f"同喷涂线近60天投诉{len(recent_line_complaints)}起")

    recent_climate_complaints = db.query(models.CustomerComplaint).join(models.ExportOrder).filter(
        models.ExportOrder.climate_id == climate_id,
        models.CustomerComplaint.reported_at >= recent_cutoff
    ).all()

    if len(recent_climate_complaints) >= 2:
        score += 20.0
        reasons.append(f"同目的港近60天投诉{len(recent_climate_complaints)}起(>=2)")
    elif len(recent_climate_complaints) >= 1:
        score += 8.0
        reasons.append(f"同目的港近60天投诉{len(recent_climate_complaints)}起")

    same_formula_line_batches = db.query(models.VehicleBatch).filter(
        models.VehicleBatch.formula_id == formula_id,
        models.VehicleBatch.spray_line_id == spray_line_id
    ).all()
    same_combo_complaints = 0
    for batch in same_formula_line_batches:
        batch_orders = db.query(models.ExportOrder).filter(
            models.ExportOrder.batch_id == batch.id
        ).all()
        for order in batch_orders:
            complaints = db.query(models.CustomerComplaint).filter(
                models.CustomerComplaint.order_id == order.id
            ).all()
            same_combo_complaints += len(complaints)

    if same_combo_complaints >= 2:
        score += 30.0
        reasons.append(f"同配方+同喷涂线组合投诉{same_combo_complaints}起(>=2)")

    return min(score, 100.0), reasons


def generate_pre_departure_warnings(db: Session, min_risk_score: float = 30.0) -> List[schemas.PreDepartureWarningItem]:
    warnings = []

    existing_reinspection_order_ids = set(
        r[0] for r in db.query(models.ReinspectionOrder.order_id).all()
    )

    orders = db.query(models.ExportOrder).filter(
        models.ExportOrder.actual_arrival == None
    ).all()

    for order in orders:
        if order.id in existing_reinspection_order_ids:
            continue

        batch = get_batch(db, order.batch_id)
        if not batch:
            continue

        formula = get_formula(db, batch.formula_id)
        spray_line = get_spray_line(db, batch.spray_line_id)
        climate = get_climate(db, order.climate_id)

        formula_score, formula_reasons = _calc_formula_risk_score(db, batch.formula_id)
        spray_line_score, spray_line_reasons = _calc_spray_line_risk_score(db, batch.spray_line_id)
        climate_score, climate_reasons = _calc_climate_risk_score(db, order.climate_id)
        complaint_score, complaint_reasons = _calc_complaint_risk_score(
            db, order.id, batch.formula_id, batch.spray_line_id, order.climate_id
        )

        total_score = round(
            formula_score * 0.30 + spray_line_score * 0.25 + climate_score * 0.25 + complaint_score * 0.20,
            2
        )

        if total_score < min_risk_score:
            continue

        risk_categories = []
        all_reasons = []

        if formula_score >= 15:
            risk_categories.append("formula")
            all_reasons.extend([f"[配方]{r}" for r in formula_reasons])
        if spray_line_score >= 15:
            risk_categories.append("spray_line")
            all_reasons.extend([f"[喷涂线]{r}" for r in spray_line_reasons])
        if climate_score >= 15:
            risk_categories.append("climate")
            all_reasons.extend([f"[气候]{r}" for r in climate_reasons])
        if complaint_score >= 15:
            if "formula" not in risk_categories:
                risk_categories.append("formula")
            if "spray_line" not in risk_categories:
                risk_categories.append("spray_line")
            all_reasons.extend([f"[投诉]{r}" for r in complaint_reasons])

        if not risk_categories:
            risk_categories.append("formula")
            all_reasons.append("[综合]多维度风险累积达到预警阈值")

        warnings.append(schemas.PreDepartureWarningItem(
            order_id=order.id,
            order_no=order.order_no,
            customer=order.customer,
            shipping_route=order.shipping_route,
            shipment_date=order.shipment_date,
            batch_code=batch.batch_code,
            formula_code=formula.code if formula else "",
            formula_name=formula.name if formula else "",
            spray_line_code=spray_line.code if spray_line else "",
            spray_line_name=spray_line.name if spray_line else "",
            port_name=climate.port_name if climate else "",
            climate_zone=climate.climate_zone if climate else None,
            avg_high_temp_c=climate.avg_high_temp_c if climate else None,
            avg_relative_humidity_pct=climate.avg_relative_humidity_pct if climate else None,
            formula_risk_score=round(formula_score, 2),
            spray_line_risk_score=round(spray_line_score, 2),
            climate_risk_score=round(climate_score, 2),
            complaint_risk_score=round(complaint_score, 2),
            total_risk_score=total_score,
            risk_categories=risk_categories,
            risk_detail="; ".join(all_reasons)
        ))

    warnings.sort(key=lambda w: w.total_risk_score, reverse=True)
    return warnings


def generate_reinspection_dispatches(db: Session, min_risk_score: float = 30.0) -> List[models.ReinspectionOrder]:
    warnings = generate_pre_departure_warnings(db, min_risk_score=min_risk_score)
    created = []

    for warning in warnings:
        existing = db.query(models.ReinspectionOrder).filter(
            models.ReinspectionOrder.order_id == warning.order_id
        ).first()
        if existing:
            continue

        categories_str = ",".join(warning.risk_categories)
        reinspection = models.ReinspectionOrder(
            order_id=warning.order_id,
            risk_categories=categories_str,
            formula_risk_score=warning.formula_risk_score,
            spray_line_risk_score=warning.spray_line_risk_score,
            climate_risk_score=warning.climate_risk_score,
            complaint_risk_score=warning.complaint_risk_score,
            total_risk_score=warning.total_risk_score,
            risk_detail=warning.risk_detail,
            status=models.ReinspectionStatus.PENDING,
        )
        db.add(reinspection)
        created.append(reinspection)

    db.commit()
    for r in created:
        db.refresh(r)
    return created


def get_reinspection_dashboard(db: Session) -> schemas.ReinspectionDashboardStats:
    all_reinspections = db.query(models.ReinspectionOrder).all()

    total = len(all_reinspections)
    pending = sum(1 for r in all_reinspections if r.status == models.ReinspectionStatus.PENDING)
    in_progress = sum(1 for r in all_reinspections if r.status == models.ReinspectionStatus.IN_PROGRESS)
    completed = sum(1 for r in all_reinspections if r.status == models.ReinspectionStatus.COMPLETED)
    cancelled = sum(1 for r in all_reinspections if r.status == models.ReinspectionStatus.CANCELLED)

    formula_count = sum(1 for r in all_reinspections if "formula" in r.risk_categories)
    spray_line_count = sum(1 for r in all_reinspections if "spray_line" in r.risk_categories)
    climate_count = sum(1 for r in all_reinspections if "climate" in r.risk_categories)

    avg_score = (sum(r.total_risk_score for r in all_reinspections) / total) if total > 0 else 0.0

    high_risk = sorted(all_reinspections, key=lambda r: r.total_risk_score, reverse=True)[:10]

    return schemas.ReinspectionDashboardStats(
        total_warnings=total,
        pending_count=pending,
        in_progress_count=in_progress,
        completed_count=completed,
        cancelled_count=cancelled,
        formula_risk_count=formula_count,
        spray_line_risk_count=spray_line_count,
        climate_risk_count=climate_count,
        avg_total_risk_score=round(avg_score, 2),
        high_risk_orders=[schemas.ReinspectionOrder.model_validate(r) for r in high_risk]
    )
