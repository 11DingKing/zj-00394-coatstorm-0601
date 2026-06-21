from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
import models
from models import PackagingMethod, BatchMarkStatus, ComplaintType, ReinspectionStatus


def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(models.CoatingFormula).count() > 0:
            print("数据已存在，跳过初始化")
            return

        formulas = [
            models.CoatingFormula(
                code="F-AK-001",
                name="阿克苏标准双组份聚氨酯漆",
                primer="AK-Primer-200",
                topcoat="AK-Topcoat-500",
                clearcoat="AK-Clear-900",
                hardener_ratio="4:1",
                supplier="阿克苏诺贝尔"
            ),
            models.CoatingFormula(
                code="F-PPG-002",
                name="PPG经济型丙烯酸漆",
                primer="PPG-Primer-150",
                topcoat="PPG-Topcoat-350",
                clearcoat="PPG-Clear-700",
                hardener_ratio="5:1",
                supplier="PPG工业"
            ),
            models.CoatingFormula(
                code="F-BAD-003",
                name="国产低价环氧漆(问题配方)",
                primer="BD-Primer-100",
                topcoat="BD-Topcoat-200",
                clearcoat=None,
                hardener_ratio="3:1",
                supplier="本地小厂"
            ),
            models.CoatingFormula(
                code="F-DUP-004",
                name="杜邦高端氟碳漆",
                primer="DP-Primer-FC",
                topcoat="DP-Topcoat-FC",
                clearcoat="DP-Clear-FC",
                hardener_ratio="4:1",
                supplier="杜邦化学"
            ),
        ]
        db.add_all(formulas)
        db.flush()

        spray_lines = [
            models.SprayLine(
                code="SL-A",
                name="A线-全自动静电喷涂",
                location="东区一号车间",
                description="自动化程度高，温度控制精准±1°C"
            ),
            models.SprayLine(
                code="SL-B",
                name="B线-半自动喷涂",
                location="东区二号车间",
                description="人工补喷结合机械臂，适合小批量"
            ),
            models.SprayLine(
                code="SL-C",
                name="C线-手工喷涂(老化线)",
                location="西区旧车间",
                description="老旧设备，温度波动较大±5°C"
            ),
        ]
        db.add_all(spray_lines)
        db.flush()

        climates = [
            models.DestinationClimate(
                port_code="SG-SIN",
                port_name="新加坡港",
                country="新加坡",
                region="东南亚",
                avg_high_temp_c=32.0,
                avg_low_temp_c=25.5,
                avg_relative_humidity_pct=85.0,
                monsoon_season="11月-次年2月东北季风",
                climate_zone="热带雨林气候"
            ),
            models.DestinationClimate(
                port_code="AE-JEA",
                port_name="杰贝阿里港",
                country="阿联酋",
                region="中东",
                avg_high_temp_c=42.0,
                avg_low_temp_c=28.0,
                avg_relative_humidity_pct=65.0,
                monsoon_season="无明显雨季",
                climate_zone="热带沙漠气候"
            ),
            models.DestinationClimate(
                port_code="BR-SDC",
                port_name="桑托斯港",
                country="巴西",
                region="南美",
                avg_high_temp_c=30.0,
                avg_low_temp_c=22.0,
                avg_relative_humidity_pct=80.0,
                monsoon_season="12月-次年3月雨季",
                climate_zone="热带草原气候"
            ),
            models.DestinationClimate(
                port_code="NL-RTM",
                port_name="鹿特丹港",
                country="荷兰",
                region="欧洲",
                avg_high_temp_c=19.0,
                avg_low_temp_c=8.0,
                avg_relative_humidity_pct=75.0,
                monsoon_season="全年降水均匀",
                climate_zone="温带海洋性气候"
            ),
            models.DestinationClimate(
                port_code="US-LAX",
                port_name="洛杉矶港",
                country="美国",
                region="北美",
                avg_high_temp_c=25.0,
                avg_low_temp_c=15.0,
                avg_relative_humidity_pct=60.0,
                monsoon_season="11月-次年3月雨季",
                climate_zone="地中海气候"
            ),
            models.DestinationClimate(
                port_code="TH-BKK",
                port_name="曼谷港",
                country="泰国",
                region="东南亚",
                avg_high_temp_c=35.0,
                avg_low_temp_c=26.0,
                avg_relative_humidity_pct=88.0,
                monsoon_season="5月-10月雨季",
                climate_zone="热带季风气候"
            ),
        ]
        db.add_all(climates)
        db.flush()

        base_date = datetime(2025, 9, 1, 8, 0, 0)

        batches = [
            models.VehicleBatch(
                batch_code="B-2025-0901-AK",
                model="RoadMaster X200 山地车",
                quantity=500,
                formula_id=formulas[0].id,
                spray_line_id=spray_lines[0].id,
                cure_temperature_c=140.0,
                cure_duration_min=30.0,
                air_dry_duration_hours=24.0,
                production_date=base_date
            ),
            models.VehicleBatch(
                batch_code="B-2025-0905-PPG",
                model="CityCruiser C100 通勤车",
                quantity=300,
                formula_id=formulas[1].id,
                spray_line_id=spray_lines[0].id,
                cure_temperature_c=135.0,
                cure_duration_min=28.0,
                air_dry_duration_hours=20.0,
                production_date=base_date + timedelta(days=4)
            ),
            models.VehicleBatch(
                batch_code="B-2025-0910-BAD",
                model="TrailBlazer T300 越野车",
                quantity=800,
                formula_id=formulas[2].id,
                spray_line_id=spray_lines[2].id,
                cure_temperature_c=120.0,
                cure_duration_min=20.0,
                air_dry_duration_hours=12.0,
                production_date=base_date + timedelta(days=9)
            ),
            models.VehicleBatch(
                batch_code="B-2025-0915-DUP",
                model="EliteTour E500 高端旅行车",
                quantity=200,
                formula_id=formulas[3].id,
                spray_line_id=spray_lines[0].id,
                cure_temperature_c=145.0,
                cure_duration_min=35.0,
                air_dry_duration_hours=36.0,
                production_date=base_date + timedelta(days=14)
            ),
            models.VehicleBatch(
                batch_code="B-2025-0920-AK",
                model="RoadMaster X200 山地车",
                quantity=450,
                formula_id=formulas[0].id,
                spray_line_id=spray_lines[1].id,
                cure_temperature_c=138.0,
                cure_duration_min=28.0,
                air_dry_duration_hours=24.0,
                production_date=base_date + timedelta(days=19)
            ),
            models.VehicleBatch(
                batch_code="B-2025-0925-BAD",
                model="SpeedRacer S100 公路车",
                quantity=600,
                formula_id=formulas[2].id,
                spray_line_id=spray_lines[2].id,
                cure_temperature_c=118.0,
                cure_duration_min=18.0,
                air_dry_duration_hours=10.0,
                production_date=base_date + timedelta(days=24)
            ),
        ]
        db.add_all(batches)
        db.flush()

        orders = [
            models.ExportOrder(
                order_no="EXP-2025-09001",
                batch_id=batches[0].id,
                climate_id=climates[0].id,
                packaging_method=PackagingMethod.WOODEN_CRATE,
                shipping_route="上海-新加坡(东南亚航线)",
                shipment_date=base_date + timedelta(days=7),
                estimated_arrival=base_date + timedelta(days=14),
                actual_arrival=base_date + timedelta(days=14),
                customer="新加坡骑行贸易公司"
            ),
            models.ExportOrder(
                order_no="EXP-2025-09002",
                batch_id=batches[1].id,
                climate_id=climates[4].id,
                packaging_method=PackagingMethod.CONTAINER_BULK,
                shipping_route="上海-洛杉矶(太平洋航线)",
                shipment_date=base_date + timedelta(days=10),
                estimated_arrival=base_date + timedelta(days=25),
                actual_arrival=base_date + timedelta(days=26),
                customer="美国西海岸自行车经销商"
            ),
            models.ExportOrder(
                order_no="EXP-2025-09003",
                batch_id=batches[2].id,
                climate_id=climates[2].id,
                packaging_method=PackagingMethod.CARTON,
                shipping_route="上海-桑托斯(南美东航线)",
                shipment_date=base_date + timedelta(days=15),
                estimated_arrival=base_date + timedelta(days=45),
                actual_arrival=base_date + timedelta(days=47),
                customer="巴西圣保罗自行车进口商"
            ),
            models.ExportOrder(
                order_no="EXP-2025-09004",
                batch_id=batches[2].id,
                climate_id=climates[5].id,
                packaging_method=PackagingMethod.PALLET_WRAP,
                shipping_route="上海-曼谷(东南亚航线)",
                shipment_date=base_date + timedelta(days=16),
                estimated_arrival=base_date + timedelta(days=23),
                actual_arrival=base_date + timedelta(days=24),
                customer="泰国曼谷运动器材公司"
            ),
            models.ExportOrder(
                order_no="EXP-2025-09005",
                batch_id=batches[3].id,
                climate_id=climates[3].id,
                packaging_method=PackagingMethod.WOODEN_CRATE,
                shipping_route="上海-鹿特丹(欧亚航线)",
                shipment_date=base_date + timedelta(days=20),
                estimated_arrival=base_date + timedelta(days=40),
                actual_arrival=base_date + timedelta(days=41),
                customer="荷兰高端自行车代理商"
            ),
            models.ExportOrder(
                order_no="EXP-2025-09006",
                batch_id=batches[4].id,
                climate_id=climates[1].id,
                packaging_method=PackagingMethod.CONTAINER_BULK,
                shipping_route="上海-杰贝阿里(中东航线)",
                shipment_date=base_date + timedelta(days=25),
                estimated_arrival=base_date + timedelta(days=35),
                actual_arrival=base_date + timedelta(days=36),
                customer="阿联酋迪拜体育用品公司"
            ),
            models.ExportOrder(
                order_no="EXP-2025-09007",
                batch_id=batches[5].id,
                climate_id=climates[2].id,
                packaging_method=PackagingMethod.CARTON,
                shipping_route="上海-桑托斯(南美东航线)",
                shipment_date=base_date + timedelta(days=30),
                estimated_arrival=base_date + timedelta(days=60),
                actual_arrival=None,
                customer="巴西里约自行车批发商"
            ),
        ]
        db.add_all(orders)
        db.flush()

        inspections = [
            models.InspectionRecord(
                batch_id=batches[0].id,
                inspector="张质检",
                inspection_date=base_date + timedelta(days=1),
                sample_size=20,
                adhesion_grade="0级",
                color_delta_e=0.8,
                film_thickness_um=65.0,
                humidity_resistance_hours=500.0,
                passed=20,
                failed=0,
                notes="全部合格，附着力优秀"
            ),
            models.InspectionRecord(
                batch_id=batches[1].id,
                inspector="李质检",
                inspection_date=base_date + timedelta(days=5),
                sample_size=15,
                adhesion_grade="1级",
                color_delta_e=1.2,
                film_thickness_um=58.0,
                humidity_resistance_hours=480.0,
                passed=15,
                failed=0,
                notes="合格"
            ),
            models.InspectionRecord(
                batch_id=batches[2].id,
                inspector="王质检",
                inspection_date=base_date + timedelta(days=10),
                sample_size=30,
                adhesion_grade="2级",
                color_delta_e=1.8,
                film_thickness_um=42.0,
                humidity_resistance_hours=240.0,
                passed=28,
                failed=2,
                notes="膜厚偏薄，耐湿热测试接近临界值，勉强通过"
            ),
            models.InspectionRecord(
                batch_id=batches[3].id,
                inspector="张质检",
                inspection_date=base_date + timedelta(days=15),
                sample_size=10,
                adhesion_grade="0级",
                color_delta_e=0.5,
                film_thickness_um=80.0,
                humidity_resistance_hours=1000.0,
                passed=10,
                failed=0,
                notes="高端产品，各项指标均优秀"
            ),
            models.InspectionRecord(
                batch_id=batches[4].id,
                inspector="李质检",
                inspection_date=base_date + timedelta(days=20),
                sample_size=20,
                adhesion_grade="1级",
                color_delta_e=1.0,
                film_thickness_um=62.0,
                humidity_resistance_hours=480.0,
                passed=20,
                failed=0,
                notes="合格"
            ),
            models.InspectionRecord(
                batch_id=batches[5].id,
                inspector="王质检",
                inspection_date=base_date + timedelta(days=25),
                sample_size=25,
                adhesion_grade="2级",
                color_delta_e=2.0,
                film_thickness_um=40.0,
                humidity_resistance_hours=200.0,
                passed=23,
                failed=2,
                notes="膜厚不达标，已上报但考虑成本继续出货"
            ),
        ]
        db.add_all(inspections)
        db.flush()

        marks = [
            models.BatchMark(
                batch_id=batches[2].id,
                status=BatchMarkStatus.RECALL,
                marked_by="质量经理-陈",
                reason="巴西客户反馈大面积起泡，经追溯该批次使用国产低价漆+老喷涂线，固化温度不足，膜厚偏薄"
            ),
            models.BatchMark(
                batch_id=batches[5].id,
                status=BatchMarkStatus.OBSERVE,
                marked_by="质量经理-陈",
                reason="同问题批次配方和喷涂线，到达目的港后重点关注，建议客户检查"
            ),
        ]
        db.add_all(marks)
        db.flush()

        complaints = [
            models.CustomerComplaint(
                order_id=orders[2].id,
                complaint_type=ComplaintType.BUBBLING,
                vehicle_count=320,
                severity="严重",
                reported_at=base_date + timedelta(days=55),
                description="集装箱到港拆箱后发现约40%的车辆车架表面出现大小不等的漆面起泡，集中在管接焊缝区域。经湿热环境放置3天后起泡面积扩大，部分区域底漆脱落暴露金属底材。现场抽样附着力测试仅为3-4级。",
                resolution="启动召回程序，安排同批次补发，停用问题配方F-BAD-003",
                resolved_at=base_date + timedelta(days=60)
            ),
            models.CustomerComplaint(
                order_id=orders[3].id,
                complaint_type=ComplaintType.BUBBLING,
                vehicle_count=85,
                severity="中等",
                reported_at=base_date + timedelta(days=30),
                description="曼谷仓库存储两周后发现约10%车辆出现轻微起泡，集中在下管和后上叉区域。高温高湿季节明显。",
                resolution="当地安排补漆处理，费用由我司承担",
                resolved_at=base_date + timedelta(days=35)
            ),
            models.CustomerComplaint(
                order_id=orders[0].id,
                complaint_type=ComplaintType.DISCOLORATION,
                vehicle_count=5,
                severity="轻微",
                reported_at=base_date + timedelta(days=20),
                description="少量车辆阳光暴晒后颜色轻微发黄",
                resolution="客户同意补偿5%货款",
                resolved_at=base_date + timedelta(days=22)
            ),
        ]
        db.add_all(complaints)

        reinspections = [
            models.ReinspectionOrder(
                order_id=orders[6].id,
                risk_categories="formula,spray_line,climate",
                formula_risk_score=75.0,
                spray_line_risk_score=63.0,
                climate_risk_score=55.0,
                complaint_risk_score=80.0,
                total_risk_score=68.0,
                risk_detail="[配方]配方投诉率100.0%过高(>=30%); [配方]起泡率100.0%严重(>=20%); [喷涂线]喷涂线投诉率100.0%过高(>=25%); [喷涂线]质检不合格批次率100.0%过高(>=50%); [气候]目的港平均高温30.0°C偏高(>=30°C); [气候]平均湿度80.0%偏高(>=75%); [气候]气候区为热带草原气候(热带)",
                status=ReinspectionStatus.PENDING,
            ),
            models.ReinspectionOrder(
                order_id=orders[3].id,
                risk_categories="formula,spray_line,climate",
                formula_risk_score=75.0,
                spray_line_risk_score=63.0,
                climate_risk_score=70.0,
                complaint_risk_score=55.0,
                total_risk_score=66.25,
                risk_detail="[配方]配方投诉率100.0%过高(>=30%); [配方]起泡率100.0%严重(>=20%); [喷涂线]喷涂线投诉率100.0%过高(>=25%); [喷涂线]质检不合格批次率100.0%过高(>=50%); [气候]目的港平均高温35.0°C极高(>=35°C); [气候]平均湿度88.0%极高(>=85%); [气候]气候区为热带季风气候(热带)",
                status=ReinspectionStatus.IN_PROGRESS,
                assigned_inspector="赵质检",
            ),
        ]
        db.add_all(reinspections)

        db.commit()
        print("数据初始化完成！")
        print(f"  - 涂料配方: {len(formulas)} 条")
        print(f"  - 喷涂线: {len(spray_lines)} 条")
        print(f"  - 目的港气候: {len(climates)} 条")
        print(f"  - 整车批次: {len(batches)} 条")
        print(f"  - 出口订单: {len(orders)} 条")
        print(f"  - 质检记录: {len(inspections)} 条")
        print(f"  - 批次标记: {len(marks)} 条")
        print(f"  - 客户投诉: {len(complaints)} 条")
        print(f"  - 复检派单: {len(reinspections)} 条")
        print()
        print("问题批次提示:")
        print("  B-2025-0910-BAD: 使用国产低价漆 F-BAD-003 + C线(手工/老化线)")
        print("    - 固化温度仅120°C (标准140°C), 风干仅12小时 (标准24小时)")
        print("    - 膜厚仅42μm (标准≥60μm), 耐湿热仅240h (标准≥480h)")
        print("    - 订单EXP-2025-09003发往巴西桑托斯(高温高湿热带雨林气候)")
        print("    - 到货后320台起泡 (占比40%), 已标记 RECALL 召回")
        print("  B-2025-0925-BAD: 同配方同喷涂线, 发往巴西, 标记 OBSERVE 观察")

    except Exception as e:
        db.rollback()
        print(f"初始化失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
