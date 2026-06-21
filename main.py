from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
import crud
from database import engine, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="涂装质量追溯系统",
    description="出口自行车涂装质量跨洋运输追溯后端 - 批次、配方、喷涂、质检、投诉全链路追踪",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "name": "涂装质量追溯系统",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/formulas/", response_model=schemas.CoatingFormula)
def create_formula(formula: schemas.CoatingFormulaCreate, db: Session = Depends(get_db)):
    db_formula = crud.get_formula_by_code(db, code=formula.code)
    if db_formula:
        raise HTTPException(status_code=400, detail="配方编码已存在")
    return crud.create_formula(db=db, formula=formula)


@app.get("/formulas/", response_model=List[schemas.CoatingFormula])
def list_formulas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_formulas(db, skip=skip, limit=limit)


@app.get("/formulas/{formula_id}", response_model=schemas.CoatingFormula)
def get_formula(formula_id: int, db: Session = Depends(get_db)):
    db_formula = crud.get_formula(db, formula_id=formula_id)
    if db_formula is None:
        raise HTTPException(status_code=404, detail="配方不存在")
    return db_formula


@app.post("/spray-lines/", response_model=schemas.SprayLine)
def create_spray_line(line: schemas.SprayLineCreate, db: Session = Depends(get_db)):
    db_line = crud.get_spray_line_by_code(db, code=line.code)
    if db_line:
        raise HTTPException(status_code=400, detail="喷涂线编码已存在")
    return crud.create_spray_line(db=db, line=line)


@app.get("/spray-lines/", response_model=List[schemas.SprayLine])
def list_spray_lines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_spray_lines(db, skip=skip, limit=limit)


@app.get("/spray-lines/{line_id}", response_model=schemas.SprayLine)
def get_spray_line(line_id: int, db: Session = Depends(get_db)):
    db_line = crud.get_spray_line(db, line_id=line_id)
    if db_line is None:
        raise HTTPException(status_code=404, detail="喷涂线不存在")
    return db_line


@app.post("/climates/", response_model=schemas.DestinationClimate)
def create_climate(climate: schemas.DestinationClimateCreate, db: Session = Depends(get_db)):
    db_climate = crud.get_climate_by_port(db, port_code=climate.port_code)
    if db_climate:
        raise HTTPException(status_code=400, detail="港口气候数据已存在")
    return crud.create_climate(db=db, climate=climate)


@app.get("/climates/", response_model=List[schemas.DestinationClimate])
def list_climates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_climates(db, skip=skip, limit=limit)


@app.get("/climates/{climate_id}", response_model=schemas.DestinationClimate)
def get_climate(climate_id: int, db: Session = Depends(get_db)):
    db_climate = crud.get_climate(db, climate_id=climate_id)
    if db_climate is None:
        raise HTTPException(status_code=404, detail="目的港气候数据不存在")
    return db_climate


@app.post("/batches/", response_model=schemas.VehicleBatch)
def create_batch(batch: schemas.VehicleBatchCreate, db: Session = Depends(get_db)):
    db_batch = crud.get_batch_by_code(db, batch_code=batch.batch_code)
    if db_batch:
        raise HTTPException(status_code=400, detail="批次编码已存在")
    return crud.create_batch(db=db, batch=batch)


@app.get("/batches/", response_model=List[schemas.VehicleBatch])
def list_batches(
    skip: int = 0,
    limit: int = 100,
    formula_id: Optional[int] = None,
    spray_line_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_batches(db, skip=skip, limit=limit, formula_id=formula_id, spray_line_id=spray_line_id)


@app.get("/batches/{batch_id}", response_model=schemas.VehicleBatch)
def get_batch(batch_id: int, db: Session = Depends(get_db)):
    db_batch = crud.get_batch(db, batch_id=batch_id)
    if db_batch is None:
        raise HTTPException(status_code=404, detail="批次不存在")
    return db_batch


@app.post("/orders/", response_model=schemas.ExportOrder)
def create_order(order: schemas.ExportOrderCreate, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_no(db, order_no=order.order_no)
    if db_order:
        raise HTTPException(status_code=400, detail="订单号已存在")
    return crud.create_order(db=db, order=order)


@app.get("/orders/", response_model=List[schemas.ExportOrder])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    batch_id: Optional[int] = None,
    climate_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_orders(db, skip=skip, limit=limit, batch_id=batch_id, climate_id=climate_id)


@app.get("/orders/{order_id}", response_model=schemas.ExportOrder)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="订单不存在")
    return db_order


@app.post("/inspections/", response_model=schemas.InspectionRecord)
def create_inspection(inspection: schemas.InspectionRecordCreate, db: Session = Depends(get_db)):
    return crud.create_inspection(db=db, inspection=inspection)


@app.get("/inspections/", response_model=List[schemas.InspectionRecord])
def list_inspections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_inspections(db, skip=skip, limit=limit)


@app.get("/inspections/{inspection_id}", response_model=schemas.InspectionRecord)
def get_inspection(inspection_id: int, db: Session = Depends(get_db)):
    db_inspection = crud.get_inspection(db, inspection_id=inspection_id)
    if db_inspection is None:
        raise HTTPException(status_code=404, detail="质检记录不存在")
    return db_inspection


@app.get("/batches/{batch_id}/inspections/", response_model=List[schemas.InspectionRecord])
def get_batch_inspections(batch_id: int, db: Session = Depends(get_db)):
    return crud.get_inspections_by_batch(db, batch_id=batch_id)


@app.post("/batch-marks/", response_model=schemas.BatchMark)
def create_batch_mark(mark: schemas.BatchMarkCreate, db: Session = Depends(get_db)):
    return crud.create_batch_mark(db=db, mark=mark)


@app.get("/batch-marks/", response_model=List[schemas.BatchMark])
def list_batch_marks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_batch_marks(db, skip=skip, limit=limit)


@app.get("/batches/{batch_id}/marks/", response_model=List[schemas.BatchMark])
def get_batch_marks(batch_id: int, db: Session = Depends(get_db)):
    return crud.get_marks_by_batch(db, batch_id=batch_id)


@app.post("/complaints/", response_model=schemas.CustomerComplaint)
def create_complaint(complaint: schemas.CustomerComplaintCreate, db: Session = Depends(get_db)):
    return crud.create_complaint(db=db, complaint=complaint)


@app.get("/complaints/", response_model=List[schemas.CustomerComplaint])
def list_complaints(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_complaints(db, skip=skip, limit=limit)


@app.get("/orders/{order_id}/complaints/", response_model=List[schemas.CustomerComplaint])
def get_order_complaints(order_id: int, db: Session = Depends(get_db)):
    return crud.get_complaints_by_order(db, order_id=order_id)


@app.get("/trace/order/{order_id}", response_model=schemas.TraceResult)
def trace_order(order_id: int, db: Session = Depends(get_db)):
    result = crud.trace_by_order(db, order_id=order_id)
    if result is None:
        raise HTTPException(status_code=404, detail="订单不存在或无法追溯")
    return result


@app.get("/trace/batch/{batch_id}", response_model=schemas.TraceResult)
def trace_batch(batch_id: int, db: Session = Depends(get_db)):
    result = crud.trace_by_batch(db, batch_id=batch_id)
    if result is None:
        raise HTTPException(status_code=404, detail="批次不存在或无法追溯")
    return result


@app.get("/analytics/formula-risks/", response_model=List[schemas.FormulaRisk])
def get_formula_risks(db: Session = Depends(get_db)):
    return crud.analyze_formula_risks(db)


@app.get("/analytics/formula-route-risks/", response_model=List[schemas.FormulaRouteRisk])
def get_formula_route_risks(
    min_orders: int = 1,
    formula_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    results = crud.analyze_formula_route_risks(db, min_orders=min_orders)
    if formula_id is not None:
        results = [r for r in results if r.formula_id == formula_id]
    return results


@app.get(
    "/analytics/formula-route-risks/{formula_id}/{shipping_route:path}",
    response_model=schemas.FormulaRouteRiskDetail
)
def get_formula_route_trace(
    formula_id: int,
    shipping_route: str,
    db: Session = Depends(get_db)
):
    result = crud.get_formula_route_trace(db, formula_id=formula_id, shipping_route=shipping_route)
    if result is None:
        raise HTTPException(status_code=404, detail="配方或线路组合不存在")
    return result
